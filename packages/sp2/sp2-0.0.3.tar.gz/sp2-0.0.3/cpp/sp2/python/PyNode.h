#ifndef _IN_SP2_PYTHON_PYNODE_H
#define _IN_SP2_PYTHON_PYNODE_H

#include <sp2/core/Time.h>
#include <sp2/engine/Node.h>
#include <sp2/python/PyObjectPtr.h>
#include <Python.h>

namespace sp2::python
{

class PyEngine;

class PyNode final: public sp2::Node
{
public:
    PyNode( sp2::Engine * engine, PyObjectPtr gen, PyObjectPtr inputs, PyObjectPtr outputs,
            NodeDef def );
    ~PyNode();

    void executeImpl() override;
    void start() override;
    void stop() override;
    bool makeActive( InputId id ) override;
    bool makePassive( InputId id ) override;

    //see .cpp for reason why this is overloaded
    void createAlarm( Sp2TypePtr & type, size_t id ) override;

    const char * name() const override;

    static PyNode * create( PyEngine * engine, PyObject * inputs, PyObject * outputs, PyObject * gen );

private:
    void init( PyObjectPtr inputs, PyObjectPtr outputs );
    void call_gen();

    PyObjectPtr  m_gen;
    PyObject *** m_localVars; //array of PyObject ** objects

    //array that contains the count of each passive input when we last converted it to Python
    //the indexing corresponds to the input index as seen by the node
    uint32_t *   m_passiveCounts;
};

};

#endif
