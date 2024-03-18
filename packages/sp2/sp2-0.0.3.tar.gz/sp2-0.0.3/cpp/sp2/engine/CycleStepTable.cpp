#include <sp2/core/Exception.h>
#include <sp2/engine/Consumer.h>
#include <sp2/engine/CycleStepTable.h>
#include <sp2/engine/Profiler.h>
#include <string.h>

namespace sp2
{

static Consumer *s_END_MARKER = reinterpret_cast<Consumer*>( 0x1 );

CycleStepTable::CycleStepTable() : m_maxRank( -1 ), m_rankBitset()
{
}

CycleStepTable::~CycleStepTable()
{
}

void CycleStepTable::resize( int32_t maxRank )
{
    if( maxRank > m_maxRank )
    {
        m_maxRank = maxRank;
        m_table.resize( m_maxRank + 1, { nullptr, nullptr } );
        m_rankBitset.resize( m_maxRank + 1 );
    }
}

void CycleStepTable::schedule( Consumer * node )
{
    //already scheduled
    if( node -> next() != nullptr )
        return;

    int32_t rank = node -> rank();
    auto & entry = m_table[ rank ];

    if( !entry.head )
    {
        m_rankBitset.set( rank );
        entry.head = entry.tail = node;
    }
    else
    {
        entry.tail -> setNext( node );
        entry.tail = node;
    }

    node -> setNext( s_END_MARKER );
}

void CycleStepTable::executeCycle( sp2::Profiler * profiler, bool isDynamic )
{
    if( unlikely( profiler && !isDynamic ) ) // prioritize case without profiler
        profiler -> startCycle();

    auto curRank = m_rankBitset.find_first();
    while( curRank != DynamicBitSet<>::npos )
    {
        m_rankBitset.reset( curRank );
        auto * curConsumer = m_table[ curRank ].head;
        // no real need to set tail to nullptr
        m_table[ curRank ].head = nullptr;

        SP2_ASSERT( curConsumer != s_END_MARKER );

        while( curConsumer != s_END_MARKER )
        {
            if( unlikely( ( bool )profiler ) )
            {
                profiler -> startNode();
                curConsumer -> execute();
                profiler -> finishNode( curConsumer -> name() );
            }
            else
                curConsumer -> execute();

            Consumer * prevConsumer = curConsumer;
            curConsumer = curConsumer -> next();
            prevConsumer -> setNext( nullptr );
        }
        curRank = m_rankBitset.find_next( curRank );
    }

    if( unlikely( profiler && !isDynamic ) )
        profiler -> finishCycle();
}

}
