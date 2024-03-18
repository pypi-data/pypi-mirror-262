set(KAFKA_HEADER_FILES
        KafkaAdapterManager.h
        KafkaConsumer.h
        KafkaInputAdapter.h
        KafkaOutputAdapter.h
        KafkaPublisher.h
        KafkaSubscriber.h
)

set(KAFKA_SOURCE_FILES
        KafkaAdapterManager.cpp
        KafkaConsumer.cpp
        KafkaInputAdapter.cpp
        KafkaOutputAdapter.cpp
        KafkaPublisher.cpp
        KafkaSubscriber.cpp
        ${KAFKA_HEADER_FILES}
)

add_library(sp2_kafka_adapter STATIC ${KAFKA_SOURCE_FILES})
set_target_properties(sp2_kafka_adapter PROPERTIES PUBLIC_HEADER "${KAFKA_HEADER_FILES}")

if(SP2_LINK_SASL)
set(SASL_LIBRARY sasl2)
endif()

target_link_libraries(sp2_kafka_adapter PRIVATE sp2_adapter_utils RdKafka::rdkafka RdKafka::rdkafka++ OpenSSL::SSL OpenSSL::Crypto lz4::lz4 ${SASL_LIBRARY})

install(TARGETS sp2_kafka_adapter
        PUBLIC_HEADER DESTINATION include/sp2/adapters/kafka
        RUNTIME DESTINATION bin/
        LIBRARY DESTINATION lib/
       )
