#ifndef _IN_SP2_PYTHON_PYINPUTADAPTERWRAPPER_H
#define _IN_SP2_PYTHON_PYINPUTADAPTERWRAPPER_H

#include <Python.h>
#include <sp2/engine/Enums.h>
#include <sp2/python/Exception.h>
#include <sp2/python/InitHelper.h>

namespace sp2 { class AdapterManager; class InputAdapter; }

namespace sp2::python
{

class PyEngine;

class PyInputAdapterWrapper : public PyObject
{
public:
    PyInputAdapterWrapper( InputAdapter * adapter ) : m_adapter( adapter )
    {}

    InputAdapter * adapter() { return m_adapter; }

    using Creator = std::function<sp2::InputAdapter *( sp2::AdapterManager * manager, PyEngine * pyengine,
                                                       PyObject *, PushMode pushMode, PyObject * args )>;

    static PyObject * createAdapter( Creator creator, PyObject * args );
    static PyObject * create( InputAdapter * adapter );

    static PyTypeObject PyType;

private:
    InputAdapter * m_adapter;
};

#define REGISTER_INPUT_ADAPTER( METHOD_NAME, CREATOR_FUNC ) \
    static PyObject * create_##METHOD_NAME( PyObject *, PyObject * args ) { return PyInputAdapterWrapper::createAdapter( CREATOR_FUNC, args ); } \
    REGISTER_MODULE_METHOD( #METHOD_NAME, create_##METHOD_NAME, METH_VARARGS, #METHOD_NAME );

}

#endif
