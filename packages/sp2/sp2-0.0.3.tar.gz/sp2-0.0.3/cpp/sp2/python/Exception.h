#ifndef _IN_SP2_PYTHON_EXCEPTION_H
#define _IN_SP2_PYTHON_EXCEPTION_H

#include <sp2/core/Exception.h>
#include <Python.h>
#include <string>

namespace sp2::python
{

class PythonPassthrough : public sp2::Exception
{
public:
    PythonPassthrough( const char * exType, const std::string &r, const char * file,
                       const char * func, int line ) :
        sp2::Exception( exType, r, file, func, line )
    {
        //Fetch the current error to clear out the error indicator while the stack gets unwound
        PyErr_Fetch( &m_type, &m_value, &m_traceback );
    }

    void restore()
    {
        if( !description().empty() )
        {
            std::string p = description() + ": ";
            PyObject * prefix = PyUnicode_FromString( p.c_str() );
            PyObject * newmsg = PyUnicode_Concat( prefix, m_value );
            Py_DECREF( m_value );
            Py_DECREF( prefix );
            m_value = newmsg;
        }

        PyErr_Restore( m_type, m_value, m_traceback );
        m_type = m_value = m_traceback = nullptr;
    }

private:
    PyObject * m_type;
    PyObject * m_value;
    PyObject * m_traceback;

};

SP2_DECLARE_EXCEPTION( AttributeError, ::sp2::Exception );

inline bool& capture_cpp_exception_trace_flag()
{
    static bool val = false; return val;
}

#define SP2_CATCH_HELPER( EXC_TYPE, PYEXC_TYPE, RETURN_STMT ) catch( const EXC_TYPE & err ) { PyErr_SetString( PYEXC_TYPE, err.full(sp2::python::capture_cpp_exception_trace_flag()).c_str() ); RETURN_STMT }
#define SP2_CATCH_HELPER_STD( EXC_TYPE, PYEXC_TYPE, RETURN_STMT ) catch( const EXC_TYPE & err ) { PyErr_SetString( PYEXC_TYPE, err.what() ); RETURN_STMT }

#define SP2_CATCH_HELPERS( RETURN_STMT )  \
    SP2_CATCH_HELPER( ::sp2::python::AttributeError,   PyExc_AttributeError, RETURN_STMT ) \
    SP2_CATCH_HELPER( ::sp2::InvalidArgument,   PyExc_TypeError,         RETURN_STMT )     \
    SP2_CATCH_HELPER( ::sp2::NotImplemented,    PyExc_NotImplementedError, RETURN_STMT )   \
    SP2_CATCH_HELPER( ::sp2::KeyError,          PyExc_KeyError,          RETURN_STMT )     \
    SP2_CATCH_HELPER( ::sp2::ValueError,        PyExc_ValueError,        RETURN_STMT )     \
    SP2_CATCH_HELPER( ::sp2::TypeError,         PyExc_TypeError,         RETURN_STMT )     \
    SP2_CATCH_HELPER( ::sp2::RangeError,        PyExc_IndexError,        RETURN_STMT )     \
    SP2_CATCH_HELPER( ::sp2::OverflowError,     PyExc_OverflowError,     RETURN_STMT )     \
    SP2_CATCH_HELPER( ::sp2::DivideByZero,      PyExc_ZeroDivisionError, RETURN_STMT )     \
    SP2_CATCH_HELPER( ::sp2::RecursionError,    PyExc_RecursionError,    RETURN_STMT )     \
    SP2_CATCH_HELPER( ::sp2::OSError,           PyExc_OSError,           RETURN_STMT )     \
    SP2_CATCH_HELPER( ::sp2::OutOfMemoryError,  PyExc_MemoryError,       RETURN_STMT )     \
    SP2_CATCH_HELPER( ::sp2::FileNotFoundError, PyExc_FileNotFoundError, RETURN_STMT )     \
    SP2_CATCH_HELPER( ::sp2::RuntimeException,  PyExc_RuntimeError,      RETURN_STMT )     \
    SP2_CATCH_HELPER( ::sp2::Exception,         PyExc_Exception,         RETURN_STMT )     \
    SP2_CATCH_HELPER_STD( std::exception,       PyExc_Exception,         RETURN_STMT )

#define SP2_BEGIN_METHOD try {
#define SP2_RETURN } catch( ::sp2::python::PythonPassthrough & err ) { err.restore(); return; } SP2_CATCH_HELPERS( return; )

#define SP2_RETURN_INT  } catch( ::sp2::python::PythonPassthrough & err ) { err.restore(); return -1;      } SP2_CATCH_HELPERS( return -1; ); return 0;
#define SP2_RETURN_NONE } catch( ::sp2::python::PythonPassthrough & err ) { err.restore(); return nullptr; } SP2_CATCH_HELPERS( return nullptr; ); Py_RETURN_NONE;
#define SP2_RETURN_NULL } catch( ::sp2::python::PythonPassthrough & err ) { err.restore(); return nullptr; } SP2_CATCH_HELPERS( return nullptr; ); return nullptr;

}

#endif
