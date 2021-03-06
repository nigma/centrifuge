# coding: utf-8
from __future__ import print_function
from tornado.gen import Task
from tornado.testing import AsyncTestCase, gen_test, main
import time
from centrifuge.state.base import State as BaseState
from centrifuge.state.redis import State as RedisState
import json


class FakeApplication(object):
    settings = {
        "config": {
            "state": {

            }
        }
    }


class BaseStateTest(AsyncTestCase):
    """ Test the client """

    def setUp(self):
        super(BaseStateTest, self).setUp()
        self.project_id = 'test'
        self.namespace = 'test'
        self.channel = 'test'
        self.uid_1 = 'test-1'
        self.uid_2 = 'test-2'
        self.user_id = 'test'
        self.user_id_extra = 'test_extra'
        self.user_info = "{}"
        self.message_1 = json.dumps('test message 1')
        self.message_2 = json.dumps('test message 2')
        self.message_3 = json.dumps('test message 3')
        self.state = BaseState(FakeApplication, io_loop=self.io_loop)
        self.state.history_size = 2
        self.state.presence_timeout = 1

    @gen_test
    def test_presence(self):
        result, error = yield self.state.get_presence(
            self.project_id, self.namespace, self.channel
        )
        self.assertEqual(result, {})

        result, error = yield self.state.add_presence(
            self.project_id, self.namespace, self.channel,
            self.uid_1, self.user_info
        )
        self.assertEqual(result, True)

        result, error = yield self.state.get_presence(
            self.project_id, self.namespace, self.channel
        )
        self.assertTrue(self.uid_1 in result)

        result, error = yield self.state.add_presence(
            self.project_id, self.namespace, self.channel,
            self.uid_1, self.user_info
        )
        self.assertEqual(result, True)

        result, error = yield self.state.get_presence(
            self.project_id, self.namespace, self.channel
        )
        self.assertTrue(self.uid_1 in result)
        self.assertEqual(len(result), 1)

        result, error = yield self.state.add_presence(
            self.project_id, self.namespace, self.channel,
            self.uid_2, self.user_info
        )
        self.assertEqual(result, True)

        result, error = yield self.state.get_presence(
            self.project_id, self.namespace, self.channel
        )
        self.assertTrue(self.uid_1 in result)
        self.assertTrue(self.uid_2 in result)
        self.assertEqual(len(result), 2)

        result, error = yield self.state.remove_presence(
            self.project_id, self.namespace, self.channel, self.uid_2
        )
        self.assertEqual(result, True)

        result, error = yield self.state.get_presence(
            self.project_id, self.namespace, self.channel
        )
        self.assertTrue(self.uid_1 in result)
        self.assertTrue(self.uid_2 not in result)
        self.assertEqual(len(result), 1)

        time.sleep(2)
        result, error = yield self.state.get_presence(
            self.project_id, self.namespace, self.channel
        )
        self.assertEqual(result, {})

    @gen_test
    def test_history(self):
        result, error = yield self.state.add_history_message(
            self.project_id, self.namespace, self.channel, self.message_1
        )
        self.assertEqual(error, None)
        self.assertEqual(result, True)

        result, error = yield self.state.get_history(
            self.project_id, self.namespace, self.channel
        )
        self.assertEqual(error, None)
        self.assertEqual(len(result), 1)

        result, error = yield self.state.add_history_message(
            self.project_id, self.namespace, self.channel, self.message_2
        )
        self.assertEqual(error, None)
        self.assertEqual(result, True)

        result, error = yield self.state.get_history(
            self.project_id, self.namespace, self.channel
        )
        self.assertEqual(error, None)
        self.assertEqual(len(result), 2)

        result, error = yield self.state.add_history_message(
            self.project_id, self.namespace, self.channel, self.message_3
        )
        self.assertEqual(error, None)
        self.assertEqual(result, True)

        result, error = yield self.state.get_history(
            self.project_id, self.namespace, self.channel
        )
        self.assertEqual(error, None)
        self.assertEqual(len(result), 2)


