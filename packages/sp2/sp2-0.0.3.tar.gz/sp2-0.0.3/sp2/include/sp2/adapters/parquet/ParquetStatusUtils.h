#ifndef _IN_SP2_ADAPTERS_PARQUET_ParquetStatusUtils_H
#define _IN_SP2_ADAPTERS_PARQUET_ParquetStatusUtils_H

#include <sp2/core/Exception.h>

#define STATUS_OK_OR_THROW_RUNTIME( EXPR, MESSAGE )                                                         \
    do                                                                                                      \
    {                                                                                                       \
        arrow::Status st = EXPR;                                                                            \
        SP2_TRUE_OR_THROW_RUNTIME( st.ok(), MESSAGE << ':' << st.ToString());                               \
    } while( 0 )

#endif
