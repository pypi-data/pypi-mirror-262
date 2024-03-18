#include <sp2/python/InitHelper.h>
#include <frameobject.h>
#include <traceback.h>

namespace sp2::python
{

static PyModuleDef _sp2typesimpl_module = {
    PyModuleDef_HEAD_INIT,
    "_sp2typesimpl",
    "_sp2typesimpl c++ module",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit__sp2typesimpl(void)
{
    PyObject* m;

    m = PyModule_Create( &_sp2typesimpl_module);
    if( m == NULL )
        return NULL;

    if( !InitHelper::instance().execute( m ) )
        return NULL;

    return m;
}

}
