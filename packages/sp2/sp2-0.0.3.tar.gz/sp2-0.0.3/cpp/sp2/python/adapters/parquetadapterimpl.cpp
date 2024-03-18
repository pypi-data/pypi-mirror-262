#include <numpy/ndarrayobject.h>
#include <sp2/adapters/parquet/ParquetInputAdapterManager.h>
#include <sp2/adapters/parquet/ParquetOutputAdapterManager.h>
#include <sp2/adapters/parquet/ParquetDictBasketOutputWriter.h>
#include <sp2/adapters/parquet/ParquetStatusUtils.h>
#include <sp2/core/Generator.h>
#include <sp2/engine/PushInputAdapter.h>
#include <sp2/python/Conversions.h>
#include <sp2/python/Exception.h>
#include <sp2/python/InitHelper.h>
#include <sp2/python/PyAdapterManagerWrapper.h>
#include <sp2/python/PyEngine.h>
#include <sp2/python/PyInputAdapterWrapper.h>
#include <sp2/python/PyOutputAdapterWrapper.h>
#include <sp2/engine/CppNode.h>
#include <sp2/engine/Sp2Type.h>
#include <sp2/python/PyCppNode.h>
#include <sp2/python/PyNodeWrapper.h>
#include <sp2/python/NumpyConversions.h>
#include <arrow/python/pyarrow.h>
#include <arrow/io/memory.h>
#include <arrow/ipc/reader.h>
#include <locale>
#include <codecvt>

using namespace sp2::adapters::parquet;
//using namespace sp2::cppnodes;
//namespace sp2::adapters::parquet
namespace sp2::cppnodes
{
DECLARE_CPPNODE( parquet_dict_basket_writer )
{
    SCALAR_INPUT( std::string, column_name );
    SCALAR_INPUT( DialectGenericType, writer );
    TS_DICTBASKET_INPUT( Generic, input );
    TS_INPUT( std::string, filename_provider );


    STATE_VAR( sp2::adapters::parquet::ParquetDictBasketOutputWriter*, s_outputWriter );

    INIT_CPPNODE( parquet_dict_basket_writer )
    {
        const sp2::python::PyObjectPtr *writerObjectPtr = reinterpret_cast<const sp2::python::PyObjectPtr *>(&writer);

        auto managerObjectPtr = sp2::python::PyObjectPtr::incref(
                PyObject_CallMethod( writerObjectPtr -> get(), "_get_output_adapter_manager", "" ) );

        auto *outputAdapterManager = dynamic_cast<ParquetOutputAdapterManager *>( sp2::python::PyAdapterManagerWrapper::extractAdapterManager(
                managerObjectPtr.get() ));

        s_outputWriter = outputAdapterManager -> createDictOutputBasketWriter( column_name.value().c_str(), input.type() );
    }

    INVOKE()
    {
        if( unlikely( filename_provider.ticked() ) )
        {
            s_outputWriter -> onFileNameChange( filename_provider.lastValue() );
        }
        if( s_outputWriter -> isFileOpen() )
        {
            const auto &shape          = input.shape();
            for( auto  &&tickedInputIt = input.tickedinputs(); tickedInputIt; ++tickedInputIt )
            {
                s_outputWriter -> writeValue( shape[ tickedInputIt.elemId() ], tickedInputIt.get() );
            }
        }
    }
};

EXPORT_CPPNODE( parquet_dict_basket_writer );
}


REGISTER_CPPNODE( sp2::cppnodes, parquet_dict_basket_writer );

namespace
{

struct PyArrowInitializer
{
    static inline bool ensureInitialized()
    {
        static bool initialized = false;
        if( unlikely( !initialized ) )
        {
            if( arrow::py::import_pyarrow() != 0 )
                SP2_THROW( sp2::python::PythonPassthrough, "" );
            initialized = true;
        }
        return initialized;
    }
};

class FileNameGenerator : public sp2::Generator<std::string, sp2::DateTime, sp2::DateTime>
{
public:

