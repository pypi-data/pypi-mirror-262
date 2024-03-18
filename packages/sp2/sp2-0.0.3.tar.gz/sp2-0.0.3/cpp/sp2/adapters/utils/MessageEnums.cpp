#include <sp2/adapters/utils/MessageEnums.h>

namespace sp2
{

INIT_SP2_ENUM( sp2::adapters::utils::DateTimeWireType,
               "UNKNOWN",
               "UINT64_NANOS",
               "UINT64_MICROS",
               "UINT64_MILLIS",
               "UINT64_SECONDS"
);

INIT_SP2_ENUM( sp2::adapters::utils::MsgProtocol,
               "UNKNOWN",
               "JSON",
               "PROTOBUF",
               "RAW_BYTES"
);

}
