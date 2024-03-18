#ifndef _IN_SP2_PYTHON_SP2TYPEFACTORY_H
#define _IN_SP2_PYTHON_SP2TYPEFACTORY_H

#include <sp2/engine/Sp2Type.h>
#include <unordered_map>
#include <Python.h>

namespace sp2::python
{

class Sp2TypeFactory
{
public:
    static Sp2TypeFactory & instance();

    Sp2TypePtr & typeFromPyType( PyObject * );
    void removeCachedType( PyTypeObject * );

private:
    using Cache = std::unordered_map<PyTypeObject *, Sp2TypePtr>;
    Cache m_cache;
};

}

#endif
