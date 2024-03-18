find_package(GTest CONFIG REQUIRED)

add_executable(test_dictionary test_dictionary.cpp )
target_link_libraries(test_dictionary sp2_engine GTest::gtest GTest::gtest_main)

add_executable(test_tick_buffer test_tick_buffer.cpp)
target_link_libraries(test_tick_buffer sp2_engine GTest::gtest GTest::gtest_main)

add_executable(test_time_series test_time_series.cpp)
target_link_libraries(test_time_series sp2_engine GTest::gtest GTest::gtest_main pthread)

add_executable(test_partial_switch_sp2_type test_partial_switch_sp2_type.cpp)
target_link_libraries(test_partial_switch_sp2_type sp2_engine GTest::gtest GTest::gtest_main)

add_executable(test_window_buffer test_window_buffer.cpp)
target_link_libraries(test_window_buffer sp2_engine GTest::gtest GTest::gtest_main)

install(TARGETS test_tick_buffer test_time_series test_partial_switch_sp2_type test_dictionary test_window_buffer
        RUNTIME DESTINATION tests/bin/
        LIBRARY DESTINATION tests/lib/
        ARCHIVE DESTINATION tests/lib/)