    FileNameGenerator( PyObject *wrappedGenerator )
            : m_wrappedGenerator( sp2::python::PyObjectPtr::incref( wrappedGenerator ) )
    {
    }

    void init( sp2::DateTime start, sp2::DateTime end ) override
    {
        PyObject *tp = PyTuple_New( 2 );
        if( !tp )
            SP2_THROW( sp2::python::PythonPassthrough, "" );

        PyTuple_SET_ITEM( tp, 0, sp2::python::toPython( start ) );
        PyTuple_SET_ITEM( tp, 1, sp2::python::toPython( end ) );
        m_iter = sp2::python::PyObjectPtr::check( PyObject_Call( m_wrappedGenerator.ptr(), tp, nullptr ) );
        SP2_TRUE_OR_THROW( PyIter_Check( m_iter.get() ), sp2::TypeError,
                           "Parquet file generator expected to return iterator" );
    }

    virtual bool next( std::string &value ) override
    {
        if( m_iter.ptr() == nullptr )
        {
            return false;
        }
        auto nextVal = sp2::python::PyObjectPtr::own( PyIter_Next( m_iter.ptr() ) );
        if( PyErr_Occurred() )
        {
            SP2_THROW( sp2::python::PythonPassthrough, "" );
        }
        if( nextVal.get() == nullptr )
        {
            return false;
        }
        value = sp2::python::fromPython<std::string>( nextVal.get() );
        return true;
    }

private:
    sp2::python::PyObjectPtr m_wrappedGenerator;
    sp2::python::PyObjectPtr m_iter;
};


class ArrowTableGenerator : public sp2::Generator<std::shared_ptr<arrow::Table>, sp2::DateTime, sp2::DateTime>
{
public:
    ArrowTableGenerator( PyObject *wrappedGenerator )
            : m_wrappedGenerator( sp2::python::PyObjectPtr::incref( wrappedGenerator ) )
    {
        PyArrowInitializer::ensureInitialized();
    }

    void init( sp2::DateTime start, sp2::DateTime end ) override
    {
        PyObject *tp = PyTuple_New( 2 );
        if( !tp )
            SP2_THROW( sp2::python::PythonPassthrough, "" );

        PyTuple_SET_ITEM( tp, 0, sp2::python::toPython( start ) );
        PyTuple_SET_ITEM( tp, 1, sp2::python::toPython( end ) );
        m_iter = sp2::python::PyObjectPtr::check( PyObject_Call( m_wrappedGenerator.ptr(), tp, nullptr ) );
        SP2_TRUE_OR_THROW( PyIter_Check( m_iter.ptr() ), sp2::TypeError,
                           "Parquet file generator expected to return iterator" );
    }

    virtual bool next( std::shared_ptr<arrow::Table> &value ) override
    {
        if( m_iter.ptr() == nullptr )
        {
            return false;
        }
        auto nextVal    = PyIter_Next( m_iter.ptr() );
        auto nextValPtr = sp2::python::PyObjectPtr::own( nextVal );
        if( PyErr_Occurred() )
        {
            SP2_THROW( sp2::python::PythonPassthrough, "" );
        }
        if( nextVal == nullptr )
        {
            return false;
        }

        if(!PyBytes_Check( nextVal ))
        {
            SP2_THROW( sp2::TypeError, "Invalid arrow buffer type, expected bytes got " << Py_TYPE( nextVal ) -> tp_name );
        }
        const char * data = PyBytes_AsString( nextVal );
        if( !data )
            SP2_THROW( sp2::python::PythonPassthrough, "" );
        auto size = PyBytes_Size(nextVal);
        m_data = sp2::python::PyObjectPtr::incref(nextVal);
        std::shared_ptr<arrow::io::BufferReader> bufferReader = std::make_shared<arrow::io::BufferReader>(
                reinterpret_cast<const uint8_t *>(data), size );
        std::shared_ptr<arrow::ipc::RecordBatchStreamReader> reader = arrow::ipc::RecordBatchStreamReader::Open(bufferReader.get()).ValueOrDie();
        auto result = reader->ToTable();
        if (!(result.ok()))
            SP2_THROW(sp2::RuntimeException, "Failed read arrow table from buffer");
        value = std::move(result.ValueUnsafe());
        return true;
    }
private:
    sp2::python::PyObjectPtr m_wrappedGenerator;
    sp2::python::PyObjectPtr m_iter;
    // We need to keep the last buffer in memory since arrow doesn't copy it but can refer to strings in it
    sp2::python::PyObjectPtr m_data;
};

template< typename V >
class NumpyArrayWriterImpl : public TypedDialectGenericListWriterInterface<V>
{
public:
    NumpyArrayWriterImpl( PyArray_Descr *expectedArrayDesc )
            : m_expectedArrayDesc( expectedArrayDesc )
    {
    }

