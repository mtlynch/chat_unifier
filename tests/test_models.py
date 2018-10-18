import datetime
import unittest

from chat_unifier import models


class MessageTest(unittest.TestCase):

    def test_identical_messages_are_equal(self):
        self.assertEqual(
            models.Message(
                sender='dummy_sender',
                timestamp=datetime.datetime(2018, 10, 18, 18, 27, 5),
                contents='hi how are you?'),
            models.Message(
                sender='dummy_sender',
                timestamp=datetime.datetime(2018, 10, 18, 18, 27, 5),
                contents='hi how are you?'))

    def test_messages_are_unequal_if_they_have_different_senders(self):
        self.assertNotEqual(
            models.Message(
                sender='dummy_senderAAA',
                timestamp=datetime.datetime(2018, 10, 18, 18, 27, 5),
                contents='hi how are you?'),
            models.Message(
                sender='dummy_senderBBB',
                timestamp=datetime.datetime(2018, 10, 18, 18, 27, 5),
                contents='hi how are you?'))

    def test_messages_are_unequal_if_they_have_different_timestamps(self):
        self.assertNotEqual(
            models.Message(
                sender='dummy_sender',
                timestamp=datetime.datetime(2016, 1, 1, 0, 0, 0),
                contents='hi how are you?'),
            models.Message(
                sender='dummy_sender',
                timestamp=datetime.datetime(2018, 10, 18, 18, 27, 5),
                contents='hi how are you?'))

    def test_messages_are_unequal_if_they_have_different_timestamps(self):
        self.assertNotEqual(
            models.Message(
                sender='dummy_sender',
                timestamp=datetime.datetime(2018, 10, 18, 18, 27, 5),
                contents='sup pal!'),
            models.Message(
                sender='dummy_sender',
                timestamp=datetime.datetime(2018, 10, 18, 18, 27, 5),
                contents='hi how are you?'))
