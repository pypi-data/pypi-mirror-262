#ifndef _IN_SP2_ENGINE_PartialSwitchSp2Type_H
#define _IN_SP2_ENGINE_PartialSwitchSp2Type_H

#include <sp2/core/Exception.h>
#include <sp2/core/System.h>
#include <sp2/core/Time.h>
#include <sp2/engine/Sp2Type.h>
#include <stdint.h>
#include <unordered_set>
#include <type_traits>
#include <string>

namespace sp2
{
SP2_DECLARE_EXCEPTION( UnsupportedSwitchType, TypeError );

template< sp2::Sp2Type::Type::_enum ...Vs >
struct PartialSwitchSp2Type
{
    static constexpr sp2::Sp2Type::Type::_enum V1_T = sp2::Sp2Type::Type::UNKNOWN;

    template< sp2::Sp2Type::Type::_enum ...ExtraVs >
    using Extend=PartialSwitchSp2Type<Vs..., ExtraVs...>;

    template< typename sp2::Sp2Type::Type::_enum T >
    static constexpr bool isSupportedType()
    {
        return false;
    }

    template< typename ArraySubtypeSwitch=void, typename F=void >
    static auto invoke( const Sp2Type *type, F &&f )
    {
        SP2_THROW( UnsupportedSwitchType, "Unsupported type " << type -> type());
    }

    template< typename ArraySubtypeSwitch=void, typename F=void >
    static auto invoke( const Sp2TypePtr& type, F &&f )
    {
        return invoke( type.get(), std::forward<F>( f ) );
    }
};

using ArraySubTypeSwitch = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::INT8,
        sp2::Sp2Type::Type::UINT8, sp2::Sp2Type::Type::INT16, sp2::Sp2Type::Type::UINT16, sp2::Sp2Type::Type::INT32,
        sp2::Sp2Type::Type::UINT32, sp2::Sp2Type::Type::INT64, sp2::Sp2Type::Type::UINT64, sp2::Sp2Type::Type::DOUBLE,
        sp2::Sp2Type::Type::DATETIME, sp2::Sp2Type::Type::TIMEDELTA, sp2::Sp2Type::Type::DATE, sp2::Sp2Type::Type::TIME,
        sp2::Sp2Type::Type::ENUM,
        sp2::Sp2Type::Type::STRING, sp2::Sp2Type::Type::STRUCT, sp2::Sp2Type::Type::DIALECT_GENERIC>;

template< sp2::Sp2Type::Type::_enum V1, sp2::Sp2Type::Type::_enum U1 >
struct SwitchCTypeResolver
{
    using TagType = Sp2Type::Type::toCType<V1>;
};

template< sp2::Sp2Type::Type::_enum U1 >
struct SwitchCTypeResolver<sp2::Sp2Type::Type::ARRAY, U1>
{
    using TagType = Sp2Type::Type::toCType<sp2::Sp2Type::Type::ARRAY, typename Sp2Type::Type::toCType<U1>::type>;
};

template< sp2::Sp2Type::Type::_enum V1, sp2::Sp2Type::Type::_enum ...Vs >
struct PartialSwitchSp2Type<V1, Vs...>
{
    template< sp2::Sp2Type::Type::_enum ...ExtraVs >
    using Extend=PartialSwitchSp2Type<Vs..., ExtraVs...>;
private:
    template< typename F >
    static F makeF();

    template< typename ArraySubSwitchType >
    using TagType = typename SwitchCTypeResolver<V1, ArraySubSwitchType::V1_T>::TagType;

    template< typename F, typename ArraySubSwitchType >
    using ResolveReturnType = decltype( makeF<F>()( TagType<ArraySubSwitchType>()));
public:
    static constexpr sp2::Sp2Type::Type::_enum V1_T = V1;

    template< typename sp2::Sp2Type::Type::_enum T >
    static constexpr bool isSupportedType()
    {
        return T == V1 || PartialSwitchSp2Type<Vs...>::template isSupportedType<T>();
    }

