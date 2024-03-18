#ifndef _IN_SP2_PYTHON_PYENGINE_H
#define _IN_SP2_PYTHON_PYENGINE_H

#include <sp2/core/Time.h>
#include <sp2/engine/RootEngine.h>
#include <sp2/python/PyObjectPtr.h>
#include <Python.h>
#include <memory>

namespace sp2 { class GraphOutputAdapter; }

namespace sp2::python
{

class PyEngine;

//This is the actual python root engine
class PythonEngine final : public sp2::RootEngine
{
public:
    PythonEngine( PyEngine * parent, const Dictionary & );

    void dialectUnlockGIL() noexcept override;
    void dialectLockGIL() noexcept override;

    PyEngine * parent() { return m_parent; }
    bool outputNumpy() { return m_outputNumpy; }
private:
    PyEngine      * m_parent;
    PyThreadState * m_pyThreadState;
    bool m_outputNumpy;
};

//This is the root engine wrapper object
class PyEngine final: public PyObject
{
public:
    PyEngine( const Dictionary & settings );
    //for dynamic engines
    PyEngine( Engine * engine );
    ~PyEngine();

    Engine * engine()           { return m_engine; }
    PythonEngine * rootEngine() { return static_cast<PythonEngine *>( engine() -> rootEngine() ); }

    PyObject * collectOutputs();

    static PyEngine * create( Engine * engine );

    static PyTypeObject PyType;

private:
    bool        m_ownEngine;
    Engine    * m_engine;
};

};

#endif
