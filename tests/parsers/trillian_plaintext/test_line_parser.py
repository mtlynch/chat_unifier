import datetime
import unittest

from chat_unifier.parsers.trillian_plaintext import line_parser


class LineParserTest(unittest.TestCase):

    def test_parses_valid_session_start_line(self):
        self.assertEqual(
            line_parser.SessionStartLine(
                timestamp=datetime.datetime(2003, 1, 5, 21, 43, 2),
                medium='AIM',
                local_username='LocalUser123',
                remote_username='RemoteBuddy456'),
            line_parser.parse(
                'Session Start (AIM - LocalUser123:RemoteBuddy456): Sun Jan 05 21:43:02 2003'
            ))
