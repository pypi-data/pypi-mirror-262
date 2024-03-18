sp2_autogen( sp2.impl.types.autogen_types autogen_types ENGINE_AUTOGEN_HEADER ENGINE_AUTOGEN_SOURCE )

set(SP2_TYPES_PUBLIC_HEADERS
        Sp2Enum.h
        Sp2Type.h
        DialectGenericType.h
        PartialSwitchSp2Type.h
        Struct.h
        TypeCast.h
)

set(SP2_TYPES_SOURCE_FILES
        Sp2Enum.cpp
        Sp2Type.cpp
        DialectGenericType.h
        PartialSwitchSp2Type.h
        Struct.cpp
        TypeCast.h
)

set(ENGINE_PUBLIC_HEADERS
        ${ENGINE_AUTOGEN_HEADER}
        AdapterManager.h
        AlarmInputAdapter.h
        BasketInfo.h
        ConstInputAdapter.h
        Consumer.h
        CppNode.h
        CycleStepTable.h
        Dictionary.h
        DynamicEngine.h
        DynamicNode.h
        Engine.h
        Enums.h
        EventPropagator.h
        Feedback.h
        GraphOutputAdapter.h
        InputAdapter.h
        InputId.h
        Node.h
        OutputAdapter.h
        PendingPushEvents.h
        Profiler.h
        PushEvent.h
        PullInputAdapter.h
        PushInputAdapter.h
        PushPullInputAdapter.h
        RootEngine.h
        Scheduler.h
        StatusAdapter.h
        TickBuffer.h
        TimerInputAdapter.h
        TimeSeries.h
        TimeSeriesProvider.h
        VectorContainer.h
        WindowBuffer.h
        )

set(ENGINE_SOURCE_FILES
        ${ENGINE_AUTOGEN_SOURCE}
        AdapterManager.cpp
        BasketInfo.cpp
        Consumer.cpp
        CycleStepTable.cpp
        Dictionary.cpp
        DynamicEngine.cpp
        DynamicNode.cpp
        Engine.cpp
        Enums.cpp
        EventPropagator.cpp
        GraphOutputAdapter.cpp
        InputAdapter.cpp
        Node.cpp
        OutputAdapter.cpp
        PendingPushEvents.cpp
        PushPullInputAdapter.cpp
        RootEngine.cpp
        Scheduler.cpp
        StatusAdapter.cpp
        TimeSeries.cpp
        TimeSeriesProvider.cpp
        VectorContainer.cpp
        ${ENGINE_PUBLIC_HEADERS}
        )

add_library(sp2_types STATIC ${SP2_TYPES_SOURCE_FILES})
set_target_properties(sp2_types PROPERTIES PUBLIC_HEADER "${SP2_TYPES_PUBLIC_HEADERS}")

add_library(sp2_engine STATIC ${ENGINE_SOURCE_FILES})
set_target_properties(sp2_engine PROPERTIES PUBLIC_HEADER "${ENGINE_PUBLIC_HEADERS}")
target_link_libraries(sp2_engine sp2_core sp2_types)

install(FILES ${SP2_TYPES_PUBLIC_HEADERS} ${ENGINE_PUBLIC_HEADERS} DESTINATION include/sp2/engine)

install(TARGETS sp2_types sp2_engine
        PUBLIC_HEADER DESTINATION include/sp2/engine
        RUNTIME DESTINATION bin/
        LIBRARY DESTINATION lib/
       )
