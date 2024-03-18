#include <sp2/engine/Engine.h>
#include <sp2/engine/InputAdapter.h>
#include <sp2/engine/Node.h>
#include <sp2/engine/PartialSwitchSp2Type.h>

namespace sp2
{

Node::Node( NodeDef def,
            Engine * engine ) : Consumer ( engine ),
                                m_outputs( nullptr ),
                                m_def ( def )
{
    m_inputs = new TimeSeriesInputBasketInfo[ m_def.numInputs ];

    if( m_def.numOutputs > 0 )
        m_outputs = new TimeSeriesOutputBasketInfo[ m_def.numOutputs ];
}

Node::~Node()
{
    for( int i = 0; i < m_def.numInputs; ++i )
    {
        if( m_inputs[ i ].isSet<InputBasketInfo>() )
        {
            //account for non-virtual dynamic basket
            auto * basket = m_inputs[i].get<InputBasketInfo>();
            if( basket -> isDynamicBasket() )
                delete static_cast<DynamicInputBasketInfo *>( basket );
            else
                delete basket;
        }
    }

    for( int i = 0; i < m_def.numOutputs; ++i )
    {
        if( m_outputs[i].isSet<TimeSeriesProvider>() )
            delete m_outputs[i].get<TimeSeriesProvider>();
        else
        {
            auto * basket = m_outputs[i].get<OutputBasketInfo>();
            //its possible to have null outputs if we had an exception on startup before creating the output ( ie cppnode NotImplemented type )
            //check for null before checking is Basket
            if( basket && basket -> isDynamicBasket() )
                delete static_cast<DynamicOutputBasketInfo *>( basket );
            else
                delete basket;
        }
    }

    delete[] m_outputs;
    delete[] m_inputs;
}

void Node::validateInputIndex( size_t id )
{
    if( id > InputId::maxId() )
        SP2_THROW( ValueError, "Input " << id << " on node \"" << name() << "\" violates maximum allowable inputs" );
}

void Node::validateOutputIndex( size_t id )
{
    if( id > OutputId::maxId() )
        SP2_THROW( ValueError, "Output " << id << " on node \"" << name() << "\" violates maximum allowable outputs" );
}

void Node::validateInputBasketSize( size_t id, size_t size )
{
    if( size > InputId::maxBasketElements() )
        SP2_THROW( ValueError, "Input " << id << " on node \"" << name() << "\" has basket size " << size << " which violates maximum"
                   << " allowable basket elements [ " << InputId::maxBasketElements() << " ]" );
}

void Node::validateOutputBasketSize( size_t id, size_t size )
{
    if( size > OutputId::maxBasketElements() )
        SP2_THROW( ValueError, "Output " << id << " on node \"" << name() << "\" has basket size " << size << " which violates maximum"
                   << " allowable basket elements [ " << OutputId::maxBasketElements() << " ]" );
}

void Node::initInputBasket( size_t id, size_t size, bool dynamicBasket )
{
    validateInputIndex( id );
    validateInputBasketSize( id, size );

    SP2_ASSERT( !m_inputs[ id ] );
    m_inputs[ id ].set( dynamicBasket ? new DynamicInputBasketInfo( rootEngine() ) : new InputBasketInfo( rootEngine(), size ) );
}

void Node::link( TimeSeriesProvider * input, InputId inputId )
{
    if( inputId.elemId == InputId::ELEM_ID_NONE )
    {
        SP2_ASSERT( !m_inputs[ inputId.id ] );
        m_inputs[ inputId.id ].set( input );
    }
    else
        inputBasket( inputId.id ) -> setElem( inputId.elemId, input );

    input -> addConsumer( this, inputId );
}

void Node::createAlarm( Sp2TypePtr & type, size_t id )
{
    switchSp2Type( type, [this,&type,id]( auto tag )
                   {
                       using T = typename decltype(tag)::type;
                       this -> createAlarm<T>( type, id );
                   } );
}

}
