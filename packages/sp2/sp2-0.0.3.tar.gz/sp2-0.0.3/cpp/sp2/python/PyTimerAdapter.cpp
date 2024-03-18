#include <sp2/engine/TimerInputAdapter.h>
#include <sp2/python/Conversions.h>
#include <sp2/python/Exception.h>
#include <sp2/python/PyEngine.h>
#include <sp2/python/PyInputAdapterWrapper.h>

namespace sp2::python
{

static InputAdapter * timer_creator( sp2::AdapterManager * manager, PyEngine * pyengine, PyObject * pyType, PushMode pushMode, PyObject * args )
{
    PyObject * pyInterval = nullptr;
    PyObject * pyValue    = nullptr;
    int        allowDeviation;

    if( !PyArg_ParseTuple( args, "OOp", &pyInterval, &pyValue, &allowDeviation ) )
        SP2_THROW( PythonPassthrough, "" );

    auto interval = fromPython<TimeDelta>( pyInterval );

    auto sp2Type = pyTypeAsSp2Type( pyType );

    return switchSp2Type( sp2Type,
                          [ engine = pyengine -> engine(), &sp2Type, interval, pyValue, allowDeviation ](
                                  auto tag ) -> InputAdapter *
                          {
                              using T = typename decltype(tag)::type;
                              return engine -> createOwnedObject<TimerInputAdapter<T>>(
                                      sp2Type, interval, fromPython<T>( pyValue, *sp2Type ), bool( allowDeviation ) );
                          } );
}

REGISTER_INPUT_ADAPTER( _timer, timer_creator );

}
