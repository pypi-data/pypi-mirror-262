#include <sp2/python/Conversions.h>
#include <datetime.h>

namespace sp2::python
{

PyObject * lastValueToPython( const sp2::TimeSeriesProvider * ts )
{
    return switchSp2Type( ts -> type(),
                          [ ts ]( auto tag )
                          {
                              return toPython( ts -> lastValueTyped<typename decltype(tag)::type>(), *ts -> type() );
                          } );
}

PyObject * valueAtIndexToPython( const sp2::TimeSeriesProvider * ts, int32_t index)
{
    return switchSp2Type( ts -> type(),
                          [ ts, index ]( auto tag )
                          {
                              return toPython( ts -> valueAtIndex<typename decltype(tag)::type>( index ), *ts -> type() );
                          } );
}

}
