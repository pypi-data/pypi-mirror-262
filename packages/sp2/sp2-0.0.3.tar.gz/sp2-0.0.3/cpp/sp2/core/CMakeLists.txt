set(CORE_PUBLIC_HEADERS
      BasicAllocator.h
      Config.h.in
      DynamicBitSet.h
      Enum.h
      EnumBitSet.h
      Exception.h
      FileUtils.h
      Generator.h
      Hash.h
      Likely.h
      QueueWaiter.h
      Platform.h
      SRMWLockFreeQueue.h
      System.h
      TaggedPointerUnion.h
      Time.h
      )

set(CORE_SOURCE_FILES
        Exception.cpp
        Time.cpp
        ${CORE_PUBLIC_HEADERS}
        )

configure_file(Config.h.in ${CMAKE_CURRENT_BINARY_DIR}/cpp/sp2/core/Config.h)

add_library(sp2_core STATIC ${CORE_SOURCE_FILES})
set_target_properties(sp2_core PROPERTIES PUBLIC_HEADER "${CORE_PUBLIC_HEADERS}")

install(TARGETS sp2_core
        PUBLIC_HEADER DESTINATION include/sp2/core
        RUNTIME DESTINATION bin/
        LIBRARY DESTINATION lib/
       )
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/cpp/sp2/core/Config.h DESTINATION include/sp2/core)
