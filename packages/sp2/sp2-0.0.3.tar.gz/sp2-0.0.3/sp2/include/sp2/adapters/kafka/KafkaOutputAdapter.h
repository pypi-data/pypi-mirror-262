#ifndef _IN_SP2_ADAPTERS_KAFKA_KAFKAOUTPUTADAPTER_H
#define _IN_SP2_ADAPTERS_KAFKA_KAFKAOUTPUTADAPTER_H

#include <sp2/adapters/utils/MessageWriter.h>
#include <sp2/engine/Dictionary.h>
#include <sp2/engine/OutputAdapter.h>
#include <string>

namespace sp2::adapters::kafka
{

class KafkaPublisher;

class KafkaOutputAdapter final: public OutputAdapter
{
public:
    KafkaOutputAdapter( Engine * engine, KafkaPublisher & publisher, Sp2TypePtr & type, const Dictionary & properties, const std::string & key );
    KafkaOutputAdapter( Engine * engine, KafkaPublisher & publisher, Sp2TypePtr & type, const Dictionary & properties, const std::vector<std::string> & keyFields );
    ~KafkaOutputAdapter();

    void executeImpl() override;

    const char * name() const override { return "KafkaOutputAdapter"; }

private:
    KafkaOutputAdapter( Engine * engine, KafkaPublisher & publisher, Sp2TypePtr & type, const Dictionary & properties );
    void addFields( const std::vector<std::string> & keyFields, Sp2TypePtr & type, size_t i = 0 );
    const std::string & getKey( const Struct * struct_ );

    KafkaPublisher &            m_publisher;
    utils::OutputDataMapperPtr  m_dataMapper;
    std::vector<StructFieldPtr> m_structFields;
};

}

#endif
