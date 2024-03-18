
#ifndef _IN_SP2_AUTOGEN_SP2_IMPL_TYPES_AUTOGEN_TYPES
#define _IN_SP2_AUTOGEN_SP2_IMPL_TYPES_AUTOGEN_TYPES

#include <sp2/core/Exception.h>
#include <sp2/engine/Struct.h>
#include <cstddef>

namespace sp2::autogen
{

class TimeIndexPolicy : public sp2::Sp2Enum
{
public:
    // Raw value quick access
    enum class enum_
    {
        INCLUSIVE = 1,
        EXCLUSIVE = 2,
        EXTRAPOLATE = 3
    };

    // Sp2Enum types
    static TimeIndexPolicy INCLUSIVE;
    static TimeIndexPolicy EXCLUSIVE;
    static TimeIndexPolicy EXTRAPOLATE;

    const char * asCString() const                { return name().c_str(); }
    const std::string & asString() const          { return name(); }

    static TimeIndexPolicy create( enum_ v )          { return s_meta -> create( ( int64_t ) v ); }
    static TimeIndexPolicy create( const char * name) { return s_meta -> fromString( name ); }
    static TimeIndexPolicy create( const std::string & s ) { return create( s.c_str() ); }

    enum_ enum_value() const { return ( enum_ ) value(); }

    static constexpr uint32_t num_types() { return 3; }

    static bool static_init();

    TimeIndexPolicy( const sp2::Sp2Enum & v ) : sp2::Sp2Enum( v ) { SP2_TRUE_OR_THROW( v.meta() == s_meta.get(), AssertionError, "Mismatched enum meta" ); }

private:

    static std::shared_ptr<sp2::Sp2EnumMeta> s_meta;
};

class DynamicBasketEvent : public sp2::Struct
{
public:

    using Ptr = sp2::TypedStructPtr<DynamicBasketEvent>;

    DynamicBasketEvent()  = delete;
    ~DynamicBasketEvent() = delete;
    DynamicBasketEvent( const DynamicBasketEvent & ) = delete;
    DynamicBasketEvent( DynamicBasketEvent && ) = delete;

    Ptr copy() const { return sp2::structptr_cast<DynamicBasketEvent>( Struct::copy() ); }

    static DynamicBasketEvent::Ptr create()
    {
        return Ptr( static_cast<DynamicBasketEvent *>( s_meta -> createRaw() ) );
    }

    static const sp2::StructMetaPtr & meta() { return s_meta; }


    const sp2::DialectGenericType & key() const
    {
        static_assert( offsetof( DynamicBasketEvent,m_key ) == 0 );
        static_assert( alignof( sp2::DialectGenericType ) == 8 );
        static_assert( sizeof( sp2::DialectGenericType ) == 8 );

        if( !key_isSet() )
            SP2_THROW( sp2::ValueError, "field key on struct DynamicBasketEvent is not set" );

        return m_key;
    }

    void set_key( const sp2::DialectGenericType & value )
    {
        
        static_assert( offsetof( DynamicBasketEvent,m_key ) == 0 );
        static_assert( alignof( sp2::DialectGenericType ) == 8 );
        static_assert( sizeof( sp2::DialectGenericType ) == 8 );

        m_DynamicBasketEvent_mask[0] |= 1;


        //TODO employ move semantics where it makes sense
        m_key = value;
    }

    

    bool key_isSet() const
    {
        static_assert(( offsetof( DynamicBasketEvent,m_DynamicBasketEvent_mask) + 0 ) == 9 );
        return m_DynamicBasketEvent_mask[0] & 1;
    }

    void clear_key()
    {
        static_assert(( offsetof( DynamicBasketEvent,m_DynamicBasketEvent_mask) + 0 ) == 9 );
        m_DynamicBasketEvent_mask[0] &= ~1;
    }

    const bool & added() const
    {
        static_assert( offsetof( DynamicBasketEvent,m_added ) == 8 );
        static_assert( alignof( bool ) == 1 );
        static_assert( sizeof( bool ) == 1 );

        if( !added_isSet() )
            SP2_THROW( sp2::ValueError, "field added on struct DynamicBasketEvent is not set" );

        return m_added;
    }

