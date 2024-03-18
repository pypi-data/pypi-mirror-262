#include <sp2/engine/AdapterManager.h>
#include <sp2/engine/PartialSwitchSp2Type.h>

namespace sp2
{

ManagedSimInputAdapter::ManagedSimInputAdapter( sp2::Engine * engine,
                                                const Sp2TypePtr & type,
                                                AdapterManager *manager,
                                                PushMode pushMode ) : InputAdapter( engine, type, pushMode ),
                                                                      m_manager( manager ),
                                                                      m_lastCycleCount( 0 )
{
}

AdapterManager::AdapterManager( sp2::Engine * engine ) : m_engine( engine ), m_statusAdapter( nullptr )
{
    if( !m_engine -> isRootEngine() )
        SP2_THROW( NotImplemented, "AdapterManager support is not currently available in dynamic graphs" );
}

AdapterManager::~AdapterManager()
{
}

void AdapterManager::start( DateTime starttime, DateTime endtime )
{
    m_starttime = starttime;
    m_endtime   = endtime;

    scheduleTimerCB( starttime );
}

void AdapterManager::stop()
{
}

void AdapterManager::processSimTimerCB()
{
    DateTime next = processNextSimTimeSlice( rootEngine() -> now() );
    if( !next.isNone() )
        scheduleTimerCB( next );
}

StatusAdapter * AdapterManager::createStatusAdapter( Sp2TypePtr & type, PushMode pushMode )
{
    if( !m_statusAdapter )
        m_statusAdapter = m_engine -> createOwnedObject<StatusAdapter>( type, pushMode, statusPushGroup() );

    return m_statusAdapter;
}

void AdapterManager::pushStatus( int64_t level, int64_t errCode, const std::string & errMsg, PushBatch *batch ) const
{
    if( m_statusAdapter )
        m_statusAdapter -> pushStatus( level, errCode, errMsg, batch );
}

}
