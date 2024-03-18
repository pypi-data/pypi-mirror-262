#include <sp2/adapters/utils/ProtobufMessageStructConverter.h>
#include <sp2/engine/Dictionary.h>
#include <sp2/core/Exception.h>
#include <google/protobuf/dynamic_message.h>

namespace proto = google::protobuf;

namespace sp2::adapters::utils
{

ProtobufMessageStructConverter::ProtobufMessageStructConverter( const Sp2TypePtr & type, const Dictionary & properties ) : MessageStructConverter( type, properties )
{
    if( type -> type() != Sp2Type::Type::STRUCT )
        SP2_THROW( TypeError, "ProtobufMessageStructConverter expects type struct got " << type -> type() );

    const std::string &protodir  = properties.get<std::string>( "proto_directory" );
    const std::string &protofile = properties.get<std::string>( "proto_filename" );
    const std::string &protomsg  = properties.get<std::string>( "proto_message" );
    const Dictionary & fieldMap  = *properties.get<DictionaryPtr>( "field_map" );

    const proto::FileDescriptor * protoFileDesc = ProtobufHelper::instance().import( protodir, protofile );

    m_protoDesc = protoFileDesc -> FindMessageTypeByName( protomsg );
    if( !m_protoDesc )
        SP2_THROW( ValueError, "Failed to find proto message " << protomsg << " in proto schema " << protofile );

    m_protoMapper.init( type, fieldMap, m_protoDesc );
}

sp2::StructPtr ProtobufMessageStructConverter::asStruct( void * bytes, size_t size )
{
    auto struct_ = m_structMeta -> create();

    auto * prototype = ProtobufHelper::instance().getMessage( m_protoDesc );
    if( !prototype )
        SP2_THROW( RuntimeException, "Failed to get proto message instance for proto descriptor " << m_protoDesc -> name() );

    std::unique_ptr<proto::Message> protoMsg( prototype -> New() );
    if( !protoMsg -> ParseFromArray( bytes, size ) )
        SP2_THROW( RuntimeException, "Failed to parse proto message on " << m_protoDesc -> name() );

    m_protoMapper.mapProtoToStruct( struct_, *protoMsg );
    return struct_;
}

}
