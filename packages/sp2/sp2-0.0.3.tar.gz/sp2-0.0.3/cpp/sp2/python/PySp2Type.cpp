#include <sp2/python/PySp2Type.h>
#include <sp2/python/PyStruct.h>
#include <sp2/python/Conversions.h>
#include <Python.h>

static_assert( sizeof( sp2::DialectGenericType ) == sizeof( sp2::python::PyObjectPtr ) );
static_assert( alignof( sp2::DialectGenericType ) == alignof( sp2::python::PyObjectPtr ) );

namespace sp2
{
DialectGenericType::DialectGenericType()
{
    new( this ) sp2::python::PyObjectPtr();
}

DialectGenericType::~DialectGenericType()
{
    using T = sp2::python::PyObjectPtr;
    reinterpret_cast<T *>(this) -> ~T();
}

DialectGenericType::DialectGenericType( const DialectGenericType &rhs )
{
    new( this ) sp2::python::PyObjectPtr( reinterpret_cast<const sp2::python::PyObjectPtr &>(rhs) );
}

DialectGenericType::DialectGenericType( DialectGenericType &&rhs )
{
    new( this ) sp2::python::PyObjectPtr( reinterpret_cast<sp2::python::PyObjectPtr &&>(rhs) );
}

DialectGenericType DialectGenericType::deepcopy() const
{
    static PyObject * pyDeepcopy = PyObject_GetAttrString( PyImport_ImportModule( "copy" ), "deepcopy" );
    PyObject * pyVal = PyObject_CallFunction( pyDeepcopy, "(O)", python::toPythonBorrowed( *this ) );
    return DialectGenericType( reinterpret_cast<DialectGenericType &&>( std::move( sp2::python::PyObjectPtr::check( pyVal ) ) ) );
}

DialectGenericType &DialectGenericType::operator=( const DialectGenericType &rhs )
{
    *reinterpret_cast<sp2::python::PyObjectPtr *>(this) = reinterpret_cast<const sp2::python::PyObjectPtr &>(rhs);
    return *this;
}

DialectGenericType &DialectGenericType::operator=( DialectGenericType &&rhs )
{
    *reinterpret_cast<sp2::python::PyObjectPtr *>(this) = std::move( reinterpret_cast<sp2::python::PyObjectPtr &&>(rhs) );
    return *this;
}


bool DialectGenericType::operator==( const DialectGenericType &rhs ) const
{
    return *reinterpret_cast<const sp2::python::PyObjectPtr *>(this) == reinterpret_cast<const sp2::python::PyObjectPtr &>(rhs);
}

size_t DialectGenericType::hash() const
{
    return reinterpret_cast<const sp2::python::PyObjectPtr *>(this) -> hash();
}

std::ostream & operator<<( std::ostream & o, const DialectGenericType & obj )
{
    o << reinterpret_cast<const python::PyObjectPtr &>( obj );
    return o;
}

}
