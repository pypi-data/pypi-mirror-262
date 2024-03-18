#include <sp2/python/Conversions.h>
#include <sp2/python/Sp2TypeFactory.h>
#include <sp2/python/InitHelper.h>
#include <sp2/python/PySp2Enum.h>
#include <sp2/python/PyObjectPtr.h>

namespace sp2::python
{

DialectSp2EnumMeta::DialectSp2EnumMeta( PyTypeObjectPtr pyType, const std::string & name,
                                        const Sp2EnumMeta::ValueDef & def ) :
    Sp2EnumMeta( name, def ),
    m_pyType( pyType )
{
}

/*
MetaClass Madness NOTES!!! -- see PyStruct.cpp for note, same idea
*/

static PyObject * PySp2EnumMeta_new( PyTypeObject *subtype, PyObject *args, PyObject *kwds )
{
    SP2_BEGIN_METHOD;

    PyObject * pyname;
    PyObject * bases;
    PyObject * dict;
    if( !PyArg_ParseTuple( args, "UO!O!",
                           &pyname,
                           &PyTuple_Type, &bases,
                           &PyDict_Type, &dict ) )
        SP2_THROW( PythonPassthrough, "" );

    //subtype is python defined Sp2EnumMeta class
    PySp2EnumMeta * pymeta = ( PySp2EnumMeta * ) PyType_Type.tp_new( subtype, args, kwds );

    //Note that we call ctor without parents so as not to 0-init the base POD PyTypeObject class after its been initialized
    new ( pymeta ) PySp2EnumMeta;

    //this would be the Sp2Enum class on python side, it doesnt create any metadata for itself
    if( pymeta -> ht_type.tp_base == &PySp2Enum::PyType )
        return ( PyObject * ) pymeta;

    std::string name = PyUnicode_AsUTF8( pyname );

    PyObject * metadata = PyDict_GetItemString( dict, "__metadata__" );
    if( !metadata )
        SP2_THROW( KeyError, "Sp2EnumMeta missing __metadata__" );

    Sp2EnumMeta::ValueDef def;

    {
        PyObject *key, *value;
        Py_ssize_t pos = 0;
        while( PyDict_Next( metadata, &pos, &key, &value ) )
        {
            const char * keystr = PyUnicode_AsUTF8( key );
            if( !keystr )
                SP2_THROW( PythonPassthrough, "" );

            if( !PyLong_Check( value ) )
                SP2_THROW( TypeError, "sp2.Enum key " << keystr << " expected an integer got " << PyObjectPtr::incref( value ) );

            def[ keystr ] = fromPython<int64_t>( value );
        }
    }

    //back reference to the sp2 enum type that will be accessible on the sp2 enum -> meta()
    //intentionally dont incref here to break the circular dep of type -> shared_ptr on Sp2EnumMeta
    PyTypeObjectPtr typePtr = PyTypeObjectPtr::own( ( PyTypeObject * ) pymeta );
    auto enumMeta = std::make_shared<DialectSp2EnumMeta>( typePtr, name, def );

    pymeta -> enumMeta = enumMeta;

    //pre-create instances
    pymeta -> enumsByName  = PyObjectPtr::own( PyDict_New() );
    pymeta -> enumsByValue = PyObjectPtr::own( PyDict_New() );

    for( auto & [ key, value ] : def )
    {
        PySp2Enum * enum_ = ( PySp2Enum * ) ( (PyTypeObject * ) pymeta ) -> tp_alloc( (PyTypeObject * ) pymeta, 0 );

        new( enum_ ) PySp2Enum( enumMeta -> create( value ) );
        enum_ -> enumName  = PyObjectPtr::own( toPython( key ) );
        enum_ -> enumValue = PyObjectPtr::own( toPython<int64_t>( value ) );

        pymeta -> enumsByCValue[ value ] = PyObjectPtr::incref( enum_ );

        if( PyDict_SetItem( pymeta -> enumsByName.get(), enum_ -> enumName.get(), enum_ ) < 0 )
            SP2_THROW( PythonPassthrough, "" );

        if( PyDict_SetItem( pymeta -> enumsByValue.get(), enum_ -> enumValue.get(), enum_ ) < 0 )
            SP2_THROW( PythonPassthrough, "" );

        //We also have to update the items in the actual type's dict so FooEnum.A is a PySp2Enum!
        if( PyDict_SetItem( ( ( PyTypeObject * ) pymeta ) -> tp_dict, enum_ -> enumName.get(), enum_ ) < 0 )
            SP2_THROW( PythonPassthrough, "" );
    }

    return ( PyObject * ) pymeta;
    SP2_RETURN_NULL;
}

PyObject * PySp2EnumMeta::toPyEnum( Sp2Enum e ) const
{
    auto it = enumsByCValue.find( e.value() );
    if( it == enumsByCValue.end() )
        return nullptr;

    PyObject * rv = it -> second.get();
    Py_INCREF( rv );
    return rv;
}

void PySp2EnumMeta_dealloc( PySp2EnumMeta * m )
{
    Sp2TypeFactory::instance().removeCachedType( reinterpret_cast<PyTypeObject*>( m ) );
    m -> ~PySp2EnumMeta();
    Py_TYPE( m ) -> tp_free( m );
}

PyObject * PySp2EnumMeta_subscript( PySp2EnumMeta * self, PyObject * key )
{
    SP2_BEGIN_METHOD;

    PyObject * obj = PyDict_GetItem( self -> enumsByName.get(), key );

    if( !obj )
        SP2_THROW( ValueError, PyObjectPtr::incref( key ) << " is not a valid name on sp2.enum type " << ( ( PyTypeObject * ) self ) -> tp_name );

    Py_INCREF( obj );
    return obj;
    SP2_RETURN_NULL;
}


static PyMappingMethods PySp2EnumMeta_MappingMethods = {
    0,                               /*mp_length */
    (binaryfunc) PySp2EnumMeta_subscript, /*mp_subscript */
};

PyTypeObject PySp2EnumMeta::PyType = {
    PyVarObject_HEAD_INIT(nullptr, 0)
    "_sp2impl.PySp2EnumMeta",  /* tp_name */
    sizeof(PySp2EnumMeta),     /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor) PySp2EnumMeta_dealloc, /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    0,                         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    &PySp2EnumMeta_MappingMethods, /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
    Py_TPFLAGS_BASETYPE | Py_TPFLAGS_TYPE_SUBCLASS, /* tp_flags */
    "sp2 enum metaclass",      /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    0,                         /* tp_methods */
    0,                         /* tp_members */
    0,                         /* tp_getset */
    &PyType_Type,              /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    0,                         /*tp_init*/
    0,                         /* tp_alloc */
    (newfunc) PySp2EnumMeta_new,/* tp_new */
    PyObject_GC_Del,           /* tp_free */
};


