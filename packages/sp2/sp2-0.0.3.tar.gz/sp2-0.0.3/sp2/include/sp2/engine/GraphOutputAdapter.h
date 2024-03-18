#ifndef _IN_SP2_ENGINE_GRAPHOUTPUTADAPTER_H
#define _IN_SP2_ENGINE_GRAPHOUTPUTADAPTER_H

#include <sp2/engine/OutputAdapter.h>
#include <memory>

namespace sp2
{

//GraphOutputAdapter - latches onto a ts for use at the end of sp2.run calls to convert the buffered data into dialect readable form
//Note some nuances with GraphOutputAdapter as it pertains to dynamic graphs.  sp2.add_graph_output calls in dynamic graphs have an interesting problem in
//that the timeseries they latch onto can be destroyed before the end of the engine run.  For this reason, processResults() can be called before
//the end of a sp2.run call to pre-process the data before the time series input is released.
//GraphOutputAdapters are also special in that they are registered in both a dynamic engine and the root engine as sahred_ptr.  They make it into root
//so that the root processes them at the end of the sp2.run call ( dynamics could be shutdown by then ).  We also register in root
//to ensure we dont hit key clashses.
class GraphOutputAdapter : public OutputAdapter, public std::enable_shared_from_this<GraphOutputAdapter>
{
public:
    GraphOutputAdapter( sp2::Engine * engine, int32_t tickCount, TimeDelta tickHistory );
    ~GraphOutputAdapter();

    const char * name() const override;

    void start() override;
    void stop() override;
    void executeImpl() override {}

    int32_t tickCount() const     { return m_tickCount; }
    TimeDelta tickHistory() const { return m_tickHistory; }

private:
    virtual void processResults() = 0;

    TimeDelta m_tickHistory;
    int32_t   m_tickCount;
};

}

#endif