    void writeItems( const sp2::DialectGenericType &listObject ) override
    {
        PyObject *object = sp2::python::toPythonBorrowed( listObject );
        if( !PyArray_Check( object ) )
        {
            SP2_THROW( sp2::TypeError, "While writing to parquet expected numpy array type, got " << Py_TYPE( object ) -> tp_name );
        }
        PyArrayObject *arrayObject = ( PyArrayObject * ) ( object );
        if( PyObject_RichCompareBool( ( PyObject * ) PyArray_DESCR( arrayObject ), ( PyObject * ) m_expectedArrayDesc, Py_EQ ) != 1 )
        {
            SP2_THROW( sp2::TypeError,
                       "Expected array of type " << sp2::python::PyObjectPtr::own( PyObject_Repr( ( PyObject * ) m_expectedArrayDesc ) )
                                                 << " got "
                                                 << sp2::python::PyObjectPtr::own( PyObject_Repr( ( PyObject * ) PyArray_DESCR( arrayObject ) ) ) );
        }

        auto ndim = PyArray_NDIM( arrayObject );

        SP2_TRUE_OR_THROW_RUNTIME( ndim == 1, "While writing to parquet expected numpy array with 1 dimension" << " got " << ndim );

        auto arraySize = PyArray_Size( object );
        if(PyArray_ISCARRAY_RO(arrayObject))
        {
            V *data = reinterpret_cast<V *>(PyArray_DATA( arrayObject ));
            for( decltype( arraySize ) i = 0; i < arraySize; ++i )
            {
                this->writeValue(data[i]);
            }
        }
        else
        {
            for(decltype( arraySize ) i = 0; i < arraySize; ++i)
            {
                this->writeValue(*reinterpret_cast<V*>(PyArray_GETPTR1(arrayObject, i)));
            }
        }
    }
private:
    PyArray_Descr *m_expectedArrayDesc;
};

class NumpyUnicodeArrayWriter : public TypedDialectGenericListWriterInterface<std::string>
{
public:
    NumpyUnicodeArrayWriter( PyArray_Descr *expectedArrayDesc )
            : m_expectedArrayDesc( expectedArrayDesc )
    {
    }

