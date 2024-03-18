#ifndef _IN_SP2_PYTHON_SP2ENUM_H
#define _IN_SP2_PYTHON_SP2ENUM_H

#include <sp2/engine/Sp2Enum.h>
#include <sp2/python/PyObjectPtr.h>
#include <memory>
#include <string>

namespace sp2::python
{

//This is the base class of sp2.Enum
struct PySp2EnumMeta : public PyHeapTypeObject
{
    //convert to PyObject ( new ref )
    PyObject * toPyEnum( Sp2Enum e ) const;

    std::shared_ptr<Sp2EnumMeta> enumMeta;

    PyObjectPtr enumsByName;
    PyObjectPtr enumsByValue;

    //for fast toPython calls
    std::unordered_map<int64_t,PyObjectPtr> enumsByCValue;

    static PyTypeObject PyType;
};

//This is an extension of sp2::Sp2EnumMeta for python dialect, we need it in order to
//keep a reference to the python enum type from conversion to/from sp2::Sp2EnumMeta <-> PyObject properly
class DialectSp2EnumMeta : public Sp2EnumMeta
{
public:
    DialectSp2EnumMeta( PyTypeObjectPtr pyType, const std::string & name,
                        const Sp2EnumMeta::ValueDef & def );
    ~DialectSp2EnumMeta() {}

    const PyTypeObjectPtr & pyType() const { return m_pyType; }

    const PySp2EnumMeta * pyMeta() const   { return ( const PySp2EnumMeta * ) m_pyType.get(); }

private:

    PyTypeObjectPtr m_pyType;
};

struct PySp2Enum : public PyObject
{
    PySp2Enum( const Sp2Enum & e ) : enum_( e ) {}
    ~PySp2Enum() {}

    Sp2Enum enum_;
    PyObjectPtr enumName;
    PyObjectPtr enumValue;

    PySp2EnumMeta * pyMeta() { return ( PySp2EnumMeta * ) ob_type; };
    const DialectSp2EnumMeta * meta() { return static_cast<const DialectSp2EnumMeta*>( pyMeta() -> enumMeta.get() ); }

    static PyTypeObject PyType;
};

}

#endif
