#ifndef _IN_SP2_ADAPTERS_UTILS_JSONMESSAGESTRUCTCONVERTER_H
#define _IN_SP2_ADAPTERS_UTILS_JSONMESSAGESTRUCTCONVERTER_H

#include <sp2/adapters/utils/MessageStructConverter.h>
#include <sp2/core/Hash.h>
#include <sp2/engine/Sp2Type.h>
#include <sp2/engine/Dictionary.h>
#include <rapidjson/document.h>
#include <list>
#include <string>
#include <unordered_map>

namespace sp2::adapters::utils
{

class JSONMessageStructConverter: public MessageStructConverter
{
public:
    JSONMessageStructConverter( const Sp2TypePtr & type, const Dictionary & properties );

    sp2::StructPtr asStruct( void * bytes, size_t size ) final;

    MsgProtocol protocol() const override { return MsgProtocol::JSON; }

    static MessageStructConverter * create( const Sp2TypePtr & type, const Dictionary & properties )
    {
        return new JSONMessageStructConverter( type, properties );
    }

private:

    //map of json field -> struct field ptr
    //we keep a hash since rapidjson Document field lookups are O(n)!
    struct FieldEntry
    {
        StructFieldPtr sField;
        std::shared_ptr<std::unordered_map<const char*,FieldEntry,sp2::hash::CStrHash,sp2::hash::CStrEq>> nestedFields;
    };

    using Fields = std::unordered_map<const char*,FieldEntry,sp2::hash::CStrHash,sp2::hash::CStrEq>;

    Fields buildFields( const Sp2StructType & type, const Dictionary & fieldMap );

    //T* only used for vector overloads
    template<typename T>
    T convertJSON( const char * fieldname, const rapidjson::Value & v, T * );

    template<typename T>
    T convertJSON( const char * fieldname, const Sp2Type & type, const FieldEntry & entry, const rapidjson::Value & v, T * foo )
    {
        return convertJSON( fieldname, v, foo );
    }

    template<typename T>
    std::vector<T> convertJSON( const char * fieldname, const Sp2Type & type, const FieldEntry & entry, const rapidjson::Value & v, std::vector<T> * );

    #ifdef __clang__
    template<>
    boost::container::vector<bool> convertJSON( const char * fieldname, const Sp2Type & type, const FieldEntry & entry, const rapidjson::Value & v, boost::container::vector<bool> * );
    #endif

    Fields           m_fields;
    DateTimeWireType m_datetimeType;
    std::list<std::string> m_jsonkeys; //intentionally stored as list so they dont invalidate on push
};

}

#endif //_IN_SP2_ADAPTERS_ACTIVEMQ_JSONMESSAGESTRUCTCONVERTER_H
