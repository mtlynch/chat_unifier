import datetime
import unittest

from chat_unifier.parsers.trillian import line_parser


class LineParserTest(unittest.TestCase):

    def test_parses_valid_session_start_line(self):
        self.assertEqual(
            line_parser.SessionStartLine(
                timestamp=datetime.datetime(2005, 11, 20, 20, 7, 57),
                medium='AIM',
                sender='LocalUser456',
                recipient='RemoteBuddy123'),
            line_parser.parse(
                '<session type="start" time="1132517277" medium="AIM" to="RemoteBuddy123" from="LocalUser456"/>'
            ))

    def test_parses_valid_session_stop_line(self):
        self.assertEqual(
            line_parser.SessionStopLine(
                timestamp=datetime.datetime(2005, 11, 20, 21, 35, 55),
                medium='AIM',
                sender='LocalUser789',
                recipient='RemoteBuddy234'),
            line_parser.parse(
                '<session type="stop" time="1132522555" medium="AIM" to="RemoteBuddy234" from="LocalUser789"/>'
            ))