    void writeItems( const sp2::DialectGenericType &listObject ) override
    {
        PyObject *object = sp2::python::toPythonBorrowed( listObject );

        if( !PyArray_Check( object ) )
        {
            SP2_THROW( sp2::TypeError, "While writing to parquet expected numpy array type, got " << Py_TYPE( object ) -> tp_name );
        }
        PyArrayObject *arrayObject = ( PyArrayObject * ) ( object );

        if( PyArray_DESCR( arrayObject ) -> type_num != NPY_UNICODE )
        {
            SP2_THROW( sp2::TypeError,
                       "Expected array of type " << sp2::python::PyObjectPtr::own( PyObject_Repr( ( PyObject * ) m_expectedArrayDesc ) )
                                                 << " got "
                                                 << sp2::python::PyObjectPtr::own(
                                                         PyObject_Repr( ( PyObject * ) PyArray_DESCR( arrayObject ) ) ) );
        }

        auto elementSize = PyArray_DESCR( arrayObject ) -> elsize;
        auto ndim        = PyArray_NDIM( arrayObject );

        SP2_TRUE_OR_THROW_RUNTIME( ndim == 1, "While writing to parquet expected numpy array with 1 dimension" << " got " << ndim );
        std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;

        auto arraySize = PyArray_Size( object );
        if( PyArray_ISCARRAY_RO( arrayObject ) )
        {
            auto data = reinterpret_cast<char *>(PyArray_DATA( arrayObject ));

            for( decltype( arraySize ) i = 0; i < arraySize; ++i )
            {

                std::string value = converter.to_bytes( reinterpret_cast<wchar_t *>(data + elementSize * i),
                                                          reinterpret_cast<wchar_t *>(data + elementSize * ( i + 1 )) );
                this -> writeValue( value );
            }
        }
        else
        {
            for( decltype( arraySize ) i = 0; i < arraySize; ++i )
            {
                char        *elementPtr = reinterpret_cast<char *>(PyArray_GETPTR1( arrayObject, i ));
                std::string value       = converter.to_bytes( reinterpret_cast<wchar_t *>(elementPtr),
                                                                reinterpret_cast<wchar_t *>(elementPtr + elementSize ) );
                this -> writeValue( value );
            }
        }
    }

private:
    PyArray_Descr *m_expectedArrayDesc;
};

static inline DialectGenericListWriterInterface::Ptr create_numpy_array_writer_impl( const sp2::Sp2TypePtr &type )
{
    try
    {
        return sp2::PartialSwitchSp2Type<sp2::Sp2Type::Type::DOUBLE, sp2::Sp2Type::Type::INT64,
                sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::STRING>::invoke(
                type.get(),
                []( auto tag ) -> DialectGenericListWriterInterface::Ptr
                {
                    using CValueType = typename decltype(tag)::type;
                    auto numpy_dtype = PyArray_DescrFromType(
                            sp2::python::NPY_TYPE<CValueType>::value );

                    if( numpy_dtype -> type_num == NPY_UNICODE )
                    {
                        return std::make_shared<NumpyUnicodeArrayWriter>(
                                numpy_dtype );
                    }
                    else
                    {
                        return std::make_shared<NumpyArrayWriterImpl<CValueType>>(
                                numpy_dtype );
                    }
                }
        );
    }
    catch( sp2::TypeError &e )
    {
        SP2_THROW( sp2::TypeError, "Unsupported array value type when writing to parquet:" << type -> type().asString() );
    }
}


template< typename V >
class NumpyArrayReaderImpl final : public TypedDialectGenericListReaderInterface<V>
{
public:
    NumpyArrayReaderImpl( PyArray_Descr *expectedArrayDesc )
    : m_expectedArrayDesc( expectedArrayDesc )
    {
    }
    virtual sp2::DialectGenericType create(uint32_t size) override
    {
        npy_intp iSize = size;

        Py_INCREF(m_expectedArrayDesc);
        PyObject* arr = PyArray_SimpleNewFromDescr( 1, &iSize, m_expectedArrayDesc );
        // Since arr already has reference count
        sp2::python::PyObjectPtr objectPtr{sp2::python::PyObjectPtr::own(arr)};

        // We need to make sure that's the case, since we are going to return pointer to raw buffer
        SP2_ASSERT(PyArray_ISCARRAY( reinterpret_cast<PyArrayObject *>(arr)));

        sp2::DialectGenericType res{sp2::python::fromPython<sp2::DialectGenericType>(arr)};
        return res;
    }

    sp2::DialectGenericType create( uint32_t size, uint32_t maxElementSize ) override
    {
        SP2_NOT_IMPLEMENTED;
    }

    virtual V *getRawDataBuffer( const sp2::DialectGenericType &list ) const override
    {
        auto arrayObject = reinterpret_cast<PyArrayObject *>(sp2::python::toPythonBorrowed(list));
        return reinterpret_cast<V *>(PyArray_DATA( arrayObject ));
    }

    virtual void setValue(const sp2::DialectGenericType& list, int index, const V& value) override
    {
        getRawDataBuffer(list)[index] = value;
    }

private:
    PyArray_Descr *m_expectedArrayDesc;
};

class NumpyUnicodeReaderImpl final : public TypedDialectGenericListReaderInterface<std::string>
{
public:
    NumpyUnicodeReaderImpl( PyArray_Descr *expectedArrayDesc )
            : m_expectedArrayDesc( expectedArrayDesc )
    {
    }

