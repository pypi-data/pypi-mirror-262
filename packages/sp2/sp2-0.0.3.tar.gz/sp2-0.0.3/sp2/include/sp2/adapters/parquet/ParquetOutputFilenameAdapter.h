#ifndef _IN_SP2_ADAPTERS_PARQUET_ParquetOutputFilenameAdapter_H
#define _IN_SP2_ADAPTERS_PARQUET_ParquetOutputFilenameAdapter_H

#include <sp2/engine/OutputAdapter.h>


namespace sp2::adapters::parquet
{
class ParquetOutputAdapterManager;

class ParquetOutputFilenameAdapter : public sp2::OutputAdapter
{
public:
    ParquetOutputFilenameAdapter( Engine *engine, ParquetOutputAdapterManager &parquetOutputAdapterManager )
            : sp2::OutputAdapter( engine ), m_parquetOutputAdapterManager( parquetOutputAdapterManager )
    {
    }

    void executeImpl() override;

    const char *name() const override { return "ParquetOutputFilenameAdapter"; }

protected:
    ParquetOutputAdapterManager &m_parquetOutputAdapterManager;
};

}

#endif
