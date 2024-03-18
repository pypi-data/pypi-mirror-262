#include <sp2/engine/InputAdapter.h>
#include <sp2/python/Conversions.h>
#include <sp2/python/Exception.h>
#include <sp2/python/InitHelper.h>
#include <sp2/python/PyEngine.h>
#include <sp2/python/PyInputAdapterWrapper.h>
#include <sp2/python/PyAdapterManagerWrapper.h>

namespace sp2::python
{

PyObject * PyInputAdapterWrapper::createAdapter( Creator creator, PyObject * args )
{
    SP2_BEGIN_METHOD;


    PyObject * pyAdapterManager = nullptr;

    PyEngine * pyEngine   = nullptr;
    PyObject * pyType     = nullptr;
    PyObject * pyArgs     = nullptr;
    int        pushmode   = -1;

    if( !PyArg_ParseTuple( args, "OO!OiO!",
                           &pyAdapterManager,
                           &PyEngine::PyType, &pyEngine,
                           &pyType,
                           &pushmode,
                           &PyTuple_Type, &pyArgs ) )
        SP2_THROW( PythonPassthrough, "" );

    if( pushmode == PushMode::UNKNOWN || pushmode >= PushMode::NUM_TYPES )
        SP2_THROW( ValueError, "invalid pushmode " << pushmode );

    sp2::AdapterManager *adapterMgr  = nullptr;
    if( PyCapsule_CheckExact( pyAdapterManager ) )
        adapterMgr = PyAdapterManagerWrapper::extractAdapterManager( pyAdapterManager );

    auto adapter = creator( adapterMgr, pyEngine, pyType, PushMode( pushmode ), pyArgs );

    return create( adapter );
    SP2_RETURN_NULL;
}

PyObject * PyInputAdapterWrapper::create( InputAdapter * adapter )
{
    SP2_BEGIN_METHOD;
    PyInputAdapterWrapper * object = ( PyInputAdapterWrapper * ) PyInputAdapterWrapper::PyType.tp_alloc( &PyInputAdapterWrapper::PyType, 0 );
    new( object ) PyInputAdapterWrapper( adapter );
    return object;
    SP2_RETURN_NULL;
}

PyTypeObject PyInputAdapterWrapper::PyType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_sp2impl.PyInputAdapterWrapper", /* tp_name */
    sizeof(PyInputAdapterWrapper),    /* tp_basicsize */
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
    Py_TPFLAGS_DEFAULT,        /* tp_flags */
    "sp2 input adapter wrapper", /* tp_doc */
};

REGISTER_TYPE_INIT( &PyInputAdapterWrapper::PyType, "PyInputAdapterWrapper" )

}
