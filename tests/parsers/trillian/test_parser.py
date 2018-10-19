import unittest

from chat_unifier.parsers.trillian import parser


class TrillianTest(unittest.TestCase):

    def test_parse_log_with_one_simple_conversation(self):
        log_contents = r"""
<session type="start" time="1132517277" medium="AIM" to="RemoteBuddy123" from="LocalUser456"/>
<message type="incoming_privateMessage" time="1132517277" medium="AIM" to="LocalUser456" from="RemoteBuddy123" from_display="RemoteBuddy123" text="what%27s%20up"/>
<message type="outgoing_privateMessage" time="1132522524" medium="AIM" to="RemoteBuddy123" from="LocalUser456" from_display="Me" text="nm"/>
<session type="stop" time="1132522555" medium="AIM" to="RemoteBuddy123" from="LocalUser456"/>
""".lstrip()
        with self.assertRaises(NotImplementedError):
            parser.Parser().parse(log_contents)
