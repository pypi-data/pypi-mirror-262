#ifndef _IN_SP2_ADAPTERS_UTILS_JSONMESSAGEWRITER_H
#define _IN_SP2_ADAPTERS_UTILS_JSONMESSAGEWRITER_H

#include <sp2/adapters/utils/MessageWriter.h>
#include <sp2/engine/Sp2Type.h>
#include <sp2/engine/Dictionary.h>
#include <sp2/engine/PartialSwitchSp2Type.h>
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <string>

namespace sp2::adapters::utils
{

class JSONMessageWriter : public MessageWriter
{
public:
    using SupportedSp2TypeSwitch = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL,
                                                        sp2::Sp2Type::Type::UINT8,
                                                        sp2::Sp2Type::Type::INT16,
                                                        sp2::Sp2Type::Type::INT32,
                                                        sp2::Sp2Type::Type::INT64,
                                                        sp2::Sp2Type::Type::DOUBLE,
                                                        sp2::Sp2Type::Type::DATETIME,
                                                        sp2::Sp2Type::Type::ENUM,
                                                        sp2::Sp2Type::Type::STRING,
                                                        sp2::Sp2Type::Type::STRUCT,
                                                        sp2::Sp2Type::Type::ARRAY
                                                        >;

    using SupportedArraySp2TypeSwitch = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL,
            sp2::Sp2Type::Type::UINT8,
            sp2::Sp2Type::Type::INT16,
            sp2::Sp2Type::Type::INT32,
            sp2::Sp2Type::Type::INT64,
            sp2::Sp2Type::Type::DOUBLE,
            sp2::Sp2Type::Type::DATETIME,
            sp2::Sp2Type::Type::ENUM,
            sp2::Sp2Type::Type::STRING
    >;

    JSONMessageWriter( const Dictionary & properties ) : MessageWriter( MsgProtocol::JSON )
    {
        m_doc.SetObject();
        m_datetimeWireType = utils::DateTimeWireType( properties.get<std::string>( "datetime_type" ) );
    }

    template<typename T>
    void setField( const std::string & field, const T & value, const Sp2Type & type, const FieldEntry & entry );

    std::pair<const void *,size_t> finalize() override
    {
        using Writer = rapidjson::Writer<rapidjson::StringBuffer,rapidjson::UTF8<>,rapidjson::UTF8<>,
                                         rapidjson::CrtAllocator,rapidjson::kWriteNanAndInfFlag>;
        m_stringBuffer.Clear();
        Writer writer( m_stringBuffer );
        m_doc.Accept( writer );
        //reset document
        //Note we have to explicitly clear the memory pool to avoid leaking!
        m_doc.GetAllocator().Clear();
        m_doc.SetObject();

        return {m_stringBuffer.GetString(),m_stringBuffer.GetSize()};
    }

private:
    void processTickImpl( const OutputDataMapper & dataMapper, const TimeSeriesProvider * sourcets ) override
    {
        dataMapper.apply( *this, sourcets );
    }

    template<typename T>
    inline auto convertValue( const T & value )
    {
        return value;
    }

    template<typename T>
    inline auto convertValue( const T & value, const Sp2Type & type, const FieldEntry & entry )
    {
        return convertValue( value );
    }


    template<typename T>
    auto convertValue( const std::vector<T> & value, const Sp2Type & type, const FieldEntry & entry );

    #ifdef __clang__
    template<>
    auto convertValue( const boost::container::vector<bool> & value, const Sp2Type & type, const FieldEntry & entry );
    #endif

