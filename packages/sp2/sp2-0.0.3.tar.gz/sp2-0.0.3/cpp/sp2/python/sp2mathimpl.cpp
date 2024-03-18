#include <sp2/python/PyCppNode.h>
#include <sp2/engine/CppNode.h>
#include <sp2/python/Conversions.h>

// Math ops
REGISTER_CPPNODE( sp2::cppnodes, add_f );
REGISTER_CPPNODE( sp2::cppnodes, add_i );
REGISTER_CPPNODE( sp2::cppnodes, sub_f );
REGISTER_CPPNODE( sp2::cppnodes, sub_i );
REGISTER_CPPNODE( sp2::cppnodes, mul_f );
REGISTER_CPPNODE( sp2::cppnodes, mul_i );
REGISTER_CPPNODE( sp2::cppnodes, div_f );
REGISTER_CPPNODE( sp2::cppnodes, div_i );
REGISTER_CPPNODE( sp2::cppnodes, pow_f );
REGISTER_CPPNODE( sp2::cppnodes, pow_i );
REGISTER_CPPNODE( sp2::cppnodes, max_f );
REGISTER_CPPNODE( sp2::cppnodes, max_i );
REGISTER_CPPNODE( sp2::cppnodes, min_f );
REGISTER_CPPNODE( sp2::cppnodes, min_i );
REGISTER_CPPNODE( sp2::cppnodes, abs_f );
REGISTER_CPPNODE( sp2::cppnodes, abs_i );
REGISTER_CPPNODE( sp2::cppnodes, ln_f );
REGISTER_CPPNODE( sp2::cppnodes, ln_i );
REGISTER_CPPNODE( sp2::cppnodes, log2_f );
REGISTER_CPPNODE( sp2::cppnodes, log2_i );
REGISTER_CPPNODE( sp2::cppnodes, log10_f );
REGISTER_CPPNODE( sp2::cppnodes, log10_i );
REGISTER_CPPNODE( sp2::cppnodes, exp_f );
REGISTER_CPPNODE( sp2::cppnodes, exp_i );
REGISTER_CPPNODE( sp2::cppnodes, exp2_f );
REGISTER_CPPNODE( sp2::cppnodes, exp2_i );
REGISTER_CPPNODE( sp2::cppnodes, sqrt_f );
REGISTER_CPPNODE( sp2::cppnodes, sqrt_i );
REGISTER_CPPNODE( sp2::cppnodes, erf_f );
REGISTER_CPPNODE( sp2::cppnodes, erf_i );
REGISTER_CPPNODE( sp2::cppnodes, sin_f );
REGISTER_CPPNODE( sp2::cppnodes, sin_i );
REGISTER_CPPNODE( sp2::cppnodes, cos_f );
REGISTER_CPPNODE( sp2::cppnodes, cos_i );
REGISTER_CPPNODE( sp2::cppnodes, tan_f );
REGISTER_CPPNODE( sp2::cppnodes, tan_i );
REGISTER_CPPNODE( sp2::cppnodes, asin_f );
REGISTER_CPPNODE( sp2::cppnodes, asin_i );
REGISTER_CPPNODE( sp2::cppnodes, acos_f );
REGISTER_CPPNODE( sp2::cppnodes, acos_i );
REGISTER_CPPNODE( sp2::cppnodes, atan_f );
REGISTER_CPPNODE( sp2::cppnodes, atan_i );
REGISTER_CPPNODE( sp2::cppnodes, sinh_f );
REGISTER_CPPNODE( sp2::cppnodes, sinh_i );
REGISTER_CPPNODE( sp2::cppnodes, cosh_f );
REGISTER_CPPNODE( sp2::cppnodes, cosh_i );
REGISTER_CPPNODE( sp2::cppnodes, tanh_f );
REGISTER_CPPNODE( sp2::cppnodes, tanh_i );
REGISTER_CPPNODE( sp2::cppnodes, asinh_f );
REGISTER_CPPNODE( sp2::cppnodes, asinh_i );
REGISTER_CPPNODE( sp2::cppnodes, acosh_f );
REGISTER_CPPNODE( sp2::cppnodes, acosh_i );
REGISTER_CPPNODE( sp2::cppnodes, atanh_f );
REGISTER_CPPNODE( sp2::cppnodes, atanh_i );

REGISTER_CPPNODE( sp2::cppnodes, bitwise_not );

// Comparisons
REGISTER_CPPNODE( sp2::cppnodes, not_ );
REGISTER_CPPNODE( sp2::cppnodes, eq_f );
REGISTER_CPPNODE( sp2::cppnodes, eq_i );
REGISTER_CPPNODE( sp2::cppnodes, ne_f );
REGISTER_CPPNODE( sp2::cppnodes, ne_i );
REGISTER_CPPNODE( sp2::cppnodes, gt_f );
REGISTER_CPPNODE( sp2::cppnodes, gt_i );
REGISTER_CPPNODE( sp2::cppnodes, lt_f );
REGISTER_CPPNODE( sp2::cppnodes, lt_i );
REGISTER_CPPNODE( sp2::cppnodes, ge_f );
REGISTER_CPPNODE( sp2::cppnodes, ge_i );
REGISTER_CPPNODE( sp2::cppnodes, le_f );
REGISTER_CPPNODE( sp2::cppnodes, le_i );

static PyModuleDef _sp2mathimpl_module = {
    PyModuleDef_HEAD_INIT,
    "_sp2mathimpl",
    "_sp2mathimpl c++ module",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit__sp2mathimpl(void)
{
    PyObject* m;

    m = PyModule_Create( &_sp2mathimpl_module);
    if( m == NULL )
        return NULL;

    if( !sp2::python::InitHelper::instance().execute( m ) )
        return NULL;

    return m;
}
