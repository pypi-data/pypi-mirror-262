#ifndef _IN_SP2_PYTHON_PYPUSHINPUTADAPTER_H
#define _IN_SP2_PYTHON_PYPUSHINPUTADAPTER_H

#include <sp2/engine/PushInputAdapter.h>

namespace sp2::python
{

//PushBatch
struct PyPushBatch
{
    PyObject_HEAD
    PushBatch batch;

    static PyTypeObject PyType;
};

}

#endif
