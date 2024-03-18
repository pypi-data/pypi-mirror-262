#ifndef _IN_SP2_ADAPTERS_UTILS_MESSAGEWRITER_H
#define _IN_SP2_ADAPTERS_UTILS_MESSAGEWRITER_H

#include <sp2/adapters/utils/MessageEnums.h>
#include <sp2/core/Enum.h>
#include <sp2/engine/Sp2Type.h>
#include <sp2/engine/Dictionary.h>
#include <sp2/engine/Struct.h>
#include <sp2/engine/TimeSeriesProvider.h>
#include <memory>
#include <mutex>
#include <string>
#include <vector>
#include <unordered_map>

namespace sp2::adapters::utils
{

//This is used to map data from an output adapter- > message writer ( can have multiple ouput adapters writing to same message )
class OutputDataMapper
{
public:
    OutputDataMapper( const Sp2TypePtr & type, const Dictionary & fieldMap );

    template<typename MessageWriterT>
    void apply( MessageWriterT & writer, const TimeSeriesProvider * sourcets ) const;

    bool hasFields() const { return m_hasFields; }

    struct FieldEntry
    {
        std::string    outField;
        StructFieldPtr sField;
        std::shared_ptr<std::vector<FieldEntry>> nestedFields; //for nested structs
    };

    using Fields = std::vector<FieldEntry>;

private:
    Fields populateStructFields( const StructMetaPtr & structMeta, const Dictionary & field_map );

    //struct outputs
    template<typename MessageWriterT>
    void applyStruct( MessageWriterT & writer, const Struct * struct_ ) const;

    //non-struct outputs
    template<typename MessageWriterT,typename T>
    void applyField( MessageWriterT & writer, const T & value ) const;

    Sp2TypePtr    m_type;
    bool          m_hasFields;

    //Struct specific
    StructMetaPtr m_structMeta;
    Fields        m_messageFields;

    //non-struct specific
    std::string m_messageFieldName;
};

using OutputDataMapperPtr=std::shared_ptr<OutputDataMapper>;

// Derived types will be used to create and write timeseries data -> target message protocol ( ie JSON, proto )
// and convert it to bytes for the output adapter
class MessageWriter
{
public:
    using FieldEntry = OutputDataMapper::FieldEntry;

    MessageWriter( MsgProtocol protocol ) : m_protocol( protocol ) {}
    virtual ~MessageWriter();

    MsgProtocol protocol() const { return m_protocol; }

    //returns the finalized message as bytes
    virtual std::pair<const void *,size_t> finalize() = 0;

    void processTick( const OutputDataMapper & dataMapper, const TimeSeriesProvider * sourcets )
    {
        if( dataMapper.hasFields() )
            processTickImpl( dataMapper, sourcets );
    }

private:
    virtual void processTickImpl( const OutputDataMapper & dataMapper, const TimeSeriesProvider * sourcets ) = 0;
    MsgProtocol m_protocol;
};

using MessageWriterPtr=std::shared_ptr<MessageWriter>;

template<typename MessageWriterT>
inline void OutputDataMapper::apply( MessageWriterT & writer, const TimeSeriesProvider * ts ) const
{
    if( !m_hasFields )
        return;

    if( ts -> type() -> type() == Sp2Type::Type::STRUCT )
        applyStruct( writer, ts -> lastValueTyped<StructPtr>().get() );
    else
    {
        MessageWriterT::SupportedSp2TypeSwitch::template invoke<typename MessageWriterT::SupportedArraySp2TypeSwitch>( ts -> type(),
                                                                 [&]( auto tag )
                                                                 {
                                                                     applyField( writer, ts -> lastValueTyped<typename decltype(tag)::type>() );
                                                                 } );
    }
}

template<typename MessageWriterT,typename T>
inline void OutputDataMapper::applyField( MessageWriterT & writer, const T & value ) const
{
    SP2_ASSERT( m_type -> type() != Sp2Type::Type::STRUCT );

    if( !m_messageFieldName.empty() )
        writer.setField( m_messageFieldName, value, *m_type, {} );
}

template<typename MessageWriterT>
inline void OutputDataMapper::applyStruct( MessageWriterT & writer, const Struct * struct_ ) const
{
    SP2_ASSERT( m_type -> type() == Sp2Type::Type::STRUCT );

    for( auto & entry : m_messageFields )
    {
        if( !entry.sField -> isSet( struct_ ) )
            continue;

        using SwitchT = typename MessageWriterT::SupportedSp2TypeSwitch;

        SwitchT::template invoke<typename MessageWriterT::SupportedArraySp2TypeSwitch>(
            entry.sField -> type().get(),
            [ & ]( auto tag )
            {
                using T = typename decltype(tag)::type;
                writer.setField( entry.outField, entry.sField -> value<T>( struct_ ), *entry.sField -> type(), entry );
            } );
    };
}

//This ensures we dont recreate duplicate writers unnecessarily
class OutputDataMapperCache
{
public:
    OutputDataMapperCache();

    static OutputDataMapperCache & instance();

    OutputDataMapperPtr create( const Sp2TypePtr &, const Dictionary & fieldMap );

private:
    using CacheKey = std::pair<const Sp2Type*,Dictionary>;
    using Cache = std::unordered_map<CacheKey,OutputDataMapperPtr,sp2::hash::hash_pair>;

    std::mutex m_cacheMutex;
    Cache      m_cache;
};

}

#endif
