#ifndef _IN_SP2_ADAPTERS_UTILS_MESSAGESTRUCTCONVERTER_H
#define _IN_SP2_ADAPTERS_UTILS_MESSAGESTRUCTCONVERTER_H

#include <sp2/adapters/utils/MessageEnums.h>
#include <sp2/core/Enum.h>
#include <sp2/engine/Dictionary.h>
#include <sp2/engine/Struct.h>
#include <functional>
#include <memory>
#include <mutex>
#include <string>

namespace sp2::adapters::utils
{

class MessageStructConverter
{
public:
    MessageStructConverter( const Sp2TypePtr & type, const Dictionary & properties );
    virtual sp2::StructPtr asStruct( void * bytes, size_t size ) = 0;

    virtual MsgProtocol protocol() const = 0;

    StructMetaPtr structMeta() { return m_structMeta; }

protected:
    Sp2TypePtr    m_type;
    StructMetaPtr m_structMeta;

private:
    using FieldEntry = std::pair<std::string,StructFieldPtr>;
    using Fields     = std::vector<FieldEntry>;

    Fields m_propertyFields;
};

using MessageStructConverterPtr=std::shared_ptr<MessageStructConverter>;

//This ensures we dont recreate converters unnecessarily for say subscription by symbol with the same
//conversion onformation
class MessageStructConverterCache
{
public:
    MessageStructConverterCache();

    static MessageStructConverterCache & instance();

    MessageStructConverterPtr create( const Sp2TypePtr &, const Dictionary & properties );

    using Creator = std::function<MessageStructConverter*( const Sp2TypePtr &, const Dictionary & )>;

    bool registerConverter( MsgProtocol protocol, Creator creator );

private:
    using CacheKey = std::pair<const Sp2Type*,Dictionary>;
    using Cache = std::unordered_map<CacheKey,MessageStructConverterPtr,sp2::hash::hash_pair>;

    std::mutex m_cacheMutex;
    Cache      m_cache;
    Creator    m_creators[ MsgProtocol::NUM_TYPES ];
};

}

#endif
