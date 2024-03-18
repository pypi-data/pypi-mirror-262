#include <sp2/engine/CppNode.h>
#include <sp2/python/PyCppNode.h>

// Data processing nodes
REGISTER_CPPNODE( sp2::cppnodes,  _tick_window_updates );
REGISTER_CPPNODE( sp2::cppnodes,  _time_window_updates );
REGISTER_CPPNODE( sp2::cppnodes,  _cross_sectional_as_list );
REGISTER_CPPNODE( sp2::cppnodes,  _min_hit_by_tick );
REGISTER_CPPNODE( sp2::cppnodes,  _in_sequence_check );
REGISTER_CPPNODE( sp2::cppnodes,  _sync_nan_f );

// Base statistics
REGISTER_CPPNODE( sp2::cppnodes,  _count );
REGISTER_CPPNODE( sp2::cppnodes,  _sum );
REGISTER_CPPNODE( sp2::cppnodes,  _kahan_sum );
REGISTER_CPPNODE( sp2::cppnodes,  _mean );
REGISTER_CPPNODE( sp2::cppnodes,  _var );
REGISTER_CPPNODE( sp2::cppnodes,  _first );
REGISTER_CPPNODE( sp2::cppnodes,  _unique );
REGISTER_CPPNODE( sp2::cppnodes,  _prod );
REGISTER_CPPNODE( sp2::cppnodes,  _weighted_mean );
REGISTER_CPPNODE( sp2::cppnodes,  _weighted_var );
REGISTER_CPPNODE( sp2::cppnodes,  _covar );
REGISTER_CPPNODE( sp2::cppnodes,  _weighted_covar );
REGISTER_CPPNODE( sp2::cppnodes,  _corr );
REGISTER_CPPNODE( sp2::cppnodes,  _weighted_corr );
REGISTER_CPPNODE( sp2::cppnodes,  _sem );
REGISTER_CPPNODE( sp2::cppnodes,  _weighted_sem );
REGISTER_CPPNODE( sp2::cppnodes,  _last );
REGISTER_CPPNODE( sp2::cppnodes,  _quantile );
REGISTER_CPPNODE( sp2::cppnodes,  _min_max );
REGISTER_CPPNODE( sp2::cppnodes,  _rank );
REGISTER_CPPNODE( sp2::cppnodes,  _arg_min_max );
REGISTER_CPPNODE( sp2::cppnodes,  _skew );
REGISTER_CPPNODE( sp2::cppnodes,  _weighted_skew );
REGISTER_CPPNODE( sp2::cppnodes,  _kurt );
REGISTER_CPPNODE( sp2::cppnodes,  _weighted_kurt );

// EMA nodes
REGISTER_CPPNODE( sp2::cppnodes,  _ema_compute );
REGISTER_CPPNODE( sp2::cppnodes,  _ema_adjusted );
REGISTER_CPPNODE( sp2::cppnodes,  _ema_timewise );
REGISTER_CPPNODE( sp2::cppnodes,  _ema_debias_alpha );
REGISTER_CPPNODE( sp2::cppnodes,  _ema_debias_halflife );

static PyModuleDef _sp2statsimpl_module = {
    PyModuleDef_HEAD_INIT,
    "_sp2statsimpl",
    "_sp2statsimpl c++ module",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit__sp2statsimpl(void)
{
    PyObject* m;

    m = PyModule_Create( &_sp2statsimpl_module);
    if( m == NULL )
        return NULL;

    if( !sp2::python::InitHelper::instance().execute( m ) )
        return NULL;

    return m;
}
