#include <sp2/adapters/parquet/ParquetOutputFilenameAdapter.h>
#include <sp2/adapters/parquet/ParquetOutputAdapterManager.h>
#include <string>

namespace sp2::adapters::parquet
{

void ParquetOutputFilenameAdapter::executeImpl()
{
    m_parquetOutputAdapterManager.changeFileName( input()->lastValueTyped<std::string>());
}

}
