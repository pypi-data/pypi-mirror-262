find_package(GTest CONFIG REQUIRED)

add_executable(test_basic_allocator test_basic_allocator.cpp)
target_link_libraries(test_basic_allocator GTest::gtest GTest::gtest_main)

add_executable(test_dynamicbitset test_dynamicbitset.cpp)
target_link_libraries(test_dynamicbitset GTest::gtest GTest::gtest_main)

add_executable(test_enum test_enum.cpp)
target_link_libraries(test_enum sp2_core sp2_engine GTest::gtest GTest::gtest_main)

add_executable(test_srmwlockfreequeue test_srmwlockfreequeue.cpp )
target_link_libraries(test_srmwlockfreequeue sp2_core GTest::gtest GTest::gtest_main)

add_executable(test_tagged_pointer_union test_tagged_pointer_union.cpp )
target_link_libraries(test_tagged_pointer_union sp2_core GTest::gtest GTest::gtest_main)

add_executable(test_time test_time.cpp )
target_link_libraries(test_time sp2_core GTest::gtest GTest::gtest_main)

install(TARGETS test_basic_allocator
                test_dynamicbitset
                test_enum
                test_srmwlockfreequeue
                test_tagged_pointer_union
                test_time
        RUNTIME DESTINATION tests/bin/
        LIBRARY DESTINATION tests/lib/
        ARCHIVE DESTINATION tests/lib/)
