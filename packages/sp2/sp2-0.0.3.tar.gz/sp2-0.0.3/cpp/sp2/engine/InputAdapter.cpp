#include <sp2/engine/Consumer.h>
#include <sp2/engine/InputAdapter.h>

namespace sp2
{

InputAdapter::InputAdapter( Engine *engine, const Sp2TypePtr &type, PushMode pushMode ) : m_rootEngine( engine -> rootEngine() ),
                                                                                          m_pushMode( pushMode )
{
    if( pushMode == PushMode::BURST )
        init( Sp2ArrayType::create( type ) );
    else
        init( type );
}

}
