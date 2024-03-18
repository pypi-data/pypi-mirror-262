
if(SP2_BUILD_KAFKA_ADAPTER)
    add_subdirectory(kafka)
endif()

if(SP2_BUILD_PARQUET_ADAPTER)
    add_subdirectory(parquet)
endif()

add_subdirectory(utils)