    rapidjson::Document     m_doc;
    rapidjson::StringBuffer m_stringBuffer;
    utils::DateTimeWireType m_datetimeWireType;
};

template<>
inline auto JSONMessageWriter::convertValue( const std::string & value )
{
    return rapidjson::StringRef( value.c_str() );
}

template<>
inline auto JSONMessageWriter::convertValue( const sp2::Date & value )
{
    return rapidjson::Value( value.asYYYYMMDD().c_str(), m_doc.GetAllocator() );
}

template<>
inline auto JSONMessageWriter::convertValue( const sp2::DateTime & value )
{
    switch( m_datetimeWireType )
    {
        case utils::DateTimeWireType::UINT64_NANOS:
            return ( uint64_t ) value.asNanoseconds();
        case utils::DateTimeWireType::UINT64_MICROS:
            return ( uint64_t ) value.asMicroseconds();
        case utils::DateTimeWireType::UINT64_MILLIS:
            return ( uint64_t ) value.asMilliseconds();
        case utils::DateTimeWireType::UINT64_SECONDS:
            return ( uint64_t ) value.asSeconds();

        default:
            SP2_THROW( NotImplemented, "datetime wire type " << m_datetimeWireType << " not supported for json msg publishing" );
    }
}

template<>
inline auto JSONMessageWriter::convertValue( const sp2::TimeDelta & value )
{
    return rapidjson::Value( value.asNanoseconds() );
}

template<>
inline auto JSONMessageWriter::convertValue( const sp2::Sp2Enum & value, const Sp2Type & type, const FieldEntry & entry )
{
    return rapidjson::StringRef( value.name().c_str() );
}

template<typename T>
inline auto JSONMessageWriter::convertValue( const std::vector<T> & value, const Sp2Type & type, const FieldEntry & entry )
{
    auto & allocator = m_doc.GetAllocator();
    rapidjson::Value array( rapidjson::kArrayType );
    size_t sz = value.size();

    const Sp2Type & elemType = *static_cast<const Sp2ArrayType &>( type ).elemType();

    //iterating by index for vector<bool> support
    for( size_t index = 0; index < sz; ++index )
    {
        //Note this passes an empty FieldEntry / wont work on vector of structs
        array.PushBack( convertValue( value[index], elemType, {} ), allocator );
    }
    return array;
}

#ifdef __clang__
template<>
inline auto JSONMessageWriter::convertValue( const boost::container::vector<bool> & value, const Sp2Type & type, const FieldEntry & entry )
{
    auto & allocator = m_doc.GetAllocator();
    rapidjson::Value array( rapidjson::kArrayType );
    size_t sz = value.size();

    const Sp2Type & elemType = *static_cast<const Sp2ArrayType &>( type ).elemType();

    //iterating by index for vector<bool> support
    for( size_t index = 0; index < sz; ++index )
    {
        //Note this passes an empty FieldEntry / wont work on vector of structs
        array.PushBack( convertValue( value[index], elemType, {} ), allocator );
    }
    return array;
}
#endif

template<>
inline auto JSONMessageWriter::convertValue( const StructPtr & struct_, const Sp2Type & type, const FieldEntry & entry )
{
    rapidjson::Value jValue( rapidjson::kObjectType );
    for( auto & nestedEntry : *entry.nestedFields )
    {
        if( !nestedEntry.sField -> isSet( struct_.get() ) )
            continue;


        SupportedSp2TypeSwitch::template invoke<SupportedArraySp2TypeSwitch>(
            nestedEntry.sField -> type().get(),
            [ & ]( auto tag )
            {
                using T = typename decltype(tag)::type;
                jValue.AddMember( rapidjson::StringRef( nestedEntry.outField.c_str() ), convertValue( nestedEntry.sField -> value<T>( struct_.get() ), *nestedEntry.sField -> type(), nestedEntry ), m_doc.GetAllocator() );
            } );
    };
    return jValue;
}


template<typename T>
inline void JSONMessageWriter::setField( const std::string & field, const T & value, const Sp2Type & type, const FieldEntry & entry )
{
    m_doc.AddMember( rapidjson::StringRef( field.c_str() ), convertValue( value, type, entry ), m_doc.GetAllocator() );
}

}

#endif
