#include <sp2/engine/PushPullInputAdapter.h>
#include <sp2/python/Common.h>
#include <sp2/python/Conversions.h>
#include <sp2/python/Exception.h>
#include <sp2/python/PyInputAdapterWrapper.h>
#include <sp2/python/PyPushInputAdapter.h>
#include <sp2/python/PyEngine.h>
#include <sp2/python/PyObjectPtr.h>

namespace sp2::python
{

class PyPushPullInputAdapter : public PushPullInputAdapter
{
public:
    PyPushPullInputAdapter( Engine * engine, AdapterManager * manager,
                            PyObjectPtr pyadapter, PyObject * pyType,
                            PushMode pushMode, PushGroup * pushGroup ) : PushPullInputAdapter( engine, pyTypeAsSp2Type( pyType ), pushMode, pushGroup ),
                                                                         m_pyadapter( pyadapter ),
                                                                         m_pyType( PyObjectPtr::incref( ( PyObject * ) pyType ) )
    {
    }

    //override nextPullEvent so we can release GIL while we wait
    PushPullInputAdapter::PullDataEvent * nextPullEvent() override
    {
        ReleaseGIL release;
        return PushPullInputAdapter::nextPullEvent();
    }

    void start( DateTime start, DateTime end ) override
    {
        PyObjectPtr rv = PyObjectPtr::own( PyObject_CallMethod( m_pyadapter.ptr(), "start", "OO",
                                                                PyObjectPtr::own( toPython( start ) ).ptr(),
                                                                PyObjectPtr::own( toPython( end ) ).ptr() ) );
        if( !rv.ptr() )
            SP2_THROW( PythonPassthrough, "" );

        PushPullInputAdapter::start( start, end );
    }

    void stop() override
    {
        PushPullInputAdapter::stop();

        PyObjectPtr rv = PyObjectPtr::own( PyObject_CallMethod( m_pyadapter.ptr(), "stop", nullptr ) );

        if( !rv.ptr() )
            SP2_THROW( PythonPassthrough, "" );
    }

    virtual void pushPyTick( bool live, PyObject * time, PyObject * value, PushBatch * batch ) = 0;

protected:
    PyObjectPtr m_pyadapter;
    PyObjectPtr m_pyType;
};

template<typename T>
class TypedPyPushPullInputAdapter : public PyPushPullInputAdapter
{
public:
    TypedPyPushPullInputAdapter( Engine * engine, AdapterManager * manager, PyObjectPtr pyadapter, PyObject * pyType,
                                 PushMode pushMode, PushGroup * pushGroup ):
        PyPushPullInputAdapter( engine, manager, pyadapter, pyType, pushMode, pushGroup )
    {
    }

    void pushPyTick( bool live, PyObject * time, PyObject * value, PushBatch * batch ) override
    {
        try
        {
            if( !validatePyType( this -> dataType(), m_pyType.ptr(), value ) )
                SP2_THROW( TypeError, "" );
            pushTick<T>( live, fromPython<DateTime>( time ), std::move( fromPython<T>( value, *this -> dataType() ) ), batch );
        }
        catch( const TypeError & )
        {
            SP2_THROW( TypeError, "\"" << Py_TYPE( m_pyadapter.ptr() ) -> tp_name << "\" push adapter expected output type to be of type \""
                       << pyTypeToString( m_pyType.ptr() ) << "\" got type \"" << Py_TYPE( value ) -> tp_name << "\"" );
        }
    }
};

struct PyPushPullInputAdapter_PyObject
{
    PyObject_HEAD
    PyPushPullInputAdapter * adapter;

