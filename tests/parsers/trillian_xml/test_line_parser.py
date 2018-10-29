import datetime
import unittest

from chat_unifier.parsers.trillian_xml import line_parser


class LineParserTest(unittest.TestCase):

    def test_parses_valid_session_start_line(self):
        self.assertEqual(
            line_parser.SessionStartLine(
                timestamp=datetime.datetime(2005, 11, 20, 20, 7, 57),
                medium='AIM',
                local_username='LocalUser456',
                remote_username='RemoteBuddy123'),
            line_parser.parse(
                '<session type="start" time="1132517277" medium="AIM" to="RemoteBuddy123" from="LocalUser456"/>'
            ))

    def test_parses_valid_session_stop_line(self):
        self.assertEqual(
            line_parser.SessionStopLine(
                timestamp=datetime.datetime(2005, 11, 20, 21, 35, 55),
                medium='AIM',
                local_username='LocalUser789',
                remote_username='RemoteBuddy234'),
            line_parser.parse(
                '<session type="stop" time="1132522555" medium="AIM" to="RemoteBuddy234" from="LocalUser789"/>'
            ))

    def test_invalid_session_type_raises_exception(self):
        with self.assertRaises(line_parser.InvalidSessionType):
            line_parser.parse('<session type="dummy_invalid_type"/>')

    def test_session_with_no_type_attribute_raises_exception(self):
        with self.assertRaises(line_parser.InvalidSessionType):
            line_parser.parse('<session />')

    def test_parses_valid_outgoing_private_message_line(self):
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

    def test_parses_valid_incoming_private_message_line(self):
        self.assertEqual(
            line_parser.IncomingPrivateMessageLine(
                timestamp=datetime.datetime(2005, 8, 25, 1, 23, 45),
                medium='AIM',
                sender='RemoteBuddy555',
                sender_display='Steve',
                recipient='LocalUser222',
                contents='hmm... no thanks'),
            line_parser.parse(
                '<message type="incoming_privateMessage" time="1124933025" medium="AIM" to="LocalUser222" from="RemoteBuddy555" from_display="Steve" text="hmm%2E%2E%2E%20no%20thanks"/>'
            ))

    def test_parses_valid_informational_message_line(self):
        self.assertEqual(
            line_parser.InformationalMessageLine(
                timestamp=datetime.datetime(2005, 9, 11, 3, 35, 37),
                medium='AIM',
                contents='"Steve" signed on at Sat Sep 10 23:35:37 2005.'),
            line_parser.parse(
                '<message type="information_standard" time="1126409737" medium="AIM" text="%22Steve%22%20signed%20on%20at%20Sat%20Sep%2010%2023%3A35%3A37%202005%2E"/>'
            ))

    def test_invalid_message_type_raises_exception(self):
        with self.assertRaises(line_parser.InvalidMessageType):
            line_parser.parse('<message type="dummy_invalid_type" />')

    def test_message_with_no_type_attribute_raises_exception(self):
        with self.assertRaises(line_parser.InvalidMessageType):
            line_parser.parse('<message />')
