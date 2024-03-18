# types library
set(SP2TYPESIMPL_PUBLIC_HEADERS
        Sp2TypeFactory.h
        PySp2Enum.h
        PySp2Type.h
        PyStruct.h)

add_library(sp2typesimpl
            sp2typesimpl.cpp
            Sp2TypeFactory.cpp
            PySp2Enum.cpp
            PySp2Type.cpp
            PyStruct.cpp)
set_target_properties(sp2typesimpl PROPERTIES PUBLIC_HEADER "${SP2TYPESIMPL_PUBLIC_HEADERS}")
target_link_libraries(sp2typesimpl sp2_core sp2_types)

set(SP2IMPL_PUBLIC_HEADERS
        Common.h
        Conversions.h
        Exception.h
        InitHelper.h
        NumpyConversions.h
        NumpyInputAdapter.h
        PyAdapterManagerWrapper.h
        PyBasketInputProxy.h
        PyBasketOutputProxy.h
        PyCppNode.h
        PyEngine.h
        PyInputAdapterWrapper.h
        PyInputProxy.h
        PyIterator.h
        PyCppNode.h
        PyNode.h
        PyNodeWrapper.h
        PyNumbaNode.h
        PyObjectPtr.h
        PyOutputAdapterWrapper.h
        PyOutputProxy.h
        PyConstants.h)

add_library(sp2impl SHARED
        sp2impl.cpp
        Conversions.cpp
        NumpyConversions.cpp
        PyAdapterManager.cpp
        PyAdapterManagerWrapper.cpp
        PyConstAdapter.cpp
        PyCppNode.cpp
        PyEngine.cpp
        PyGraphOutputAdapter.cpp
        PyInputAdapterWrapper.cpp
        PyBasketInputProxy.cpp
        PyBasketOutputProxy.cpp
        PyDynamicNode.cpp
        PyFeedbackAdapter.cpp
        PyInputProxy.cpp
        PyNode.cpp
        PyNodeWrapper.cpp
        PyNumbaNode.cpp
        PyNumpyAdapter.cpp
        PyOutputAdapter.cpp
        PyOutputAdapterWrapper.cpp
        PyOutputProxy.cpp
        PyPullInputAdapter.cpp
        PyPushInputAdapter.cpp
        PyPushPullInputAdapter.cpp
        PyManagedSimInputAdapter.cpp
        PyTimerAdapter.cpp
        PyConstants.cpp
        ${SP2IMPL_PUBLIC_HEADERS})

set_target_properties(sp2impl PROPERTIES PUBLIC_HEADER "${SP2IMPL_PUBLIC_HEADERS}")

target_link_libraries(sp2impl sp2typesimpl sp2_core sp2_engine)
target_compile_definitions(sp2impl PUBLIC NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION)

## Baselib c++ module
add_library(sp2baselibimpl SHARED sp2baselibimpl.cpp)
target_link_libraries(sp2baselibimpl sp2impl baselibimpl)

# Include exprtk include directory for exprtk node
target_include_directories(sp2baselibimpl PRIVATE ${EXPRTK_INCLUDE_DIRS})

## Basketlib c++ module
add_library(sp2basketlibimpl SHARED sp2basketlibimpl.cpp)
target_link_libraries(sp2basketlibimpl sp2impl basketlibimpl)

## Math c++ module
add_library(sp2mathimpl SHARED sp2mathimpl.cpp)
target_link_libraries(sp2mathimpl sp2impl mathimpl)

## Stats c++ module
add_library(sp2statsimpl SHARED sp2statsimpl.cpp)
target_link_libraries(sp2statsimpl sp2impl statsimpl)

## NumPy stats c++ module
add_library(npstatsimpl STATIC npstatsimpl.cpp)
add_library(sp2npstatsimpl SHARED sp2npstatsimpl.cpp)
target_link_libraries(sp2npstatsimpl sp2impl npstatsimpl)
target_include_directories(npstatsimpl PRIVATE ${NUMPY_INCLUDE_DIRS})
target_include_directories(sp2npstatsimpl PRIVATE ${NUMPY_INCLUDE_DIRS})

install(TARGETS sp2typesimpl sp2impl sp2baselibimpl sp2basketlibimpl sp2mathimpl sp2statsimpl sp2npstatsimpl
        PUBLIC_HEADER DESTINATION include/sp2/python
        RUNTIME DESTINATION bin/
        LIBRARY DESTINATION lib/
       )
