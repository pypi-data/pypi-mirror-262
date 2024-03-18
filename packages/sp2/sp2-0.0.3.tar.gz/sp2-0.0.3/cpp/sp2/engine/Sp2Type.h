#ifndef _IN_SP2_ENGINE_SP2TYPE_H
#define _IN_SP2_ENGINE_SP2TYPE_H

#include <sp2/core/Enum.h>
#include <sp2/core/Time.h>
#include <sp2/engine/Sp2Enum.h>
#include <sp2/engine/DialectGenericType.h>
#include <cstdint>
#include <memory>
#include <string>

#ifdef __clang__
#include <boost/container/vector.hpp>
#endif

namespace sp2
{

class Sp2StringType;

class Sp2Type
{
public:

    struct TypeTraits
    {
    public:

        enum _enum : uint8_t
        {
            UNKNOWN,
            BOOL,
            INT8,
            UINT8,
            INT16,
            UINT16,
            INT32,
            UINT32,
            INT64,
            UINT64,
            DOUBLE,
            DATETIME,
            TIMEDELTA,
            DATE,
            TIME,
            ENUM,

            //Native implied the data is memcpy-able
            MAX_NATIVE_TYPE = ENUM,

            STRING,
            STRUCT,
            ARRAY,

            //These types are currently all dialect specific, no native primitives
            DIALECT_GENERIC,

            NUM_TYPES
        };

        constexpr TypeTraits() : m_value(_enum::UNKNOWN) {}

        template< typename T >
        struct fromCType;

        template< uint8_t T, typename ELEM_T=void >
        struct toCType;

    protected:
        _enum m_value;
    };

    using Type = Enum<TypeTraits>;

    Sp2Type( Type t ) : m_type( t ) {}

    Type type() const { return m_type; }

    using Ptr = std::shared_ptr<const Sp2Type>;

    static Ptr & BOOL()            { static auto s_type = std::make_shared<const Sp2Type>( Type::BOOL );            return s_type; }
    static Ptr & INT8()            { static auto s_type = std::make_shared<const Sp2Type>( Type::INT8 );            return s_type; }
    static Ptr & UINT8()           { static auto s_type = std::make_shared<const Sp2Type>( Type::UINT8 );           return s_type; }
    static Ptr & INT16()           { static auto s_type = std::make_shared<const Sp2Type>( Type::INT16 );           return s_type; }
    static Ptr & UINT16()          { static auto s_type = std::make_shared<const Sp2Type>( Type::UINT16 );          return s_type; }
    static Ptr & INT32()           { static auto s_type = std::make_shared<const Sp2Type>( Type::INT32 );           return s_type; }
    static Ptr & UINT32()          { static auto s_type = std::make_shared<const Sp2Type>( Type::UINT32 );          return s_type; }
    static Ptr & INT64()           { static auto s_type = std::make_shared<const Sp2Type>( Type::INT64 );           return s_type; }
    static Ptr & UINT64()          { static auto s_type = std::make_shared<const Sp2Type>( Type::UINT64 );          return s_type; }
    static Ptr & DOUBLE()          { static auto s_type = std::make_shared<const Sp2Type>( Type::DOUBLE );          return s_type; }
    static Ptr & DATETIME()        { static auto s_type = std::make_shared<const Sp2Type>( Type::DATETIME );        return s_type; }
    static Ptr & TIMEDELTA()       { static auto s_type = std::make_shared<const Sp2Type>( Type::TIMEDELTA );       return s_type; }
    static Ptr & DATE()            { static auto s_type = std::make_shared<const Sp2Type>( Type::DATE );            return s_type; }
    static Ptr & TIME()            { static auto s_type = std::make_shared<const Sp2Type>( Type::TIME );            return s_type; }
    static Ptr & STRING();
    static Ptr & BYTES();
    static Ptr & DIALECT_GENERIC() { static auto s_type = std::make_shared<const Sp2Type>( Type::DIALECT_GENERIC ); return s_type; }

    static constexpr bool isNative( Type t ) { return t <= Type::MAX_NATIVE_TYPE; }

    bool isNative() const { return isNative( m_type ); }

    template<typename T>
    struct fromCType;

