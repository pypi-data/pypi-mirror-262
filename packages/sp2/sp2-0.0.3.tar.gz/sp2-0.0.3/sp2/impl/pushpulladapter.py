from sp2.impl.__sp2impl import _sp2impl

PushGroup = _sp2impl.PushGroup
PushBatch = _sp2impl.PushBatch


class PushPullInputAdapter(_sp2impl.PyPushPullInputAdapter):
    def start(self, starttime, endtime):
        pass

    def stop(self):
        pass

    # base class
    # def push_tick( self, time, value )
