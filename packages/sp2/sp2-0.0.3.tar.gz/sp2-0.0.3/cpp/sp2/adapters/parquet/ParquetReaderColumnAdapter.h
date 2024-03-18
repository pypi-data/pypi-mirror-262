#ifndef _IN_SP2_ADAPTERS_PARQUET_ParquetReaderColumnAdapter_H
#define _IN_SP2_ADAPTERS_PARQUET_ParquetReaderColumnAdapter_H

#include <sp2/adapters/utils/StructAdapterInfo.h>
#include <sp2/adapters/utils/ValueDispatcher.h>
#include <sp2/core/Generator.h>
#include <sp2/engine/AdapterManager.h>
#include <sp2/engine/Sp2Type.h>
#include <sp2/engine/PartialSwitchSp2Type.h>
#include <sp2/engine/Struct.h>
#include <sp2/adapters/parquet/DialectGenericListReaderInterface.h>

#include <arrow/table.h>
#include <arrow/type.h>
#include <memory>
#include <optional>
#include <parquet/arrow/reader.h>
#include <string>
#include <unordered_map>
#include <vector>
#include <set>

namespace arrow::io
{
class ReadableFile;
}

namespace sp2::adapters::parquet
{
SP2_DECLARE_EXCEPTION( ParquetColumnTypeError, sp2::TypeError );

class ParquetReader;
class ParquetStructAdapter;

class ParquetColumnAdapter
{
public:
    ParquetColumnAdapter( ParquetReader &parquetReader, const std::string& columnName ) : m_parquetReader( parquetReader ), m_columnName(columnName){}

    virtual ~ParquetColumnAdapter(){}

    const std::string& getColumnName() const {return m_columnName;}

    virtual bool isListType() const {return false;};
    virtual Sp2TypePtr  getContainerValueType() const {SP2_THROW(TypeError, "Trying to get list value on non container type");}

    virtual void addSubscriber( ManagedSimInputAdapter *inputAdapter, std::optional<utils::Symbol> symbol = {} ) = 0;

    virtual void dispatchValue( const utils::Symbol *symbol ) = 0;

    virtual void ensureType( Sp2Type::Ptr sp2Type ) = 0;

    virtual void readCurValue() = 0;

    ParquetReader &getReader(){ return m_parquetReader; }

    const ParquetReader &getReader() const{ return m_parquetReader; }

    virtual bool isNativeType() const {return getNativeSp2Type() && getNativeSp2Type()->type() < Sp2Type::TypeTraits::MAX_NATIVE_TYPE;}
    virtual bool isMissingColumn() const { return false;}
    virtual Sp2TypePtr getNativeSp2Type() const =0;

    template< typename T >
    std::optional<T> &getCurValue()
    {
        return *static_cast<std::optional<T> *>(getCurValueUntyped());
    }

    virtual void handleNewBatch( const std::shared_ptr<::arrow::ChunkedArray> &data ) = 0;
    virtual void handleNewBatch( const std::shared_ptr<::arrow::Array> &data ) = 0;

protected:
    friend class ParquetReader;

    virtual void *getCurValueUntyped() = 0;

protected:
    ParquetReader     &m_parquetReader;
    const std::string m_columnName;
};

class ParquetStructAdapter final
{
public:
    using ValueDispatcher = sp2::adapters::utils::ValueDispatcher<StructPtr &>;
    using FieldSetter = std::function<void( StructPtr & )>;

    ParquetStructAdapter( ParquetReader &parquetReader,
                          sp2::adapters::utils::StructAdapterInfo adapterInfo );
    ParquetStructAdapter( ParquetReader &parquetReader,
                          std::shared_ptr<::arrow::StructType> arrowType,
                          const std::shared_ptr<StructMeta> &structMeta,
                          const std::vector<std::unique_ptr<ParquetColumnAdapter>> &columnAdapters );

    void addSubscriber( ManagedSimInputAdapter *inputAdapter, std::optional<utils::Symbol> symbol = {} );
    void addSubscriber( ValueDispatcher::SubscriberType subscriber, std::optional<utils::Symbol> symbol = {} );

    void dispatchValue( const utils::Symbol *symbol, bool isNull = false );

    const std::shared_ptr<StructMeta> &getStructMeta(){ return m_structMeta; }

    void onSchemaChange(){ m_needsReset = true; }
private:
    void createFieldSetter( const std::string &fieldName, ParquetColumnAdapter &columnAdapter );

private:
    using StructAdapterInfo = sp2::adapters::utils::StructAdapterInfo;

    ParquetReader               &m_parquetReader;
    std::shared_ptr<StructMeta> m_structMeta;
    ValueDispatcher             m_valueDispatcher;
    std::vector<FieldSetter>    m_fieldSetters;
    std::function<void()>       m_resetFunc;
    bool                        m_needsReset = false;
};

class MissingColumnAdapter : public ParquetColumnAdapter
{
public:
    using ParquetColumnAdapter::ParquetColumnAdapter;

