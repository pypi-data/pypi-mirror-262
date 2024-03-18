#ifndef _IN_SP2_ADAPTERS_KAFKA_KAFKASUBSCRIBER_H
#define _IN_SP2_ADAPTERS_KAFKA_KAFKASUBSCRIBER_H

#include <sp2/adapters/kafka/KafkaAdapterManager.h>
#include <sp2/adapters/kafka/KafkaInputAdapter.h>
#include <sp2/engine/PushInputAdapter.h>

#include <librdkafka/rdkafkacpp.h>

namespace sp2::adapters::kafka
{

class KafkaSubscriber
{
public:
    KafkaSubscriber( KafkaAdapterManager * mgr, const Dictionary & properties );
    ~KafkaSubscriber();

    PushInputAdapter * getInputAdapter( Sp2TypePtr & type, PushMode pushMode, const Dictionary & properties );

    void onMessage( RdKafka::Message* message, bool live );
    void flagReplayComplete();

private:
    using Adapters = std::vector<KafkaInputAdapter *>;
    Adapters              m_adapters;

    KafkaAdapterManager & m_adapterMgr;
    Engine *              m_engine;
    PushGroup             m_pushGroup;
};




}

#endif
