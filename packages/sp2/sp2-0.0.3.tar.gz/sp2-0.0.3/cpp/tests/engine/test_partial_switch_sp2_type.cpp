#include <sp2/core/Exception.h>
#include <sp2/engine/PartialSwitchSp2Type.h>
#include <sp2/engine/TypeCast.h>
#include <gtest/gtest.h>
#include <iostream>

#ifdef __clang__
#include <boost/container/vector.hpp>
#endif

template< typename T, typename B >
auto getConverter( std::shared_ptr<const sp2::Sp2Type> curType )
{
    return sp2::ConstructibleTypeSwitch<T>::invoke( curType . get(), []( auto tag )
    {
        return std::function( []( T val ) { return B(( typename decltype(tag)::type ) ( val )); } );
    } );
}

template< sp2::Sp2Type::TypeTraits::_enum v, typename B=long long, typename T=typename sp2::Sp2Type::Type::toCType<v>::type >
void runTypeConversionSupportTest( std::set<sp2::Sp2Type::Type> supportedTypes,
                                   std::set<sp2::Sp2Type::Type> unsupportedTypes )
{
    ASSERT_EQ( supportedTypes . size() + unsupportedTypes . size(), 10 );
    for( auto t:supportedTypes )
    {
        try
        {
            auto converter = getConverter<T, B>( std::make_shared<const sp2::Sp2Type>( t ));
            if( t != sp2::Sp2Type::Type::BOOL )
            {
                const bool specialIntCase = ( v == sp2::Sp2Type::Type::UINT64 ) && ( t == sp2::Sp2Type::Type::INT64 );
                if( !specialIntCase )
                {
                    ASSERT_EQ( B( std::numeric_limits<T>::max()), converter( std::numeric_limits<T>::max()));
                }
                ASSERT_EQ( std::numeric_limits<T>::min(), converter( std::numeric_limits<T>::min()));
            }
            else
            {
                ASSERT_EQ( std::numeric_limits<T>::max() != 0, converter( std::numeric_limits<T>::max()));
                ASSERT_EQ( std::numeric_limits<T>::min() != 0, converter( std::numeric_limits<T>::min()));
            }
        }
        catch( const sp2::UnsupportedSwitchType &e )
        {
            throw;
        }
    }
    for( auto t:unsupportedTypes )
    {
        ASSERT_THROW(( getConverter<T, B>( std::make_shared<const sp2::Sp2Type>( t ))), sp2::UnsupportedSwitchType );
    }
}


