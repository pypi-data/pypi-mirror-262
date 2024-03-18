#include <sp2/engine/OutputAdapter.h>
#include <sp2/engine/TimeSeriesProvider.h>

namespace sp2
{

OutputAdapter::OutputAdapter( sp2::Engine * engine ) : Consumer( engine ),
                                                       m_input( nullptr )
{
}

OutputAdapter::~OutputAdapter()
{
}

void OutputAdapter::link( TimeSeriesProvider * input )
{
    if( m_input )
        SP2_THROW( ValueError, "Attempted to link input to output adapter " << name() << " multiple times" );
    m_input = input;
    input -> addConsumer( this, InputId( 0 ) );
}

}
