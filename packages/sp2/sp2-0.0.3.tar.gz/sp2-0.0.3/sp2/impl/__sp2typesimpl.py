try:
    # Import available at the top level when running sp2_autogen
    import _sp2typesimpl
except ModuleNotFoundError:
    from sp2.lib import _sp2typesimpl
