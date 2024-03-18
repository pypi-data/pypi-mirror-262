# Find the Python SP2 package
# SP2_INCLUDE_DIR
# SP2_LIBS_DIR
# SP2_FOUND
#
# SP2_AUTOGEN
# SP2_LIBRARY
# SP2_CORE_LIBRARY
# SP2_ENGINE_LIBRARY
# SP2_TYPES_LIBRARY
# SP2_TYPES_STATIC_LIBRARY
# SP2_BASELIB_LIBARY
# SP2_BASELIB_STATIC_LIBRARY
# SP2_BASKETLIB_LIBRARY
# SP2_BASKETLIB_STATIC_LIBRARY
# SP2_MATH_LIBRARY
# SP2_MATH_STATIC_LIBRARY
# SP2_STATS_LIBRARY
# SP2_STATS_STATIC_LIBRARY
# SP2_NPSTATS_LIBRARY
# SP2_ADAPTER_UTILS_LIBRARY
# SP2_KAFKAADAPTER_LIBRARY
# SP2_KAFKAADAPTER_STATIC_LIBRARY
# SP2_PARQUETADAPTER_LIBRARY
# SP2_PARQUETADAPTER_STATIC_LIBRARY
#
# will be set by this script

cmake_minimum_required(VERSION 3.7.2)

find_package(Python ${SP2_PYTHON_VERSION} EXACT REQUIRED COMPONENTS Interpreter)

set(ENV{PYTHONPATH} "${CMAKE_SOURCE_DIR}/ext:$ENV{PYTHONPATH}")

# Find out the base path
execute_process(
  COMMAND "${Python_EXECUTABLE}" -c
          "from __future__ import print_function;import os.path;import sp2;print(os.path.dirname(sp2.__file__), end='')"
          OUTPUT_VARIABLE __sp2_base_path)

# Find out the include path
execute_process(
  COMMAND "${Python_EXECUTABLE}" -c
          "from __future__ import print_function;import sp2;print(sp2.get_include_path(), end='')"
          OUTPUT_VARIABLE __sp2_include_path)

# Find out the lib path
execute_process(
    COMMAND "${Python_EXECUTABLE}" -c
            "from __future__ import print_function;import sp2;print(sp2.get_lib_path(), end='')"
            OUTPUT_VARIABLE __sp2_lib_path)

# And the version
execute_process(
  COMMAND "${Python_EXECUTABLE}" -c
          "from __future__ import print_function;import sp2;print(sp2.__version__, end='')"
  OUTPUT_VARIABLE __sp2_version)

# Now look for files
find_file(SP2_AUTOGEN sp2_autogen.py HINTS "${__sp2_base_path}/build" NO_DEFAULT_PATH)
find_path(SP2_INCLUDE_DIR sp2/core/System.h HINTS "${__sp2_include_path}" "${PYTHON_INCLUDE_PATH}" NO_DEFAULT_PATH)
find_path(SP2_LIBS_DIR _sp2impl.so HINTS "${__sp2_lib_path}" NO_DEFAULT_PATH)

find_library(SP2_LIBRARY NAMES _sp2impl.so PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)
find_library(SP2_CORE_LIBRARY NAMES libsp2_core_static.a PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)
find_library(SP2_ENGINE_LIBRARY NAMES libsp2_engine_static.a PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)

find_library(SP2_TYPES_LIBRARY NAMES _sp2typesimpl.so PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)
find_library(SP2_TYPES_STATIC_LIBRARY NAMES libsp2_types_static.a PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)

find_library(SP2_BASELIB_LIBARY NAMES _sp2baselibimpl.so PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)
find_library(SP2_BASELIB_STATIC_LIBRARY NAMES libbaselibimpl_static.a PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)

find_library(SP2_BASKETLIB_LIBRARY NAMES _sp2basketlibimpl.so PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)
find_library(SP2_BASKETLIB_STATIC_LIBRARY NAMES libbasketlibimpl_static.a PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)

find_library(SP2_MATH_LIBRARY NAMES _sp2mathimpl.so PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)
find_library(SP2_MATH_STATIC_LIBRARY NAMES libmathimpl_static.a PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)

find_library(SP2_STATS_LIBRARY NAMES _sp2statsimpl.so PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)
find_library(SP2_STATS_STATIC_LIBRARY NAMES libstatsimpl_static.a PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)

find_library(SP2_NPSTATS_LIBRARY NAMES _sp2npstatsimpl.so PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)

find_library(SP2_ADAPTER_UTILS_LIBRARY NAMES libsp2_adapter_utils_static.a PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)

find_library(SP2_KAFKAADAPTER_LIBRARY NAMES _kafkaadapterimpl.so PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)
find_library(SP2_KAFKAADAPTER_STATIC_LIBRARY NAMES libsp2_kafka_adapter_static.a PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)

find_library(SP2_PARQUETADAPTER_LIBRARY NAMES _parquetadapterimpl.so PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)
find_library(SP2_PARQUETADAPTER_STATIC_LIBRARY NAMES libsp2_parquet_adapter_static.a PATHS "${__sp2_lib_path}" NO_DEFAULT_PATH)

if(SP2_INCLUDE_DIR AND SP2_LIBS_DIR AND SP2_AUTOGEN)
  set(SP2_FOUND 1 CACHE INTERNAL "SP2 found")
endif()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(SP2 REQUIRED_VARS SP2_INCLUDE_DIR SP2_LIBS_DIR SP2_AUTOGEN VERSION_VAR __sp2_version)

find_package(sp2_autogen)