class RedisStateTest(AsyncTestCase):
    """ Test the client """

    def setUp(self):
        super(RedisStateTest, self).setUp()
        self.project_id = 'test'
        self.namespace = 'test'
        self.channel = 'test'
        self.uid_1 = 'test-1'
        self.uid_2 = 'test-2'
        self.user_id = 'test'
        self.user_id_extra = 'test_extra'
        self.user_info = "{}"
        self.message_1 = json.dumps('test message 1')
        self.message_2 = json.dumps('test message 2')
        self.message_3 = json.dumps('test message 3')
        self.state = RedisState(FakeApplication, io_loop=self.io_loop)
        self.state.history_size = 2
        self.state.presence_timeout = 1
        self.state.initialize()

    @gen_test
    def test_presence(self):
        result = yield Task(self.state.client.flushdb)
        self.assertEqual(result, "OK")

        result, error = yield self.state.get_presence(
            self.project_id, self.namespace, self.channel
        )
        self.assertEqual(result, {})

        result, error = yield self.state.add_presence(
            self.project_id, self.namespace, self.channel,
            self.uid_1, self.user_info
        )
        self.assertEqual(result, True)

        result, error = yield self.state.get_presence(
            self.project_id, self.namespace, self.channel
        )
        self.assertTrue(self.uid_1 in result)

        result, error = yield self.state.add_presence(
            self.project_id, self.namespace, self.channel,
            self.uid_1, self.user_info
        )
        self.assertEqual(result, True)

        result, error = yield self.state.get_presence(
            self.project_id, self.namespace, self.channel
        )
        self.assertTrue(self.uid_1 in result)
        self.assertEqual(len(result), 1)

        result, error = yield self.state.add_presence(
            self.project_id, self.namespace, self.channel,
            self.uid_2, self.user_info
        )
        self.assertEqual(result, True)

        result, error = yield self.state.get_presence(
            self.project_id, self.namespace, self.channel
        )
        self.assertTrue(self.uid_1 in result)
        self.assertTrue(self.uid_2 in result)
        self.assertEqual(len(result), 2)

        result, error = yield self.state.remove_presence(
            self.project_id, self.namespace, self.channel, self.uid_2
        )
        self.assertEqual(result, True)

        result, error = yield self.state.get_presence(
            self.project_id, self.namespace, self.channel
        )
        self.assertTrue(self.uid_1 in result)
        self.assertTrue(self.uid_2 not in result)
        self.assertEqual(len(result), 1)

        time.sleep(2)
        result, error = yield self.state.get_presence(
            self.project_id, self.namespace, self.channel
        )
        self.assertEqual(result, {})

    @gen_test
    def test_history(self):
        result = yield Task(self.state.client.flushdb)
        self.assertEqual(result, "OK")

        result, error = yield self.state.add_history_message(
            self.project_id, self.namespace, self.channel, self.message_1
        )
        self.assertEqual(error, None)
        self.assertEqual(result, True)

        result, error = yield self.state.get_history(
            self.project_id, self.namespace, self.channel
        )
        self.assertEqual(error, None)
        self.assertEqual(len(result), 1)

        result, error = yield self.state.add_history_message(
            self.project_id, self.namespace, self.channel, self.message_2
        )
        self.assertEqual(error, None)
        self.assertEqual(result, True)

        result, error = yield self.state.get_history(
            self.project_id, self.namespace, self.channel
        )
        self.assertEqual(error, None)
        self.assertEqual(len(result), 2)

        result, error = yield self.state.add_history_message(
            self.project_id, self.namespace, self.channel, self.message_3
        )
        self.assertEqual(error, None)
        self.assertEqual(result, True)

        result, error = yield self.state.get_history(
            self.project_id, self.namespace, self.channel
        )
        self.assertEqual(error, None)
        self.assertEqual(len(result), 2)


if __name__ == '__main__':
    main()