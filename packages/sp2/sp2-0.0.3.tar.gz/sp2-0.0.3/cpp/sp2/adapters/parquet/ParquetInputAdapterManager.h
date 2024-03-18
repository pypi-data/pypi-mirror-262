#ifndef _IN_SP2_ADAPTERS_PARQUET_ParquetInputAdapterManager_H
#define _IN_SP2_ADAPTERS_PARQUET_ParquetInputAdapterManager_H

#include <sp2/adapters/parquet/ParquetReader.h>
#include <sp2/adapters/utils/StructAdapterInfo.h>
#include <sp2/core/Generator.h>
#include <sp2/engine/AdapterManager.h>
#include <sp2/engine/Dictionary.h>
#include <unordered_map>
#include <set>
#include <string>
#include <optional>
#include <sp2/adapters/parquet/DialectGenericListReaderInterface.h>


namespace sp2::adapters::parquet
{


//Top level AdapterManager object for all parquet adapters in the engine
class ParquetInputAdapterManager final : public sp2::AdapterManager
{
public:
    using GeneratorPtr = sp2::Generator<std::string, sp2::DateTime, sp2::DateTime>::Ptr;
    using TableGeneratorPtr = sp2::Generator<std::shared_ptr<arrow::Table>, sp2::DateTime, sp2::DateTime>::Ptr;

    ParquetInputAdapterManager( sp2::Engine *engine, const Dictionary &properties, GeneratorPtr generatorPtr, TableGeneratorPtr tableGeneratorPtr );

    ~ParquetInputAdapterManager();

    const char *name() const override{ return "ParquetInputAdapterManager"; }

    //start subscriptions and processing thread
    void start( DateTime starttime, DateTime endtime ) override;

    //stop subscriptions and processing thread
    void stop() override;

    DateTime processNextSimTimeSlice( DateTime time ) override;

    ManagedSimInputAdapter *getInputAdapter( Sp2TypePtr &type, const Dictionary &properties, PushMode pushMode,
                                             const DialectGenericListReaderInterface::Ptr &listReaderInterface = nullptr );
private:
    using StructAdapterInfo = sp2::adapters::utils::StructAdapterInfo;

    struct AdapterInfo
    {
        AdapterInfo(ManagedSimInputAdapter* adapter, const DialectGenericListReaderInterface::Ptr listReaderInterface = nullptr)
        : m_adapter(adapter), m_listReaderInterface(listReaderInterface)
        {
        }
        ManagedSimInputAdapter * m_adapter;
        DialectGenericListReaderInterface::Ptr m_listReaderInterface = nullptr;
    };

    struct AdaptersSingleSymbol
    {
        using AdaptersByColumnName = std::unordered_map<std::string, AdapterInfo>;
        using StructAdaptersByStructKey = std::unordered_map<StructAdapterInfo, AdapterInfo>;
        AdaptersByColumnName      m_adaptersByColumnName;

        StructAdaptersByStructKey m_structAdapters;
    };
    struct DictBasketReaderRecord
    {
        ColumnAdapterReference         m_valueCountColumn;
        std::unique_ptr<ParquetReader> m_reader;
    };

    using AdaptersBySymbol = std::unordered_map<utils::Symbol, AdaptersSingleSymbol>;
    using DictBasketSymbolAdapters = std::unordered_map<std::string, AdaptersBySymbol>;

    std::unique_ptr<ParquetReader> initializeParquetReader( const std::optional<std::string> &symbolColumn,
                                                            const std::set<std::string> &neededColumns,
                                                            const AdaptersBySymbol &adaptersBySymbol,
                                                            bool subscribeAllOnEmptySymbol = true,
                                                            bool nullOnEmpty = false ) const;

    ManagedSimInputAdapter *getRegularAdapter( const Sp2TypePtr &type,
                                               const Dictionary &properties, const PushMode &pushMode, const utils::Symbol &symbol,
                                               const DialectGenericListReaderInterface::Ptr &listReaderInterface = nullptr);
    ManagedSimInputAdapter *getDictBasketAdapter( const Sp2TypePtr &type,
                                                  const Dictionary &properties, const PushMode &pushMode, const utils::Symbol &symbol,
                                                  const std::string &basketName );

    ManagedSimInputAdapter *getOrCreateSingleColumnAdapter( AdaptersBySymbol &inputAdaptersContainer,
                                                            const Sp2TypePtr &type, const utils::Symbol &symbol,
                                                            const std::string &field, const PushMode &pushMode,
                                                            const DialectGenericListReaderInterface::Ptr &listReaderInterface = nullptr );
    ManagedSimInputAdapter *getSingleColumnAdapter( const Sp2TypePtr &type,
                                                    const utils::Symbol &symbol, const std::string &field, PushMode pushMode,
                                                    const DialectGenericListReaderInterface::Ptr &listReaderInterface = nullptr);
    ManagedSimInputAdapter *getOrCreateStructColumnAdapter( AdaptersBySymbol &inputAdaptersContainer,
                                                            const Sp2TypePtr &type, const utils::Symbol &symbol,
                                                            const sp2::DictionaryPtr &fieldMap, const PushMode &pushMode );
    ManagedSimInputAdapter *getStructAdapter( const Sp2TypePtr &type, const utils::Symbol &symbol,
                                              const sp2::DictionaryPtr &fieldMap, PushMode pushMode );


    DictBasketSymbolAdapters m_dictBasketInputAdapters;
    AdaptersBySymbol         m_simInputAdapters;


    FileNameGeneratorReplicator::Ptr    m_fileNameGeneratorReplicator;
    sp2::DateTime                       m_startTime;
    sp2::DateTime                       m_endTime;
    sp2::TimeDelta                      m_time_shift;
    TableGeneratorPtr                   m_tableGenerator;
    std::string                         m_symbolColumn;
    std::string                         m_timeColumn;
    std::string                         m_defaultTimezone;
    bool                                m_splitColumnsToFiles;
    bool                                m_isArrowIPC;
    bool                                m_allowOverlappingPeriods;
    bool                                m_allowMissingColumns;
    bool                                m_allowMissingFiles;
    std::unique_ptr<ParquetReader>      m_reader;
    ColumnAdapterReference              m_timestampColumnAdapter;
    std::vector<DictBasketReaderRecord> m_dictBasketReaders;
    std::optional<PushMode>             m_pushMode;
    bool                                m_subscribedBySymbol      = false;
    bool                                m_subscribedForAll        = false;


};

}

#endif