TEST( ConstructibleTypeSelectorTest, test_basic_type_support )
{
    runTypeConversionSupportTest<sp2::Sp2Type::Type::BOOL>( {
                                                                    sp2::Sp2Type::Type::BOOL,
                                                                    sp2::Sp2Type::Type::INT8,
                                                                    sp2::Sp2Type::Type::UINT8,
                                                                    sp2::Sp2Type::Type::INT16,
                                                                    sp2::Sp2Type::Type::UINT16,
                                                                    sp2::Sp2Type::Type::INT32,
                                                                    sp2::Sp2Type::Type::UINT32,
                                                                    sp2::Sp2Type::Type::INT64,
                                                                    sp2::Sp2Type::Type::UINT64,
                                                                    sp2::Sp2Type::Type::DOUBLE,
                                                            },
                                                            {} );

    runTypeConversionSupportTest<sp2::Sp2Type::Type::INT8>( {
                                                                    sp2::Sp2Type::Type::BOOL,
                                                                    sp2::Sp2Type::Type::INT8,
                                                                    sp2::Sp2Type::Type::INT16,
                                                                    sp2::Sp2Type::Type::INT32,
                                                                    sp2::Sp2Type::Type::INT64,
                                                                    sp2::Sp2Type::Type::DOUBLE },
                                                            { sp2::Sp2Type::Type::UINT8,
                                                              sp2::Sp2Type::Type::UINT16,
                                                              sp2::Sp2Type::Type::UINT32,
                                                              sp2::Sp2Type::Type::UINT64,
                                                            } );

    runTypeConversionSupportTest<sp2::Sp2Type::Type::UINT8>( {
                                                                     sp2::Sp2Type::Type::BOOL,
                                                                     sp2::Sp2Type::Type::UINT8,
                                                                     sp2::Sp2Type::Type::INT16,
                                                                     sp2::Sp2Type::Type::UINT16,
                                                                     sp2::Sp2Type::Type::INT32,
                                                                     sp2::Sp2Type::Type::UINT32,
                                                                     sp2::Sp2Type::Type::INT64,
                                                                     sp2::Sp2Type::Type::UINT64,
                                                                     sp2::Sp2Type::Type::DOUBLE },
                                                             {
                                                                     sp2::Sp2Type::Type::INT8
                                                             } );

    runTypeConversionSupportTest<sp2::Sp2Type::Type::INT16>( {
                                                                     sp2::Sp2Type::Type::BOOL,
                                                                     sp2::Sp2Type::Type::INT16,
                                                                     sp2::Sp2Type::Type::INT32,
                                                                     sp2::Sp2Type::Type::INT64,
                                                                     sp2::Sp2Type::Type::DOUBLE },
                                                             { sp2::Sp2Type::Type::UINT8,
                                                               sp2::Sp2Type::Type::INT8,
                                                               sp2::Sp2Type::Type::UINT16,
                                                               sp2::Sp2Type::Type::UINT32,
                                                               sp2::Sp2Type::Type::UINT64
                                                             } );

    runTypeConversionSupportTest<sp2::Sp2Type::Type::UINT16>( {
                                                                      sp2::Sp2Type::Type::BOOL,
                                                                      sp2::Sp2Type::Type::UINT16,
                                                                      sp2::Sp2Type::Type::INT32,
                                                                      sp2::Sp2Type::Type::UINT32,
                                                                      sp2::Sp2Type::Type::INT64,
                                                                      sp2::Sp2Type::Type::UINT64,
                                                                      sp2::Sp2Type::Type::DOUBLE },
                                                              {
                                                                      sp2::Sp2Type::Type::INT8,
                                                                      sp2::Sp2Type::Type::UINT8,
                                                                      sp2::Sp2Type::Type::INT16
                                                              } );

    runTypeConversionSupportTest<sp2::Sp2Type::Type::INT32>( {
                                                                     sp2::Sp2Type::Type::BOOL,
                                                                     sp2::Sp2Type::Type::INT32,
                                                                     sp2::Sp2Type::Type::INT64,
                                                                     sp2::Sp2Type::Type::DOUBLE },
                                                             { sp2::Sp2Type::Type::UINT8,
                                                               sp2::Sp2Type::Type::INT8,
                                                               sp2::Sp2Type::Type::INT16,
                                                               sp2::Sp2Type::Type::UINT16,
                                                               sp2::Sp2Type::Type::UINT32,
                                                               sp2::Sp2Type::Type::UINT64
                                                             } );

    runTypeConversionSupportTest<sp2::Sp2Type::Type::UINT32>( {
                                                                      sp2::Sp2Type::Type::BOOL,
                                                                      sp2::Sp2Type::Type::UINT32,
                                                                      sp2::Sp2Type::Type::INT64,
                                                                      sp2::Sp2Type::Type::UINT64,
                                                                      sp2::Sp2Type::Type::DOUBLE },
                                                              {
                                                                      sp2::Sp2Type::Type::INT8,
                                                                      sp2::Sp2Type::Type::UINT8,
                                                                      sp2::Sp2Type::Type::INT16,
                                                                      sp2::Sp2Type::Type::UINT16,
                                                                      sp2::Sp2Type::Type::INT32,
                                                              } );

    runTypeConversionSupportTest<sp2::Sp2Type::Type::INT64, double>( {
                                                                             sp2::Sp2Type::Type::BOOL,
                                                                             sp2::Sp2Type::Type::INT64,
                                                                             sp2::Sp2Type::Type::DOUBLE },
                                                                     { sp2::Sp2Type::Type::UINT8,
                                                                       sp2::Sp2Type::Type::INT8,
                                                                       sp2::Sp2Type::Type::INT16,
                                                                       sp2::Sp2Type::Type::UINT16,
                                                                       sp2::Sp2Type::Type::INT32,
                                                                       sp2::Sp2Type::Type::UINT32,
                                                                       sp2::Sp2Type::Type::UINT64
                                                                     } );

    runTypeConversionSupportTest<sp2::Sp2Type::Type::UINT64, double>( {
                                                                              sp2::Sp2Type::Type::BOOL,
                                                                              sp2::Sp2Type::Type::UINT64,
                                                                              sp2::Sp2Type::Type::INT64,
                                                                              sp2::Sp2Type::Type::DOUBLE },
                                                                      {
                                                                              sp2::Sp2Type::Type::INT8,
                                                                              sp2::Sp2Type::Type::UINT8,
                                                                              sp2::Sp2Type::Type::INT16,
                                                                              sp2::Sp2Type::Type::UINT16,
                                                                              sp2::Sp2Type::Type::INT32,
                                                                              sp2::Sp2Type::Type::UINT32,

                                                                      } );
    std::uint64_t aux = std::numeric_limits<const std::uint64_t>::max();
    ASSERT_THROW( sp2::cast<int64_t>( std::numeric_limits<std::uint64_t>::max()), sp2::RangeError );
    ASSERT_THROW( sp2::cast<const int64_t>( std::numeric_limits<std::uint64_t>::max()), sp2::RangeError );
    ASSERT_THROW( sp2::cast<int64_t>( aux ), sp2::RangeError );
    ASSERT_THROW( sp2::cast<const int64_t>( aux ), sp2::RangeError );

    runTypeConversionSupportTest<sp2::Sp2Type::Type::DOUBLE, double>( {
                                                                              sp2::Sp2Type::Type::BOOL,
                                                                              sp2::Sp2Type::Type::DOUBLE },
                                                                      {
                                                                              sp2::Sp2Type::Type::INT8,
                                                                              sp2::Sp2Type::Type::UINT8,
                                                                              sp2::Sp2Type::Type::INT16,
                                                                              sp2::Sp2Type::Type::UINT16,
                                                                              sp2::Sp2Type::Type::INT32,
                                                                              sp2::Sp2Type::Type::UINT32,
                                                                              sp2::Sp2Type::Type::INT64,
                                                                              sp2::Sp2Type::Type::UINT64,
                                                                      } );
}


