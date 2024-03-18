#ifndef _IN_SP2_PYTHON_PYADAPTERMANAGER_H
#define _IN_SP2_PYTHON_PYADAPTERMANAGER_H

#include <Python.h>

namespace sp2 { class AdapterManager; }

namespace sp2::python
{

struct PyAdapterManager_PyObject
{
    PyObject_HEAD
    sp2::AdapterManager * manager;

    static PyTypeObject PyType;
};

}

#endif
