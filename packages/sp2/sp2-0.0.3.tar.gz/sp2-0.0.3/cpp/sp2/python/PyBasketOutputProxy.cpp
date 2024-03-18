#include <sp2/engine/BasketInfo.h>
#include <sp2/engine/Node.h>
#include <sp2/python/Conversions.h>
#include <sp2/python/Exception.h>
#include <sp2/python/InitHelper.h>
#include <sp2/python/PyBasketOutputProxy.h>
#include <sp2/python/PyConstants.h>
#include <sp2/python/PyOutputProxy.h>
#include <sp2/python/PyIterator.h>
#include <sp2/python/PyNode.h>

namespace sp2::python
{

PyBaseBasketOutputProxy::PyBaseBasketOutputProxy( Node * node, INOUT_ID_TYPE id ) : m_node( node ),
                                                                                    m_id( id )
{
}

PyListBasketOutputProxy::PyListBasketOutputProxy( PyObject *pyType, Node *node, INOUT_ID_TYPE id, size_t shape ) : PyBaseBasketOutputProxy( node, id )
{
    for( size_t elemId = 0; elemId < shape; ++elemId )
        m_proxies.emplace_back( PyOutputProxyPtr::own( PyOutputProxy::create( pyType, node, OutputId( id, elemId ) ) ) );
}

PyListBasketOutputProxy * PyListBasketOutputProxy::create( PyObject *pyType, Node *node, INOUT_ID_TYPE id, size_t shape )
{
    if( shape > OutputId::maxBasketElements() )
        SP2_THROW( ValueError, "List basket size of " << shape << " exceeds basket size limit of " << OutputId::maxBasketElements() << " in node " << node -> name() );

    PyListBasketOutputProxy * proxy = ( PyListBasketOutputProxy * ) PyType.tp_new( &PyType, nullptr, nullptr );
    new( proxy ) PyListBasketOutputProxy( pyType, node, id, shape );
    return proxy;
}

static void PyListBasketOutputProxy_dealloc( PyListBasketOutputProxy * self )
{
    SP2_BEGIN_METHOD;
    self -> ~PyListBasketOutputProxy();
    Py_TYPE( self ) -> tp_free( self );
    SP2_RETURN;
}

static PyObject * PyListBasketOutputProxy_getproxy( PyListBasketOutputProxy * proxy, Py_ssize_t idx )
{
    SP2_BEGIN_METHOD;
    PyObject * rv = proxy -> proxy( idx );
    Py_INCREF( rv );
    return rv;
    SP2_RETURN_NONE;
}

static PyObject * PyListBasketOutputProxy_output( PyListBasketOutputProxy * proxy, PyObject * obj )
{
    SP2_BEGIN_METHOD;
    if( !PyDict_Check(obj) )
        SP2_THROW( TypeError, "output called on list basket output proxy with non dict object: " << PyObjectPtr::incref( obj ) );

    PyObject *key, *value;
    Py_ssize_t pos = 0;
    while( PyDict_Next(obj, &pos, &key, &value) )
    {
        if( !PyIndex_Check(key) )
            SP2_THROW( TypeError, "output called on list basket with non-index key: " << PyObjectPtr::incref( key ) );

        Py_ssize_t index = PyNumber_AsSsize_t( key, PyExc_IndexError );
        if( index == -1 )
            SP2_THROW( PythonPassthrough, "" );

        PyOutputProxy * outproxy = proxy -> proxy( index );
        outproxy -> outputTick( value );
    }
    SP2_RETURN_NONE;
}

static PyNumberMethods PyListBasketOutputProxy_NumberMethods = {
        (binaryfunc ) PyListBasketOutputProxy_output, /* binaryfunc nb_add */
        0, /* binaryfunc nb_subtract */
        0, /* binaryfunc nb_multiply */
        0, /* binaryfunc nb_remainder */
        0, /* binaryfunc nb_divmod */
        0, /* ternaryfunc nb_power */
        0, /* unaryfunc nb_negative */
        0, /* unaryfunc nb_positive */
        0, /* unaryfunc nb_absolute */
        0, /* inquiry nb_nonzero */
        0, /* unaryfunc nb_invert */
        0, /* binaryfunc nb_lshift */
        0, /* binaryfunc nb_rshift */
        0, /* binaryfunc nb_and */
        0, /* binaryfunc nb_xor */
        0, /* binaryfunc nb_or */
        0, /* unaryfunc nb_int */
        0, /* void * reserved */
        0  /* unaryfunc nb_float */
};

static PySequenceMethods PyListBasketOutputProxy_SeqMethods = {
        0,                                      /*sq_length */
        0,                                      /*sq_concat */
        0,                                      /*sq_repeat */
        (ssizeargfunc) PyListBasketOutputProxy_getproxy, /*sq_item */
        0,                                      /*sq_ass_item */
        0,                                      /*sq_contains */
        0,                                      /*sq_inplace_concat */
        0                                       /*sq_inplace_repeat */
};

PyTypeObject PyListBasketOutputProxy::PyType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        "_sp2impl.PyListBasketOutputProxy",   /* tp_name */
        sizeof(PyListBasketOutputProxy),      /* tp_basicsize */
        0,                         /* tp_itemsize */
        (destructor) PyListBasketOutputProxy_dealloc, /* tp_dealloc */
        0,                         /* tp_print */
        0,                         /* tp_getattr */
        0,                         /* tp_setattr */
        0,                         /* tp_reserved */
        0,                         /* tp_repr */
        &PyListBasketOutputProxy_NumberMethods, /* tp_as_number */
        &PyListBasketOutputProxy_SeqMethods,    /* tp_as_sequence */
        0,                         /* tp_as_mapping */
        0,                         /* tp_hash  */
        0,                         /* tp_call */
        0,                         /* tp_str */
        0,                         /* tp_getattro */
        0,                         /* tp_setattro */
        0,                         /* tp_as_buffer */
        Py_TPFLAGS_DEFAULT,        /* tp_flags */
        "sp2 list output proxy",    /* tp_doc */
        0,                         /* tp_traverse */
        0,                         /* tp_clear */
        0,                         /* tp_richcompare */
        0,                         /* tp_weaklistoffset */
        0,                         /* tp_iter */
        0,                         /* tp_iternext */
        0,                         /* tp_methods */
        0,                         /* tp_members */
        0,                         /* tp_getset */
        0,                         /* tp_base */
        0,                         /* tp_dict */
        0,                         /* tp_descr_get */
        0,                         /* tp_descr_set */
        0,                         /* tp_dictoffset */
        0,                         /* tp_init */
        0,                         /* tp_alloc */
        PyType_GenericNew,         /* tp_new */
};