    template< typename ArraySubTypeSwitchT=ArraySubTypeSwitch, typename F=void >
    static auto invoke( const Sp2Type *type, F &&f )
    {
        using R_T = ResolveReturnType<F, ArraySubTypeSwitchT>;
        switch( type -> type())
        {
            case Sp2Type::Type::BOOL:
                return handleType<Sp2Type::Type::BOOL, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::INT8:
                return handleType<Sp2Type::Type::INT8, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::UINT8:
                return handleType<Sp2Type::Type::UINT8, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::INT16:
                return handleType<Sp2Type::Type::INT16, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::UINT16:
                return handleType<Sp2Type::Type::UINT16, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::INT32:
                return handleType<Sp2Type::Type::INT32, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::UINT32:
                return handleType<Sp2Type::Type::UINT32, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::INT64:
                return handleType<Sp2Type::Type::INT64, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::UINT64:
                return handleType<Sp2Type::Type::UINT64, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::DOUBLE:
                return handleType<Sp2Type::Type::DOUBLE, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::DATETIME:
                return handleType<Sp2Type::Type::DATETIME, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::TIMEDELTA:
                return handleType<Sp2Type::Type::TIMEDELTA, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::DATE:
                return handleType<Sp2Type::Type::DATE, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::TIME:
                return handleType<Sp2Type::Type::TIME, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::ENUM:
                return handleType<Sp2Type::Type::ENUM, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::STRING:
                return handleType<Sp2Type::Type::STRING, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::STRUCT:
                return handleType<Sp2Type::Type::STRUCT, F, R_T>( type, std::forward<F>( f ));
            case Sp2Type::Type::ARRAY:
                return handleArrayType<F, R_T, ArraySubTypeSwitchT>( type, std::forward<F>( f ));
            case Sp2Type::Type::DIALECT_GENERIC:
                return handleType<Sp2Type::Type::DIALECT_GENERIC, F, R_T>( type, std::forward<F>( f ));
            case sp2::Sp2Type::Type::UNKNOWN:
            case sp2::Sp2Type::Type::NUM_TYPES:
                SP2_THROW( TypeError, "Unexpected Sp2Type: " << type -> type());
        }
        SP2_THROW( TypeError, "Unexpected Sp2Type: " << type -> type());
    }

    template< typename ArraySubtypeSwitch=void, typename F=void >
    static auto invoke( const Sp2TypePtr& type, F &&f )
    {
        return invoke( type.get(), std::forward<F>( f ) );
    }

private:
    template< typename F,
            typename R_T,
            typename ArraySubTypeSwitchT,
            sp2::Sp2Type::Type::_enum T = Sp2Type::Type::ARRAY,
            std::enable_if_t<isSupportedType<T>(), int> = 1 >
    static R_T handleArrayType( const Sp2Type *type, F &&f )
    {
        const auto *arrayType = static_cast<const Sp2ArrayType *>( type );
        return ArraySubTypeSwitchT::invoke( arrayType -> elemType().get(), [ &f ]( auto tag )
        {

            return f( Sp2Type::Type::toCType<T, typename decltype(tag)::type>());
        } );
    }

    template< typename F,
            typename R_T,
            typename ArraySubTypeSwitchT,
            sp2::Sp2Type::Type::_enum T = Sp2Type::Type::ARRAY,
            std::enable_if_t<!isSupportedType<T>(), int> = 0 >
    static R_T handleArrayType( const Sp2Type *type, F &&f )
    {
        SP2_THROW( UnsupportedSwitchType, "Unsupported type " << Sp2Type::Type( T ));
    }

    template< sp2::Sp2Type::Type::_enum T,
            typename F,
            typename R_T,
            std::enable_if_t<isSupportedType<T>(), int> = 0 >
    static R_T handleType( const Sp2Type *type, F &&f )
    {
        return f( Sp2Type::Type::toCType<T>());
    }