//PySp2Enum
void PySp2Enum_dealloc( PySp2Enum * self )
{
    self -> ~PySp2Enum();
    Py_TYPE( self ) -> tp_free( self );
}

PyObject * PySp2Enum_new( PyTypeObject * type, PyObject *args, PyObject *kwds )
{
    SP2_BEGIN_METHOD;

    PyObject * pyvalue;
    if( !PyArg_ParseTuple( args, "O", &pyvalue ) )
        SP2_THROW( PythonPassthrough, "" );

    auto pymeta = (PySp2EnumMeta * ) type;
    PyObject * obj = nullptr;
    if( PyLong_Check( pyvalue ) )
        obj = PyDict_GetItem( pymeta -> enumsByValue.get(), pyvalue );
    else if( PyUnicode_Check( pyvalue ) )
        obj = PyDict_GetItem( pymeta -> enumsByName.get(), pyvalue );

    if( !obj )
        SP2_THROW( ValueError, PyObjectPtr::incref( pyvalue ) << " is not a valid value on sp2.enum type " << type -> tp_name );

    Py_INCREF( obj );
    return obj;
    SP2_RETURN_NULL;
}

PyObject * PySp2Enum_name( PySp2Enum * self, void * )
{
    Py_INCREF( self -> enumName.get() );
    return self -> enumName.get();
}

PyObject * PySp2Enum_value( PySp2Enum * self, void * )
{
    Py_INCREF( self -> enumValue.get() );
    return self -> enumValue.get();
}

static PyGetSetDef PySp2Enum_getset[] = {
    { ( char * ) "name",  (getter) PySp2Enum_name,  0, ( char * ) "string name of the enum instance", 0 },
    { ( char * ) "value", (getter) PySp2Enum_value, 0, ( char * ) "long value of the enum instance", 0 },
    { NULL }
};

PyTypeObject PySp2Enum::PyType = {
    PyVarObject_HEAD_INIT(nullptr, 0)
    "_sp2impl.PySp2Enum",      /* tp_name */
    sizeof(PySp2Enum),         /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor) PySp2Enum_dealloc, /* tp_dealloc */
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
    Py_TPFLAGS_DEFAULT |
       Py_TPFLAGS_BASETYPE,    /* tp_flags */
    "sp2 enum",                /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    0,                         /* tp_methods */
    0,                         /* tp_members */
    PySp2Enum_getset,          /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    0,                         /* tp_init */
    0,                         /* tp_alloc */
    (newfunc) PySp2Enum_new,   /* tp_new */
    0,                         /* tp_free */
};

REGISTER_TYPE_INIT( &PySp2EnumMeta::PyType, "PySp2EnumMeta" )
REGISTER_TYPE_INIT( &PySp2Enum::PyType,     "PySp2Enum" )

}