    static PyObject * pushTick( PyPushPullInputAdapter_PyObject * self, PyObject * args, PyObject **kwargs )
    {
        SP2_BEGIN_METHOD;
        PyObject *pylive;
        PyObject *pytime;
        PyObject *pyvalue;
        PyObject *pybatch = nullptr;

        if( !PyArg_UnpackTuple( args, "push_tick", 3, 4, &pylive, &pytime, &pyvalue, &pybatch ) )
            SP2_THROW( PythonPassthrough, "" );

        PushBatch * batch = nullptr;
        if( pybatch )
        {
            if( pybatch -> ob_type != &PyPushBatch::PyType )
                SP2_THROW( TypeError, "push_tick expected PushBatch type as second argument, got " << pybatch -> ob_type -> tp_name );

            batch = &( ( PyPushBatch * ) pybatch ) -> batch;
        }

        self -> adapter -> pushPyTick( fromPython<bool>( pylive ), pytime, pyvalue, batch );

        SP2_RETURN_NONE;
    }

    static PyObject * flagReplayComplete( PyPushPullInputAdapter_PyObject * self, PyObject * args, PyObject **kwargs )
    {
        SP2_BEGIN_METHOD;
        self -> adapter -> flagReplayComplete();
        SP2_RETURN_NONE;
    }

    static PyTypeObject PyType;
};

static PyMethodDef PyPushPullInputAdapter_PyObject_methods[] = {
    { "push_tick", (PyCFunction) PyPushPullInputAdapter_PyObject::pushTick, METH_VARARGS, "push new tick" },
    { "flag_replay_complete", (PyCFunction) PyPushPullInputAdapter_PyObject::flagReplayComplete, METH_VARARGS, "finish replay ticks" },
    {NULL}
};

PyTypeObject PyPushPullInputAdapter_PyObject::PyType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_sp2impl.PyPushPullInputAdapter", /* tp_name */
    sizeof(PyPushPullInputAdapter_PyObject),    /* tp_basicsize */
    0,                         /* tp_itemsize */
    0,                         /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    0,                         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "sp2 push input adapter",  /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    PyPushPullInputAdapter_PyObject_methods,    /* tp_methods */
    0,                         /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    0,                         /* tp_init */
    0,
    PyType_GenericNew,
};

static InputAdapter * pypushpullinputadapter_creator( sp2::AdapterManager * manager, PyEngine * pyengine,
                                                      PyObject * pyType, PushMode pushMode, PyObject * args )
{
    PyTypeObject * pyAdapterType = nullptr;
    PyObject * adapterArgs = nullptr;
    PyObject * pyPushGroup;

    if( !PyArg_ParseTuple( args, "O!OO!", &PyType_Type, &pyAdapterType, &pyPushGroup, &PyTuple_Type, &adapterArgs ) )
        SP2_THROW( PythonPassthrough, "" );

    if( !PyType_IsSubtype( pyAdapterType, &PyPushPullInputAdapter_PyObject::PyType ) )
        SP2_THROW( TypeError, "Expected PushPullInputAdapter derived type, got " << pyAdapterType -> tp_name );

    sp2::PushGroup *pushGroup = nullptr;
    if( pyPushGroup != Py_None )
    {
        pushGroup = ( sp2::PushGroup * ) PyCapsule_GetPointer( pyPushGroup, nullptr );
        if( !pushGroup )
            SP2_THROW( PythonPassthrough, "" );
    }

    PyPushPullInputAdapter_PyObject * pyAdapter = ( PyPushPullInputAdapter_PyObject * ) PyObject_Call( ( PyObject * ) pyAdapterType, adapterArgs, nullptr );
    if( !pyAdapter )
        SP2_THROW( PythonPassthrough, "" );

    switchPyType( pyType,
                  [&]( auto tag )
                  {
                      pyAdapter -> adapter = pyengine -> engine() -> createOwnedObject<TypedPyPushPullInputAdapter<typename decltype(tag)::type>>(
                          manager, PyObjectPtr::own( ( PyObject * ) pyAdapter ), pyType, pushMode, pushGroup );
                  } );

    return pyAdapter -> adapter;
}

REGISTER_TYPE_INIT( &PyPushPullInputAdapter_PyObject::PyType, "PyPushPullInputAdapter" );
REGISTER_INPUT_ADAPTER( _pushpulladapter, pypushpullinputadapter_creator );

}