    template< sp2::Sp2Type::Type::_enum T,
            typename F,
            typename R_T,
            std::enable_if_t<!isSupportedType<T>(), int> = 0 >
    static R_T handleType( const Sp2Type *type, F &&f )
    {
        SP2_THROW( UnsupportedSwitchType, "Unsupported type " << Sp2Type::Type( T ));
    }
};

template< typename T1, typename T2 >
struct Sp2TypeSwitchConcat
{
};

template< typename T1, sp2::Sp2Type::Type::_enum ...Vs2 >
struct Sp2TypeSwitchConcat<T1, PartialSwitchSp2Type<Vs2...>>
{
private:
    template< sp2::Sp2Type::Type::_enum ...Vs1 >
    static PartialSwitchSp2Type<Vs1..., Vs2...> aux( PartialSwitchSp2Type<Vs1...> );

public:
    using type = decltype( aux( T1()));
};

using AllSp2TypeSwitch = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::INT8,
        sp2::Sp2Type::Type::UINT8, sp2::Sp2Type::Type::INT16, sp2::Sp2Type::Type::UINT16, sp2::Sp2Type::Type::INT32,
        sp2::Sp2Type::Type::UINT32, sp2::Sp2Type::Type::INT64, sp2::Sp2Type::Type::UINT64, sp2::Sp2Type::Type::DOUBLE,
        sp2::Sp2Type::Type::DATETIME, sp2::Sp2Type::Type::TIMEDELTA, sp2::Sp2Type::Type::DATE, sp2::Sp2Type::Type::TIME, sp2::Sp2Type::Type::ENUM,
        sp2::Sp2Type::Type::STRING, sp2::Sp2Type::Type::STRUCT, sp2::Sp2Type::Type::ARRAY, sp2::Sp2Type::Type::DIALECT_GENERIC>;
using ArithmeticSp2TypeSwitch = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::INT8,
        sp2::Sp2Type::Type::UINT8, sp2::Sp2Type::Type::INT16, sp2::Sp2Type::Type::UINT16, sp2::Sp2Type::Type::INT32,
        sp2::Sp2Type::Type::UINT32, sp2::Sp2Type::Type::INT64, sp2::Sp2Type::Type::UINT64, sp2::Sp2Type::Type::DOUBLE>;
using NativeSp2TypeSwitch = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::INT8,
        sp2::Sp2Type::Type::UINT8, sp2::Sp2Type::Type::INT16, sp2::Sp2Type::Type::UINT16, sp2::Sp2Type::Type::INT32,
        sp2::Sp2Type::Type::UINT32, sp2::Sp2Type::Type::INT64, sp2::Sp2Type::Type::UINT64, sp2::Sp2Type::Type::DOUBLE,
        sp2::Sp2Type::Type::DATETIME, sp2::Sp2Type::Type::TIMEDELTA, sp2::Sp2Type::Type::DATE, sp2::Sp2Type::Type::TIME, sp2::Sp2Type::Type::ENUM>;
using PrimitiveSp2TypeSwitch = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::INT8,
        sp2::Sp2Type::Type::UINT8, sp2::Sp2Type::Type::INT16, sp2::Sp2Type::Type::UINT16, sp2::Sp2Type::Type::INT32,
        sp2::Sp2Type::Type::UINT32, sp2::Sp2Type::Type::INT64, sp2::Sp2Type::Type::UINT64, sp2::Sp2Type::Type::DOUBLE,
        sp2::Sp2Type::Type::DATETIME, sp2::Sp2Type::Type::TIMEDELTA, sp2::Sp2Type::Type::DATE, sp2::Sp2Type::Type::TIME, sp2::Sp2Type::Type::ENUM, sp2::Sp2Type::Type::STRING>;


/**
 * A class that that defines a single member type "type" to PartialSwitchSp2Type of all types that can be constructed from T.
 * For example ConstructibleTypeSwitchAux<double> will have its type defined to
 * PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::DOUBLE> since double can be cast to bool or double.
 * @tparam T
 */
template< typename T >
struct ConstructibleTypeSwitchAux
{
};

template<>
struct ConstructibleTypeSwitchAux<bool>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::INT8, sp2::Sp2Type::Type::UINT8, sp2::Sp2Type::Type::INT16,
            sp2::Sp2Type::Type::UINT16, sp2::Sp2Type::Type::INT32, sp2::Sp2Type::Type::UINT32, sp2::Sp2Type::Type::INT64,
            sp2::Sp2Type::Type::UINT64, sp2::Sp2Type::Type::DOUBLE>;
};

