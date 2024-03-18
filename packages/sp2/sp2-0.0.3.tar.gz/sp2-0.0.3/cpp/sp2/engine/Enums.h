#ifndef _IN_SP2_ENGINE_ENUMS_H
#define _IN_SP2_ENGINE_ENUMS_H

#include <sp2/core/Enum.h>

namespace sp2
{

// NOTE this must align with the python side Enum definition ///
struct PushModeTraits
{
    enum _enum : unsigned char
    {
        UNKNOWN        = 0,
        LAST_VALUE     = 1,
        NON_COLLAPSING = 2,
        BURST          = 3,

        NUM_TYPES
    };

protected:
    _enum m_value;
};

using PushMode = Enum<PushModeTraits>;

}

#endif
