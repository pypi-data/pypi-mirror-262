#ifndef _IN_SP2_ENGINE_DYNAMIC_H
#define _IN_SP2_ENGINE_DYNAMIC_H

#include <sp2/engine/Sp2Type.h>
#include <sp2/engine/CycleStepTable.h>
#include <sp2/engine/Node.h>
#include <functional>
#include <string>

namespace sp2
{

class DynamicEngine;

//DynamicNode Is an instance of an outter node that is responsible for a single sp2.dynamic() call in the graph
//Internally it will maintain N DynamicEngines, 1 per instantiated key.  It is responsible for reacting to all
//external inputs and triggering a cycle step.
//All dynamic engine input adapters as well as all external timeseries wired into dynamic are registered as inputs
//into the DynanicNode instance so that it can invoke cycle step at the appropriate times.
class DynamicNode final : public Node
{
public:
    using Outputs = std::vector<const TimeSeriesProvider *>;
    using EngineBuilder = std::function<Outputs( DynamicNode *, DynamicEngine *, const DialectGenericType & key )>;

    DynamicNode( Engine * engine, const std::string & nodename,
                 std::vector<INOUT_ID_TYPE> snapIds,
                 EngineBuilder builder,
                 NodeDef def );
    ~DynamicNode();

    void executeImpl() override;
    void start() override;
    void stop() override;

    const char * name() const override { return m_name.c_str(); }

    void handleEvent( InputId id ) override;

    int64_t elemId( const DialectGenericType & key );

private:
    using InstanceMap = std::unordered_map<DialectGenericType, std::unique_ptr<DynamicEngine>>;

    void addDynamicInstance( const DialectGenericType & key );
    void removeDynamicInstance( const DialectGenericType & key );

    //All instance engines share a single CycleStepTable on the DynamicNode
    CycleStepTable m_cycleStepTable;
    InstanceMap    m_instanceMap;
    EngineBuilder  m_engineBuilder;
    std::string    m_name;

    //set of keys requesting dynamic shutdown via sp2.stop_engine calls
    std::unordered_set<DialectGenericType> m_dynamicShutdowns;

    std::vector<INOUT_ID_TYPE> m_snapIds; //temporary storage to make them passive

    //We may be able to remove this once we move key management into DynamicBasketInfo
    //only need to maintain one per DynamicNode, since keys are always added/removed in lockstep
    std::unordered_map<DialectGenericType,INOUT_ELEMID_TYPE> m_dynamicKeyMap;
    std::vector<DialectGenericType>                          m_dynamicElemIdMap;
};

}

#endif
