#ifndef _IN_SP2_ADAPTERS_PARQUET_ArrowIPCFileReaderWrapper_H
#define _IN_SP2_ADAPTERS_PARQUET_ArrowIPCFileReaderWrapper_H

#include <sp2/adapters/parquet/FileReaderWrapper.h>
#include <arrow/ipc/reader.h>
#include <string>

namespace sp2::adapters::parquet
{
class ArrowIPCFileReaderWrapper : public FileReaderWrapper
{
public:
    ~ArrowIPCFileReaderWrapper();
    virtual void open( const std::string &fileName ) override;
    virtual void close() override;

    bool readNextRowGroup( const std::vector<int> neededColumns, std::shared_ptr<::arrow::Table> &dst ) override;
    void getSchema( std::shared_ptr<::arrow::Schema> &dst ) override;

private:
    std::shared_ptr<::arrow::ipc::RecordBatchReader> m_fileReader;
};
}


#endif
