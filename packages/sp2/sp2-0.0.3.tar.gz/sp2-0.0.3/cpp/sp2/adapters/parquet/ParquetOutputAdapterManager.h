#ifndef _IN_SP2_ADAPTERS_PARQUET_ParquetOutputAdapterManager_H
#define _IN_SP2_ADAPTERS_PARQUET_ParquetOutputAdapterManager_H

#include <sp2/adapters/parquet/ParquetReader.h>
#include <sp2/adapters/utils/StructAdapterInfo.h>
#include <sp2/core/Generator.h>
#include <sp2/engine/AdapterManager.h>
#include <sp2/engine/Dictionary.h>
#include <set>
#include <string>
#include <unordered_map>
#include <sp2/adapters/parquet/DialectGenericListWriterInterface.h>


namespace sp2::adapters::parquet
{
class ParquetWriter;

class ParquetOutputFilenameAdapter;

class ParquetDictBasketOutputWriter;

//Top level AdapterManager object for all parquet adapters in the engine
class ParquetOutputAdapterManager final : public sp2::AdapterManager
{
public:
    using FileVisitorCallback = std::function<void(const std::string &)>;

    ParquetOutputAdapterManager( sp2::Engine *engine, const Dictionary &properties, FileVisitorCallback fileVisitor );
    ~ParquetOutputAdapterManager();

    const char *name() const override{ return "ParquetOutputAdapterManager"; }

    const std::string &getFileName() const{ return m_fileName; }

    const std::string &getTimestampColumnName() const{ return m_timestampColumnName; }

    bool isAllowOverwrite() const{ return m_allowOverwrite; }

    uint32_t getBatchSize() const{ return m_batchSize; }

    std::string getCompression() const{ return m_compression; }

    bool isWriteArrowBinary() const{ return m_writeArrowBinary; }

    bool isSplitColumnsToFiles() const{ return m_splitColumnsToFiles; }

    //start the writer, open file if necessary
    void start( DateTime starttime, DateTime endtime ) override;

    //stop the writer, write any unwritten data and close file
    void stop() override;

    DateTime processNextSimTimeSlice( DateTime time ) override;

    OutputAdapter *getOutputAdapter( Sp2TypePtr &type, const Dictionary &properties );
    OutputAdapter *getListOutputAdapter( Sp2TypePtr &elemType, const Dictionary &properties,
                                         const DialectGenericListWriterInterface::Ptr& listWriterInterface );
    ParquetDictBasketOutputWriter *createDictOutputBasketWriter( const char *columnName, const Sp2TypePtr &sp2TypePtr);
    OutputAdapter *createOutputFileNameAdapter();

    void changeFileName( const std::string &filename );

    void scheduleEndCycle();

private:
    OutputAdapter *getScalarOutputAdapter( Sp2TypePtr &type, const Dictionary &properties );
    OutputAdapter *getStructOutputAdapter( Sp2TypePtr &type, const Dictionary &properties );

    std::string                                                 m_fileName;
    std::string                                                 m_timestampColumnName;
    bool                                                        m_allowOverwrite;
    uint32_t                                                    m_batchSize;
    std::string                                                 m_compression;
    bool                                                        m_writeArrowBinary;
    bool                                                        m_splitColumnsToFiles;
    std::unique_ptr<ParquetWriter>                              m_parquetWriter;
    std::unordered_map<std::string, int>                        m_dictBasketWriterIndexByName;
    std::vector<std::unique_ptr<ParquetDictBasketOutputWriter>> m_dictBasketWriters;
    FileVisitorCallback                                         m_fileVisitor;
    ParquetOutputFilenameAdapter                                *m_outputFilenameAdapter;
};

}

#endif
