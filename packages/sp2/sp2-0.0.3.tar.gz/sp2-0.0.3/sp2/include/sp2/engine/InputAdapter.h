#ifndef _IN_SP2_ENGINE_INPUTADAPTER_H
#define _IN_SP2_ENGINE_INPUTADAPTER_H

#include <sp2/core/Time.h>
#include <sp2/engine/Enums.h>
#include <sp2/engine/RootEngine.h>
#include <sp2/engine/TimeSeriesProvider.h>

namespace sp2
{

class Consumer;

class InputAdapter : public TimeSeriesProvider, public EngineOwned
{
public:
    InputAdapter( Engine * engine, const Sp2TypePtr & type, PushMode pushMode );
    virtual ~InputAdapter() {}

    using TimeSeriesProvider::outputTickTyped;

    virtual void start( DateTime start, DateTime end ) {}
    virtual void stop() {}

    template< typename T > void outputTickTyped( DateTime timestamp, const T & value )
    {
        outputTickTyped( rootEngine() -> cycleCount(), timestamp, value );
    }

    //used by sim and realtime input adapters
    template<typename T>
    bool consumeTick( const T & value );

    RootEngine * rootEngine() { return m_rootEngine; }

    PushMode pushMode() const { return m_pushMode; }

    //if adapter is BURST this will return the type of the data, rather than the BURST vector<Data>
    const Sp2Type * dataType() const
    {
        if( m_pushMode == PushMode::BURST )
            return static_cast<const Sp2ArrayType *>( type() ) -> elemType().get();
        return type();
    }

protected:
    RootEngine * m_rootEngine;
    PushMode     m_pushMode;
};

template<typename T>
bool InputAdapter::consumeTick( const T & value )
{
    switch( pushMode() )
    {
        case PushMode::LAST_VALUE:
        {
            if( unlikely( rootEngine() -> cycleCount() == lastCycleCount() ) )
                m_timeseries -> lastValueTyped<T>() = value;
            else
                this -> outputTickTyped<T>( rootEngine() -> now(), value );
            return true;
        }

        case PushMode::BURST:
        {
            SP2_ASSERT( type() -> type() == Sp2Type::Type::ARRAY );
            SP2_ASSERT( static_cast<const Sp2ArrayType * >( type() ) -> elemType() -> type() == Sp2Type::Type::fromCType<T>::type );

            using ArrayT = typename Sp2Type::Type::toCType<Sp2Type::Type::ARRAY,T>::type;
            if( likely( rootEngine() -> cycleCount() != lastCycleCount() ) )
            {
                //ensure we reuse vector memory in our buffer by using reserve api and
                //clearing existing value if any
                reserveTickTyped<ArrayT>( rootEngine() -> cycleCount(), rootEngine() -> now() ).clear();
            }

            m_timeseries -> lastValueTyped<ArrayT>().push_back( value );
            return true;
        }

        case PushMode::NON_COLLAPSING:
        {
            if( unlikely( rootEngine() -> cycleCount() == lastCycleCount() ) )
                return false;

            this -> outputTickTyped<T>( rootEngine() -> now(), value );
            return true;
        }

        default:
            SP2_THROW( NotImplemented, pushMode() << " mode is not yet supported" );
            break;
    }

    return true;
}

};

#endif
