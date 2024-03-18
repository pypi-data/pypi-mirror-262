//this is included first so that we do include without NO_IMPORT_ARRAY defined, which is done in NumpyInputAdapter.h
#include <numpy/ndarrayobject.h>
//
// BUT!  really we can't have this here and in NumpyConversions.cpp....
//

#include <sp2/python/Conversions.h>
#include <sp2/python/Exception.h>
#include <sp2/python/NumpyInputAdapter.h>
#include <sp2/python/PyEngine.h>
#include <sp2/python/PyInputAdapterWrapper.h>


namespace sp2::python
{

static bool numpy_initialized = false;

static InputAdapter * numpy_adapter_creator( sp2::AdapterManager * manager, PyEngine * pyengine, PyObject * pyType, PushMode pushMode, PyObject * args )
{
    if( !numpy_initialized )
    {
        import_array()
        numpy_initialized = true;
    }

    PyObject * type;
    PyArrayObject * pyDatetimes = nullptr;
    PyArrayObject * pyValues    = nullptr;

    if( !PyArg_ParseTuple( args, "OO!O!",
                           &type,
                           &PyArray_Type, &pyDatetimes,
                           &PyArray_Type, &pyValues ) )
        SP2_THROW( PythonPassthrough, "" );

    auto sp2Type = pyTypeAsSp2Type( pyType );

    return switchSp2Type( sp2Type,
                          [ engine = pyengine -> engine(), &sp2Type, pyDatetimes, pyValues ](
                                  auto tag ) -> InputAdapter *
                          {
                              using T = typename decltype(tag)::type;
                              return engine -> createOwnedObject<NumpyInputAdapter<T>>(
                                      sp2Type, pyDatetimes, pyValues );
                          } );
}

REGISTER_INPUT_ADAPTER( _npcurve, numpy_adapter_creator );

}
