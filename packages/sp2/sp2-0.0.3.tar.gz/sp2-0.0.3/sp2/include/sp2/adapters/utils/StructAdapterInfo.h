#ifndef _IN_SP2_ADAPTERS_PARQUET_StructAdapterInfo_H
#define _IN_SP2_ADAPTERS_PARQUET_StructAdapterInfo_H

#include <sp2/engine/Dictionary.h>
#include <sp2/engine/Sp2Type.h>
#include <string>


namespace sp2::adapters::utils
{

class StructAdapterInfo
{
public:
    StructAdapterInfo( Sp2TypePtr type, DictionaryPtr fieldMap )
            : m_type( type ), m_fieldMap( fieldMap ), m_hash( 0x9e3779b9 )
    {
        std::hash<std::string> stringHasher;
        if( m_fieldMap )
        {
            for( auto it = m_fieldMap -> begin(); it != m_fieldMap -> end(); ++it )
            {
                m_hash ^= stringHasher( it.key());
                m_hash ^= stringHasher( it.value<std::string>());
            }
        }
    }

    Sp2TypePtr type() const
    {
        return m_type;
    }

    DictionaryPtr fieldMap() const
    {
        return m_fieldMap;
    }

    std::size_t hash() const
    {
        return m_hash;
    }

    bool operator==( const StructAdapterInfo &other ) const
    {
        auto meta      = std::static_pointer_cast<const Sp2StructType>( m_type ) -> meta();
        auto otherMeta = std::static_pointer_cast<const Sp2StructType>( other.m_type ) -> meta();
        if( meta != otherMeta )
        {
            return false;
        }
        if( bool( m_fieldMap ) != bool( other.m_fieldMap ))
        {
            return false;
        }

        if( m_fieldMap )
        {
            if( m_fieldMap -> size() != other.m_fieldMap -> size())
            {
                return false;
            }
            for( auto it = m_fieldMap -> begin(); it != m_fieldMap -> end(); ++it )
            {
                if( !other.m_fieldMap -> exists( it.key()))
                {
                    return false;
                }
                if( it.value<std::string>() != other.m_fieldMap -> get<std::string>( it.key()))
                {
                    return false;
                }
            }
        }
        return true;
    }

private:
    friend class std::hash<StructAdapterInfo>;

    Sp2TypePtr    m_type;
    DictionaryPtr m_fieldMap;
    std::size_t   m_hash;
};

}

namespace std
{
template<>
struct hash<sp2::adapters::utils::StructAdapterInfo>
{
    size_t
    operator()( const sp2::adapters::utils::StructAdapterInfo &o ) const noexcept { return o.hash(); }
};

}

#endif
