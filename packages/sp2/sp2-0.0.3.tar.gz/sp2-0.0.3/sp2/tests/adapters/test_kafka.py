import os
import pytest
from datetime import datetime, timedelta

import sp2
from sp2 import ts
from sp2.adapters.kafka import (
    DateTimeType,
    JSONTextMessageMapper,
    KafkaAdapterManager,
    KafkaStartOffset,
    RawBytesMessageMapper,
    RawTextMessageMapper,
)

from .kafka_utils import _precreate_topic


class MyData(sp2.Struct):
    b: bool
    i: int
    d: float
    s: str
    dt: datetime


class SubData(sp2.Struct):
    b: bool
    i: int
    d: float
    s: str
    dt: datetime
    b2: bool
    i2: int
    d2: float
    s2: str
    dt2: datetime
    prop1: float
    prop2: str


class MetaTextStruct(sp2.Struct):
    mapped_c: str


class MetaSubStruct(sp2.Struct):
    mapped_b: MetaTextStruct


class MetaPubData(sp2.Struct):
    mapped_a: MetaSubStruct
    mapped_count: int


class MetaSubData(sp2.Struct):
    mapped_a: MetaSubStruct
    mapped_count: int
    mapped_partition: int
    mapped_offset: int
    mapped_live: bool
    mapped_timestamp: datetime


