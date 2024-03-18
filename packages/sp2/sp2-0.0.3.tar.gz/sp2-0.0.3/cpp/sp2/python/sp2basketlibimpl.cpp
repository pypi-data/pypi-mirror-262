#include <sp2/engine/CppNode.h>
#include <sp2/python/PyCppNode.h>

REGISTER_CPPNODE( sp2::cppnodes, _sync_list );
REGISTER_CPPNODE( sp2::cppnodes, _sample_list );

static PyModuleDef _sp2basketlibimpl_module = {
        PyModuleDef_HEAD_INIT,
        "_sp2basketlibimpl",
        "_sp2basketlibimpl c++ module",
        -1,
        NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit__sp2basketlibimpl(void)
{
    PyObject* m;

    m = PyModule_Create( &_sp2basketlibimpl_module);
    if( m == NULL )
        return NULL;

    if( !sp2::python::InitHelper::instance().execute( m ) )
        return NULL;

    return m;
}