PyDictBasketOutputProxy::PyDictBasketOutputProxy( PyObject *pyType, Node *node, INOUT_ID_TYPE id,
                                                  PyObject * shape ) : PyBaseBasketOutputProxy( node, id )
{
    m_proxyMapping = PyObjectPtr::own( PyDict_New() );
    if( !m_proxyMapping.ptr() )
        SP2_THROW( PythonPassthrough, "" );

    Py_ssize_t numElements = PyList_GET_SIZE( shape );
    for( Py_ssize_t elemId = 0; elemId < numElements; ++elemId )
    {
        auto proxy = PyOutputProxyPtr::own( PyOutputProxy::create( pyType, node, OutputId( id, elemId ) ) );
        if( PyDict_SetItem( m_proxyMapping.ptr(), PyList_GET_ITEM( shape, elemId ), proxy.ptr() ) < 0 )
            SP2_THROW( PythonPassthrough, "" );

    }
}

PyDictBasketOutputProxy * PyDictBasketOutputProxy::create( PyObject *pyType, Node *node, INOUT_ID_TYPE id, PyObject * shape )
{
    if( !PyList_Check( shape ) )
        SP2_THROW( TypeError, "Invalid shape for dict basket, expect list got: " << Py_TYPE( shape ) -> tp_name );

    if( ( size_t ) PyList_GET_SIZE( shape ) > OutputId::maxBasketElements() )
        SP2_THROW( ValueError, "Dict basket size of " << PyList_GET_SIZE( shape ) << " exceeds basket size limit of " <<
                                                     OutputId::maxBasketElements() << " in node " << node -> name() );

    PyDictBasketOutputProxy * proxy = ( PyDictBasketOutputProxy * ) PyType.tp_new( &PyType, nullptr, nullptr );
    new( proxy ) PyDictBasketOutputProxy( pyType, node, id, shape );
    return proxy;
}

