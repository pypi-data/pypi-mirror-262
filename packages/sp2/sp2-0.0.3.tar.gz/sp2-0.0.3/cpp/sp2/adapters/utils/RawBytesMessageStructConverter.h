#ifndef _IN_SP2_ADAPTERS_UTILS_RAWBYTESMESSAGESTRUCTCONVERTER_H
#define _IN_SP2_ADAPTERS_UTILS_RAWBYTESMESSAGESTRUCTCONVERTER_H

#include <sp2/adapters/utils/MessageStructConverter.h>
#include <sp2/engine/Dictionary.h>

namespace sp2::adapters::utils
{

class RawBytesMessageStructConverter : public MessageStructConverter
{
public:

    RawBytesMessageStructConverter( const Sp2TypePtr & type, const Dictionary & properties );

    sp2::StructPtr asStruct( void * bytes, size_t size ) override;

    MsgProtocol protocol() const override { return MsgProtocol::RAW_BYTES; }

    static MessageStructConverter * create( const Sp2TypePtr & type, const Dictionary & properties )
    {
        return new RawBytesMessageStructConverter( type, properties );
    }

private:
    const StringStructField * m_targetField;
};

}

#endif
