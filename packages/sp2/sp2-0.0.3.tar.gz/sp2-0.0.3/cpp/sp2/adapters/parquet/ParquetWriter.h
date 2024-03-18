#ifndef _IN_SP2_ADAPTERS_PARQUET_ParquetWriter_H
#define _IN_SP2_ADAPTERS_PARQUET_ParquetWriter_H

#include <sp2/adapters/parquet/DialectGenericListWriterInterface.h>
#include <sp2/adapters/parquet/ParquetOutputAdapterManager.h>
#include <sp2/engine/Dictionary.h>
#include <sp2/engine/Engine.h>
#include <string>
#include <optional>
#include <unordered_map>

namespace arrow{ class KeyValueMetadata; }

namespace sp2::adapters::parquet
{
class ArrowSingleColumnArrayBuilder;

class ParquetOutputHandler;
class SingleColumnParquetOutputHandler;
class SingleColumnParquetOutputAdapter;
class StructParquetOutputHandler;
class StructParquetOutputAdapter;
class ListColumnParquetOutputHandler;
class ListColumnParquetOutputAdapter;

class FileWriterWrapper;

class FileWriterWrapperContainer;


class ParquetWriter : public EndCycleListener
{
public:
    ParquetWriter( ParquetOutputAdapterManager *mgr, std::optional<bool> writeTimestampColumn = {} );
    ParquetWriter( ParquetOutputAdapterManager *mgr, const Dictionary & properties );

    ~ParquetWriter();

    SingleColumnParquetOutputAdapter *getScalarOutputAdapter( Sp2TypePtr &type, const std::string &columnName );
    StructParquetOutputAdapter *getStructOutputAdapter( Sp2TypePtr &type, sp2::DictionaryPtr fieldMap );
    ListColumnParquetOutputAdapter *getListOutputAdapter( Sp2TypePtr &elemType, const std::string &columnName,
                                                          const DialectGenericListWriterInterface::Ptr &listWriterInterface );

    SingleColumnParquetOutputHandler *getScalarOutputHandler( Sp2TypePtr &type, const std::string &columnName );
    StructParquetOutputHandler *getStructOutputHandler( Sp2TypePtr &type, sp2::DictionaryPtr fieldMap );
    ListColumnParquetOutputHandler *getListOutputHandler( Sp2TypePtr &elemType, const std::string &columnName,
                                                          const DialectGenericListWriterInterface::Ptr &listWriterInterface );

    PushInputAdapter *getStatusAdapter();

    virtual void start();
    virtual void stop();

    void onEndCycle() override;

    std::uint32_t getChunkSize() const{ return m_adapterMgr.getBatchSize(); }

    virtual void scheduleEndCycleEvent()
    {
        m_adapterMgr.scheduleEndCycle();
    }

    bool isFileOpen() const;

    virtual void onFileNameChange(const std::string& fileName);
protected:
    virtual SingleColumnParquetOutputHandler *createScalarOutputHandler( Sp2TypePtr type, const std::string& name );
    virtual ListColumnParquetOutputHandler *createListOutputHandler( Sp2TypePtr &elemType, const std::string &columnName,
                                                                     DialectGenericListWriterInterface::Ptr listWriterInterface );
    virtual StructParquetOutputHandler *createStructOutputHandler( Sp2TypePtr type, const DictionaryPtr &fieldMap );

private:
    void initFileWriterContainer( std::shared_ptr<arrow::Schema> schema );
    void writeCurChunkToFile();
protected:
    using Adapters = std::vector<ParquetOutputHandler *>;
    using PublishedColumnNames = std::unordered_set<std::string>;

    ParquetOutputAdapterManager &m_adapterMgr;
    Engine                      *m_engine;
private:
    Adapters             m_adapters;
    PublishedColumnNames m_publishedColumnNames;


    std::unique_ptr<FileWriterWrapperContainer> m_fileWriterWrapperContainer;

    std::vector<std::shared_ptr<ArrowSingleColumnArrayBuilder>> m_columnBuilders;
    std::uint32_t                                               m_curChunkSize;
    std::optional<bool>                                         m_writeTimestampColumn;

    std::shared_ptr<arrow::KeyValueMetadata>                                 m_fileMetaData;
    std::unordered_map<std::string,std::shared_ptr<arrow::KeyValueMetadata>> m_columnMetaData;
};

}

#endif
