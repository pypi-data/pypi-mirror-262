#include <sp2/adapters/kafka/KafkaInputAdapter.h>

#include <iostream>

namespace sp2::adapters::kafka
{

KafkaInputAdapter::KafkaInputAdapter( Engine *engine, Sp2TypePtr &type,
                                      PushMode pushMode, PushGroup *group,
                                      const Dictionary &properties)
    : PushPullInputAdapter( engine, type, pushMode, group,
                            properties.get<bool>( "adjust_out_of_order_time") )
{
    if( type -> type() != Sp2Type::Type::STRUCT &&
        type -> type() != Sp2Type::Type::STRING )
        SP2_THROW( RuntimeException, "Unsupported type: " << type -> type() );


    if( properties.exists( "meta_field_map" ) )
    {
        const Sp2StructType & structType = static_cast<const Sp2StructType &>( *type );
        const Dictionary & metaFieldMap = *properties.get<DictionaryPtr>( "meta_field_map" );

        if( !metaFieldMap.empty() && type -> type() != Sp2Type::Type::STRUCT )
            SP2_THROW( ValueError, "meta_field_map is not supported on non-struct types" );

        if( metaFieldMap.exists( "partition" ) )
        {
            std::string partitionFieldName = metaFieldMap.get<std::string>( "partition" );
            m_partitionField = structType.meta() -> field( partitionFieldName );
            if( !m_partitionField )
                SP2_THROW( ValueError, "field " << partitionFieldName << " is not a valid field on struct type " << structType.meta() -> name() );
            if( m_partitionField -> type() -> type() != Sp2Type::Type::INT64 )
                SP2_THROW( ValueError, "field " << partitionFieldName << " must be of type int on struct type " << structType.meta() -> name() );
        }
        if( metaFieldMap.exists( "offset" ) )
        {
            std::string offsetFieldName = metaFieldMap.get<std::string>( "offset" );
            m_offsetField = structType.meta() -> field( offsetFieldName );
            if( !m_offsetField )
                SP2_THROW( ValueError, "field " << offsetFieldName << " is not a valid field on struct type " << structType.meta() -> name() );
            if( m_offsetField -> type() -> type() != Sp2Type::Type::INT64 )
                SP2_THROW( ValueError, "field " << offsetFieldName << " must be of type int on struct type " << structType.meta() -> name() );
        }
        if( metaFieldMap.exists( "live" ) )
        {
            std::string liveFieldName = metaFieldMap.get<std::string>( "live" );
            m_liveField = structType.meta() -> field( liveFieldName );
            if( !m_liveField )
                SP2_THROW( ValueError, "field " << liveFieldName << " is not a valid field on struct type " << structType.meta() -> name() );
            if( m_liveField -> type() -> type() != Sp2Type::Type::BOOL )
                SP2_THROW( ValueError, "field " << liveFieldName << " must be of type bool on struct type " << structType.meta() -> name() );
        }
        if( metaFieldMap.exists( "timestamp" ) )
        {
            std::string timestampFieldName = metaFieldMap.get<std::string>( "timestamp" );
            m_timestampField = structType.meta() -> field( timestampFieldName );
            if( !m_timestampField )
                SP2_THROW( ValueError, "field " << timestampFieldName << " is not a valid field on struct type " << structType.meta() -> name() );
            if( m_timestampField -> type() -> type() != Sp2Type::Type::DATETIME )
                SP2_THROW( ValueError, "field " << timestampFieldName << " must be of type datetime on struct type " << structType.meta() -> name() );
        }
        if( metaFieldMap.exists( "key" ) )
        {
            std::string keyFieldName = metaFieldMap.get<std::string>( "key" );
            m_keyField = structType.meta() -> field( keyFieldName );
            if( !m_keyField )
                SP2_THROW( ValueError, "field " << keyFieldName << " is not a valid field on struct type " << structType.meta() -> name() );
            if( m_keyField -> type() -> type() != Sp2Type::Type::STRING )
                SP2_THROW( ValueError, "field " << keyFieldName << " must be of type string on struct type " << structType.meta() -> name() );
        }
    }

    m_converter = utils::MessageStructConverterCache::instance().create( type, properties );
}

void KafkaInputAdapter::processMessage( RdKafka::Message* message, bool live, sp2::PushBatch* batch )
{
    bool pushLive = live || flaggedLive();
    DateTime msgTime;
    auto ts = message -> timestamp();
    if( ts.type != RdKafka::MessageTimestamp::MSG_TIMESTAMP_NOT_AVAILABLE )
    {
        msgTime = DateTime::fromMilliseconds( ts.timestamp );

        //If user requested kafka data earlier than engine start, we will force it as live so it makes it into the engine
        if( msgTime < rootEngine() -> startTime() )
            pushLive = true;
    }
    else
    {
        //if we cant extract time from the msg we cant push sim, so make force it live/realtime
        pushLive = true;
    }

    if( type() -> type() == Sp2Type::Type::STRUCT )
    {
        auto tick = m_converter -> asStruct( message -> payload(), message -> len() );

        if( m_partitionField )
            m_partitionField -> setValue( tick.get(), message -> partition() );

        if( m_offsetField )
            m_offsetField -> setValue( tick.get(), message -> offset() );

        if( m_liveField )
            m_liveField -> setValue( tick.get(), live );

        if( m_timestampField && !msgTime.isNone() )
            m_timestampField -> setValue( tick.get(), msgTime );

        if( m_keyField )
            m_keyField -> setValue( tick.get(), *message -> key() );

        pushTick( pushLive, msgTime, std::move( tick ), batch );
    }
    else if( type() -> type() == Sp2Type::Type::STRING )
    {
        pushTick( pushLive, msgTime, std::string( ( const char * ) message -> payload(), message -> len() ) );
    }
}

}
