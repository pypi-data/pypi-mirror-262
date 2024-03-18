#ifndef _IN_SP2_ADAPTERS_UTILS_MESSAGEENUMS_H
#define _IN_SP2_ADAPTERS_UTILS_MESSAGEENUMS_H

#include <sp2/core/Enum.h>

namespace sp2::adapters::utils
{

struct DateTimeWireTypeTraits
{
    enum _enum : unsigned char
    {
        UNKNOWN = 0,
        UINT64_NANOS   = 1,
        UINT64_MICROS  = 2,
        UINT64_MILLIS  = 3,
        UINT64_SECONDS = 4,

        NUM_TYPES
    };

protected:
    _enum m_value;
};

using DateTimeWireType = sp2::Enum<DateTimeWireTypeTraits>;

//Note this should match enum defined in python
struct MsgProtocolTraits
{
    enum _enum : unsigned char
    {
        UNKNOWN = 0,
        JSON = 1,
        PROTOBUF = 2,
        RAW_BYTES = 3,
        NUM_TYPES
    };

protected:
    _enum m_value;
};

using MsgProtocol = sp2::Enum<MsgProtocolTraits>;

};

#endif
