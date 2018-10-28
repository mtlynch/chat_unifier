import datetime
import json
import unittest

from chat_unifier import json_serializer
from chat_unifier import models


class HistoryTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_serializes_simple_history(self):
        self.assertMultiLineEqual(
            """
[
  {
    "localUsername": "dummy_local123", 
    "messages": [
      {
        "contents": "hi how are you?", 
        "sender": "dummy_local123", 
        "timestamp": "2018-10-18T18:27:05Z"
      }
    ], 
    "remoteUsername": "dummy_remote345"
  }, 
  {
    "localUsername": "dummy_local123", 
    "messages": [
      {
        "contents": "hello good sir", 
        "sender": "dummy_remote456", 
        "timestamp": "2018-10-20T04:15:43Z"
      }
    ], 
    "remoteUsername": "dummy_remote456"
  }
]
""".strip(),
            json.dumps(
                [
                    models.History(
                        local_username='dummy_local123',
                        remote_username='dummy_remote345',
                        messages=[
                            models.Message(
                                sender='dummy_local123',
                                timestamp=datetime.datetime(
                                    2018, 10, 18, 18, 27, 5),
                                contents='hi how are you?')
                        ]),
                    models.History(
                        local_username='dummy_local123',
                        remote_username='dummy_remote456',
                        messages=[
                            models.Message(
                                sender='dummy_remote456',
                                timestamp=datetime.datetime(
                                    2018, 10, 20, 4, 15, 43),
                                contents='hello good sir')
                        ])
                ],
                sort_keys=True,
                indent=2,
                cls=json_serializer.Serializer))
