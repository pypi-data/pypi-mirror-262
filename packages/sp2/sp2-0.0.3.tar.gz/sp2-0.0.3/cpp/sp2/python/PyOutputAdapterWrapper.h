#ifndef _IN_SP2_PYTHON_PYOUTPUTADAPTERWRAPPER_H
#define _IN_SP2_PYTHON_PYOUTPUTADAPTERWRAPPER_H

#include <sp2/python/Conversions.h>
#include <sp2/python/Exception.h>
#include <sp2/python/InitHelper.h>

namespace sp2 { class OutputAdapter; }

namespace sp2::python
{

class PyEngine;

class PyOutputAdapterWrapper final: public PyObject
{
public:
    PyOutputAdapterWrapper( OutputAdapter * adapter ) : m_adapter( adapter )
    {}

    OutputAdapter * adapter() { return m_adapter; }

    using Creator = std::function<sp2::OutputAdapter *( sp2::AdapterManager * manager, PyEngine * pyengine, PyObject * args )>;

    static PyObject * createAdapter( Creator creator, PyObject * args );
    static PyTypeObject PyType;

private:
    OutputAdapter * m_adapter;
};

#define REGISTER_OUTPUT_ADAPTER( METHOD_NAME, CREATOR_FUNC ) \
    static PyObject * create_##METHOD_NAME( PyObject *, PyObject * args ) { return PyOutputAdapterWrapper::createAdapter( CREATOR_FUNC, args ); } \
    REGISTER_MODULE_METHOD( #METHOD_NAME, create_##METHOD_NAME, METH_VARARGS, #METHOD_NAME );

}

#endif