template< typename T1, typename T2 >
void verifySameTypes()
{
    if( !std::is_same_v<T1, T2> )
    {
        static_assert( !std::is_same_v<T1, std::vector<void>> );
        static_assert( !std::is_same_v<T2, std::vector<void>> );
        SP2_THROW( sp2::RuntimeException, "Types mismatch" << typeid( T1 ).name() << "," << typeid( T2 ).name());
    }
}

TEST( ArraySwitchTest, test_basic_switch )
{
    auto uint64Type      = sp2::Sp2Type::UINT64();
    auto uint64ArrayType = sp2::Sp2ArrayType::create( sp2::Sp2Type::UINT64());
    auto boolArrayType   = sp2::Sp2ArrayType::create( sp2::Sp2Type::BOOL());
    sp2::PrimitiveSp2TypeSwitch::invoke( uint64Type.get(), []( auto tag )
    {
        if( !std::is_same_v<typename decltype(tag)::type, std::uint64_t> )
        {
            SP2_THROW( sp2::RuntimeException, "Dummy error" );
        }
    } );
    // Primitive shouldn't support arrays
    ASSERT_THROW( sp2::PrimitiveSp2TypeSwitch::invoke( uint64ArrayType.get(), []( auto tag ) {} ), sp2::UnsupportedSwitchType );

    // Should work fine
    sp2::PartialSwitchSp2Type<sp2::Sp2Type::Type::INT16, sp2::Sp2Type::Type::ARRAY>::invoke( uint64ArrayType.get(), []( auto tag )
    {
        verifySameTypes<typename decltype(tag)::type, std::vector<std::uint64_t>>();
    } );
    sp2::PartialSwitchSp2Type<sp2::Sp2Type::Type::ARRAY>::invoke( uint64ArrayType.get(), []( auto tag )
    {
        verifySameTypes<typename decltype(tag)::type, std::vector<std::uint64_t>>();
    } );
    sp2::PartialSwitchSp2Type<sp2::Sp2Type::Type::ARRAY>::invoke( boolArrayType.get(), []( auto tag )
    {
#ifdef __clang__
        verifySameTypes<typename decltype(tag)::type, boost::container::vector<bool>>();
#else
        verifySameTypes<typename decltype(tag)::type, std::vector<bool>>();
#endif
    } );

    sp2::PartialSwitchSp2Type<sp2::Sp2Type::Type::ARRAY>::invoke<sp2::PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL>>(
    boolArrayType.get(), []( auto tag )
    { 
#ifdef __clang__
        verifySameTypes<typename decltype(tag)::type, boost::container::vector<bool>>();
#else
        verifySameTypes<typename decltype(tag)::type, std::vector<bool>>();
#endif
    } );
    sp2::PartialSwitchSp2Type<sp2::Sp2Type::Type::ARRAY>::invoke<sp2::PartialSwitchSp2Type<sp2::Sp2Type::Type::UINT64>>(
    uint64ArrayType.get(), []( auto tag )
    { 
        verifySameTypes<typename decltype(tag)::type, std::vector<std::uint64_t>>();
    } );

    // Should raise since we support only array of bool
    ASSERT_THROW( sp2::PartialSwitchSp2Type<sp2::Sp2Type::Type::ARRAY>::invoke<sp2::PartialSwitchSp2Type<sp2::Sp2Type::Type::BOOL>>(
            uint64ArrayType.get(), []( auto tag ) {} ), sp2::UnsupportedSwitchType );

    // Should raise since we support only array of uint64_t
    ASSERT_THROW( sp2::PartialSwitchSp2Type<sp2::Sp2Type::Type::ARRAY>::invoke<sp2::PartialSwitchSp2Type<sp2::Sp2Type::Type::UINT64>>(
            boolArrayType.get(), []( auto tag ) {} ), sp2::UnsupportedSwitchType );
}

