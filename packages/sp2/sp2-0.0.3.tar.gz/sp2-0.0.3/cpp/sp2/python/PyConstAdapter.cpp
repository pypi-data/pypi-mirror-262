#include <sp2/engine/ConstInputAdapter.h>
#include <sp2/python/Conversions.h>
#include <sp2/python/PyEngine.h>
#include <sp2/python/Exception.h>
#include <sp2/python/PyInputAdapterWrapper.h>

namespace sp2::python
{

static InputAdapter * const_creator( sp2::AdapterManager * manager, PyEngine * engine,
                                     PyObject * pyType, PushMode pushMode, PyObject * args )
{
    PyObject * pyValue  = nullptr;
    PyObject * pyDelay  = nullptr;

    if( !PyArg_ParseTuple( args, "OO",
                           &pyValue,
                           &pyDelay ) )
        SP2_THROW( PythonPassthrough, "" );

    auto delay = fromPython<TimeDelta>( pyDelay );

    auto & sp2Type = pyTypeAsSp2Type( pyType );

    InputAdapter *adapter = switchSp2Type( sp2Type,
                                           [ engine, &sp2Type, pyValue, delay ]( auto tag ) -> InputAdapter *
                                           {
                                               using T = typename decltype(tag)::type;
                                               return engine -> engine() -> createOwnedObject<ConstInputAdapter<T>>( sp2Type,
                                                                                                                     fromPython<T>(
                                                                                                                             pyValue,
                                                                                                                             *sp2Type ),
                                                                                                                     delay );
                                           } );
    return adapter;
}

REGISTER_INPUT_ADAPTER( _const, const_creator );

}
