#ifndef _IN_SP2_ADAPTERS_PARQUET_DialectGenericListWriterInterface_H
#define _IN_SP2_ADAPTERS_PARQUET_DialectGenericListWriterInterface_H

#include <memory>
#include <sp2/engine/DialectGenericType.h>
#include <sp2/adapters/parquet/ParquetReaderColumnAdapter.h>
#include <arrow/array/builder_base.h>

namespace sp2::adapters::parquet
{

class DialectGenericListWriterInterface
{
public:
    using ArrayBuilderPtr = std::shared_ptr<arrow::ArrayBuilder>;
    using Ptr = std::shared_ptr<DialectGenericListWriterInterface>;

    virtual void writeItems( const sp2::DialectGenericType &listObject ) = 0;
    virtual ~DialectGenericListWriterInterface() = default;
};

template< typename T >
class TypedDialectGenericListWriterInterface : public DialectGenericListWriterInterface
{
public:
    using WriteFuncT = std::function<void( const T & )>;

    TypedDialectGenericListWriterInterface()
    {
        m_writeFunc = []( const T & )
        {
            SP2_THROW( RuntimeException, "Write function for TypedDialectGenericListWriterInterface is not set" );
        };
    }

    void setWriteFunction( const WriteFuncT &func )
    {
        m_writeFunc = func;
    }


    void writeValue( const T &value )
    {
        m_writeFunc( value );
    }

private:
    std::function<void( const T & )> m_writeFunc;
};


}

#endif