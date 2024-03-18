#ifndef _IN_SP2_ADAPTERS_PARQUET_DialectGenericListReaderInterface_H
#define _IN_SP2_ADAPTERS_PARQUET_DialectGenericListReaderInterface_H

#include <memory>
#include <sp2/engine/DialectGenericType.h>
#include <sp2/adapters/parquet/ParquetReaderColumnAdapter.h>
#include <arrow/array/builder_base.h>

namespace sp2::adapters::parquet
{

class DialectGenericListReaderInterface
{
public:
    using Ptr = std::shared_ptr<DialectGenericListReaderInterface>;
    virtual ~DialectGenericListReaderInterface() = default;
    virtual sp2::DialectGenericType create( uint32_t size ) = 0;
    /**
     * This form of creation is needed for elements that need to know the element size in advance, such as numpy arrays of strings
     * @param size
     * @return
     */
    virtual sp2::DialectGenericType create( uint32_t size, uint32_t maxElementSize ) = 0;
    virtual Sp2TypePtr getValueType() = 0;
};

template< typename T >
class TypedDialectGenericListReaderInterface : public DialectGenericListReaderInterface
{
public:
    using Ptr = std::shared_ptr<TypedDialectGenericListReaderInterface<T>>;
    Sp2TypePtr getValueType() override{ return Sp2Type::fromCType<T>::type(); }

    /**
     * Return a raw data buffer for the object that was generated using the call to create. Should return the pointer to internal buffer
     * that can be written directly into if that's supported, otherwise, should return nullptr in which case setValue will be used for
     * inserting the elements
     * @param list: The list object that was created using the call to create function
     * @return Internal write buffer of the list of nullptr if the list doesn't support writing to internal buffer
     */
    virtual T *getRawDataBuffer( const sp2::DialectGenericType &list ) const{ return nullptr; }
    virtual void setValue( const sp2::DialectGenericType &list, int index, const T &value ) = 0;
};


}

#endif