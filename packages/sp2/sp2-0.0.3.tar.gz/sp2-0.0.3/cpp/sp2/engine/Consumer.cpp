#include <sp2/engine/Consumer.h>
#include <sp2/engine/Engine.h>
#include <sp2/engine/InputAdapter.h>

namespace sp2
{

Consumer::Consumer( Engine * engine ) : m_engine( engine ),
                                        m_next( nullptr ),
                                        m_rank( -1 )
{
}

Consumer::~Consumer()
{
}

void Consumer::start()
{
}

void Consumer::stop()
{
}

}