template<>
struct ConstructibleTypeSwitchAux<std::int8_t>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::INT8, sp2::Sp2Type::Type::INT16,
            sp2::Sp2Type::Type::INT32, sp2::Sp2Type::Type::INT64, sp2::Sp2Type::Type::DOUBLE>;
};

template<>
struct ConstructibleTypeSwitchAux<std::uint8_t>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::UINT8, sp2::Sp2Type::Type::INT16,
            sp2::Sp2Type::Type::UINT16, sp2::Sp2Type::Type::INT32, sp2::Sp2Type::Type::UINT32, sp2::Sp2Type::Type::INT64,
            sp2::Sp2Type::Type::UINT64, sp2::Sp2Type::Type::DOUBLE>;
};

template<>
struct ConstructibleTypeSwitchAux<std::int16_t>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::INT16,
            sp2::Sp2Type::Type::INT32, sp2::Sp2Type::Type::INT64, sp2::Sp2Type::Type::DOUBLE>;
};

template<>
struct ConstructibleTypeSwitchAux<std::uint16_t>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL,
            sp2::Sp2Type::Type::UINT16, sp2::Sp2Type::Type::INT32, sp2::Sp2Type::Type::UINT32, sp2::Sp2Type::Type::INT64,
            sp2::Sp2Type::Type::UINT64, sp2::Sp2Type::Type::DOUBLE>;
};
template<>
struct ConstructibleTypeSwitchAux<std::int32_t>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::INT32, sp2::Sp2Type::Type::INT64, sp2::Sp2Type::Type::DOUBLE>;
};

template<>
struct ConstructibleTypeSwitchAux<std::uint32_t>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::UINT32, sp2::Sp2Type::Type::INT64,
            sp2::Sp2Type::Type::UINT64, sp2::Sp2Type::Type::DOUBLE>;
};
template<>
struct ConstructibleTypeSwitchAux<std::int64_t>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::INT64, sp2::Sp2Type::Type::DOUBLE>;
};

template<>
struct ConstructibleTypeSwitchAux<std::uint64_t>
{
    // Note we allow INT64 but it should be range checked
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::UINT64, sp2::Sp2Type::Type::INT64, sp2::Sp2Type::Type::DOUBLE>;
};

template<>
struct ConstructibleTypeSwitchAux<std::double_t>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL, sp2::Sp2Type::Type::DOUBLE>;
};

template<>
struct ConstructibleTypeSwitchAux<sp2::DateTime>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::DATETIME>;
};

template<>
struct ConstructibleTypeSwitchAux<sp2::TimeDelta>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::TIMEDELTA>;
};

template<>
struct ConstructibleTypeSwitchAux<sp2::Date>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::DATE>;
};

template<>
struct ConstructibleTypeSwitchAux<sp2::Time>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::TIME>;
};

template<>
struct ConstructibleTypeSwitchAux<sp2::Sp2Enum>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::ENUM>;
};

template<>
struct ConstructibleTypeSwitchAux<std::string>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::STRING>;
};

template< typename T >
struct ConstructibleTypeSwitchAux<std::vector<T>>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::ARRAY>;
};

#ifdef __clang__
template<>
struct ConstructibleTypeSwitchAux<boost::container::vector<bool>>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::ARRAY>;
};
#endif

template<>
struct ConstructibleTypeSwitchAux<StructPtr>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::STRUCT>;
};

template<>
struct ConstructibleTypeSwitchAux<const StructPtr>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::STRUCT>;
};

template<>
struct ConstructibleTypeSwitchAux<DialectGenericType>
{
    using type = PartialSwitchSp2Type<sp2::Sp2Type::Type::DIALECT_GENERIC>;
};


template< typename T >
using ConstructibleTypeSwitch = typename ConstructibleTypeSwitchAux<T>::type;

template< typename ArraySubTypeSwitchT=ArraySubTypeSwitch, typename F=void >
inline auto switchSp2Type( const Sp2Type *type, F &&f )
{
    return AllSp2TypeSwitch::invoke(type, std::forward<F>(f));
}

template< typename ArraySubTypeSwitchT=ArraySubTypeSwitch, typename F=void >
inline auto switchSp2Type( const Sp2TypePtr& type, F &&f )
{
    return AllSp2TypeSwitch::invoke(type, std::forward<F>(f));
}

}
#endif