    using StringCType = std::string;

private:
    Type m_type;
};

class Sp2StringType:public Sp2Type
{
public:
    Sp2StringType(bool isBytes)
    : Sp2Type(Sp2Type::Type::STRING), m_isBytes(isBytes) {}
    inline bool isBytes() const {return m_isBytes;}
private:
    const bool m_isBytes;
};

inline Sp2Type::Ptr & Sp2Type::STRING() { static Sp2Type::Ptr s_type = std::make_shared<const Sp2StringType>( false ); return s_type; }
inline Sp2Type::Ptr & Sp2Type::BYTES() { static Sp2Type::Ptr s_type = std::make_shared<const Sp2StringType>( true ); return s_type; }


using Sp2TypePtr = Sp2Type::Ptr;

class Sp2Enum;

class Sp2EnumMeta;

class Sp2EnumType : public Sp2Type
{
public:
    Sp2EnumType( std::shared_ptr<Sp2EnumMeta> & meta ) : Sp2Type( Sp2Type::Type::ENUM ),
                                                         m_meta( meta )
    {}

    const std::shared_ptr<Sp2EnumMeta> & meta() const { return m_meta; }

private:
    std::shared_ptr<Sp2EnumMeta> m_meta;
};

class Struct;
template<typename T>
class TypedStructPtr;
using StructPtr = TypedStructPtr<Struct>;

class StructMeta;

class Sp2StructType : public Sp2Type
{
public:
    Sp2StructType( const std::shared_ptr<StructMeta> & meta ) : Sp2Type( Sp2Type::Type::STRUCT ),
                                                                m_meta( meta )
    {}

    const std::shared_ptr<StructMeta> & meta() const { return m_meta; }

private:
    std::shared_ptr<StructMeta> m_meta;
};

class Sp2ArrayType : public Sp2Type
{
public:
    Sp2ArrayType( Sp2TypePtr elemType ) : Sp2Type( Sp2Type::Type::ARRAY ),
                                          m_elemType( elemType )
    {}

    const Sp2TypePtr & elemType() const { return m_elemType; }