    virtual void addSubscriber( ManagedSimInputAdapter *inputAdapter, std::optional<utils::Symbol> symbol = {} ) override {};

    virtual void dispatchValue( const utils::Symbol *symbol ) override {};

    virtual void ensureType( Sp2Type::Ptr sp2Type ) override {};

    virtual void readCurValue() override {};

    bool isNativeType() const override
    {
        SP2_THROW( sp2::RuntimeException, "Trying to check type of a missing column " << getColumnName() );
    }

    bool isMissingColumn() const override{ return true; }

    virtual Sp2TypePtr getNativeSp2Type() const override
    {
        SP2_THROW( sp2::RuntimeException, "Trying to get native type of a missing column " << getColumnName() );
    }

    virtual void handleNewBatch( const std::shared_ptr<::arrow::ChunkedArray> &data ) override
    {
        SP2_THROW( sp2::RuntimeException, "Trying to handle new batch for a missing column " << getColumnName() );
    }

    virtual void handleNewBatch( const std::shared_ptr<::arrow::Array> &data ) override
    {
        SP2_THROW( sp2::RuntimeException, "Trying to handle new batch for a missing column " << getColumnName() );
    }

protected:
    void *getCurValueUntyped() override
    {
        SP2_THROW( sp2::RuntimeException, "Trying to get value of a missing column " << getColumnName() );
    }
};

template< typename ValueType, typename ArrowArrayType, typename ValueDispatcherT = sp2::adapters::utils::ValueDispatcher<const ValueType &>>
class BaseTypedColumnAdapter : public ParquetColumnAdapter
{
public:
    BaseTypedColumnAdapter( ParquetReader &parquetReader, const std::string& columnName )
            : ParquetColumnAdapter( parquetReader, columnName )
    {
    }

    void addSubscriber( ManagedSimInputAdapter *inputAdapter, std::optional<utils::Symbol> symbol = {} ) override;

    void dispatchValue( const utils::Symbol *symbol ) override;

    void ensureType( Sp2Type::Ptr sp2Type ) override;

protected:
    void *getCurValueUntyped() override;

    void handleNewBatch( const std::shared_ptr<::arrow::ChunkedArray> &data ) override;
    void handleNewBatch( const std::shared_ptr<::arrow::Array> &data ) override;

protected:
    using CompatibleTypeSwitch = ConstructibleTypeSwitch<ValueType>;
    using ValueDispatcher = ValueDispatcherT;

