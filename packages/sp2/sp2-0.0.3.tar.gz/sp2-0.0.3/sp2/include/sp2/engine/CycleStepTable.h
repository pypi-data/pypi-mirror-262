#ifndef _IN_SP2_ENGINE_CYCLESTEPTABLE_H
#define _IN_SP2_ENGINE_CYCLESTEPTABLE_H

#include <sp2/core/DynamicBitSet.h>
#include <stdint.h>
#include <vector>

namespace sp2
{

class Consumer;
class Profiler;

class CycleStepTable
{
public:
    CycleStepTable();
    ~CycleStepTable();

    void resize( int32_t maxRank );

    void schedule( Consumer *consumer );
    //execute a single engine cycle
    void executeCycle( sp2::Profiler * profiler, bool isDynamic = false );

private:

    struct TableEntry
    {
        Consumer * head;
        Consumer * tail;
    };

    using Table = std::vector<TableEntry>;

    int32_t         m_maxRank;
    Table           m_table;
    DynamicBitSet<> m_rankBitset;
};

};
#endif
