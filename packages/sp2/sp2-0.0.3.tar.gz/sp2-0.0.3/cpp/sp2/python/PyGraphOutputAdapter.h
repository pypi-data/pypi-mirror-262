#ifndef _IN_SP2_PYTHON_PYGRAPHOUPUTADAPTER_H
#define _IN_SP2_PYTHON_PYGRAPHOUPUTADAPTER_H

#include <sp2/engine/GraphOutputAdapter.h>
#include <sp2/python/PyObjectPtr.h>

namespace sp2::python
{

class PyGraphOutputAdapter : public GraphOutputAdapter
{
public:
    using GraphOutputAdapter::GraphOutputAdapter;

    PyObjectPtr result();

private:
    void processResults() override;

    PyObjectPtr m_result;
};

}

#endif