    virtual sp2::DialectGenericType create( uint32_t size ) override
    {
        SP2_NOT_IMPLEMENTED;
    }

    sp2::DialectGenericType create( uint32_t size, uint32_t maxElementSize ) override
    {
        npy_intp iSize = size;

        PyArray_Descr *typ;
        PyObject      *type_string_descr = sp2::python::toPython( std::string( "U" ) + std::to_string( maxElementSize ) );
        PyArray_DescrConverter( type_string_descr, &typ );
        Py_DECREF( type_string_descr );

        PyObject *arr = PyArray_SimpleNewFromDescr( 1, &iSize, typ );

        // Since arr already has reference count
        sp2::python::PyObjectPtr objectPtr{ sp2::python::PyObjectPtr::own( arr ) };

        sp2::DialectGenericType res{ sp2::python::fromPython<sp2::DialectGenericType>( arr ) };
        return res;
    }

    std::string *getRawDataBuffer( const sp2::DialectGenericType &list ) const override
    {
        return nullptr;
    }

    void setValue( const sp2::DialectGenericType &list, int index, const std::string &value ) override
    {
        auto arrayObject = reinterpret_cast<PyArrayObject *>(sp2::python::toPythonBorrowed( list ));
        std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
        auto elementSize = PyArray_DESCR( arrayObject ) -> elsize;
        auto wideValue = converter.from_bytes( value );
        auto nElementsToCopy = std::min( int(elementSize / sizeof(wchar_t)), int( wideValue.size() + 1 ) );
        std::copy_n( wideValue.c_str(), nElementsToCopy, reinterpret_cast<wchar_t *>(PyArray_GETPTR1( arrayObject, index )) );
    }

private:
    PyArray_Descr *m_expectedArrayDesc;
};


inline DialectGenericListReaderInterface::Ptr create_numpy_array_reader_impl( const sp2::Sp2TypePtr &type )

{
    try
    {
        return sp2::PartialSwitchSp2Type<sp2::Sp2Type::Type::DOUBLE, sp2::Sp2Type::Type::INT64,
                sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::STRING>::invoke( type.get(),
                                                                               []( auto tag ) -> DialectGenericListReaderInterface::Ptr
                                                                               {
                                                                                   using CValueType = typename decltype(tag)::type;
                                                                                   auto numpy_dtype = PyArray_DescrFromType(
                                                                                           sp2::python::NPY_TYPE<CValueType>::value );

                                                                                   if( numpy_dtype -> type_num == NPY_UNICODE )
                                                                                   {
                                                                                       return std::make_shared<NumpyUnicodeReaderImpl>(
                                                                                               numpy_dtype );
                                                                                   }
                                                                                   else
                                                                                   {
                                                                                       return std::make_shared<NumpyArrayReaderImpl<CValueType>>(
                                                                                               numpy_dtype );
                                                                                   }
                                                                               }
        );
    }
    catch( sp2::TypeError &e )
    {
        SP2_THROW( sp2::TypeError, "Unsupported array value type when reading from parquet:" << type -> type().asString() );
    }
}

}

