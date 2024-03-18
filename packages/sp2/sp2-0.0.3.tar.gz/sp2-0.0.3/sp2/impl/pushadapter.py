from sp2.impl.__sp2impl import _sp2impl

PushGroup = _sp2impl.PushGroup
PushBatch = _sp2impl.PushBatch


class PushInputAdapter(_sp2impl.PyPushInputAdapter):
    def start(self, starttime, endtime):
        pass

    def stop(self):
        pass

    # base class
    # def push_tick( self, value )
