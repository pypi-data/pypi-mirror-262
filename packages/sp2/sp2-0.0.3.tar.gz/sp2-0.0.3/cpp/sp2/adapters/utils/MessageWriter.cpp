#include <sp2/adapters/utils/MessageWriter.h>
#include <sp2/adapters/utils/JSONMessageWriter.h>

namespace sp2::adapters::utils
{

MessageWriter::~MessageWriter()
{
}

OutputDataMapper::OutputDataMapper( const Sp2TypePtr & type, const Dictionary & fieldMap ) : m_type( type )
{
    m_hasFields = !fieldMap.empty();

    bool isStruct = type -> type() == Sp2Type::Type::STRUCT;
    if( isStruct )
        m_structMeta = std::static_pointer_cast<const Sp2StructType>( type ) -> meta();

    if( isStruct )
        m_messageFields = populateStructFields( m_structMeta, fieldMap );
    else if( !fieldMap.empty() )
    {
        if( fieldMap.size() != 1 || !fieldMap.exists( "" ) )
            SP2_THROW( ValueError, "non-struct output adapter expected single field_map entry with blank key" );

        m_messageFieldName = fieldMap.get<std::string>( "" );
    }
}

OutputDataMapper::Fields OutputDataMapper::populateStructFields( const StructMetaPtr & structMeta, const Dictionary & fieldMap )
{
    Fields out;
    for( auto it = fieldMap.begin(); it != fieldMap.end(); ++it )
    {
        auto & structField = it.key();
        auto sField = structMeta -> field( structField );
        if( !sField )
            SP2_THROW( ValueError, "field " << structField << " is not a valid field on struct type " << structMeta -> name() );

        if( it.hasValue<std::string>() )
        {
            if( sField -> type() -> type() == Sp2Type::Type::STRUCT )
                SP2_THROW( TypeError, "Expected non-struct type for fieldmap on struct field " << structField << " on struct " << structMeta -> name() );

            auto & fieldName   = it.value<std::string>();
            out.emplace_back( FieldEntry{ fieldName, sField, {} } );
        }
        else
        {
            if( !it.hasValue<DictionaryPtr>() )
                SP2_THROW( TypeError, "fieldMap expected string or dict for field \"" << structField << "\" on struct \"" << structMeta -> name() << "\"");

            auto nestedEntry = it.value<DictionaryPtr>();
            if( nestedEntry -> size() != 1 || !nestedEntry -> begin().hasValue<DictionaryPtr>() )
                SP2_THROW( ValueError, "Expected nested fieldmap for outgoing field \"" << structField << "\" on struct \"" << structMeta -> name() <<
                           "\" to have a dict of single key : nested_fieldmap entry" );

            if( sField -> type() -> type() != Sp2Type::Type::STRUCT )
                SP2_THROW( TypeError, "Expected structed type for nested struct field \"" << structField << "\" on struct \"" << structMeta -> name() << "\" got: \"" << sField -> type() -> type() << "\"" );

            //sub-struct
            auto nestedStructType = std::static_pointer_cast<const Sp2StructType>( sField -> type() );
            auto fieldName        = nestedEntry -> begin().key();
            auto nestedFieldMap   = nestedEntry -> begin().value<DictionaryPtr>();

            auto nestedFields = std::make_shared<Fields>( populateStructFields( nestedStructType -> meta(), *nestedFieldMap ) );
            out.emplace_back( FieldEntry{ fieldName, sField, nestedFields } );
        }
    }

    return out;
}

OutputDataMapperCache::OutputDataMapperCache()
{
}

OutputDataMapperCache & OutputDataMapperCache::instance()
{
    static OutputDataMapperCache s_instance;
    return s_instance;
}

OutputDataMapperPtr OutputDataMapperCache::create( const Sp2TypePtr & type, const Dictionary & fieldMap )
{
    std::lock_guard<std::mutex> guard( m_cacheMutex );

    auto rv = m_cache.emplace( CacheKey{ type.get(), fieldMap }, nullptr );
    if( !rv.second )
        return rv.first -> second;

    auto helper = std::make_shared<OutputDataMapper>( type, fieldMap );
    rv.first -> second = helper;
    return rv.first -> second;
}

}