    void set_added( const bool & value )
    {
        
        static_assert( offsetof( DynamicBasketEvent,m_added ) == 8 );
        static_assert( alignof( bool ) == 1 );
        static_assert( sizeof( bool ) == 1 );

        m_DynamicBasketEvent_mask[0] |= 2;


        //TODO employ move semantics where it makes sense
        m_added = value;
    }

    

    bool added_isSet() const
    {
        static_assert(( offsetof( DynamicBasketEvent,m_DynamicBasketEvent_mask) + 0 ) == 9 );
        return m_DynamicBasketEvent_mask[0] & 2;
    }

    void clear_added()
    {
        static_assert(( offsetof( DynamicBasketEvent,m_DynamicBasketEvent_mask) + 0 ) == 9 );
        m_DynamicBasketEvent_mask[0] &= ~2;
    }


    static bool static_init();

private:

    sp2::DialectGenericType m_key;
    bool m_added;
    char m_DynamicBasketEvent_mask[1];


    static sp2::StructMetaPtr s_meta;

    static void assert_mask()
    {
        static_assert( offsetof( DynamicBasketEvent, m_DynamicBasketEvent_mask ) == 9 );
    }
};

class DynamicBasketEvents : public sp2::Struct
{
public:

    using Ptr = sp2::TypedStructPtr<DynamicBasketEvents>;

    DynamicBasketEvents()  = delete;
    ~DynamicBasketEvents() = delete;
    DynamicBasketEvents( const DynamicBasketEvents & ) = delete;
    DynamicBasketEvents( DynamicBasketEvents && ) = delete;

    Ptr copy() const { return sp2::structptr_cast<DynamicBasketEvents>( Struct::copy() ); }

    static DynamicBasketEvents::Ptr create()
    {
        return Ptr( static_cast<DynamicBasketEvents *>( s_meta -> createRaw() ) );
    }

    static const sp2::StructMetaPtr & meta() { return s_meta; }


    const std::vector<sp2::autogen::DynamicBasketEvent::Ptr> & events() const
    {
        static_assert( offsetof( DynamicBasketEvents,m_events ) == 0 );
        static_assert( alignof( std::vector<sp2::autogen::DynamicBasketEvent::Ptr> ) == 8 );
        static_assert( sizeof( std::vector<sp2::autogen::DynamicBasketEvent::Ptr> ) == 24 );

        if( !events_isSet() )
            SP2_THROW( sp2::ValueError, "field events on struct DynamicBasketEvents is not set" );

        return m_events;
    }

    void set_events( const std::vector<sp2::autogen::DynamicBasketEvent::Ptr> & value )
    {
        
        static_assert( offsetof( DynamicBasketEvents,m_events ) == 0 );
        static_assert( alignof( std::vector<sp2::autogen::DynamicBasketEvent::Ptr> ) == 8 );
        static_assert( sizeof( std::vector<sp2::autogen::DynamicBasketEvent::Ptr> ) == 24 );

        m_DynamicBasketEvents_mask[0] |= 1;


        //TODO employ move semantics where it makes sense
        m_events = value;
    }

    

    bool events_isSet() const
    {
        static_assert(( offsetof( DynamicBasketEvents,m_DynamicBasketEvents_mask) + 0 ) == 24 );
        return m_DynamicBasketEvents_mask[0] & 1;
    }

    void clear_events()
    {
        static_assert(( offsetof( DynamicBasketEvents,m_DynamicBasketEvents_mask) + 0 ) == 24 );
        m_DynamicBasketEvents_mask[0] &= ~1;
    }


    static bool static_init();

private:

    std::vector<sp2::autogen::DynamicBasketEvent::Ptr> m_events;
    char m_DynamicBasketEvents_mask[1];


    static sp2::StructMetaPtr s_meta;

    static void assert_mask()
    {
        static_assert( offsetof( DynamicBasketEvents, m_DynamicBasketEvents_mask ) == 24 );
    }
};

}
#endif