#ifndef _IN_SP2_ADAPTERS_KAFKA_KAFKAADAPTERMANAGER_H
#define _IN_SP2_ADAPTERS_KAFKA_KAFKAADAPTERMANAGER_H

#include <sp2/core/Enum.h>
#include <sp2/core/Hash.h>
#include <sp2/engine/AdapterManager.h>
#include <sp2/engine/Dictionary.h>
#include <sp2/engine/PushInputAdapter.h>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>

namespace RdKafka
{

class Conf;
class DeliveryReportCb;
class EventCb;
class Producer;
}

namespace sp2::adapters::kafka
{

class KafkaConsumer;
class KafkaPublisher;
class KafkaSubscriber;

struct KafkaStatusMessageTypeTraits
{
    enum _enum : unsigned char
    {
        OK = 0,
        MSG_DELIVERY_FAILED = 1,
        MSG_SEND_ERROR = 2,
        MSG_RECV_ERROR = 3,
        GENERIC_ERROR = 4,

        NUM_TYPES
    };

protected:
    _enum m_value;
};

using KafkaStatusMessageType = sp2::Enum<KafkaStatusMessageTypeTraits>;

//Top level AdapterManager object for all kafka adapters in the engine
class KafkaAdapterManager final : public sp2::AdapterManager
{
public:
    KafkaAdapterManager( sp2::Engine * engine, const Dictionary & properties );
    ~KafkaAdapterManager();

    const char * name() const override { return "KafkaAdapterManager"; }

    void start( DateTime starttime, DateTime endtime ) override;

    void stop() override;

    DateTime processNextSimTimeSlice( DateTime time ) override;

    //properties will have topic and fieldmap information, amongst other things
    PushInputAdapter * getInputAdapter( Sp2TypePtr & type, PushMode pushMode, const Dictionary & properties );
    OutputAdapter * getOutputAdapter( Sp2TypePtr & type, const Dictionary & properties );

    KafkaConsumer * getConsumer( const std::string & topic, const Dictionary & properties );

    RdKafka::Conf * getConsumerConf() { return m_consumerConf.get(); }

    const Dictionary::Value & startOffsetProperty() const { return m_startOffsetProperty; }

    int pollTimeoutMs() const { return m_pollTimeoutMs; }

    void forceShutdown( const std::string & err );

private:

    using TopicKeyPair = std::pair<std::string, std::string>;

    void setConfProperties( RdKafka::Conf * conf, const Dictionary & properties );
    void pollProducers();
    void forceConsumerReplayComplete();

    KafkaSubscriber * getSubscriber( const std::string & topic, const std::string & key, const Dictionary & properties );
    KafkaPublisher * getStaticPublisher( const TopicKeyPair & pair, const Dictionary & properties );
    KafkaPublisher * getDynamicPublisher( const std::string & topic, const Dictionary & properties );

    using ConsumerVector = std::vector<std::shared_ptr<KafkaConsumer>>;
    ConsumerVector                             m_consumerVector;
    using ConsumerMap = std::unordered_map<std::string, std::shared_ptr<KafkaConsumer>>;
    ConsumerMap                                m_consumerMap;

    using StaticPublishers = std::unordered_map<TopicKeyPair, std::unique_ptr<KafkaPublisher>, hash::hash_pair>;
    StaticPublishers                           m_staticPublishers;

    using DynamicPublishers = std::vector<std::unique_ptr<KafkaPublisher>>;
    DynamicPublishers                          m_dynamicPublishers;

    using Subscribers = std::unordered_map<TopicKeyPair, std::unique_ptr<KafkaSubscriber>, hash::hash_pair>;
    Subscribers                                m_subscribers;

    int                                        m_pollTimeoutMs;
    size_t                                     m_maxThreads;
    size_t                                     m_consumerIdx;

    std::unique_ptr<RdKafka::EventCb>          m_eventCb;
    std::shared_ptr<RdKafka::Producer>         m_producer;
    std::unique_ptr<RdKafka::DeliveryReportCb> m_producerCb;
    std::unique_ptr<std::thread>               m_producerPollThread;
    volatile bool                              m_producerPollThreadActive;

    std::unique_ptr<RdKafka::Conf>             m_consumerConf;
    std::unique_ptr<RdKafka::Conf>             m_producerConf;
    Dictionary::Value                          m_startOffsetProperty;
};

}

#endif
