#include <sp2/engine/VectorContainer.h>
#include <sp2/engine/PartialSwitchSp2Type.h>
#include <sp2/engine/Struct.h>
#include <optional>

namespace
{
template< typename T >
class TypedVectorContainer : public sp2::VectorContainer
{
protected:
    void *getVectorUntyped()
    {
        return &m_vector;
    }

private:
    std::vector<T> m_vector;
};
}

namespace sp2
{

std::unique_ptr<VectorContainer> VectorContainer::createForSp2Type(Sp2TypePtr &type, bool optionalValues)
{
    return createForSp2Type(type.get());
}

std::unique_ptr<VectorContainer> VectorContainer::createForSp2Type( const Sp2Type *type, bool optionalValues )
{
    return AllSp2TypeSwitch::invoke(type, [type, optionalValues]( auto tag )
    {
        if(optionalValues)
        {
            return std::unique_ptr<VectorContainer>( new TypedVectorContainer<std::optional<typename decltype(tag)::type>> );
        }
        else
        {
            return std::unique_ptr<VectorContainer>( new TypedVectorContainer<typename decltype(tag)::type> );
        }
    });
}

}
