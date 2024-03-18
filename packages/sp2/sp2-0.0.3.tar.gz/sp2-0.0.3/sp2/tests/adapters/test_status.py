import os
import pytest
from datetime import datetime, timedelta

import sp2
from sp2 import ts
from sp2.adapters.kafka import DateTimeType, JSONTextMessageMapper, KafkaStatusMessageType
from sp2.adapters.status import Level

from .kafka_utils import _precreate_topic


class SubData(sp2.Struct):
    a: bool


class TestStatus:
    @pytest.mark.skipif(not os.environ.get("SP2_TEST_KAFKA"), reason="Skipping kafka adapter tests")
    def test_basic(self, kafkaadapter):
        topic = f"sp2.unittest.{os.getpid()}"
        key = "test_status"

        def graph():
            # publish as string
            a = sp2.timer(timedelta(seconds=1), "string")

            msg_mapper = JSONTextMessageMapper(datetime_type=DateTimeType.UINT64_MICROS)

            kafkaadapter.publish(msg_mapper, topic, key, a, field_map="a")

            # subscribe as bool
            sub_data = kafkaadapter.subscribe(
                ts_type=SubData, msg_mapper=msg_mapper, topic=topic, key=key, push_mode=sp2.PushMode.NON_COLLAPSING
            )
            status = kafkaadapter.status()

            sp2.add_graph_output("sub_data", sub_data)
            sp2.add_graph_output("status", status)

            # stop after first message
            done_flag = sp2.count(status) == 1
            sp2.stop_engine(done_flag)

        _precreate_topic(topic)
        results = sp2.run(graph, starttime=datetime.utcnow(), endtime=timedelta(seconds=10), realtime=True)
        status = results["status"][0][1]
        assert status.status_code == KafkaStatusMessageType.MSG_RECV_ERROR
        assert status.level == Level.ERROR


if __name__ == "__main__":
    pytest.main()
