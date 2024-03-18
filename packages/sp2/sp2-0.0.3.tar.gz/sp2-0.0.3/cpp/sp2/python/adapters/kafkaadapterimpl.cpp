#include <sp2/adapters/kafka/KafkaAdapterManager.h>
#include <sp2/engine/PushInputAdapter.h>
#include <sp2/python/Conversions.h>
#include <sp2/python/Exception.h>
#include <sp2/python/InitHelper.h>
#include <sp2/python/PyAdapterManagerWrapper.h>
#include <sp2/python/PyEngine.h>
#include <sp2/python/PyInputAdapterWrapper.h>
#include <sp2/python/PyOutputAdapterWrapper.h>

using namespace sp2::adapters::kafka;

namespace sp2::python
{

//AdapterManager
sp2::AdapterManager * create_kafka_adapter_manager( PyEngine * engine, const Dictionary & properties )
{
    return engine -> engine() -> createOwnedObject<KafkaAdapterManager>( properties );
}

static InputAdapter * create_kafka_input_adapter( sp2::AdapterManager * manager, PyEngine * pyengine, PyObject * pyType, PushMode pushMode, PyObject * args )
{
    auto & sp2Type = pyTypeAsSp2Type( pyType );

    PyObject * pyProperties;
    PyObject * type;

    auto * kafkaManager = dynamic_cast<KafkaAdapterManager*>( manager );
    if( !kafkaManager )
        SP2_THROW( TypeError, "Expected KafkaAdapterManager" );

    if( !PyArg_ParseTuple( args, "O!O!",
                           &PyType_Type, &type,
                           &PyDict_Type, &pyProperties ) )
        SP2_THROW( PythonPassthrough, "" );

    return kafkaManager -> getInputAdapter( sp2Type, pushMode, fromPython<Dictionary>( pyProperties ) );
}

static OutputAdapter * create_kafka_output_adapter( sp2::AdapterManager * manager, PyEngine * pyengine, PyObject * args )
{
    PyObject * pyProperties;
    PyObject * pyType;

    auto * kafkaManager = dynamic_cast<KafkaAdapterManager*>( manager );
    if( !kafkaManager )
        SP2_THROW( TypeError, "Expected KafkaAdapterManager" );

    if( !PyArg_ParseTuple( args, "OO!",
                           &pyType,
                           &PyDict_Type, &pyProperties ) )
        SP2_THROW( PythonPassthrough, "" );

    auto & sp2Type = pyTypeAsSp2Type( pyType );

    return kafkaManager -> getOutputAdapter( sp2Type, fromPython<Dictionary>( pyProperties ) );
}

REGISTER_ADAPTER_MANAGER( _kafka_adapter_manager, create_kafka_adapter_manager );
REGISTER_INPUT_ADAPTER(   _kafka_input_adapter,   create_kafka_input_adapter );
REGISTER_OUTPUT_ADAPTER(  _kafka_output_adapter,  create_kafka_output_adapter );

static PyModuleDef _kafkaadapterimpl_module = {
        PyModuleDef_HEAD_INIT,
        "_kafkaadapterimpl",
        "_kafkaadapterimpl c++ module",
        -1,
        NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit__kafkaadapterimpl(void)
{
    PyObject* m;

    m = PyModule_Create( &_kafkaadapterimpl_module);
    if( m == NULL )
        return NULL;

    if( !InitHelper::instance().execute( m ) )
        return NULL;

    return m;
}

}
