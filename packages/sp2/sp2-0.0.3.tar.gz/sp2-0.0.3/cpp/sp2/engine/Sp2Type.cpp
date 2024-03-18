#include <sp2/engine/Sp2Type.h>
#include <mutex>

namespace sp2
{

INIT_SP2_ENUM( Sp2Type::Type,
           "UNKNOWN",
           "BOOL",
           "INT8",
           "UINT8",
           "INT16",
           "UINT16",
           "INT32",
           "UINT32",
           "INT64",
           "UINT64",
           "DOUBLE",
           "DATETIME",
           "TIMEDELTA",
           "DATE",
           "TIME",
           "ENUM",
           "STRING",
           "STRUCT",
           "ARRAY",
           "DIALECT_GENERIC"
    );

Sp2TypePtr & Sp2ArrayType::create( const Sp2TypePtr & elemType )
{
    using Cache = std::unordered_map<const Sp2Type*,Sp2TypePtr>;
    static std::mutex s_mutex;
    static Cache      s_cache;

    std::lock_guard<std::mutex> guard( s_mutex );
    auto rv = s_cache.emplace( elemType.get(), nullptr );
    if( rv.second )
        rv.first -> second = std::make_shared<Sp2ArrayType>( elemType );
    return rv.first -> second;
}

}