static void PyDictBasketOutputProxy_dealloc( PyDictBasketOutputProxy * self )
{
    SP2_BEGIN_METHOD;
    self -> ~PyDictBasketOutputProxy();
    Py_TYPE( self ) -> tp_free( self );
    SP2_RETURN;
}

PyOutputProxy * PyDictBasketOutputProxy::proxyByKey( PyObject * key )
{
    PyOutputProxy * out_proxy = static_cast<PyOutputProxy *>( PyDict_GetItem( m_proxyMapping.ptr(), key ) );
    if( !out_proxy )
        SP2_THROW( KeyError, "key " << PyObjectPtr::incref( key ) << " is not a member of the dict basket" );
    return out_proxy;
}

static PyObject * PyDictBasketOutputProxy_getproxy( PyDictBasketOutputProxy * proxy, PyObject * key )
{
    SP2_BEGIN_METHOD;
    PyObject * rv = proxy -> proxyByKey( key );
    Py_INCREF( rv );
    return rv;
    SP2_RETURN_NONE;
}

static PyObject * PyDictBasketOutputProxy_output( PyDictBasketOutputProxy * proxy, PyObject * obj )
{
    SP2_BEGIN_METHOD;
    if( !PyDict_Check(obj) )
        SP2_THROW( TypeError, "output called on dict basket output proxy with non dict object: " << PyObjectPtr::incref( obj ) );

    PyObject *key, *value;
    Py_ssize_t pos = 0;
    while( PyDict_Next(obj, &pos, &key, &value) )
    {
        PyOutputProxy * outproxy = proxy -> proxyByKey( key );
        outproxy -> outputTick( value );
    }
    SP2_RETURN_NONE;
}

static PyNumberMethods PyDictBasketOutputProxy_NumberMethods = {
        (binaryfunc ) PyDictBasketOutputProxy_output, /* binaryfunc nb_add */
        0, /* binaryfunc nb_subtract */
        0, /* binaryfunc nb_multiply */
        0, /* binaryfunc nb_remainder */
        0, /* binaryfunc nb_divmod */
        0, /* ternaryfunc nb_power */
        0, /* unaryfunc nb_negative */
        0, /* unaryfunc nb_positive */
        0, /* unaryfunc nb_absolute */
        0, /* inquiry nb_nonzero */
        0, /* unaryfunc nb_invert */
        0, /* binaryfunc nb_lshift */
        0, /* binaryfunc nb_rshift */
        0, /* binaryfunc nb_and */
        0, /* binaryfunc nb_xor */
        0, /* binaryfunc nb_or */
        0, /* unaryfunc nb_int */
        0, /* void * reserved */
        0  /* unaryfunc nb_float */
};

static PyMappingMethods PyDictBasketOutputProxy_MappingMethods = {
        0,                                  /*mp_length */
        (binaryfunc) PyDictBasketOutputProxy_getproxy, /*mp_subscript */
        0                              /*mp_ass_subscript */
};

