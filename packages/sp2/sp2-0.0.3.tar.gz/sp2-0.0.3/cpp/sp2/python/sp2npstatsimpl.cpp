#include <sp2/engine/CppNode.h>
#include <sp2/python/PyCppNode.h>

// Register nodes and create module

// Data processing
REGISTER_CPPNODE( sp2::python,  _np_tick_window_updates );
REGISTER_CPPNODE( sp2::python,  _np_time_window_updates );
REGISTER_CPPNODE( sp2::python,  _cross_sectional_as_np );
REGISTER_CPPNODE( sp2::python,  _np_cross_sectional_as_list );
REGISTER_CPPNODE( sp2::python,  _np_cross_sectional_as_np );
REGISTER_CPPNODE( sp2::python,  _list_to_np );
REGISTER_CPPNODE( sp2::python,  _np_to_list );
REGISTER_CPPNODE( sp2::python,  _sync_nan_np );

// Computation nodes
REGISTER_CPPNODE( sp2::python,  _np_count );
REGISTER_CPPNODE( sp2::python,  _np_first );
REGISTER_CPPNODE( sp2::python,  _np_last );
REGISTER_CPPNODE( sp2::python,  _np_sum );
REGISTER_CPPNODE( sp2::python,  _np_kahan_sum );
REGISTER_CPPNODE( sp2::python,  _np_mean );
REGISTER_CPPNODE( sp2::python,  _np_prod );
REGISTER_CPPNODE( sp2::python,  _np_unique );
REGISTER_CPPNODE( sp2::python,  _np_quantile );
REGISTER_CPPNODE( sp2::python,  _np_min_max );
REGISTER_CPPNODE( sp2::python,  _np_rank );
REGISTER_CPPNODE( sp2::python,  _np_arg_min_max );
REGISTER_CPPNODE( sp2::python,  _np_weighted_mean );
REGISTER_CPPNODE( sp2::python,  _np_var );
REGISTER_CPPNODE( sp2::python,  _np_weighted_var );
REGISTER_CPPNODE( sp2::python,  _np_sem );
REGISTER_CPPNODE( sp2::python,  _np_weighted_sem );
REGISTER_CPPNODE( sp2::python,  _np_covar );
REGISTER_CPPNODE( sp2::python,  _np_weighted_covar );
REGISTER_CPPNODE( sp2::python,  _np_corr );
REGISTER_CPPNODE( sp2::python,  _np_weighted_corr );
REGISTER_CPPNODE( sp2::python,  _np_cov_matrix );
REGISTER_CPPNODE( sp2::python,  _np_weighted_cov_matrix );
REGISTER_CPPNODE( sp2::python,  _np_corr_matrix );
REGISTER_CPPNODE( sp2::python,  _np_weighted_corr_matrix );
REGISTER_CPPNODE( sp2::python,  _np_skew );
REGISTER_CPPNODE( sp2::python,  _np_weighted_skew );
REGISTER_CPPNODE( sp2::python,  _np_kurt );
REGISTER_CPPNODE( sp2::python,  _np_weighted_kurt );

// EMA nodes
REGISTER_CPPNODE( sp2::python,  _np_ema_compute );
REGISTER_CPPNODE( sp2::python,  _np_ema_adjusted );
REGISTER_CPPNODE( sp2::python,  _np_ema_timewise );
REGISTER_CPPNODE( sp2::python,  _np_ema_debias_alpha );
REGISTER_CPPNODE( sp2::python,  _np_ema_debias_halflife );


static PyModuleDef _sp2npstatsimpl_module = {
    PyModuleDef_HEAD_INIT,
    "_sp2npstatsimpl",
    "_sp2npstatsimpl c++ module",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit__sp2npstatsimpl(void)
{
    PyObject* m;

    m = PyModule_Create( &_sp2npstatsimpl_module);
    if( m == NULL )
        return NULL;

    if( !sp2::python::InitHelper::instance().execute( m ) )
        return NULL;

    return m;
}