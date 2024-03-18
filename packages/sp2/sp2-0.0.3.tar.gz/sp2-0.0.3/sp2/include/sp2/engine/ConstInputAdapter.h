#ifndef _IN_SP2_ENGINE_CONSTINPUTADAPTER_H
#define _IN_SP2_ENGINE_CONSTINPUTADAPTER_H

#include <sp2/engine/InputAdapter.h>

namespace sp2
{

template<typename T>
class ConstInputAdapter final : public InputAdapter
{
public:
    ConstInputAdapter( Engine * engine, Sp2TypePtr & type, const T & value,
                       TimeDelta delay ) : InputAdapter( engine, type, PushMode::LAST_VALUE ), m_delay( delay ), m_value( value )
    {
    }

    void start( DateTime start, DateTime end ) override
    {
        m_timerHandle = rootEngine() -> scheduleCallback( m_delay,
                                                          [this]
                                                          {
                                                              this -> outputTickTyped<T>( rootEngine() -> now(), m_value );
                                                              return nullptr;
                                                          } );
    }

    void stop() override
    {
        rootEngine() -> cancelCallback( m_timerHandle );
    }

private:
    Scheduler::Handle m_timerHandle;
    TimeDelta m_delay;
    T         m_value;
};

};

#endif