    //Used by BURST mode to avoid creating more instances of Sp2ArrayTypes than needed
    //returns Sp2ArrayType with the given elemType
    static Sp2TypePtr & create( const Sp2TypePtr & elemType );

private:
    Sp2TypePtr m_elemType;
};

#ifndef __clang__
template<> struct Sp2Type::Type::fromCType<std::_Bit_reference>      { static constexpr Sp2Type::Type type = Sp2Type::Type::BOOL;            };
#endif
template<> template<> struct Sp2Type::Type::fromCType<bool>                     { static constexpr Sp2Type::Type type = Sp2Type::Type::BOOL;            };
template<> template<> struct Sp2Type::Type::fromCType<int8_t>                   { static constexpr Sp2Type::Type type = Sp2Type::Type::INT8;            };
template<> template<> struct Sp2Type::Type::fromCType<uint8_t>                  { static constexpr Sp2Type::Type type = Sp2Type::Type::UINT8;           };
template<> template<> struct Sp2Type::Type::fromCType<int16_t>                  { static constexpr Sp2Type::Type type = Sp2Type::Type::INT16;           };
template<> template<> struct Sp2Type::Type::fromCType<uint16_t>                 { static constexpr Sp2Type::Type type = Sp2Type::Type::UINT16;          };
template<> template<> struct Sp2Type::Type::fromCType<int32_t>                  { static constexpr Sp2Type::Type type = Sp2Type::Type::INT32;           };
template<> template<> struct Sp2Type::Type::fromCType<uint32_t>                 { static constexpr Sp2Type::Type type = Sp2Type::Type::UINT32;          };
template<> template<> struct Sp2Type::Type::fromCType<int64_t>                  { static constexpr Sp2Type::Type type = Sp2Type::Type::INT64;           };
template<> template<> struct Sp2Type::Type::fromCType<uint64_t>                 { static constexpr Sp2Type::Type type = Sp2Type::Type::UINT64;          };
template<> template<> struct Sp2Type::Type::fromCType<double>                   { static constexpr Sp2Type::Type type = Sp2Type::Type::DOUBLE;          };
template<> template<> struct Sp2Type::Type::fromCType<DateTime>                 { static constexpr Sp2Type::Type type = Sp2Type::Type::DATETIME;        };
template<> template<> struct Sp2Type::Type::fromCType<TimeDelta>                { static constexpr Sp2Type::Type type = Sp2Type::Type::TIMEDELTA;       };
template<> template<> struct Sp2Type::Type::fromCType<Date>                     { static constexpr Sp2Type::Type type = Sp2Type::Type::DATE;            };
template<> template<> struct Sp2Type::Type::fromCType<Time>                     { static constexpr Sp2Type::Type type = Sp2Type::Type::TIME;            };
template<> template<> struct Sp2Type::Type::fromCType<Sp2Enum>                  { static constexpr Sp2Type::Type type = Sp2Type::Type::ENUM;            };
template<> template<> struct Sp2Type::Type::fromCType<Sp2Type::StringCType>     { static constexpr Sp2Type::Type type = Sp2Type::Type::STRING;          };
template<> template<> struct Sp2Type::Type::fromCType<StructPtr>                { static constexpr Sp2Type::Type type = Sp2Type::Type::STRUCT;          };
template<> template<typename T> struct Sp2Type::Type::fromCType<TypedStructPtr<T>> { static constexpr Sp2Type::Type type = Sp2Type::Type::STRUCT;       };
template<> template<> struct Sp2Type::Type::fromCType<DialectGenericType>       { static constexpr Sp2Type::Type type = Sp2Type::Type::DIALECT_GENERIC; };
template<> template<typename T> struct Sp2Type::Type::fromCType<std::vector<T>> { static constexpr Sp2Type::Type type = Sp2Type::Type::ARRAY;           };
#ifdef __clang__
template<> template<> struct Sp2Type::Type::fromCType<boost::container::vector<bool>> { static constexpr Sp2Type::Type type = Sp2Type::Type::ARRAY;     };
#endif

template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::BOOL,void>            { using type = bool;                 };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::INT8,void>            { using type = int8_t;               };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::UINT8,void>           { using type = uint8_t;              };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::INT16,void>           { using type = int16_t;              };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::UINT16,void>          { using type = uint16_t;             };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::INT32,void>           { using type = int32_t;              };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::UINT32,void>          { using type = uint32_t;             };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::INT64,void>           { using type = int64_t;              };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::UINT64,void>          { using type = uint64_t;             };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::DOUBLE,void>          { using type = double;               };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::DATETIME,void>        { using type = DateTime;             };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::TIMEDELTA,void>       { using type = TimeDelta;            };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::DATE,void>            { using type = Date;                 };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::TIME,void>            { using type = Time;                 };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::ENUM,void>            { using type = Sp2Enum;              };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::STRING,void>          { using type = Sp2Type::StringCType; };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::STRUCT,void>          { using type = StructPtr;            };
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::DIALECT_GENERIC,void> { using type = DialectGenericType;   };
template<> template<typename T> struct Sp2Type::Type::toCType<Sp2Type::Type::ARRAY, T>   { using type = std::vector<T>;       };
#ifdef __clang__
template<> template<> struct Sp2Type::Type::toCType<Sp2Type::Type::ARRAY, bool>          { using type = boost::container::vector<bool>; };
#endif

template<> struct Sp2Type::fromCType<bool>                 { static Sp2TypePtr & type() { return Sp2Type::BOOL();      } };
template<> struct Sp2Type::fromCType<int8_t>               { static Sp2TypePtr & type() { return Sp2Type::INT8();      } };
template<> struct Sp2Type::fromCType<uint8_t>              { static Sp2TypePtr & type() { return Sp2Type::UINT8();     } };
template<> struct Sp2Type::fromCType<int16_t>              { static Sp2TypePtr & type() { return Sp2Type::INT16();     } };
template<> struct Sp2Type::fromCType<uint16_t>             { static Sp2TypePtr & type() { return Sp2Type::UINT16();    } };
template<> struct Sp2Type::fromCType<int32_t>              { static Sp2TypePtr & type() { return Sp2Type::INT32();     } };
template<> struct Sp2Type::fromCType<uint32_t>             { static Sp2TypePtr & type() { return Sp2Type::UINT32();    } };
template<> struct Sp2Type::fromCType<int64_t>              { static Sp2TypePtr & type() { return Sp2Type::INT64();     } };
template<> struct Sp2Type::fromCType<uint64_t>             { static Sp2TypePtr & type() { return Sp2Type::UINT64();    } };
template<> struct Sp2Type::fromCType<double>               { static Sp2TypePtr & type() { return Sp2Type::DOUBLE();    } };
template<> struct Sp2Type::fromCType<DateTime>             { static Sp2TypePtr & type() { return Sp2Type::DATETIME();  } };
template<> struct Sp2Type::fromCType<TimeDelta>            { static Sp2TypePtr & type() { return Sp2Type::TIMEDELTA(); } };
template<> struct Sp2Type::fromCType<Date>                 { static Sp2TypePtr & type() { return Sp2Type::DATE();      } };
template<> struct Sp2Type::fromCType<Time>                 { static Sp2TypePtr & type() { return Sp2Type::TIME();      } };
template<> struct Sp2Type::fromCType<Sp2Type::StringCType> { static Sp2TypePtr & type() { return Sp2Type::STRING();    } };
}

#endif
