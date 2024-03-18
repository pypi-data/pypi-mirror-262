#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    sse_core.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    sse消息推送和订阅逻辑

    :author: Tangshimin
    :copyright: (c) 2024, Tungee
    :date created: 2024-01-29

"""
import json
from datetime import datetime
import traceback
import time

from .sse_cache import SseConnectStatsCache, SseEventMessageCache, SseOpenSwitchCache
from .sse_constant import RedisPubSubField, SseSystemEventType
from .sse_message import SseMessage, SseMessageField
from .sse_constant import RedisPubSubConfig, SseClientConfig


class SseRedisPubSub(object):
    """
    全局redis-pub-sub对象
    """
    def __init__(self, redis_client, key_prefix, sse_clients):
        self.redis = redis_client
        self.redis_pubsub = redis_client.pubsub()
        self.sse_connect_stats_cache = SseConnectStatsCache(
            redis_client, key_prefix
        )
        self.sse_event_message_cache = SseEventMessageCache(
            redis_client, key_prefix
        )
        self.sse_open_switch_cache = SseOpenSwitchCache(
            redis_client, key_prefix
        )
        self.listen_interval = RedisPubSubConfig.LISTEN_INTERVAL
        self.heartbeat_interval = RedisPubSubConfig.HEARTBEAT_INTERVAL
        self.sse_clients = sse_clients

    def listen(self):
        """
        监听redis订阅频道，将收到的消息推送到全局sse连接对象
        """
        channel = ''
        try:
            print({
                'title': '开启监听redis频道',
                'channel_count': self.sse_clients.count()
            })
            while True:
                if not self.sse_clients.is_running:
                    print({
                        'title': '监听redis频道线程停止',
                        'channel_count': self.sse_clients.count()
                    })
                    break

                # 每隔5s向所有连接推送心跳包
                if int(time.time()) % self.heartbeat_interval == 0:
                    self.sse_clients.add_heartbeat()

                sub_message = self.redis_pubsub.get_message(timeout=1)
                if not sub_message:
                    time.sleep(self.listen_interval)
                    continue

                channel, message = self.sse_event_message_handler(sub_message)
                if not message:
                    time.sleep(self.listen_interval)
                    continue

                self.sse_event_message_cache.add_sub_message({
                    'channel': channel,
                    'message': message.to_dict(),
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                })

                if self.illegal_message(message):
                    time.sleep(self.listen_interval)
                    continue

                # 消息推送到全局sse连接对象
                self.sse_clients.add_message(channel, message)
                time.sleep(self.listen_interval)

        except:
            print({
                'title': '监听redis频道异常',
                'channel': channel,
                'exp': traceback.format_exc(),
                'channel_count': self.sse_clients.count()
            })
            pass

    def subscribe_channel(self, channel, extra=None):
        """
        订阅sse频道消息
        """
        self.redis_pubsub.subscribe(channel)

        ok, msg = self.sse_clients.connect(channel)
        if not ok:
            print({
                'title': '订阅失败',
                'channel': channel,
                'msg': msg,
                'channel_count': self.sse_clients.count()
            })
            self.redis_pubsub.unsubscribe(channel)
            return ok, msg

        # 连接成功，记录连接信息
        self.sse_connect_stats_cache.add(channel, {
            'connect_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ln_id': self.sse_clients.get_local_node_id(),
            'extra': extra,
        })

        self.publish_message(
            channel=channel,
            data={
                'msg': 'connect success',
                'ln_id': self.sse_clients.get_local_node_id()
            },
            event=SseSystemEventType.CONNECT,
            _id=str(int(datetime.now().timestamp() * 1000000)),
            retry=SseClientConfig.MAX_CONNECT_TIME * 1000
        )

        print({
            'title': '订阅成功',
            'channel': channel,
            'channel_count': self.sse_clients.count()
        })

        return ok, msg

    def publish_sse_message(self, sse_message):
        if not isinstance(sse_message, SseMessage):
            return 0

        message = sse_message.to_dict()

        return self.publish_message(
            channel=message.get(SseMessageField.CHANNEL),
            data=message.get(SseMessageField.DATA),
            event=message.get(SseMessageField.EVENT),
            _id=message.get(SseMessageField.ID),
            retry=message.get(SseMessageField.RETRY)
        )

    def publish_message(self, channel, data, event=None, _id=None, retry=None):
        """
        推送sse消息, 添加信息到redis发布队列记录
        """
        message = SseMessage(
            channel=channel, data=data, event=event, _id=_id, retry=retry
        ).to_dict()

        push_count = self.redis.publish(channel=channel, message=json.dumps(message))

        self.sse_event_message_cache.add_pub_message({
            'channel': channel,
            'message': message,
            'push_count': push_count,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })

        if push_count > 0:
            print({
                'title': '消息推送成功',
                'channel': channel,
                'event': event,
                'push_count': push_count,
                'channel_count': self.sse_clients.count()
            })
        else:
            print({
                'title': '消息推送失败，频道不存在',
                'channel': channel,
                'event': event,
                'channel_count': self.sse_clients.count()
            })

        return push_count

    def disconnect(self, channel):
        """
        断开sse连接, 清理redis连接缓存
        """
        print({
            'title': '断开sse连接',
            'channel': channel,
            'channel_count': self.sse_clients.count()
        })
        # 清理连接缓存
        self.sse_connect_stats_cache.delete(channel)

    def unsubscribe_channel(self, channel):
        """
        取消订阅sse频道
        """
        print({
            'title': '取消订阅',
            'channel': channel,
            'channel_count': self.sse_clients.count()
        })
        self.redis_pubsub.unsubscribe(channel)

    def disconnect_all(self):
        """
        断开所有sse连接，关闭服务时调用
        """
        channel_list = self.sse_clients.sse_global_clients.keys()
        if channel_list:
            # 清理全局连接对象
            self.sse_clients.release_all()

    def get_pub_message_stat(self, day=datetime.now().strftime('%Y%m%d'), start=0, end=100):
        """
        获取指定日期推送消息统计
        """
        return self.sse_event_message_cache.get_pub_all_by_day(day, start, end)

    def get_sub_message_stat(self, day=datetime.now().strftime('%Y%m%d'), start=0, end=100):
        """
        获取指定日期接收消息统计
        """
        return self.sse_event_message_cache.get_sub_all_by_day(day, start, end)

    def get_connect_stat(self, day=datetime.now().strftime('%Y%m%d')):
        """
        某天连接统计
        """
        return self.sse_connect_stats_cache.get_all_by_day(day)

    def is_open_sse_switch(self):
        """
        sse开关
        """
        status = self.sse_open_switch_cache.get()
        return status == 'open'

    def open_sse_switch(self):
        return self.sse_open_switch_cache.set("open")

    def close_sse_switch(self):
        return self.sse_open_switch_cache.set("close")

    @staticmethod
    def illegal_message(message):
        """
        是否是非法消息
        """
        if not message:
            return True
        if not isinstance(message, SseMessage):
            return True
        event = message.to_dict().get(SseMessageField.EVENT, '')
        return event in [
            SseSystemEventType.ERROR, SseSystemEventType.REDIS,
        ]

    @staticmethod
    def sse_event_message_handler(sub_message):
        """
        sse消息类型处理
        :param sub_message: redis订阅消息

        :return:
            message: sse消息
            brk: 是否中断结束
        """
        try:
            if not sub_message:
                return SseSystemEventType.ERROR, None

            # 需要先解码
            for key, value in sub_message.items():
                if isinstance(key, bytes):
                    key = key.decode('utf-8')
                if isinstance(value, bytes):
                    value = value.decode('utf-8')
                sub_message[key] = value

            channel = sub_message.get(SseMessageField.CHANNEL)
            if not channel:
                return SseSystemEventType.ERROR, None

            # 非message类型不处理
            if sub_message[RedisPubSubField.TYPE] != RedisPubSubField.Type.MESSAGE:
                return SseSystemEventType.REDIS, None

            sub_message_data = sub_message.get(RedisPubSubField.DATA, '')
            if not sub_message_data:
                return SseSystemEventType.ERROR, None

            # 消息
            sse_message = json.loads(sub_message_data)
            message = SseMessage(
                channel=sse_message.get(SseMessageField.CHANNEL),
                data=sse_message.get(SseMessageField.DATA),
                event=sse_message.get(SseMessageField.EVENT),
                _id=sse_message.get(SseMessageField.ID),
                retry=sse_message.get(SseMessageField.RETRY)
            )

            return channel, message
        except:
            return SseSystemEventType.ERROR, None


