#include <sp2/engine/Node.h>
#include <Python.h>

namespace sp2::python
{

//simple wrapper for python level access when wiring
class PyNodeWrapper : public PyObject
{
public:
    sp2::Node * node() { return m_node; }

    static PyNodeWrapper * create( sp2::Node * node );
    static PyTypeObject PyType;

private:

    PyNodeWrapper( sp2::Node * node ) : m_node( node ) {}
    sp2::Node * m_node;
};

}