class TestKafka:
    @pytest.mark.skipif(not os.environ.get("SP2_TEST_KAFKA"), reason="Skipping kafka adapter tests")
    def test_metadata(self, kafkaadapter):
        def graph(count: int):
            msg_mapper = JSONTextMessageMapper(datetime_type=DateTimeType.UINT64_MICROS)

            pub_field_map = {"mapped_a": {"a": {"mapped_b": {"b": {"mapped_c": "c"}}}}, "mapped_count": "count"}

            sub_field_map = {"a": {"mapped_a": {"b": {"mapped_b": {"c": "mapped_c"}}}}, "count": "mapped_count"}

            meta_field_map = {
                "partition": "mapped_partition",
                "offset": "mapped_offset",
                "live": "mapped_live",
                "timestamp": "mapped_timestamp",
            }

            topic = f"test.metadata.{os.getpid()}"
            _precreate_topic(topic)
            subKey = "foo"
            pubKey = ["mapped_a", "mapped_b", "mapped_c"]

            c = sp2.count(sp2.timer(timedelta(seconds=0.1)))
            t = sp2.sample(c, sp2.const("foo"))

            pubStruct = MetaPubData.collectts(
                mapped_a=MetaSubStruct.collectts(mapped_b=MetaTextStruct.collectts(mapped_c=t)), mapped_count=c
            )

            # sp2.print('pub', pubStruct)
            kafkaadapter.publish(msg_mapper, topic, pubKey, pubStruct, field_map=pub_field_map)

            sub_data = kafkaadapter.subscribe(
                MetaSubData,
                msg_mapper,
                topic,
                subKey,
                field_map=sub_field_map,
                meta_field_map=meta_field_map,
                push_mode=sp2.PushMode.NON_COLLAPSING,
            )

            sp2.add_graph_output("sub_data", sub_data)
            # sp2.print('sub', sub_data)
            # Wait for at least count ticks and until we get a live tick
            done_flag = sp2.count(sub_data) >= count
            done_flag = sp2.and_(done_flag, sub_data.mapped_live is True)
            stop = sp2.filter(done_flag, done_flag)
            sp2.stop_engine(stop)

        count = 5
        results = sp2.run(graph, count, starttime=datetime.utcnow(), endtime=timedelta(seconds=30), realtime=True)
        assert len(results["sub_data"]) >= 5
        print(results)
        for result in results["sub_data"]:
            assert result[1].mapped_partition >= 0
            assert result[1].mapped_offset >= 0
            assert result[1].mapped_live is not None
            assert result[1].mapped_timestamp < datetime.utcnow()
        assert results["sub_data"][-1][1].mapped_live

    @pytest.mark.skipif(not os.environ.get("SP2_TEST_KAFKA"), reason="Skipping kafka adapter tests")
    def test_basic(self, kafkaadapter):
        @sp2.node
        def curtime(x: ts[object]) -> ts[datetime]:
            if sp2.ticked(x):
                return sp2.now()

        def graph(symbols: list, count: int):
            b = sp2.merge(
                sp2.timer(timedelta(seconds=0.2), True),
                sp2.delay(sp2.timer(timedelta(seconds=0.2), False), timedelta(seconds=0.1)),
            )
            i = sp2.count(sp2.timer(timedelta(seconds=0.15)))
            d = sp2.count(sp2.timer(timedelta(seconds=0.2))) / 2.0
            s = sp2.sample(sp2.timer(timedelta(seconds=0.4)), sp2.const("STRING"))
            dt = curtime(b)
            struct = MyData.collectts(b=b, i=i, d=d, s=s, dt=dt)

            msg_mapper = JSONTextMessageMapper(datetime_type=DateTimeType.UINT64_MICROS)

            struct_field_map = {"b": "b2", "i": "i2", "d": "d2", "s": "s2", "dt": "dt2"}

            done_flags = []
            topic = f"mktdata.{os.getpid()}"
            _precreate_topic(topic)
            for symbol in symbols:
                kafkaadapter.publish(msg_mapper, topic, symbol, b, field_map="b")
                kafkaadapter.publish(msg_mapper, topic, symbol, i, field_map="i")
                kafkaadapter.publish(msg_mapper, topic, symbol, d, field_map="d")
                kafkaadapter.publish(msg_mapper, topic, symbol, s, field_map="s")
                kafkaadapter.publish(msg_mapper, topic, symbol, dt, field_map="dt")
                kafkaadapter.publish(msg_mapper, topic, symbol, struct, field_map=struct_field_map)

                # This isnt used to publish just to collect data for comparison at the end
                pub_data = SubData.collectts(
                    b=b, i=i, d=d, s=s, dt=dt, b2=struct.b, i2=struct.i, d2=struct.d, s2=struct.s, dt2=struct.dt
                )
                sp2.add_graph_output(f"pall_{symbol}", pub_data)

                # sp2.print('status', kafkaadapter.status())

                sub_data = kafkaadapter.subscribe(
                    ts_type=SubData,
                    msg_mapper=msg_mapper,
                    topic=topic,
                    key=symbol,
                    push_mode=sp2.PushMode.NON_COLLAPSING,
                )

                sub_data = sp2.firstN(sub_data, count)

                sp2.add_graph_output(f"sall_{symbol}", sub_data)

                done_flag = sp2.count(sub_data) == count
                done_flag = sp2.filter(done_flag, done_flag)
                done_flags.append(done_flag)

            stop = sp2.and_(*done_flags)
            stop = sp2.filter(stop, stop)
            sp2.stop_engine(stop)

        symbols = ["AAPL", "MSFT"]
        count = 100
        results = sp2.run(
            graph, symbols, count, starttime=datetime.utcnow(), endtime=timedelta(seconds=30), realtime=True
        )
        for symbol in symbols:
            pub = results[f"pall_{symbol}"]
            sub = results[f"sall_{symbol}"]

            assert len(sub) == count
            assert [v[1] for v in sub] == [v[1] for v in pub[:count]]

    @pytest.mark.skipif(not os.environ.get("SP2_TEST_KAFKA"), reason="Skipping kafka adapter tests")
    def test_start_offsets(self, kafkaadapter, kafkabroker):
        topic = f"test_start_offsets.{os.getpid()}"
        _precreate_topic(topic)
        msg_mapper = JSONTextMessageMapper(datetime_type=DateTimeType.UINT64_MICROS)
        count = 10

        # Prep the data first
        def pub_graph():
            i = sp2.count(sp2.timer(timedelta(seconds=0.1)))
            struct = MyData.collectts(i=i)
            kafkaadapter.publish(msg_mapper, topic, "AAPL", struct)
            stop = sp2.count(struct) == count
            stop = sp2.filter(stop, stop)
            sp2.stop_engine(stop)
            # sp2.print('pub', struct)

        sp2.run(pub_graph, starttime=datetime.utcnow(), endtime=timedelta(seconds=30), realtime=True)

        # grab start/end times
        def get_times_graph():
            kafkaadapter = KafkaAdapterManager(broker=kafkabroker, start_offset=KafkaStartOffset.EARLIEST)
            data = kafkaadapter.subscribe(
                MyData,
                msg_mapper=msg_mapper,
                topic=topic,
                key="AAPL",
                meta_field_map={"timestamp": "dt"},
                push_mode=sp2.PushMode.NON_COLLAPSING,
            )
            stop = sp2.count(data) == count
            sp2.stop_engine(sp2.filter(stop, stop))
            sp2.add_graph_output("data", data)

            # sp2.print('sub', data)
            # sp2.print('status', kafkaadapter.status())

        all_data = sp2.run(get_times_graph, starttime=datetime.utcnow(), endtime=timedelta(seconds=30), realtime=True)[
            "data"
        ]
        min_time = all_data[0][1].dt

        def get_data(start_offset, expected_count):
            kafkaadapter = KafkaAdapterManager(broker=kafkabroker, start_offset=start_offset)
            data = kafkaadapter.subscribe(
                MyData,
                msg_mapper=msg_mapper,
                topic=topic,
                key="AAPL",
                meta_field_map={"timestamp": "dt"},
                push_mode=sp2.PushMode.NON_COLLAPSING,
            )
            stop = sp2.count(data) == expected_count
            sp2.stop_engine(sp2.filter(stop, stop))
            sp2.add_graph_output("data", data)

            # sp2.print('data', data)

        res = sp2.run(
            get_data,
            KafkaStartOffset.EARLIEST,
            10,
            starttime=datetime.utcnow(),
            endtime=timedelta(seconds=30),
            realtime=True,
        )["data"]
        # print(res)
        # If we playback from earliest but start "now", all data should still arrive but as realtime ticks
        assert len(res) == 10

        res = sp2.run(
            get_data,
            KafkaStartOffset.LATEST,
            1,
            starttime=datetime.utcnow(),
            endtime=timedelta(seconds=1),
            realtime=True,
        )["data"]
        assert len(res) == 0

        res = sp2.run(
            get_data, KafkaStartOffset.START_TIME, 10, starttime=min_time, endtime=timedelta(seconds=30), realtime=True
        )["data"]
        assert len(res) == 10

        # Test sim playback time as well
        for t, v in res:
            assert t == v.dt

        stime = all_data[2][1].dt + timedelta(milliseconds=1)
        expected = [x for x in all_data if x[1].dt >= stime]
        res = sp2.run(
            get_data, stime, len(expected), starttime=datetime.utcnow(), endtime=timedelta(seconds=30), realtime=True
        )["data"]
        assert len(res) == len(expected)

        res = sp2.run(
            get_data, timedelta(seconds=0), len(expected), starttime=stime, endtime=timedelta(seconds=30), realtime=True
        )["data"]
        assert len(res) == len(expected)

    @pytest.mark.skipif(not os.environ.get("SP2_TEST_KAFKA"), reason="Skipping kafka adapter tests")
    @pytest.fixture(autouse=True)
    def test_raw_pubsub(self, kafkaadapter):
        @sp2.node
        def data(x: ts[object]) -> ts[bytes]:
            if sp2.ticked(x):
                return str(sp2.now())

        class SubData(sp2.Struct):
            msg: bytes

        def graph(symbols: list, count: int):
            t = sp2.timer(timedelta(seconds=0.1), True)
            d = data(t)

            msg_mapper = RawBytesMessageMapper()

            done_flags = []
            topic = f"test_str.{os.getpid()}"
            _precreate_topic(topic)
            for symbol in symbols:
                topic = f"test_str.{os.getpid()}"
                kafkaadapter.publish(msg_mapper, topic, symbol, d)
                sp2.add_graph_output(f"pub_{symbol}", d)

                # sp2.print('status', kafkaadapter.status())

                sub_data = kafkaadapter.subscribe(
                    ts_type=SubData,
                    msg_mapper=RawTextMessageMapper(),
                    field_map={"": "msg"},
                    topic=topic,
                    key=symbol,
                    push_mode=sp2.PushMode.NON_COLLAPSING,
                )

                sub_data_bytes = kafkaadapter.subscribe(
                    ts_type=bytes,
                    msg_mapper=RawTextMessageMapper(),
                    field_map="",
                    topic=topic,
                    key=symbol,
                    push_mode=sp2.PushMode.NON_COLLAPSING,
                )

                sub_data = sp2.firstN(sub_data.msg, count)
                sub_data_bytes = sp2.firstN(sub_data_bytes, count)

                # sp2.print('sub', sub_data)
                sp2.add_graph_output(f"sub_{symbol}", sub_data)
                sp2.add_graph_output(f"sub_bytes_{symbol}", sub_data_bytes)

                done_flag = sp2.count(sub_data) + sp2.count(sub_data_bytes) == count * 2
                done_flag = sp2.filter(done_flag, done_flag)
                done_flags.append(done_flag)

            stop = sp2.and_(*done_flags)
            stop = sp2.filter(stop, stop)
            sp2.stop_engine(stop)

        symbols = ["AAPL", "MSFT"]
        count = 10
        results = sp2.run(
            graph, symbols, count, starttime=datetime.utcnow(), endtime=timedelta(seconds=30), realtime=True
        )
        # print(results)
        for symbol in symbols:
            pub = results[f"pub_{symbol}"]
            sub = results[f"sub_{symbol}"]
            sub_bytes = results[f"sub_bytes_{symbol}"]

            assert len(sub) == count
            assert [v[1] for v in sub] == [v[1] for v in pub[:count]]
            assert [v[1] for v in sub_bytes] == [v[1] for v in pub[:count]]

    @pytest.mark.skipif(not os.environ.get("SP2_TEST_KAFKA"), reason="Skipping kafka adapter tests")
    @pytest.fixture(autouse=True)
    def test_invalid_topic(self, kafkaadapter):
        class SubData(sp2.Struct):
            msg: str

        # Was a bug where engine would stall
        def graph():
            # sp2.print('status', kafkaadapter.status())
            return kafkaadapter.subscribe(
                ts_type=SubData, msg_mapper=RawTextMessageMapper(), field_map={"": "msg"}, topic="foobar", key="none"
            )

        # With bug this would deadlock
        sp2.run(graph, starttime=datetime.utcnow(), endtime=timedelta(seconds=2), realtime=True)
