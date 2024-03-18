#ifndef _IN_SP2_ENGINE_SP2ENUM_H
#define _IN_SP2_ENGINE_SP2ENUM_H

#include <sp2/core/Exception.h>
#include <sp2/core/Hash.h>
#include <limits>
#include <string>
#include <vector>
#include <unordered_map>
#include <memory>

namespace sp2
{

class Sp2EnumMeta;

class Sp2EnumInstance
{
public:
    Sp2EnumInstance( std::string name, int64_t value, sp2::Sp2EnumMeta * meta ) : m_name( name ), m_value( value ), m_meta( meta ) {}
    Sp2EnumInstance( Sp2EnumInstance && o ) : m_name( o.m_name ), m_value( o.m_value ), m_meta( o.m_meta ) {}
    Sp2EnumInstance( const Sp2EnumInstance & o ) = delete;
    Sp2EnumInstance & operator=( Sp2EnumInstance o ) = delete;

    int64_t value() const { return m_value; }
    const std::string & name() const { return m_name; }
    const Sp2EnumMeta * meta() const { return m_meta; }

private:
    std::string m_name;
    int64_t m_value;
    Sp2EnumMeta * m_meta;
};

//As an optimization we do NOT attach meta or value to every instance of an enum.  Instead, the enum
//holds only a pointer to a singleton Sp2EnumInstance, which holds the value, name, and meta pointer.
class Sp2Enum
{
public:
    Sp2Enum();
    Sp2Enum( const Sp2Enum & other ) { m_instance = other.m_instance; }

    const int64_t value() const { return m_instance -> value(); }
    const Sp2EnumMeta * meta() const { return m_instance -> meta(); }
    const std::string & name() const { return m_instance -> name(); }

    // check instance to ensure value and meta are the same
    bool operator==( const Sp2Enum & rhs ) const { return m_instance == rhs.m_instance; }
    bool operator!=( const Sp2Enum & rhs ) const { return m_instance != rhs.m_instance; }

protected:
    explicit Sp2Enum( const Sp2EnumInstance * instance ) : m_instance( instance ) {}

    const Sp2EnumInstance * m_instance;

    friend class Sp2EnumMeta;
};

std::ostream &operator<<( std::ostream &os, const Sp2Enum & rhs );

class Sp2EnumMeta
{
public:
    using ValueDef = std::unordered_map<std::string,int64_t>;
    using Ptr = std::shared_ptr<Sp2EnumMeta>;

    Sp2EnumMeta( const std::string & name, const ValueDef & def );
    virtual ~Sp2EnumMeta();

    const std::string & name() const { return m_name; }
    size_t size() const              { return m_mapping.size(); }

    //note this will throw on invalid values
    Sp2Enum fromString( const char * key ) const
    {
        auto it = m_mapping.find( key );
        if( it == m_mapping.end() )
            SP2_THROW( ValueError, "Unrecognized enum name " << key << " for enum " << m_name );
        return Sp2Enum( &it -> second -> second );
    }

    Sp2Enum create( int64_t value ) const
    {
        auto found = m_instanceMap.find( value );
        if( found == m_instanceMap.end() )
            SP2_THROW( RuntimeException, "Unrecognized value " << value << " for enum " << m_name );
        return Sp2Enum( &found -> second );
    }

private:
    using InstanceMapping = std::unordered_map<int64_t, Sp2EnumInstance>;
    using Mapping        = std::unordered_map<const char *,InstanceMapping::iterator, hash::CStrHash, hash::CStrEq >;

    std::string    m_name;
    Mapping        m_mapping;

    InstanceMapping m_instanceMap;
};

}

namespace std
{

template<>
struct hash<sp2::Sp2Enum>
{
    size_t operator()( sp2::Sp2Enum e ) const
    {
        return std::hash<int64_t>()( e.value() );
    }
};

}

#endif
