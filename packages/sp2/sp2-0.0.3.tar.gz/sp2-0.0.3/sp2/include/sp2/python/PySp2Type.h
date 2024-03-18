#ifndef _IN_SP2_PYTHON_PYSP2TYPE_H
#define _IN_SP2_PYTHON_PYSP2TYPE_H

#include <sp2/engine/Sp2Type.h>
#include <sp2/python/PyObjectPtr.h>

static_assert( sizeof( sp2::DialectGenericType ) == sizeof( sp2::python::PyObjectPtr ) );
static_assert( alignof( sp2::DialectGenericType ) == alignof( sp2::python::PyObjectPtr ) );


//hook in fromCtype conversion
namespace sp2
{
template<>
template<>
struct Sp2Type::Type::fromCType<sp2::python::PyObjectPtr>
{
    static constexpr sp2::Sp2Type::Type type = sp2::Sp2Type::Type::DIALECT_GENERIC;
};

}

#endif
