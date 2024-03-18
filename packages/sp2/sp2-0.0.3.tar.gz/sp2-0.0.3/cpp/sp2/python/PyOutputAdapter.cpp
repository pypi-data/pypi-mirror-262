#include <sp2/core/Time.h>
#include <sp2/engine/OutputAdapter.h>
#include <sp2/python/Conversions.h>
#include <sp2/python/Exception.h>
#include <sp2/python/PyEngine.h>
#include <sp2/python/PyInputAdapterWrapper.h>
#include <sp2/python/PyObjectPtr.h>
#include <sp2/python/PyOutputAdapterWrapper.h>
#include <sp2/python/PyNodeWrapper.h>

namespace sp2::python
{

class PyOutputAdapter : public OutputAdapter
{
public:
    PyOutputAdapter(
        Engine * engine,
        PyObjectPtr pyadapter
    )
        : OutputAdapter( engine ),
          m_pyadapter( pyadapter )
    {}

    void executeImpl() override;
    void start() override;
    void stop() override;

    const char * name() const override { return "PyOutputAdapter"; }
private:
    PyObjectPtr m_pyadapter;
};

void PyOutputAdapter::executeImpl()
{
    const TimeSeriesProvider *inputs = input();

    PyObject* last_time = toPython(inputs->lastTime());
    PyObject* last_value = lastValueToPython(inputs);

    PyObjectPtr rv = PyObjectPtr::own(
        PyObject_CallMethod(
            m_pyadapter.ptr(),
            "on_tick",
            "OO",
            PyObjectPtr::own(last_time).ptr(),
            PyObjectPtr::own(last_value).ptr()
        )
    );
    if( !rv.ptr() )
        SP2_THROW( PythonPassthrough, "" );
}

void PyOutputAdapter::start()
{
    PyObjectPtr rv = PyObjectPtr::own( PyObject_CallMethod( m_pyadapter.ptr(), "start", nullptr ) );
    if( !rv.ptr() )
        SP2_THROW( PythonPassthrough, "" );
}

void PyOutputAdapter::stop()
{
    PyObjectPtr rv = PyObjectPtr::own( PyObject_CallMethod( m_pyadapter.ptr(), "stop", nullptr ) );
    if( !rv.ptr() )
        SP2_THROW( PythonPassthrough, "" );
}

static OutputAdapter * pyoutputadapter_creator( sp2::AdapterManager * manager, PyEngine * pyengine, PyObject * args )
{
    PyTypeObject * pyAdapterType = nullptr;
    PyObject * adapterArgs = nullptr;

     if( !PyArg_ParseTuple( args, "O!O!", &PyType_Type, &pyAdapterType,
                           &PyTuple_Type, &adapterArgs ) )
        SP2_THROW( PythonPassthrough, "" );

    PyObject * pyAdapter = PyObject_Call( ( PyObject * ) pyAdapterType, adapterArgs, nullptr );
    if( !pyAdapter )
        SP2_THROW( PythonPassthrough, "" );

    return pyengine -> engine() -> createOwnedObject<PyOutputAdapter>( PyObjectPtr::own( pyAdapter ) );
}

// NOTE: no python object is exported as its not needed
// at this time.

REGISTER_OUTPUT_ADAPTER( _outputadapter, pyoutputadapter_creator );

}
