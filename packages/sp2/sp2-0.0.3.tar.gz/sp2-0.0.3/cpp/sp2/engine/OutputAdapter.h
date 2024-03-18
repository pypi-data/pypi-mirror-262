#ifndef _IN_SP2_ENGINE_OUTPUTADAPTER_H
#define _IN_SP2_ENGINE_OUTPUTADAPTER_H

#include <sp2/engine/Consumer.h>
#include <sp2/engine/Engine.h>

namespace sp2
{

class TimeSeriesProvider;

class OutputAdapter : public Consumer, public EngineOwned
{
public:
    OutputAdapter( sp2::Engine * engine );
    ~OutputAdapter();

    TimeSeriesProvider * input() const { return m_input; }

    void link( TimeSeriesProvider * input );

    input_iterator inputs() const override { return input_iterator( &m_input ); }

private:
    //not owned
    TimeSeriesProvider * m_input;

};

}

#endif
