#include <sp2/engine/Feedback.h>
#include <sp2/python/Conversions.h>
#include <sp2/python/PyEngine.h>
#include <sp2/python/PyInputAdapterWrapper.h>
#include <sp2/python/PyOutputAdapterWrapper.h>

namespace sp2::python
{

static OutputAdapter * output_creator( sp2::AdapterManager * manager, PyEngine * pyengine, PyObject * args )
{
    PyObject * pyType;
    PyInputAdapterWrapper * pyFeedbackInput = nullptr;

    if( !PyArg_ParseTuple( args, "OO!",
                           &pyType,
                           &PyInputAdapterWrapper::PyType, &pyFeedbackInput ) )
        SP2_THROW( PythonPassthrough, "" );

    auto & sp2Type = pyTypeAsSp2Type( pyType );
    return switchSp2Type( sp2Type,
                          [ pyengine, pyFeedbackInput ]( auto tag ) -> OutputAdapter *
                          {
                              using T = typename decltype(tag)::type;
                              return pyengine -> engine()
                                              -> createOwnedObject<FeedbackOutputAdapter<T>>( pyFeedbackInput -> adapter() );
                          } );
}

static InputAdapter * input_creator( sp2::AdapterManager * manager, PyEngine * engine,
                                     PyObject * pyType, PushMode pushMode, PyObject * args )
{
    auto & sp2Type = pyTypeAsSp2Type( pyType );
    return switchSp2Type( sp2Type.get(),
                          [ engine, &sp2Type, pushMode ]( auto tag ) -> InputAdapter *
                          {
                              using T = typename decltype(tag)::type;
                              return engine -> engine() -> createOwnedObject<FeedbackInputAdapter<T>>( sp2Type, pushMode );
                          } );
}

REGISTER_INPUT_ADAPTER( _feedback_input_adapter, input_creator );
REGISTER_OUTPUT_ADAPTER( _feedback_output_adapter, output_creator );

}
