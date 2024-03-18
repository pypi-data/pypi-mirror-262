#ifndef _IN_SP2_ADAPTERS_PARQUET_ParquetDictBasketOutputHandler_H
#define _IN_SP2_ADAPTERS_PARQUET_ParquetDictBasketOutputHandler_H

#include <sp2/adapters/parquet/FileWriterWrapperContainer.h>
#include <sp2/adapters/parquet/ParquetWriter.h>
#include <sp2/engine/Sp2Type.h>
#include <parquet/arrow/writer.h>
#include <string>

namespace sp2::adapters::parquet
{
class ParquetOutputAdapterManager;

class ParquetDictBasketOutputWriter : public ParquetWriter
{
public:
    ParquetDictBasketOutputWriter( ParquetOutputAdapterManager *outputAdapterManager, const std::string &columnName );
    void start() override;
    void stop() override;

    virtual void writeValue( const std::string &valueKey, const TimeSeriesProvider *ts );

    void onEndCycle() override final;
    void onFileNameChange( const std::string &fileName ) override;
protected:
    SingleColumnParquetOutputHandler *createScalarOutputHandler( Sp2TypePtr type, const std::string &name ) override;
    StructParquetOutputHandler *createStructOutputHandler( Sp2TypePtr type, const DictionaryPtr &fieldMap ) override;

private:
    SingleColumnParquetOutputHandler                    *m_symbolOutputAdapter;
    SingleColumnParquetOutputHandler                    *m_cycleIndexOutputAdapter;
    std::uint16_t                                       m_nextCycleIndex;
    std::vector<std::unique_ptr<ParquetOutputHandler>>  m_allHandlers;
    std::unique_ptr<MultipleFileWriterWrapperContainer> m_indexFileWriterContainer;
};

class ParquetScalarDictBasketOutputWriter final : public ParquetDictBasketOutputWriter
{
public:
    ParquetScalarDictBasketOutputWriter( ParquetOutputAdapterManager *outputAdapterManager, const std::string &columnName,
                                         Sp2TypePtr sp2TypePtr );

    void writeValue( const std::string &valueKey, const TimeSeriesProvider *ts ) override;
private:
    SingleColumnParquetOutputHandler *m_valueOutputAdapter;
};

class ParquetStructDictBasketOutputWriter final : public ParquetDictBasketOutputWriter
{
public:
    ParquetStructDictBasketOutputWriter( ParquetOutputAdapterManager *outputAdapterManager, const std::string &columnName,
                                         Sp2TypePtr sp2TypePtr );

    void writeValue( const std::string &valueKey, const TimeSeriesProvider *ts ) override;
private:
    StructParquetOutputHandler *m_valueOutputAdapter;
};

}


#endif