PyTypeObject PyDictBasketOutputProxy::PyType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        "_sp2impl.PyDictBasketOutputProxy",   /* tp_name */
        sizeof(PyDictBasketOutputProxy),      /* tp_basicsize */
        0,                         /* tp_itemsize */
        (destructor) PyDictBasketOutputProxy_dealloc,  /* tp_dealloc */
        0,                         /* tp_print */
        0,                         /* tp_getattr */
        0,                         /* tp_setattr */
        0,                         /* tp_reserved */
        0,                         /* tp_repr */
        &PyDictBasketOutputProxy_NumberMethods,   /* tp_as_number */
        0,                         /* tp_as_sequence */
        &PyDictBasketOutputProxy_MappingMethods,  /* tp_as_mapping */
        0,                         /* tp_hash  */
        0,                         /* tp_call */
        0,                         /* tp_str */
        0,                         /* tp_getattro */
        0,                         /* tp_setattro */
        0,                         /* tp_as_buffer */
        Py_TPFLAGS_DEFAULT,        /* tp_flags */
        "sp2 dict output proxy",   /* tp_doc */
        0,                         /* tp_traverse */
        0,                         /* tp_clear */
        0,                         /* tp_richcompare */
        0,                         /* tp_weaklistoffset */
        0,                         /* tp_iter */
        0,                         /* tp_iternext */
        0,                         /* tp_methods */
        0,                         /* tp_members */
        0,                         /* tp_getset */
        0,                         /* tp_base */
        0,                         /* tp_dict */
        0,                         /* tp_descr_get */
        0,                         /* tp_descr_set */
        0,                         /* tp_dictoffset */
        0,                         /* tp_init */
        0,                         /* tp_alloc */
        PyType_GenericNew,         /* tp_new */
};

PyDynamicBasketOutputProxy::PyDynamicBasketOutputProxy( PyObject *pyType, Node * node,
                                                        INOUT_ID_TYPE id, PyObject * shape ) : PyDictBasketOutputProxy( pyType, node, id, shape )
{
    m_elemType = PyObjectPtr::incref( pyType );
}

PyDynamicBasketOutputProxy * PyDynamicBasketOutputProxy::create( PyObject * pyType, Node * node, INOUT_ID_TYPE id )
{
    PyObjectPtr shape = PyObjectPtr::own( PyList_New( 0 ) );
    PyDynamicBasketOutputProxy * proxy = ( PyDynamicBasketOutputProxy * ) PyType.tp_new( &PyType, nullptr, nullptr );
    new( proxy ) PyDynamicBasketOutputProxy( pyType, node, id, shape.get() );
    return proxy;
}

static void PyDynamicBasketOutputProxy_dealloc( PyDynamicBasketOutputProxy * self )
{
    SP2_BEGIN_METHOD;
    self -> ~PyDynamicBasketOutputProxy();
    Py_TYPE( self ) -> tp_free( self );
    SP2_RETURN;
}

PyOutputProxy * PyDynamicBasketOutputProxy::getOrCreateProxy( PyObject * key )
{
    PyOutputProxy * outproxy = static_cast<PyOutputProxy *>( PyDict_GetItem( m_proxyMapping.ptr(), key ) );
    if( outproxy == nullptr )
    {
        //create the new entry
        auto * dynBasket = static_cast<DynamicOutputBasketInfo *>( m_node -> outputBasket( m_id ) );
        auto elemId = dynBasket -> addDynamicKey( fromPython<DialectGenericType>( key ) );
        auto proxy = PyOutputProxyPtr::own( PyOutputProxy::create( m_elemType.get(), m_node, OutputId( m_id, elemId ) ) );
        if( PyDict_SetItem( m_proxyMapping.ptr(), key, proxy.ptr() ) < 0 )
            SP2_THROW( PythonPassthrough, "" );

        outproxy = proxy.ptr();

        if( ( size_t ) elemId >= m_keyMapping.size() )
            m_keyMapping.resize( elemId + 1 );
        m_keyMapping[ elemId ] = PyObjectPtr::incref( key );
    }
    return static_cast<PyOutputProxy *>( outproxy );
}