    ValueDispatcher                 m_dispatcher;
    std::shared_ptr<ArrowArrayType> m_curChunkArray;
    std::optional<ValueType>        m_curValue;
};

template< typename ValueType, typename ArrowArrayType >
class NativeTypeColumnAdapter : public BaseTypedColumnAdapter<ValueType, ArrowArrayType>
{
public:
    using BaseTypedColumnAdapter<ValueType, ArrowArrayType>::BaseTypedColumnAdapter;
    virtual Sp2TypePtr getNativeSp2Type() const override {return Sp2Type::fromCType<ValueType>::type();}

protected:
    void readCurValue() override;
};

template< long UNIT >
class DatetimeColumnAdapter : public BaseTypedColumnAdapter<sp2::DateTime, arrow::TimestampArray>
{
public:
    using BaseTypedColumnAdapter::BaseTypedColumnAdapter;
    virtual Sp2TypePtr getNativeSp2Type() const override {return Sp2Type::fromCType<sp2::DateTime>::type();}
protected:
    void readCurValue() override;
};

template< long UNIT >
class DurationColumnAdapter : public BaseTypedColumnAdapter<sp2::TimeDelta, arrow::DurationArray>
{
public:
    using BaseTypedColumnAdapter::BaseTypedColumnAdapter;
    virtual Sp2TypePtr getNativeSp2Type() const override {return Sp2Type::fromCType<sp2::TimeDelta>::type();}
protected:
    void readCurValue() override;
};

template< long UNIT, typename ArrowDateArray >
class DateColumnAdapter : public BaseTypedColumnAdapter<sp2::Date, ArrowDateArray>
{
public:
    using BaseTypedColumnAdapter<sp2::Date, ArrowDateArray>::BaseTypedColumnAdapter;
    virtual Sp2TypePtr getNativeSp2Type() const override {return Sp2Type::fromCType<sp2::Date>::type();}
protected:
    void readCurValue() override;
};

template< long UNIT, typename ArrowTimeArray >
class TimeColumnAdapter : public BaseTypedColumnAdapter<sp2::Time, ArrowTimeArray>
{
public:
    using BaseTypedColumnAdapter<sp2::Time, ArrowTimeArray>::BaseTypedColumnAdapter;
    virtual Sp2TypePtr getNativeSp2Type() const override {return Sp2Type::fromCType<sp2::Time>::type();}
protected:
    void readCurValue() override;
};

class StringColumnAdapter : public BaseTypedColumnAdapter<std::string, arrow::StringArray>
{
public:
    using BaseTypedColumnAdapter::BaseTypedColumnAdapter;
    void addSubscriber( ManagedSimInputAdapter *inputAdapter, std::optional<utils::Symbol> symbol = {} ) override;
    virtual Sp2TypePtr getNativeSp2Type() const override {return nullptr;}
protected:
    void readCurValue() override;
};

class BytesColumnAdapter : public BaseTypedColumnAdapter<std::string, arrow::BinaryArray>
{
public:
    using BaseTypedColumnAdapter::BaseTypedColumnAdapter;
    virtual Sp2TypePtr getNativeSp2Type() const override {return nullptr;}
protected:
    void readCurValue() override;
};

class FixedSizeBinaryColumnAdapter : public BaseTypedColumnAdapter<std::string, arrow::FixedSizeBinaryArray>
{
public:
    using BaseTypedColumnAdapter::BaseTypedColumnAdapter;
    virtual Sp2TypePtr getNativeSp2Type() const override {return nullptr;}
protected:
    void readCurValue() override;
};

class DictionaryColumnAdapter : public BaseTypedColumnAdapter<std::string, arrow::DictionaryArray>
{
public:
    using BaseTypedColumnAdapter::BaseTypedColumnAdapter;
    virtual Sp2TypePtr getNativeSp2Type() const override {return nullptr;}
protected:
    void readCurValue() override;
};

template<typename ValueArrayType, typename ValueType=typename ValueArrayType::TypeClass::c_type>
class ListColumnAdapter : public BaseTypedColumnAdapter<DialectGenericType, arrow::ListArray>
{
public:
    using Base = BaseTypedColumnAdapter<DialectGenericType, arrow::ListArray>;
    using BaseTypedColumnAdapter::BaseTypedColumnAdapter;
    void addSubscriber( ManagedSimInputAdapter *inputAdapter, std::optional<utils::Symbol> symbol = {} ) override;
    void addSubscriber( ManagedSimInputAdapter *inputAdapter,
                        std::optional<utils::Symbol> symbol, const DialectGenericListReaderInterface::Ptr &listReader);
    Sp2TypePtr getNativeSp2Type() const override {return nullptr;}

    bool isListType() const override{ return true; };
    Sp2TypePtr getContainerValueType() const override{ return Sp2Type::fromCType<ValueType>::type(); }
protected:
    void readCurValue() override;
private:
    // For now we allow only one subscription for list columns. In the future we might allow multiple subscriptions using different readers.
    // For example we could subscritbe to the same column as a list and as array, we would need to do more book keepting in this case.
    typename TypedDialectGenericListReaderInterface<ValueType>::Ptr m_listReader = nullptr;
};

class StructColumnAdapter : public BaseTypedColumnAdapter<StructPtr, arrow::StructArray, sp2::adapters::utils::ValueDispatcher<StructPtr &>>
{
public:
    using BASE = BaseTypedColumnAdapter<StructPtr, arrow::StructArray, sp2::adapters::utils::ValueDispatcher<StructPtr &>>;

    StructColumnAdapter( ParquetReader &parquetReader, const std::shared_ptr<::arrow::StructType> &arrowType,
                         const std::string& columnName)
        : BASE( parquetReader, columnName ), m_arrowType( arrowType )
    {
    }

    virtual Sp2TypePtr getNativeSp2Type() const override {return nullptr;}

    void setStructMeta( const std::shared_ptr<StructMeta> &structMeta ){ initFromStructMeta( structMeta ); }
    void addSubscriber( ManagedSimInputAdapter *inputAdapter, std::optional<utils::Symbol> symbol = {} ) override;
protected:
    void readCurValue() override;
    void handleNewBatch( const std::shared_ptr<::arrow::ChunkedArray> &data ) override;
    void handleNewBatch( const std::shared_ptr<::arrow::Array> &data ) override;
private:
    void initFromStructMeta( const std::shared_ptr<StructMeta> &structMeta );

private:
    friend class ParquetStructAdapter;

    std::shared_ptr<::arrow::StructType>               m_arrowType;
    std::unique_ptr<ParquetStructAdapter>              m_structAdapter;
    std::vector<std::unique_ptr<ParquetColumnAdapter>> m_childColumnAdapters;
};

std::unique_ptr<ParquetColumnAdapter> createColumnAdapter(
        ParquetReader &parquetReader,
        const ::arrow::Field& field,
        const std::string& fileName,
        const std::map<std::string, std::shared_ptr<StructMeta>>* structMetaByColumnName = nullptr);

std::unique_ptr<ParquetColumnAdapter> createMissingColumnAdapter(ParquetReader &parquetReader,const std::string& columnName);

}


#endif
