import datetime
import unittest

from chat_unifier import history_merger
from chat_unifier import models


class HistoryMergerTest(unittest.TestCase):

    def test_merges_histories_from_same_remote_user(self):
        merger = history_merger.Merger()
        merger.add(
            models.History(
                local_username='dummy_local123',
                remote_usernames=['dummy_remote345'],
                messages=[
                    models.Message(
                        sender='dummy_remote345',
                        timestamp=datetime.datetime(2018, 10, 18, 18, 27, 5),
                        contents='hi how are you?'),
                    models.Message(
                        sender='dummy_local123',
                        timestamp=datetime.datetime(2018, 10, 18, 18, 27, 8),
                        contents='bye bye'),
                ]))
        merger.add(
            models.History(
                local_username='dummy_local123',
                remote_usernames=['dummy_remote345'],
                messages=[
                    models.Message(
                        sender='dummy_remote345',
                        timestamp=datetime.datetime(2018, 10, 18, 18, 27, 6),
                        contents='u coming to my party?'),
                    models.Message(
                        sender='dummy_local123',
                        timestamp=datetime.datetime(2018, 10, 18, 18, 27, 7),
                        contents='of course!'),
                ]))
        merged_histories = [x for x in merger]
        self.assertEqual(1, len(merged_histories))
        merged_history = merged_histories[0]
        self.assertEqual(
            merged_history,
            models.History(
                local_username='dummy_local123',
                remote_usernames=['dummy_remote345'],
                messages=[
                    models.Message(
                        sender='dummy_remote345',
                        timestamp=datetime.datetime(2018, 10, 18, 18, 27, 5),
                        contents='hi how are you?'),
                    models.Message(
                        sender='dummy_remote345',
                        timestamp=datetime.datetime(2018, 10, 18, 18, 27, 6),
                        contents='u coming to my party?'),
                    models.Message(
                        sender='dummy_local123',
                        timestamp=datetime.datetime(2018, 10, 18, 18, 27, 7),
                        contents='of course!'),
                    models.Message(
                        sender='dummy_local123',
                        timestamp=datetime.datetime(2018, 10, 18, 18, 27, 8),
                        contents='bye bye'),
                ]))

    def test_does_not_merge_histories_from_different_remote_users(self):
        merger = history_merger.Merger()
        merger.add(
            models.History(
                local_username='dummy_local123',
                remote_usernames=['dummy_remote345'],
                messages=[
                    models.Message(
                        sender='dummy_remote345',
                        timestamp=datetime.datetime(2018, 10, 18, 18, 27, 5),
                        contents='hi how are you?'),
                    models.Message(
                        sender='dummy_local123',
                        timestamp=datetime.datetime(2018, 10, 18, 18, 27, 8),
                        contents='bye bye'),
                ]))
        merger.add(
            models.History(
                local_username='dummy_local123',
                remote_usernames=['dummy_remote999'],
                messages=[
                    models.Message(
                        sender='dummy_remote999',
                        timestamp=datetime.datetime(2018, 10, 18, 18, 27, 6),
                        contents='u coming to my party?'),
                    models.Message(
                        sender='dummy_local123',
                        timestamp=datetime.datetime(2018, 10, 18, 18, 27, 7),
                        contents='of course!'),
                ]))
        merged_histories = [x for x in merger]
        self.assertEqual(2, len(merged_histories))
