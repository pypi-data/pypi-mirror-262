#ifndef _IN_SP2_ENGINE_VECTORALLOCATOR_H
#define _IN_SP2_ENGINE_VECTORALLOCATOR_H

#include <sp2/engine/Sp2Type.h>

namespace sp2
{
class VectorContainer
{
public:
    VectorContainer(const VectorContainer&) = delete;

    virtual ~VectorContainer(){};
    VectorContainer& operator=(const VectorContainer&) = delete;

    template< typename T >
    std::vector<T> &getVector()
    {
        return *reinterpret_cast<std::vector<T> *>(getVectorUntyped());
    }

    static std::unique_ptr<VectorContainer> createForSp2Type( Sp2TypePtr &type, bool optionalValues = true );
    static std::unique_ptr<VectorContainer> createForSp2Type( const Sp2Type *type, bool optionalValues = true );
protected:
    VectorContainer() = default;
    virtual void *getVectorUntyped() = 0;
};

}

#endif
