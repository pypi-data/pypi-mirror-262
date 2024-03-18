#include <sp2/adapters/utils/RawBytesMessageStructConverter.h>

namespace sp2::adapters::utils
{

RawBytesMessageStructConverter::RawBytesMessageStructConverter( const Sp2TypePtr & type,
                                                  const Dictionary & properties ) : MessageStructConverter( type, properties ),
                                                                                    m_targetField( nullptr )
{
    const Dictionary & fieldMap = *properties.get<DictionaryPtr>( "field_map" );
    if( fieldMap.size() > 1 )
        SP2_THROW( ValueError, "RawBytesMessageStructConverter expects one entry in fieldMap" );

    if( fieldMap.size() == 1 )
    {
        if( type -> type() != Sp2Type::Type::STRUCT )
            SP2_THROW( ValueError, "field_map provided on non-struct type " << type -> type() << " in adapter" );

        if( !fieldMap.exists( "" ) )
            SP2_THROW( ValueError, "RawBytesMessageStructConverter expects one entry in fieldMap with empty string as source key" );
        auto targetKey = fieldMap.get<std::string>( "" );
        auto sField = m_structMeta -> field( targetKey );
        if( !sField || sField -> type() -> type() != Sp2Type::Type::STRING )
            SP2_THROW( TypeError, "field " << targetKey << " on struct " << m_structMeta -> name() << ( sField ? "is not string type" : "does not exist" ) );
        m_targetField = static_cast<const StringStructField *>( sField.get() );
    }
    else if( type -> type() != Sp2Type::Type::STRING )
        SP2_THROW( TypeError, "TestMessageStructConverter expected type of STRING for empty field_map got " << type -> type() );
}

sp2::StructPtr RawBytesMessageStructConverter::asStruct( void * bytes, size_t size )
{
    if( m_type -> type() == Sp2Type::Type::STRUCT )
    {
        StructPtr data = m_structMeta -> create();
        m_targetField -> setValue( data.get(), std::string( ( const char * ) bytes, size ) );
        return data;
    }
    else
        abort(); //TBD doesnt fit asStruct API
}

}
