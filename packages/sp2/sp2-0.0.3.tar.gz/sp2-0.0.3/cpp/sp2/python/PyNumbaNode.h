#ifndef _IN_PYTHON_PYNUMBANODE_H
#define _IN_PYTHON_PYNUMBANODE_H

#include <sp2/core/Time.h>
#include <sp2/engine/Node.h>
#include <sp2/python/PyObjectPtr.h>
#include <Python.h>

namespace sp2::python
{
class PyEngine;

typedef void (*CallbackType)(void *node, void *state);

class PyNumbaNode final : public sp2::Node
{
public:
    // TODO: Add suppot for initialization callback as well
    PyNumbaNode(sp2::Engine *engine,
                void *stateObject, CallbackType numbaInitCallback, CallbackType numbaImplCallback, PyObjectPtr inputs,
                PyObjectPtr outputs,
                NodeDef def, PyObject *dataReference);

    ~PyNumbaNode();

    void executeImpl() override;

    void start() override;

    void stop() override;

    const char *name() const override;

    static PyNumbaNode *create(PyEngine *engine, PyObject *inputs, PyObject *outputs,
                               PyObject *stateObject, PyObject *numbaInitCallback, PyObject *numbaImplCallback,
                               PyObject *dataReference);

private:
    void init(PyObjectPtr inputs, PyObjectPtr outputs);

    void call_callback();

    void *m_stateObject;
    CallbackType m_numbaInitCallback;
    CallbackType m_numbaImplCallback;
    PyObjectPtr m_dataReference;
};
};

#endif
