#include <sp2/python/Conversions.h>
#include <sp2/python/Sp2TypeFactory.h>
#include <sp2/python/PyStruct.h>
#include <datetime.h>

namespace sp2::python
{

Sp2TypeFactory & Sp2TypeFactory::instance()
{
    static Sp2TypeFactory s_instance;
    return s_instance;
}

Sp2TypePtr & Sp2TypeFactory::typeFromPyType( PyObject * pyTypeObj )
{
    // List objects shouldn't be cached since they are temporary objects
    if( PyList_Check( pyTypeObj ) )
    {
        if( PyList_GET_SIZE( ( PyObject * ) pyTypeObj ) != 1 )
            SP2_THROW( TypeError, "Expected list types to be single element of sub-type" );

        PyObject *pySubType = PyList_GET_ITEM( pyTypeObj, 0 );
        if( !PyType_Check( pySubType ) )
            SP2_THROW( TypeError, "nested typed lists are not supported" );
        Sp2TypePtr elemType = typeFromPyType( pySubType );
        return Sp2ArrayType::create( elemType );
    }

    PyTypeObject *pyType = (PyTypeObject*) pyTypeObj;
    auto rv = m_cache.emplace( pyType, nullptr );
    if( rv.second )
    {
        if( pyType == &PyFloat_Type )
            rv.first -> second = sp2::Sp2Type::DOUBLE();
        else if( pyType == &PyLong_Type )
            rv.first -> second = sp2::Sp2Type::INT64();
        else if( pyType == &PyBool_Type )
            rv.first -> second = sp2::Sp2Type::BOOL();
        else if( pyType == &PyUnicode_Type )
            rv.first -> second = sp2::Sp2Type::STRING();
        else if( pyType == &PyBytes_Type )
            rv.first -> second = sp2::Sp2Type::BYTES();
        else if( PyType_IsSubtype( pyType, &PyStruct::PyType ) )
        {
            auto meta = ( ( PyStructMeta * ) pyType ) -> structMeta;
            rv.first -> second = std::make_shared<sp2::Sp2StructType>( meta );
        }
        else if( PyType_IsSubtype( pyType, &PySp2Enum::PyType ) )
        {
            auto meta = ( ( PySp2EnumMeta * ) pyType ) -> enumMeta;
            rv.first -> second = std::make_shared<sp2::Sp2EnumType>( meta );
        }
        else if( pyType == PyDateTimeAPI -> DateTimeType )
            rv.first -> second = sp2::Sp2Type::DATETIME();
        else if( pyType == PyDateTimeAPI -> DeltaType )
            rv.first -> second = sp2::Sp2Type::TIMEDELTA();
        else if( pyType == PyDateTimeAPI -> DateType )
            rv.first -> second = sp2::Sp2Type::DATE();
        else if( pyType == PyDateTimeAPI -> TimeType )
            rv.first -> second = sp2::Sp2Type::TIME();
        else
        {
            if( !PyType_Check( pyType ) )
                SP2_THROW( TypeError, "expected python type for Sp2Type got " << PyObjectPtr::incref( ( PyObject * ) pyType ) );
            rv.first -> second = sp2::Sp2Type::DIALECT_GENERIC();
        }
    }

    return rv.first -> second;
}

void Sp2TypeFactory::removeCachedType( PyTypeObject * pyType )
{
    m_cache.erase( pyType );
}

}
