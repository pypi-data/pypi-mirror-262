#include <sp2/adapters/utils/JSONMessageStructConverter.h>
#include <sp2/engine/Sp2Type.h>
#include <sp2/engine/PartialSwitchSp2Type.h>
#include <rapidjson/document.h>
#include <rapidjson/error/en.h>
#include <type_traits>

namespace sp2::adapters::utils
{

using SupportedSp2TypeSwitch = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL,
                                                    sp2::Sp2Type::Type::INT32,
                                                    sp2::Sp2Type::Type::INT64,
                                                    sp2::Sp2Type::Type::DOUBLE,
                                                    sp2::Sp2Type::Type::DATETIME,
                                                    sp2::Sp2Type::Type::STRING,
                                                    sp2::Sp2Type::Type::ENUM,
                                                    sp2::Sp2Type::Type::STRUCT,
                                                    sp2::Sp2Type::Type::ARRAY
                                                    >;

using SupportedArraySp2TypeSwitch = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL,
                                                    sp2::Sp2Type::Type::INT32,
                                                    sp2::Sp2Type::Type::INT64,
                                                    sp2::Sp2Type::Type::DOUBLE,
                                                    sp2::Sp2Type::Type::DATETIME,
                                                    sp2::Sp2Type::Type::STRING,
                                                    sp2::Sp2Type::Type::ENUM
                                                    >;


template<>
bool JSONMessageStructConverter::convertJSON( const char * fieldname, const rapidjson::Value & jValue, bool * )
{
    if( jValue.IsBool() )
        return jValue.GetBool();
    else
        SP2_THROW( TypeError, "expected type BOOL for json field " << fieldname );
}

template<>
int32_t JSONMessageStructConverter::convertJSON( const char * fieldname, const rapidjson::Value & jValue, int32_t * )
{
    if( jValue.IsInt() )
        return jValue.GetInt();
    else
        SP2_THROW( TypeError, "expected INT32 type for json field " << fieldname );
}

template<>
int64_t JSONMessageStructConverter::convertJSON( const char * fieldname, const rapidjson::Value & jValue, int64_t * )
{
    if( jValue.IsInt64() )
        return jValue.GetInt64();
    else
        SP2_THROW( TypeError, "expected INT64 type for json field " << fieldname );
}

template<>
double JSONMessageStructConverter::convertJSON( const char * fieldname, const rapidjson::Value & jValue, double * )
{
    if( jValue.IsNumber() )
        return jValue.GetDouble();
    else
        SP2_THROW( TypeError, "expected DOUBLE type for json field " << fieldname );
}

template<>
std::string JSONMessageStructConverter::convertJSON( const char * fieldname, const rapidjson::Value & jValue, std::string * )
{
    if( jValue.IsString() )
        return jValue.GetString();
    else
        SP2_THROW( TypeError, "expected STRING type for json field " << fieldname );
}

template<>
DateTime JSONMessageStructConverter::convertJSON( const char * fieldname, const rapidjson::Value & jValue, DateTime * )
{
    if( jValue.IsUint64() )
    {
        uint64_t raw = jValue.GetUint64();
        DateTime dt;
        switch( m_datetimeType )
        {
            case DateTimeWireType::UINT64_NANOS:   dt = DateTime::fromNanoseconds( raw ); break;
            case DateTimeWireType::UINT64_MICROS:  dt = DateTime::fromMicroseconds( raw ); break;
            case DateTimeWireType::UINT64_MILLIS:  dt = DateTime::fromMilliseconds( raw ); break;
            case DateTimeWireType::UINT64_SECONDS: dt = DateTime::fromSeconds( raw ); break;

            case DateTimeWireType::UNKNOWN:
            case DateTimeWireType::NUM_TYPES:
                SP2_THROW( TypeError, "json field " << fieldname << " is datetime but datetimeType is not configured" );
        }

        return dt;
    }
    else
        SP2_THROW( TypeError, "expected UINT64 for DATETIME for json field " << fieldname );
}

template<>
Sp2Enum JSONMessageStructConverter::convertJSON( const char * fieldname, const Sp2Type & type, const FieldEntry &, const rapidjson::Value & jValue, Sp2Enum * )
{
    if( !jValue.IsString() )
        SP2_THROW( TypeError, "expected ENUM type for json field " << fieldname );

    auto & sp2EnumType = static_cast<const Sp2EnumType &>( type );
    return sp2EnumType.meta() -> fromString( jValue.GetString() );
}

template<>
StructPtr JSONMessageStructConverter::convertJSON( const char * fieldname, const Sp2Type &, const FieldEntry & entry, const rapidjson::Value & jValue, StructPtr * )
{
    if( !jValue.IsObject() )
        SP2_THROW( TypeError, "expected Nested object type for json field " << fieldname );

    const Sp2StructType & sType = static_cast<const Sp2StructType &>( *entry.sField -> type() );
    auto struct_ = sType.meta() -> create();
    auto & fields = *entry.nestedFields;
    for( auto jit = jValue.MemberBegin(); jit != jValue.MemberEnd(); ++jit )
    {
        auto sIt = fields.find( jit -> name.GetString() );
        if( sIt == fields.end() )
            continue;

        auto & nestedEntry = sIt -> second;

        SupportedSp2TypeSwitch::invoke<SupportedArraySp2TypeSwitch>(
            nestedEntry.sField -> type().get(), [this,&jit,&nestedEntry,&struct_]( auto tag )
            {
                using T = typename decltype(tag)::type;
                auto & jValue = jit -> value;

                nestedEntry.sField -> setValue( struct_.get(), convertJSON( jit -> name.GetString(), *nestedEntry.sField -> type(), nestedEntry, jValue, static_cast<T*>( nullptr ) ) );
            } );
    }

    return struct_;
}

template<typename T>
std::vector<T> JSONMessageStructConverter::convertJSON( const char * fieldname, const Sp2Type & type, const FieldEntry &, const rapidjson::Value & jValue, std::vector<T> * x )
{
    if( !jValue.IsArray() )
        SP2_THROW( TypeError, "expected ARRAY type for json field " << fieldname );

    auto jArray = jValue.GetArray();

    const Sp2Type & elemType = *static_cast<const Sp2ArrayType &>( type ).elemType();

    std::vector<T> out;
    out.reserve( jArray.Size() );
    for( auto & v : jArray )
    {
        //note that we dont pass FieldEntry to convert here, this doesnt support arrays of structs
        out.emplace_back( convertJSON( fieldname, elemType, {}, v, ( T * ) nullptr) );
    }

    return out;
}

#ifdef __clang__
template <>
boost::container::vector<bool> JSONMessageStructConverter::convertJSON( const char * fieldname, const Sp2Type & type, const FieldEntry &, const rapidjson::Value & jValue, boost::container::vector<bool> * x )
{
    if( !jValue.IsArray() )
        SP2_THROW( TypeError, "expected ARRAY type for json field " << fieldname );

    auto jArray = jValue.GetArray();

    const Sp2Type & elemType = *static_cast<const Sp2ArrayType &>( type ).elemType();

    boost::container::vector<bool> out;
    out.reserve( jArray.Size() );
    for( auto & v : jArray )
    {
        //note that we dont pass FieldEntry to convert here, this doesnt support arrays of structs
        out.emplace_back( convertJSON( fieldname, elemType, {}, v, ( bool * ) nullptr) );
    }

    return out;
}
#endif

JSONMessageStructConverter::JSONMessageStructConverter( const Sp2TypePtr & type,
                                                        const Dictionary & properties ) : MessageStructConverter( type, properties )
{
    if( type -> type() != Sp2Type::Type::STRUCT )
        SP2_THROW( TypeError, "JSONMessageStructConverter expects type struct got " << type -> type() );

    const Dictionary & fieldMap = *properties.get<DictionaryPtr>( "field_map" );
    m_datetimeType = DateTimeWireType( properties.get<std::string>( "datetime_type" ) );
    m_fields = buildFields( static_cast<const Sp2StructType &>( *type ), fieldMap );
}

JSONMessageStructConverter::Fields JSONMessageStructConverter::buildFields( const Sp2StructType & type, const Dictionary & fieldMap )
{
    JSONMessageStructConverter::Fields out;

    for( auto it = fieldMap.begin(); it != fieldMap.end(); ++it )
    {
        auto & fieldName  = it.key();

        std::string structField;
        DictionaryPtr nestedFieldMap;

        if( it.hasValue<std::string>() )
            structField = it.value<std::string>();
        else
        {
            if( !it.hasValue<DictionaryPtr>() )
                SP2_THROW( TypeError, "fieldMap expected string or dict for field " << fieldName << " on struct " << type.meta() -> name() );
            auto nestedDict = it.value<DictionaryPtr>();
            if( nestedDict -> size() != 1 )
                SP2_THROW( ValueError, "Expected nested fieldmap for incoming JSON field " << fieldName << " to have a single key : map entry" );
            structField    = nestedDict -> begin().key();
            nestedFieldMap = nestedDict -> begin().value<DictionaryPtr>();
        }

        auto sField = type.meta() -> field( structField );
        if( !sField )
            SP2_THROW( ValueError, "field " << structField << " is not a valid field on struct type " << type.meta() -> name() );

        std::shared_ptr<Fields> nestedFields;
        if( sField -> type() -> type() == Sp2Type::Type::STRUCT )
        {
            if( !nestedFieldMap )
                SP2_THROW( ValueError, "invalid field_map entry for nested struct field " << sField -> fieldname() << " on struct type " << type.meta() -> name() );
            nestedFields = std::make_shared<Fields>( buildFields( static_cast<const Sp2StructType &>( *sField -> type() ), *nestedFieldMap ) );
        }

        //keep strings around to keep const char * keys alive
        m_jsonkeys.emplace_back( fieldName );
        out.emplace( m_jsonkeys.back().c_str(), FieldEntry{ sField, nestedFields } );
    }
    return out;
}

sp2::StructPtr JSONMessageStructConverter::asStruct( void * bytes, size_t size )
{
    const char * rawmsg = (const char *) bytes;

    rapidjson::Document document;
    rapidjson::ParseResult ok = document.Parse<rapidjson::kParseNanAndInfFlag>( rawmsg, size );
    if( !ok )
        SP2_THROW( ValueError, "Failed to parse message as JSON: " << rapidjson::GetParseError_En( ok.Code() ) << " on msg: " << std::string( rawmsg, size ) );

    StructPtr data = m_structMeta -> create();

    for( auto jit = document.MemberBegin(); jit != document.MemberEnd(); ++jit )
    {
        auto sIt = m_fields.find( jit -> name.GetString() );
        if( sIt == m_fields.end() )
            continue;

        auto & entry = sIt -> second;
        SupportedSp2TypeSwitch::invoke<SupportedArraySp2TypeSwitch>(
            entry.sField -> type().get(), [this,&jit,&entry,&data]( auto tag )
            {
                using T = typename decltype(tag)::type;
                auto & jValue = jit -> value;
                entry.sField -> setValue( data.get(), convertJSON( jit -> name.GetString(), *entry.sField -> type(), entry, jValue, static_cast<T*>( nullptr ) ) );
            }
        );
    }

    return data;
}
}
