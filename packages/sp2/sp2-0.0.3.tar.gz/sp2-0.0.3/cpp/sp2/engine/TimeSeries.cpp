#include <sp2/engine/TimeSeries.h>

namespace sp2 {
    using DuplicatePolicyEnum=TimeSeries::DuplicatePolicyEnum;
    INIT_SP2_ENUM(DuplicatePolicyEnum,
              "UNKNOWN",
              "LAST_VALUE",
              "FIRST_VALUE",
              "ALL_VALUES",
    );

}
