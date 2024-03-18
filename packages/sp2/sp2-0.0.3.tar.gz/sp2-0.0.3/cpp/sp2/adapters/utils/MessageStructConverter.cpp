#include <sp2/adapters/utils/MessageStructConverter.h>
#include <sp2/adapters/utils/JSONMessageStructConverter.h>
#include <sp2/adapters/utils/ProtobufMessageStructConverter.h>
#include <sp2/adapters/utils/RawBytesMessageStructConverter.h>

namespace sp2::adapters::utils
{

MessageStructConverter::MessageStructConverter( const Sp2TypePtr & type, const Dictionary & properties ) : m_type( type )
{
    if( type -> type() == Sp2Type::Type::STRUCT )
        m_structMeta = std::static_pointer_cast<const Sp2StructType>( type ) -> meta();
}

MessageStructConverterCache::MessageStructConverterCache()
{
    registerConverter( MsgProtocol::RAW_BYTES, &RawBytesMessageStructConverter::create );
    registerConverter( MsgProtocol::JSON,      &JSONMessageStructConverter::create );
    registerConverter( MsgProtocol::PROTOBUF,  &ProtobufMessageStructConverter::create );
}

bool MessageStructConverterCache::registerConverter( MsgProtocol protocol, Creator creator )
{
    if( m_creators[ protocol ] )
        SP2_THROW( RuntimeException, "Attempted to register creator for MessageStructConverter type " << protocol << " more than once" );

    m_creators[ protocol ] = creator;
    return true;
}

MessageStructConverterCache & MessageStructConverterCache::instance()
{
    static MessageStructConverterCache s_instance;
    return s_instance;
}

MessageStructConverterPtr MessageStructConverterCache::create( const Sp2TypePtr & type, const Dictionary & properties )
{
    std::lock_guard<std::mutex> guard( m_cacheMutex );

    auto rv = m_cache.emplace( CacheKey{ type.get(), properties }, nullptr );
    if( !rv.second )
        return rv.first -> second;

    auto protocol = MsgProtocol( properties.get<std::string>( "protocol" ) );
    auto creator = m_creators[ protocol ];
    if( !creator )
        SP2_THROW( ValueError, "MessageStructConverter for type " << protocol << " is not defined" );

    auto result = std::shared_ptr<MessageStructConverter>( creator( type, properties ) );
    rv.first -> second = result;
    return rv.first -> second;
}

}
