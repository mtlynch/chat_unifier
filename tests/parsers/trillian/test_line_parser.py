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

    def test_parsers_valid_outgoing_private_message_line(self):
        self.assertEqual(
            line_parser.OutgoingPrivateMessageLine(
                timestamp=datetime.datetime(2005, 8, 25, 1, 23, 31),
                medium='AIM',
                sender='LocalUser111',
                sender_display='Me',
                recipient='RemoteBuddy888',
                contents='do you want me to bring up the books tomorrow?'),
            line_parser.parse(
                '<message type="outgoing_privateMessage" time="1124933011" medium="AIM" to="RemoteBuddy888" from="LocalUser111" from_display="Me" text="do%20you%20want%20me%20to%20bring%20up%20the%20books%20tomorrow%3F"/>'
            ))