namespace sp2::python
{

//AdapterManager
sp2::AdapterManager *create_parquet_input_adapter_manager_impl( PyEngine *engine, const Dictionary &properties,
                                                                FileNameGenerator::Ptr fileNameGenerator,
                                                                ArrowTableGenerator::Ptr arrowTableGenerator )
{
    auto res = engine -> engine() -> createOwnedObject<ParquetInputAdapterManager>( properties, fileNameGenerator, arrowTableGenerator );
    return res;
}

static InputAdapter *
create_parquet_input_adapter( sp2::AdapterManager *manager, PyEngine *pyengine, PyObject *pyType, PushMode pushMode,
                              PyObject *args )
{
    auto &sp2Type = pyTypeAsSp2Type( pyType );

    PyObject *pyProperties;
    PyObject *type;

    auto *parquetManager = dynamic_cast<ParquetInputAdapterManager *>( manager );
    if( !parquetManager )
        SP2_THROW( TypeError, "Expected ParquetAdapterManager" );

    if( !PyArg_ParseTuple( args, "O!O!",
                           &PyType_Type, &type,
                           &PyDict_Type, &pyProperties ) )
        SP2_THROW( PythonPassthrough, "" );

    auto propertiesDict = fromPython<Dictionary>( pyProperties );

    if( propertiesDict.get( "is_array", false ) )
    {
        auto &&valueType = pyTypeAsSp2Type( toPythonBorrowed( propertiesDict.get<DialectGenericType>( "array_value_type" ) ) );
        return parquetManager -> getInputAdapter( valueType, propertiesDict, pushMode,
                                                  create_numpy_array_reader_impl( valueType ) );
    }
    else
    {
        return parquetManager -> getInputAdapter( sp2Type, propertiesDict, pushMode );
    }
}

static OutputAdapter *create_parquet_output_adapter( sp2::AdapterManager *manager, PyEngine *pyengine, PyObject *args )
{
    PyObject *pyProperties;
    PyObject *pyType;

    auto *parquetManager = dynamic_cast<ParquetOutputAdapterManager *>( manager );
    if( !parquetManager )
        SP2_THROW( TypeError, "Expected ParquetAdapterManager" );

    if( !PyArg_ParseTuple( args, "O!O!",
                           &PyType_Type, &pyType,
                           &PyDict_Type, &pyProperties ) )
        SP2_THROW( PythonPassthrough, "" );

    auto &sp2Type = pyTypeAsSp2Type( pyType );
    auto &&propertiesDict = fromPython<Dictionary>( pyProperties );
    if( propertiesDict.get( "is_array", false ) )
    {
        auto &&valueType = pyTypeAsSp2Type( toPythonBorrowed( propertiesDict.get<DialectGenericType>( "array_value_type" ) ) );
        return parquetManager -> getListOutputAdapter( valueType, propertiesDict, create_numpy_array_writer_impl( valueType ) );
    }
    else
    {
        return parquetManager -> getOutputAdapter( sp2Type, propertiesDict );
    }
}

static OutputAdapter *create_parquet_dict_basket_output_adapter( sp2::AdapterManager *manager, PyEngine *pyengine, PyObject *args )
{
    PyObject *pyProperties;
    PyObject *pyType;
    auto     *parquetManager = dynamic_cast<ParquetOutputAdapterManager *>( manager );
    if( !parquetManager )
        SP2_THROW( TypeError, "Expected ParquetOutputAdapterManager" );
    if( !PyArg_ParseTuple( args, "O!O!",
                           &PyTuple_Type, &pyType,
                           &PyDict_Type, &pyProperties ) )
        SP2_THROW( PythonPassthrough, "" );
    PyObject *keyType;
    PyObject *valueType;
    if( !PyArg_ParseTuple( pyType, "O!O!",
                           &PyType_Type, &keyType,
                           &PyType_Type, &valueType ) )
        SP2_THROW( PythonPassthrough, "Invalid basket key/value tuple" );

    auto sp2KeyType   = pyTypeAsSp2Type( keyType );
    auto sp2ValueType = pyTypeAsSp2Type( valueType );

    SP2_THROW( NotImplemented, "Output basket is not implement yet" );
//    PyObject *pyProperties;
//    PyObject *pyType;
//
//
//    if( !PyArg_ParseTuple( args, "O!O!",
//                           &PyType_Type, &pyType,
//                           &PyDict_Type, &pyProperties ))
//        SP2_THROW( PythonPassthrough, "" );
//
//    auto &sp2Type = pyTypeAsSp2Type( pyType );
//
//    return parquetManager->getOutputAdapter( sp2Type, fromPython<Dictionary>( pyProperties ));
}

static OutputAdapter *parquet_output_filename_adapter( sp2::AdapterManager *manager, PyEngine *pyengine, PyObject *args )
{
    auto *parquetManager = dynamic_cast<ParquetOutputAdapterManager *>( manager );
    if( !parquetManager )
        SP2_THROW( TypeError, "Expected ParquetAdapterManager" );

    if( !PyArg_ParseTuple( args, "" ) )
        SP2_THROW( PythonPassthrough, "" );

    return parquetManager -> createOutputFileNameAdapter();
}

static PyObject *create_parquet_input_adapter_manager( PyObject *args )
{
    SP2_BEGIN_METHOD ;
        PyEngine *pyEngine        = nullptr;
        PyObject *pyProperties    = nullptr;
        PyObject *pyFileGenerator = nullptr;

        if( !PyArg_ParseTuple( args, "O!O!O!",
                               &PyEngine::PyType, &pyEngine,
                               &PyDict_Type, &pyProperties,
                               &PyFunction_Type, &pyFileGenerator ) )
            SP2_THROW( PythonPassthrough, "" );

        std::shared_ptr<FileNameGenerator>   fileNameGenerator;
        std::shared_ptr<ArrowTableGenerator> arrowTableGenerator;

        auto dictionary = fromPython<Dictionary>( pyProperties );
        if( dictionary.get<bool>( "read_from_memory_tables" ) )
        {
            arrowTableGenerator = std::make_shared<ArrowTableGenerator>( pyFileGenerator );
        }
        else
        {
            fileNameGenerator = std::make_shared<FileNameGenerator>( pyFileGenerator );
        }
        auto *adapterMgr = create_parquet_input_adapter_manager_impl( pyEngine, fromPython<Dictionary>( pyProperties ),
                                                                      fileNameGenerator, arrowTableGenerator );
        auto res         = PyCapsule_New( adapterMgr, "adapterMgr", nullptr );
        return res;
    SP2_RETURN_NULL;
}

//AdapterManager
sp2::AdapterManager *create_parquet_output_adapter_manager( PyEngine *engine, const Dictionary &properties )
{
    ParquetOutputAdapterManager::FileVisitorCallback fileVisitor;
    DialectGenericType pyFilenameVisitorDG;
    if( properties.tryGet( "file_visitor", pyFilenameVisitorDG ) )
    {
        PyObjectPtr pyFilenameVisitor = PyObjectPtr::own( toPython( pyFilenameVisitorDG ) );
        fileVisitor = [pyFilenameVisitor]( const std::string & filename )
            {
                PyObjectPtr rv =  PyObjectPtr::own( PyObject_CallFunction( pyFilenameVisitor.get(), "O", PyObjectPtr::own( toPython( filename ) ).get() ) );
                if( !rv.get() )
                    SP2_THROW( PythonPassthrough, "" );
            };
    }
    return engine -> engine() -> createOwnedObject<ParquetOutputAdapterManager>( properties, fileVisitor );
}


REGISTER_ADAPTER_MANAGER_CUSTOM_CREATOR( _parquet_input_adapter_manager, create_parquet_input_adapter_manager );

REGISTER_ADAPTER_MANAGER( _parquet_output_adapter_manager, create_parquet_output_adapter_manager );

REGISTER_INPUT_ADAPTER( _parquet_input_adapter, create_parquet_input_adapter );

REGISTER_OUTPUT_ADAPTER( _parquet_output_adapter, create_parquet_output_adapter );

REGISTER_OUTPUT_ADAPTER( _parquet_dict_basket_output_adapter, create_parquet_dict_basket_output_adapter );

REGISTER_OUTPUT_ADAPTER( _parquet_output_filename_adapter, parquet_output_filename_adapter );
static PyModuleDef _parquetadapterimpl_module = {
        PyModuleDef_HEAD_INIT,
        "_parquetadapterimpl",
        "_parquetadapterimpl c++ module",
        -1,
        NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit__parquetadapterimpl( void )
{
    PyObject *m;

    m = PyModule_Create( &_parquetadapterimpl_module );
    if( m == NULL )
    {
        return NULL;
    }

    if( !InitHelper::instance().execute( m ) )
    {
        return NULL;
    }

    import_array();

    return m;
}

}
