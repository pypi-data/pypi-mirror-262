#include <sp2/engine/DynamicEngine.h>
#include <sp2/python/Conversions.h>
#include <sp2/python/InitHelper.h>
#include <sp2/python/PyEngine.h>
#include <sp2/python/PyNode.h>
#include <frameobject.h>
#include <traceback.h>
namespace sp2::python
{

static PyObject * _sp2_now( PyObject*, PyObject * nodeptr )
{
    SP2_BEGIN_METHOD;

    sp2::Node * node = reinterpret_cast<sp2::Node *>( fromPython<uint64_t>( nodeptr ) );
    return toPython( node -> now() );

    SP2_RETURN_NULL;
}

static PyObject * _engine_start_time( PyObject*, PyObject * nodeptr )
{
    SP2_BEGIN_METHOD;

    sp2::Node * node = reinterpret_cast<sp2::Node *>( fromPython<uint64_t>( nodeptr ) );
    return toPython( node -> rootEngine() -> startTime() );

    SP2_RETURN_NULL;
}

static PyObject * _engine_stats( PyObject*, PyObject * nodeptr )
{
    SP2_BEGIN_METHOD;

    sp2::Node * node = reinterpret_cast<sp2::Node *>( fromPython<uint64_t>( nodeptr ) );
    return toPython( node -> rootEngine() -> engine_stats() );

    SP2_RETURN_NULL;
}


static PyObject * _engine_end_time( PyObject*, PyObject * nodeptr )
{
    SP2_BEGIN_METHOD;

    sp2::Node * node = reinterpret_cast<sp2::Node *>( fromPython<uint64_t>( nodeptr ) );
    return toPython( node -> rootEngine() -> endTime() );

    SP2_RETURN_NULL;
}

static PyObject * _sp2_stop_engine( PyObject*, PyObject * args, PyObject * kwargs )
{
    SP2_BEGIN_METHOD;
    int dynamicOnly = 0;
    uint64_t nodeptr;
    static const char * kwlist[] = { "node", "dynamic", nullptr };
    if( !PyArg_ParseTupleAndKeywords( args, kwargs, "L|p", ( char ** ) kwlist, &nodeptr, &dynamicOnly ) )
        SP2_THROW( PythonPassthrough, "" );

    sp2::Node * node = reinterpret_cast<sp2::Node *>( nodeptr );
    if( dynamicOnly && !node -> engine() -> isRootEngine() )
        static_cast<DynamicEngine *>( node -> engine() ) -> shutdown();
    else
        node -> rootEngine() -> shutdown();
    SP2_RETURN_NONE;
}

//Ingloriously stolen from Python 3.7.0!
static PyObject *_create_traceback( PyObject *, PyObject * args )
{
    SP2_BEGIN_METHOD;

    PyObject *next;
    PyFrameObject *frame;
    int lasti;
    int lineno;

    if( !PyArg_ParseTuple( args, "OO!ii",
                           &next,
                           &PyFrame_Type, &frame, &lasti, &lineno ) )
        SP2_THROW( PythonPassthrough, "" );

    if( next == Py_None )
        next = nullptr;
    else if( !PyTraceBack_Check( next ) )
        SP2_THROW( TypeError, "expected traceback type" );

    PyTracebackObject *tb;
    tb = PyObject_GC_New( PyTracebackObject, &PyTraceBack_Type );
    if( tb != NULL )
    {
        Py_XINCREF(next);
        tb -> tb_next = (PyTracebackObject * ) next;
        Py_XINCREF(frame);
        tb -> tb_frame = frame;
        tb -> tb_lasti = lasti;
        tb -> tb_lineno = lineno;
        PyObject_GC_Track( tb );
    }

    return (PyObject *)tb;

    SP2_RETURN_NULL
}

static PyObject *_set_capture_cpp_backtrace( PyObject *, PyObject *args )
{
    SP2_BEGIN_METHOD;
    int value;

    if( !PyArg_ParseTuple( args, "p", &value ) )
        SP2_THROW( PythonPassthrough, "" );
    capture_cpp_exception_trace_flag() = bool( value );
    SP2_RETURN_NONE;
}


static PyMethodDef _sp2impl_methods[] = {
    {"_sp2_now",                    (PyCFunction) _sp2_now,                   METH_O, "current engine time"},
    {"_sp2_engine_start_time",      (PyCFunction) _engine_start_time,         METH_O, "engine start time"},
    {"_sp2_engine_end_time",        (PyCFunction) _engine_end_time,           METH_O, "engine end time"},
    {"_sp2_stop_engine",            (PyCFunction) _sp2_stop_engine,           METH_VARARGS | METH_KEYWORDS, "stop engine"},
    {"create_traceback",            (PyCFunction) _create_traceback,          METH_VARARGS,   "internal"},
    {"_sp2_engine_stats",           (PyCFunction) _engine_stats,              METH_O, "engine statistics"},
    {"set_capture_cpp_backtrace",   (PyCFunction) _set_capture_cpp_backtrace, METH_VARARGS,   "internal"},
    { nullptr },
};

static PyModuleDef _sp2impl_module = {
    PyModuleDef_HEAD_INIT,
    "_sp2impl",
    "_sp2impl c++ module",
    -1,
    _sp2impl_methods, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit__sp2impl(void)
{
    PyObject* m;

    m = PyModule_Create( &_sp2impl_module);
    if( m == NULL )
        return NULL;

    if( !InitHelper::instance().execute( m ) )
        return NULL;

    return m;
}

}
