#include <sp2/engine/AdapterManager.h>
#include <sp2/engine/StatusAdapter.h>
#include <sp2/python/Conversions.h>
#include <sp2/python/Exception.h>
#include <sp2/python/PyEngine.h>
#include <sp2/python/PyAdapterManagerWrapper.h>
#include <sp2/python/PyInputAdapterWrapper.h>

namespace sp2::python
{

PyObject * PyAdapterManagerWrapper::create( Creator creator, PyObject * args )
{
    SP2_BEGIN_METHOD;

    PyEngine * pyEngine     = nullptr;
    PyObject * pyProperties = nullptr;

    if( !PyArg_ParseTuple( args, "O!O!",
                           &PyEngine::PyType, &pyEngine,
                           &PyDict_Type, &pyProperties ) )
        SP2_THROW( PythonPassthrough, "" );

    auto * adapterMgr = creator( pyEngine, fromPython<Dictionary>( pyProperties ) );

    return PyCapsule_New( adapterMgr, "adapterMgr", nullptr );
    SP2_RETURN_NULL;
}

sp2::AdapterManager * PyAdapterManagerWrapper::extractAdapterManager( PyObject * wrapper )
{
    return ( sp2::AdapterManager * ) PyCapsule_GetPointer( wrapper, "adapterMgr" );
}

static StatusAdapter * create_status_adapter( sp2::AdapterManager * manager, PyEngine * pyengine, PyObject * pyType, PushMode pushMode, PyObject * args )
{
    auto & sp2Type = pyTypeAsSp2Type( pyType );
    return manager -> createStatusAdapter( sp2Type, pushMode );
}

REGISTER_INPUT_ADAPTER( _status_adapter, create_status_adapter );

}