void PyDynamicBasketOutputProxy::removeProxy( PyObject * key )
{
    PyOutputProxy * outproxy = static_cast<PyOutputProxy *>( PyDict_GetItem( m_proxyMapping.ptr(), key ) );
    if( outproxy == nullptr )
        SP2_THROW( KeyError, "attempting to remove unknown key " << PyObjectPtr::incref( key ) << " from dynamic basket" );

    //Disallow removing timeseries that ticked in the same cycle
    if( outproxy -> ts() -> lastCycleCount() == m_node -> cycleCount() )
        SP2_THROW( RuntimeException, "Attempted to delete dynamic basket key '" << PyObjectPtr::incref( key ) << "' which was already ticked this cycle" );

    auto elemId = outproxy -> outputId().elemId;

    if( PyDict_DelItem( m_proxyMapping.ptr(), key ) < 0 )
        SP2_THROW( PythonPassthrough, "" );

    auto * dynBasket = static_cast<DynamicOutputBasketInfo *>( m_node -> outputBasket( m_id ) );
    auto replaceId = dynBasket -> removeDynamicKey( fromPython<DialectGenericType>( key ), elemId );

    if( replaceId != -1 )
    {
        //need to find which key moved in the internal basket
        auto & replaceKey = m_keyMapping[ replaceId ];
        PyOutputProxy * replacedproxy = static_cast<PyOutputProxy *>( PyDict_GetItem( m_proxyMapping.ptr(), replaceKey.get() ) );
        SP2_ASSERT( replacedproxy != nullptr );

        replacedproxy -> setElemId( elemId );

        m_keyMapping[ elemId ] = replaceKey;
        m_keyMapping[ replaceId ].reset();
    }
    else
        m_keyMapping[ elemId ].reset();
}

static PyObject * PyDynamicBasketOutputProxy_output( PyDynamicBasketOutputProxy * proxy, PyObject * obj )
{
    SP2_BEGIN_METHOD;
    if( !PyDict_Check(obj) )
        SP2_THROW( TypeError, "output called on dict basket output proxy with non dict object: " << PyObjectPtr::incref( obj ) );

    PyObject *key, *value;
    Py_ssize_t pos = 0;
    while( PyDict_Next(obj, &pos, &key, &value) )
    {
        if( value == constants::REMOVE_DYNAMIC_KEY() )
            proxy -> removeProxy( key );
        else
        {
            auto * outproxy = proxy -> getOrCreateProxy( key );
            outproxy -> outputTick( value );
        }
    }
    SP2_RETURN_NONE;
}

static PyNumberMethods PyDynamicBasketOutputProxy_NumberMethods = {
        (binaryfunc ) PyDynamicBasketOutputProxy_output, /* binaryfunc nb_add */
        0, /* binaryfunc nb_subtract */
        0, /* binaryfunc nb_multiply */
        0, /* binaryfunc nb_remainder */
        0, /* binaryfunc nb_divmod */
        0, /* ternaryfunc nb_power */
        0, /* unaryfunc nb_negative */
        0, /* unaryfunc nb_positive */
        0, /* unaryfunc nb_absolute */
        0, /* inquiry nb_nonzero */
        0, /* unaryfunc nb_invert */
        0, /* binaryfunc nb_lshift */
        0, /* binaryfunc nb_rshift */
        0, /* binaryfunc nb_and */
        0, /* binaryfunc nb_xor */
        0, /* binaryfunc nb_or */
        0, /* unaryfunc nb_int */
        0, /* void * reserved */
        0  /* unaryfunc nb_float */
};

PyTypeObject PyDynamicBasketOutputProxy::PyType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_sp2impl.PyDynamicBasketOutputProxy",   /* tp_name */
    sizeof(PyDynamicBasketOutputProxy),      /* tp_basicsize */
    0,                         /* tp_itemsize */
    ( destructor ) PyDynamicBasketOutputProxy_dealloc, /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    0,                         /* tp_repr */
    &PyDynamicBasketOutputProxy_NumberMethods,   /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,        /* tp_flags */
    "sp2 dynamic basket output proxy",    /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    0,                         /* tp_methods */
    0,                         /* tp_members */
    0,                         /* tp_getset */
    &PyDictBasketOutputProxy::PyType, /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    0,                         /* tp_init */
    0,                         /* tp_alloc */
    PyType_GenericNew,         /* tp_new */
};


REGISTER_TYPE_INIT( &PyListBasketOutputProxy::PyType,    "PyListBasketOutputProxy" );
REGISTER_TYPE_INIT( &PyDictBasketOutputProxy::PyType,    "PyDictBasketOutputProxy" );
REGISTER_TYPE_INIT( &PyDynamicBasketOutputProxy::PyType, "PyDynamicBasketOutputProxy" );

}
