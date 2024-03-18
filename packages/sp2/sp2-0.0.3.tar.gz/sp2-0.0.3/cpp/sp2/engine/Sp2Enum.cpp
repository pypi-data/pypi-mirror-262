#include <sp2/engine/Sp2Enum.h>

namespace sp2
{

static Sp2EnumInstance s_stubInstance( "", 0, new Sp2EnumMeta( "", Sp2EnumMeta::ValueDef{{ "", 0 }} ) );

Sp2Enum::Sp2Enum()
{
    m_instance = &s_stubInstance;
}

Sp2EnumMeta::Sp2EnumMeta( const std::string & name, const ValueDef & def ) : m_name( name )
{
    for( auto [ key,value ] : def )
    {
        auto [rit, inserted] = m_instanceMap.emplace( value, Sp2EnumInstance( key, value, this ) );
        if( !inserted )
            SP2_THROW( TypeError, "Sp2Enum type " << name << " defined with multiple entries for " << value );

        m_mapping[ rit -> second.name().c_str() ] = rit;
    }
}

Sp2EnumMeta::~Sp2EnumMeta()
{
}

std::ostream &operator<<( std::ostream &os, const Sp2Enum & rhs )
{
    os << rhs.name();
    return os;
};

}
