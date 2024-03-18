#include <sp2/engine/Dictionary.h>
#include <sp2/engine/CppNode.h>
#include <numeric>

namespace sp2::cppnodes
{

/*
def sample(trigger: ts['Y'], x: ts['T']):
    __outputs__(ts['T'])
    '''will return current value of x on trigger ticks'''
*/
DECLARE_CPPNODE( sample )
{
    INIT_CPPNODE( sample )
    {}

    TS_INPUT( Generic, trigger );
    TS_INPUT( Generic, x );

    TS_OUTPUT( Generic );

    START()
    {
        sp2.make_passive( x );
    }

    INVOKE()
    {
        if( sp2.ticked( trigger ) && sp2.valid( x ) )
            RETURN( x );
    }
};

EXPORT_CPPNODE( sample );

/*
@sp2.node(cppimpl=_sp2baselibimpl.firstN)
def firstN(x: ts['T'], N: int):
    __outputs__(ts['T'])
*/

DECLARE_CPPNODE( firstN )
{
    INIT_CPPNODE( firstN )
    {
    }

    TS_INPUT(     Generic, x );
    SCALAR_INPUT( int64_t, N );

    TS_OUTPUT( Generic );

    STATE_VAR( int, s_count{0} );

    START()
    {
        if( N <= 0 )
            sp2.make_passive( x );
    }

    INVOKE()
    {
        if( ++s_count == N )
            sp2.make_passive( x );
        RETURN( x );
    }
};

EXPORT_CPPNODE( firstN );

/*
@sp2.node(cppimpl=_sp2baselibimpl.count)
def count(x: ts['T']):
    __outputs__(ts[int])
    ''' return count of ticks of input '''
*/
DECLARE_CPPNODE( count )
{
    INIT_CPPNODE( count )
    {}

    TS_INPUT( Generic, x );
    TS_OUTPUT( int64_t );

    INVOKE()
    {
        RETURN( sp2.count( x ) );
    }
};

EXPORT_CPPNODE( count );

/*
@sp2.node(cppimpl=_sp2baselibimpl._delay_by_timedelta)
def _delay_by_timedelta(x: ts['T'], delay: timedelta):
    ''' delay input ticks by given delay '''
    __outputs__(ts['T'])
*/
DECLARE_CPPNODE( _delay_by_timedelta )
{
    INIT_CPPNODE( _delay_by_timedelta )
    {}

    TS_INPUT( Generic, x );
    SCALAR_INPUT( TimeDelta, delay );

    TS_OUTPUT( Generic );
    ALARM( Generic, alarm );

    INVOKE()
    {
        if( sp2.ticked( x ) )
            sp2.schedule_alarm( alarm, delay, x );

        if( sp2.ticked( alarm ) )
            RETURN( alarm );
    }
};

EXPORT_CPPNODE( _delay_by_timedelta );

/*
@sp2.node
def _delay_by_ticks(x: ts['T'], delay: int):
    __outputs__(ts['T'])
*/
DECLARE_CPPNODE( _delay_by_ticks )
{
    TS_INPUT( Generic, x );
    SCALAR_INPUT( int64_t, delay );

    TS_OUTPUT( Generic );

    INIT_CPPNODE( _delay_by_ticks )
    {}

    START()
    {
        if( delay <= 0 )
            SP2_THROW( ValueError, "delay/lag must be > 0, received " << delay );

        x.setTickCountPolicy( delay + 1 );
    }

    INVOKE()
    {
        if( sp2.ticked( x ) && sp2.count( x ) > delay )
        {
            switchSp2Type( x.type(), [this]( auto tag )
            {
                using ElemT = typename decltype(tag)::type;
                RETURN( x.valueAtIndex<ElemT>( delay ) );
            } );
        }
    }
};

EXPORT_CPPNODE( _delay_by_ticks );

/*
@sp2.node
def merge(x: ts['T'], y : ts[ 'T' ] ):
    ''' merge two timeseries into one.  If both tick at the same time, left side wins'''
    __outputs__(ts['T'])
*/
DECLARE_CPPNODE( merge )
{
    INIT_CPPNODE( merge )
    {}

    TS_INPUT( Generic, x );
    TS_INPUT( Generic, y );

    TS_OUTPUT( Generic );

    INVOKE()
    {
        if( sp2.ticked( x ) )
            RETURN( x );

        RETURN( y );
    }
};

EXPORT_CPPNODE( merge );


/*
@sp2.node(cppimpl=_sp2baselibimpl.split)
def split(flag: ts[bool], x: ts['T']):
    __outputs__(false=ts['T'], true=ts['T'])
    ''' based on flag tick input on true/false __outputs__ '''
*/
DECLARE_CPPNODE( split )
{
    INIT_CPPNODE( split )
    {}

    TS_INPUT( bool,    flag );
    TS_INPUT( Generic, x );
    TS_NAMED_OUTPUT_RENAMED( Generic, false, false_ );
    TS_NAMED_OUTPUT_RENAMED( Generic, true,  true_ );

    START()
    {
        sp2.make_passive( flag );
    }

    INVOKE()
    {
        if( sp2.ticked( x ) && sp2.valid( flag ) )
        {
            if( flag )
                true_.output( x );
            else
                false_.output( x );
        }
    }
};

EXPORT_CPPNODE( split );

/*
@sp2.node
def cast_int_to_float(x: sp2.ts[int]):
    __outputs__(sp2.ts[float])
*/
DECLARE_CPPNODE( cast_int_to_float )
{
    INIT_CPPNODE( cast_int_to_float )
    {}

    TS_INPUT( int64_t, x );
    TS_OUTPUT( double );

    INVOKE()
    {
        if( sp2.ticked( x ) )
            RETURN( x );
    }
};

EXPORT_CPPNODE( cast_int_to_float );

/*
@sp2.node
def filter(flag: ts[bool], x: ts['T']):
    __outputs__(ts['T'])
*/
DECLARE_CPPNODE( filter )
{
    INIT_CPPNODE( filter )
    {}

    TS_INPUT( bool,    flag );
    TS_INPUT( Generic, x );
    TS_OUTPUT( Generic );

    START()
    {
        sp2.make_passive( flag );
    }

    INVOKE()
    {
        if( sp2.valid( flag ) && flag )
            RETURN( x );
    }
};

EXPORT_CPPNODE( filter )

/*
@sp2.node
def _drop_dups_float(x: ts[float], eps: float):
    __outputs__(ts[float])
*/
DECLARE_CPPNODE( _drop_dups_float )
{
    INIT_CPPNODE( _drop_dups_float )
    {}

    TS_INPUT( double, x );

    SCALAR_INPUT( double, eps );

    TS_OUTPUT( double );

    STATE_VAR( bool, s_first{true} );
    STATE_VAR( double, s_prev{} );

    INVOKE()
    {
        if( sp2.ticked( x ) )
        {
            if( s_first || ( isnan( x ) != isnan( s_prev ) ) || ( !isnan( x ) && fabs( x - s_prev ) >= eps ))
            {
                s_first = false;
                s_prev = x;
                RETURN( x );
            }
        }
    }
};

EXPORT_CPPNODE( _drop_dups_float )

/*
@sp2.node
def drop_nans(x: ts[float]):
    '''removes any nan values from the input series'''
    __outputs__(ts[float])
*/
DECLARE_CPPNODE( drop_nans )
{
    TS_INPUT( double, x );
    TS_OUTPUT( double );

    INIT_CPPNODE( drop_nans ) {}

    INVOKE()
    {
        if( likely( !isnan( x ) ) )
            RETURN( x );
    }
};

EXPORT_CPPNODE( drop_nans );

/*
@sp2.node
def unroll(x: ts[['T']]):
    __outputs__(ts['T'])
    ''' "unrolls" timeseries of lists of type 'T' into individual ticks of type 'T' '''
*/
DECLARE_CPPNODE( unroll )
{
    TS_INPUT(  Generic,  x );
    ALARM(     Generic,  alarm );
    STATE_VAR( uint32_t, s_pending{0} );

    TS_OUTPUT( Generic );

    Sp2TypePtr elemType;

    INIT_CPPNODE( unroll )
    {
        //we need to access type information using the input / outout defs because the actual
        //ts() instances arent created at this point
        auto & x_def = tsinputDef( "x" );
        if( x_def.type -> type() != Sp2Type::Type::ARRAY )
            SP2_THROW( TypeError, "unroll expected ts array type, got " << x_def.type -> type() );

        auto * aType = static_cast<const Sp2ArrayType *>( x_def.type.get() );
        elemType = aType -> elemType();

        //we cant easily support unrolling list of typed lists ( ts[ [[int]] ] ).  Since we dont recurse type info more than one level
        //the input elemType would be DIALECT_GENERIC, but the output type would be the correct ARRAY:Type type.  Briding the two here is
        //complex and not (currently) wirht the effort, so fallback to python by throwing NotImplemented
        auto & out_def = tsoutputDef( "" );
        if( out_def.type -> type() == Sp2Type::Type::ARRAY )
            SP2_THROW( NotImplemented, "unroll cppimpl doesnt currently support unrolloing lists of typed lists" );
    }

    INVOKE()
    {
        //single switch up front, no need to do it multiple times
        switchSp2Type( elemType, [this]( auto tag )
        {
            using ElemT  = typename decltype(tag)::type;
            using ArrayT = typename Sp2Type::Type::toCType<Sp2Type::Type::ARRAY,ElemT>::type;

            if( sp2.ticked( x ) )
            {
                auto & v = x.lastValue<ArrayT>();
                size_t sz = v.size();
                if( likely( sz > 0 ) )
                {
                    size_t idx = 0;
                    if( !s_pending )
                        SP2_OUTPUT( v[idx++] );

                    s_pending += sz - idx;
                    for( ; idx < sz; ++idx )
                        sp2.schedule_alarm( alarm, TimeDelta::ZERO(), v[idx] );
                }
            }

            if( sp2.ticked( alarm ) )
            {
                --s_pending;
                RETURN( alarm.lastValue<ElemT>() );
            }

        } );
    }
};

EXPORT_CPPNODE( unroll )

/*
@sp2.node
def collect(x: [ts['T']]):
    __outputs__(ts[['T']])
    ''' convert basket of timeseries into timeseries of list of ticked values '''
*/
DECLARE_CPPNODE( collect )
{
    TS_LISTBASKET_INPUT( Generic, x );
    TS_OUTPUT( Generic );

    Sp2TypePtr elemType;

    INIT_CPPNODE( collect )
    {
        //we cant process 'T' of type typed list ( it [int] ) because the input type would be ARRAY:INT64
        //but the output type would become ARRAY:DIALECT_GENERIC, which we cant create.  just fallback to python
        auto & x_def = tsinputDef( "x" );
        if( x_def.type -> type() == Sp2Type::Type::ARRAY )
            SP2_THROW( NotImplemented, "cppimpl of collect cannot handle typed lists inputs" );

        auto & out_def = tsoutputDef( "" );
        if( out_def.type -> type() != Sp2Type::Type::ARRAY )
            SP2_THROW( TypeError, "cppimpl for collect expected output type to be list, got " << out_def.type -> type() );

        auto * aType = static_cast<const Sp2ArrayType *>( out_def.type.get() );
        elemType = aType -> elemType();

        if( elemType -> type() != x_def.type -> type() )
            SP2_THROW( TypeError, "cppimpl for collect has unexpected type mistmatch, input type is " << x_def.type -> type () <<
                       " but output array type is " << elemType -> type() );
    }

    START()
    {
        //to avoid the need to check in every invoke
        if( x.size() == 0 )
            sp2.make_passive( x );
    }

    INVOKE()
    {
        //single switch up front, no need to do it multiple times
        //we expect all elements to be of the same type
        switchSp2Type( elemType, [this]( auto tag )
                       {
                           using ElemT  = typename decltype(tag)::type;
                           using ArrayT = typename Sp2Type::Type::toCType<Sp2Type::Type::ARRAY,ElemT>::type;

                           ArrayT & out = unnamed_output().reserveSpace<ArrayT>();
                           out.clear();
                           for( auto it = x.tickedinputs(); it; ++it )
                               out.emplace_back( it -> lastValueTyped<ElemT>() );
                       } );
    }
};

EXPORT_CPPNODE( collect );

/*
@sp2.node
def demultiplex( x:ts['T'], key:ts['K'], keys : ['K'], raise_on_bad_key : bool = False):
    __outputs__( { 'K' : ts['T']}.with_shape(keys) )
*/
DECLARE_CPPNODE( demultiplex )
{
    TS_INPUT( Generic, x );
    TS_INPUT( Generic, key );
    SCALAR_INPUT( bool, raise_on_bad_key );

    TS_DICTBASKET_OUTPUT( Generic )

    INIT_CPPNODE( demultiplex )
    {
        auto & key_def = tsinputDef( "key" );
        if( key_def.type -> type() != Sp2Type::Type::STRING )
            SP2_THROW( NotImplemented, "cppimpl for demultiplex not supported on non-string key types" );
    }

    START()
    {
        sp2.make_passive( key );
    }

    INVOKE()
    {
        if( sp2.valid( key ) )
        {
            auto &key_str = key.lastValue<std::string>();
            auto elemId = unnamed_output().elemId( key_str );
            if( elemId != InputId::ELEM_ID_NONE )
            {
                unnamed_output()[elemId].output( x );
            }
            else if( raise_on_bad_key )
                SP2_THROW( ValueError, "key " << key_str << " not in keys" );
        }
    }
};

EXPORT_CPPNODE( demultiplex )

/*
@sp2.node
def multiplex(x: {'K': ts['T']}, key: ts['K'], tick_on_index: bool = False, raise_on_bad_key: bool = False):
    __outputs__(ts['T'])
*/
DECLARE_CPPNODE( multiplex )
{
    TS_DICTBASKET_INPUT( Generic, x );
    TS_INPUT( Generic, key );

    SCALAR_INPUT( bool, tick_on_index );
    SCALAR_INPUT( bool, raise_on_bad_key );

    TS_OUTPUT( Generic );

    STATE_VAR( bool, s_key_valid{false} );

    INIT_CPPNODE( multiplex )
    {
        auto & key_def = tsinputDef( "key" );
        if( key_def.type -> type() != Sp2Type::Type::STRING )
            SP2_THROW( NotImplemented, "cppimpl for multiplex not supported on non-string key types" );
    }

    INVOKE()
    {
        if( sp2.ticked( key ) )
        {
            auto &key_str = key.lastValue<std::string>();

            sp2.make_passive( x );
            int64_t elemId = x.elemId( key_str );
            if( elemId != InputId::ELEM_ID_NONE )
            {
                sp2.make_active( x[elemId] );
                s_key_valid = true;
            }
            else
            {
                if( raise_on_bad_key )
                    SP2_THROW( ValueError, "key " << key_str << " not in input basket" );
                s_key_valid = false;
            }
        }

        if( s_key_valid )
        {
            auto &key_str = key.lastValue<std::string>();
            int64_t elemId = x.elemId( key_str );
            if( sp2.ticked( x[elemId] ) ||
                ( tick_on_index && sp2.ticked(key) && sp2.valid(x[elemId]) ) )
            {
                SP2_OUTPUT( x[elemId] );
            }
        }
    }
};

EXPORT_CPPNODE( multiplex );

/*
@sp2.node(cppimpl=_sp2baselibimpl.times)
def times(x: ts[object]):
    """
    Returns a time-series of datetimes at which x ticks
    """
    __outputs__(ts[datetime])
*/

DECLARE_CPPNODE( times )
{
    TS_INPUT( Generic, x );
    TS_OUTPUT( DateTime );

    INIT_CPPNODE( times ) { }

    INVOKE()
    {
        RETURN( now() );
    }
};

EXPORT_CPPNODE( times );

/*
@sp2.node(cppimpl=_sp2baselibimpl.times_ns)
def times_ns(x: ts[object])
    """
    Returns a time-series of ints representing the epoch time (in nanoseconds) at which x ticks
    """
    __outputs__(ts[int])
*/

DECLARE_CPPNODE( times_ns )
{
    TS_INPUT( Generic, x );
    TS_OUTPUT( int64_t );

    INIT_CPPNODE( times_ns ) { }

    INVOKE()
    {
        RETURN( now().asNanoseconds() );
    }
};

EXPORT_CPPNODE( times_ns );

/*
@sp2.node
def struct_field(x: ts['T'], field: str, fieldType: 'Y'):
    __outputs__(ts['Y'])
*/
DECLARE_CPPNODE( struct_field )
{
    INIT_CPPNODE( struct_field )
    {}

    TS_INPUT(     StructPtr, x );
    SCALAR_INPUT( std::string, field );

    TS_OUTPUT( Generic );

    START()
    {
        auto * structType = static_cast<const Sp2StructType *>( x.type() );
        m_fieldAccess = structType -> meta() -> field( field );
        if( !m_fieldAccess )
            SP2_THROW( TypeError, "Struct " << structType -> meta() -> name() << " has no field named " << field.value() );
    }

    INVOKE()
    {
        if( m_fieldAccess -> isSet( x.lastValue().get() ) )
        {
            switchSp2Type( m_fieldAccess -> type(), [this]( auto tag )
                           {
                               using T = typename decltype(tag)::type;
                               RETURN( m_fieldAccess -> value<T>( x.lastValue().get() ) );
                           } );
        }
    }

private:
    StructFieldPtr m_fieldAccess;
};

EXPORT_CPPNODE( struct_field );

//fromts and collectts are unfortunately identical except for tickeditems() vs validitems()
//but i dont think its enough to warrant any refactoring at the moment
/*
@sp2.node
def struct_fromts(cls: 'T', inputs: {str: ts[object]}):
    __outputs__(ts['T'])
*/
DECLARE_CPPNODE( struct_fromts )
{
    TS_DICTBASKET_INPUT( Generic, inputs );
    TS_INPUT( Generic,            trigger );
    SCALAR_INPUT( StructMetaPtr,  cls );
    SCALAR_INPUT( bool,           use_trigger );

    TS_OUTPUT( StructPtr );

    INIT_CPPNODE( struct_fromts )
    {
    }

    START()
    {
        for( size_t elemId = 0; elemId < inputs.shape().size(); ++elemId )
        {
            auto & key = inputs.shape()[ elemId ];
            auto & structField = cls.value() -> field( key );
            if( !structField )
                SP2_THROW( ValueError, cls.value() -> name() << ".fromts() received unknown struct field \"" << key << "\"" );

            if( structField -> type() -> type() != inputs[ elemId ].type() -> type() )
                SP2_THROW( TypeError, cls.value()  -> name() << ".fromts() field \"" << key << "\" expected ts type "
                           << structField -> type() -> type() << " but got " << inputs[ elemId ].type() -> type() );

            m_structFields.push_back( structField.get() );
        }

        if( use_trigger )
            sp2.make_passive( inputs );
    }

    INVOKE()
    {
        auto out = cls.value()  -> create();
        for( auto it = inputs.validinputs(); it; ++it )
        {
            auto * fieldAccess = m_structFields[it.elemId()];
            switchSp2Type( it -> type(), [&it,&out,fieldAccess]( auto tag )
                           {
                               using ElemT  = typename decltype(tag)::type;
                               fieldAccess -> setValue( out.get(), it -> lastValueTyped<ElemT>() );
                           }
                );
        }

        SP2_OUTPUT( std::move( out ) );
    }

    std::vector<StructField *> m_structFields;
};

EXPORT_CPPNODE( struct_fromts );

/*
@sp2.node
def struct_collectts(cls: 'T', inputs: {str: ts[object]}):
    __outputs__(ts['T'])
*/
DECLARE_CPPNODE( struct_collectts )
{
    TS_DICTBASKET_INPUT( Generic, inputs );
    SCALAR_INPUT( StructMetaPtr, cls );
    TS_OUTPUT( StructPtr );

    INIT_CPPNODE( struct_collectts )
    {
    }

    START()
    {
        for( size_t elemId = 0; elemId < inputs.shape().size(); ++elemId )
        {
            auto & key = inputs.shape()[ elemId ];
            auto & structField = cls.value() -> field( key );
            if( !structField )
                SP2_THROW( ValueError, cls.value() -> name() << ".collectts() received unknown struct field \"" << key << "\"" );

            if( structField -> type() -> type() != inputs[ elemId ].type() -> type() )
                SP2_THROW( TypeError, cls.value()  -> name() << ".collectts() field \"" << key << "\" expected ts type "
                           << structField -> type() -> type() << " but got " << inputs[ elemId ].type() -> type() );

            m_structFields.push_back( structField.get() );
        }
    }

    INVOKE()
    {
        auto out = cls.value()  -> create();
        for( auto it = inputs.tickedinputs(); it; ++it )
        {
            auto * fieldAccess = m_structFields[it.elemId()];
            switchSp2Type( it -> type(), [&it,&out,fieldAccess]( auto tag )
                           {
                               using ElemT  = typename decltype(tag)::type;
                               fieldAccess -> setValue( out.get(), it -> lastValueTyped<ElemT>() );
                           }
                );
        }

        SP2_OUTPUT( std::move( out ) );
    }

    std::vector<StructField *> m_structFields;
};

EXPORT_CPPNODE( struct_collectts );

}
