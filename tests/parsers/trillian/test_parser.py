import datetime
import unittest

from chat_unifier import models
from chat_unifier.parsers.trillian import parser


class ParserTest(unittest.TestCase):

    def test_parse_log_with_one_simple_conversation(self):
        self.assertEqual(
            parser.Parser().parse("""
<session type="start" time="1132517277" medium="AIM" to="RemoteBuddy123" from="LocalUser456"/>
<message type="incoming_privateMessage" time="1132517277" medium="AIM" to="LocalUser456" from="RemoteBuddy123" from_display="RemoteBuddy123" text="what%27s%20up"/>
<message type="outgoing_privateMessage" time="1132522524" medium="AIM" to="RemoteBuddy123" from="LocalUser456" from_display="Me" text="nm"/>
<session type="stop" time="1132522555" medium="AIM" to="RemoteBuddy123" from="LocalUser456"/>
""".lstrip()),
            models.History(
                local_username=u'LocalUser456',
                remote_username=u'RemoteBuddy123',
                messages=[
                    models.Message(
                        sender=u'RemoteBuddy123',
                        timestamp=datetime.datetime(2005, 11, 20, 20, 7, 57),
                        contents=u'what\'s up'),
                    models.Message(
                        sender=u'LocalUser456',
                        timestamp=datetime.datetime(2005, 11, 20, 21, 35, 24),
                        contents=u'nm')
                ]))

    def test_parse_usernames_with_encoded_characters(self):
        self.assertEqual(
            parser.Parser().parse("""
<session type="start" time="1132517277" medium="AIM" to="AOL%20System%20Msg" from="t%2Djohndoe%40example%2Ecom"/>
<message type="incoming_privateMessage" time="1132517277" medium="AIM" to="t%2Djohndoe%40example%2Ecom" from="AOL%20System%20Msg" from_display="AOL%20System%20Msg" text="what%27s%20up"/>
<message type="outgoing_privateMessage" time="1132522524" medium="AIM" to="AOL%20System%20Msg" from="t%2Djohndoe%40example%2Ecom" from_display="Me" text="nm"/>
<session type="stop" time="1132522555" medium="AIM" to="AOL%20System%20Msg" from="t%2Djohndoe%40example%2Ecom"/>
""".lstrip()),
            models.History(
                local_username=u't-johndoe@example.com',
                remote_username=u'AOL System Msg',
                messages=[
                    models.Message(
                        sender=u'AOL System Msg',
                        timestamp=datetime.datetime(2005, 11, 20, 20, 7, 57),
                        contents=u'what\'s up'),
                    models.Message(
                        sender=u't-johndoe@example.com',
                        timestamp=datetime.datetime(2005, 11, 20, 21, 35, 24),
                        contents=u'nm')
                ]))
