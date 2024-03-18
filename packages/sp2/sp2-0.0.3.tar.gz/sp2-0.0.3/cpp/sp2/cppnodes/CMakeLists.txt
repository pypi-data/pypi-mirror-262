add_library(baselibimpl STATIC baselibimpl.cpp)
target_link_libraries(baselibimpl sp2_core sp2_engine)

add_library(basketlibimpl STATIC basketlibimpl.cpp)
target_link_libraries(basketlibimpl baselibimpl sp2_core sp2_engine)

add_library(mathimpl STATIC mathimpl.cpp)
target_link_libraries(mathimpl sp2_core sp2_engine)

add_library(statsimpl STATIC statsimpl.cpp)
set_target_properties(statsimpl PROPERTIES PUBLIC_HEADER statsimpl.h)
target_link_libraries(statsimpl baselibimpl sp2_core sp2_engine)

install(TARGETS baselibimpl basketlibimpl mathimpl statsimpl
        PUBLIC_HEADER DESTINATION include/sp2/cppnodes
        RUNTIME DESTINATION bin/
        LIBRARY DESTINATION lib/
       )
