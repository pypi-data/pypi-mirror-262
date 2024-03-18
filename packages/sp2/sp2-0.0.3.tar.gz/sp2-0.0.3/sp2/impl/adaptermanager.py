"""This is for Python-defined adapters, not meant to be used for c++ implemented adapters"""

import sp2
from sp2.impl.__sp2impl import _sp2impl


class AdapterManagerImpl(_sp2impl.PyAdapterManager):
    def start(self, starttime, endtime):
        """start up the manager, connect to any external sources / files you need.  Spawn any threads you may need
        ( usually for realtime only )"""
        raise NotImplementedError("%s.start is not implemented" % type(self).__name__)

    def stop(self):
        """called on engine shutdown, optional"""
        pass

    def process_next_sim_timeslice(self, now):
        """
        this method should iterate over all data for the requested time, and push data onto all of the adapters inputs
        that need to tick
        :return: next datetime with data for this adapter manager

        NOTE: Simulation Adapters should overload this method!
        """
        return None


class ManagedSimInputAdapter(_sp2impl.PyManagedSimInputAdapter):
    def __init__(self, typ, field_map):
        if field_map is None or isinstance(field_map, dict):
            if not issubclass(typ, sp2.Struct):
                raise TypeError("type must be sp2.Struct when no fieldMap or dict fieldMap is used")
        elif not isinstance(field_map, str):
            raise TypeError("fieldMap should be str for single field mapping or dict for sp2.Struct mapping")

        self._type = typ
        self._field_map = field_map or {k: k for k in typ.metadata().keys()}

    def start(self, starttime, endtime):
        pass

    def stop(self):
        pass

    def process_dict(self, data: dict, keep_none=True):
        """convenience method to convert dict of data into typ using fieldMap"""
        if isinstance(self._field_map, str):
            orig_val = data[self._field_map]
            if orig_val is None:
                return
            if isinstance(orig_val, self._type):
                value = orig_val
            else:
                value = self._type(orig_val)
        else:
            final = {}
            for source_key, dest_key in self._field_map.items():
                dest_type = self._type.metadata()[dest_key]
                value = data[source_key]
                if keep_none or value is not None:
                    final[dest_key] = dest_type(value) if not isinstance(value, dest_type) else value

            value = self._type(**final)
        self.push_tick(value)
