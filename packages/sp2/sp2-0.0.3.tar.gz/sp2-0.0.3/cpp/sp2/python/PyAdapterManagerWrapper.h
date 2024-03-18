#ifndef _IN_SP2_PYTHON_PYADAPTERMANAGERWRAPPER_H
#define _IN_SP2_PYTHON_PYADAPTERMANAGERWRAPPER_H

#include <Python.h>
#include <sp2/python/Exception.h>
#include <sp2/python/InitHelper.h>

namespace sp2 { class AdapterManager; }

namespace sp2::python
{

class PyEngine;

class PyAdapterManagerWrapper
{
public:
    using Creator = std::function<sp2::AdapterManager *( PyEngine * pyengine, const Dictionary & properties )>;

    static PyObject * create( Creator creator, PyObject * args );
    static sp2::AdapterManager * extractAdapterManager( PyObject * wrapper );
};

#define REGISTER_ADAPTER_MANAGER( METHOD_NAME, CREATOR_FUNC ) \
    static PyObject * create_##METHOD_NAME( PyObject *, PyObject * args ) { return sp2::python::PyAdapterManagerWrapper::create( CREATOR_FUNC, args ); } \
    REGISTER_MODULE_METHOD( #METHOD_NAME, create_##METHOD_NAME, METH_VARARGS, #METHOD_NAME );

#define REGISTER_ADAPTER_MANAGER_CUSTOM_CREATOR( METHOD_NAME, CREATOR_FUNC ) \
    static PyObject * create_##METHOD_NAME( PyObject *, PyObject * args ) { return CREATOR_FUNC( args ); } \
    REGISTER_MODULE_METHOD( #METHOD_NAME, create_##METHOD_NAME, METH_VARARGS, #METHOD_NAME );

}

#endif
