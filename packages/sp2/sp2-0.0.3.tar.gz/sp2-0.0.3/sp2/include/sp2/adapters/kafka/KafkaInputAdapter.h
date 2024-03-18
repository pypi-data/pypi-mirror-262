#ifndef _IN_SP2_ADAPTERS_KAFKA_KAFKAINPUTADAPTER_H
#define _IN_SP2_ADAPTERS_KAFKA_KAFKAINPUTADAPTER_H

#include <sp2/adapters/utils/MessageStructConverter.h>
#include <sp2/engine/PushPullInputAdapter.h>
#include <sp2/engine/Struct.h>
#include <librdkafka/rdkafkacpp.h>

namespace sp2::adapters::kafka
{

class KafkaInputAdapter final: public PushPullInputAdapter
{
public:
    KafkaInputAdapter( Engine * engine, Sp2TypePtr & type,
                       PushMode pushMode, PushGroup * group,
                       const Dictionary & properties );

    void processMessage( RdKafka::Message* message, bool live, sp2::PushBatch* batch );

private:
    utils::MessageStructConverterPtr m_converter;
    StructFieldPtr m_partitionField;
    StructFieldPtr m_offsetField;
    StructFieldPtr m_liveField;
    StructFieldPtr m_timestampField;
    StructFieldPtr m_keyField;
};

}

#endif
