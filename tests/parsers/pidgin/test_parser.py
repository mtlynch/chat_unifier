import datetime
import unittest

from chat_unifier import models
from chat_unifier.parsers.pidgin import parser


class PidginParserTest(unittest.TestCase):

    def test_parse_log_with_one_simple_conversation(self):
        self.assertEqual(
            parser.Parser().parse("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>Conversation with RemoteUser345 at 12/20/2006 12:18:08 PM on LocalUser123 (aim)</title></head><body><h3>Conversation with RemoteUser345 at 12/20/2006 12:18:08 PM on LocalUser123 (aim)</h3>
<font color="#A82F2F"><font size="2">(12:18:08 PM)</font> <b>Alice:</b></font> <html><span style='background: #ffffff;'>how are you</span></span></html><br/>
<font color="#16569E"><font size="2">(12:18:37 PM)</font> <b>Bob:</b></font>good good<br/>
</body></html>
""".lstrip()),
            models.History(
                local_username='LocalUser123',
                remote_username='RemoteUser345',
                messages=[
                    models.Message(
                        sender='RemoteUser345',
                        timestamp=datetime.datetime(2006, 12, 20, 12, 18, 8),
                        contents='how are you'),
                    models.Message(
                        sender='LocalUser123',
                        timestamp=datetime.datetime(2006, 12, 20, 12, 18, 37),
                        contents='good good')
                ]))

    def test_parse_log_with_one_simple_conversation_starting_in_am(self):
        self.assertEqual(
            parser.Parser().parse("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>Conversation with RemoteUser345 at 12/20/2006 12:18:08 AM on LocalUser123 (aim)</title></head><body><h3>Conversation with RemoteUser345 at 12/20/2006 12:18:08 AM on LocalUser123 (aim)</h3>
<font color="#A82F2F"><font size="2">(12:18:08 AM)</font> <b>Alice:</b></font> <html><span style='background: #ffffff;'>how are you</span></span></html><br/>
<font color="#16569E"><font size="2">(12:18:37 AM)</font> <b>Bob:</b></font>good good<br/>
</body></html>
""".lstrip()),
            models.History(
                local_username='LocalUser123',
                remote_username='RemoteUser345',
                messages=[
                    models.Message(
                        sender='RemoteUser345',
                        timestamp=datetime.datetime(2006, 12, 20, 0, 18, 8),
                        contents='how are you'),
                    models.Message(
                        sender='LocalUser123',
                        timestamp=datetime.datetime(2006, 12, 20, 0, 18, 37),
                        contents='good good')
                ]))

    def test_detects_when_timestamps_roll_over_to_next_day(self):
        self.assertEqual(
            parser.Parser().parse("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>Conversation with RemoteUser345 at 5/15/2006 11:59:59 PM on LocalUser123 (aim)</title></head><body><h3>Conversation with RemoteUser345 at 5/15/2006 11:59:59 PM on LocalUser123 (aim)</h3>
<font color="#A82F2F"><font size="2">(11:59:59 PM)</font> <b>Alice:</b></font> <html><span style='background: #ffffff;'>get ready for midnight</span></span></html><br/>
<font color="#A82F2F"><font size="2">(12:00:02 AM)</font> <b>Alice:</b></font> <html><span style='background: #ffffff;'>that was everything I dreamed</span></span></html><br/>
</body></html>
""".lstrip()),
            models.History(
                local_username='LocalUser123',
                remote_username='RemoteUser345',
                messages=[
                    models.Message(
                        sender='RemoteUser345',
                        timestamp=datetime.datetime(2006, 5, 15, 23, 59, 59),
                        contents='get ready for midnight'),
                    models.Message(
                        sender='RemoteUser345',
                        timestamp=datetime.datetime(2006, 5, 16, 0, 0, 2),
                        contents='that was everything I dreamed')
                ]))

    def test_handles_message_timestamps_with_date(self):
        self.assertEqual(
            parser.Parser().parse("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>Conversation with RemoteUser345 at 5/15/2006 11:59:59 PM on LocalUser123 (aim)</title></head><body><h3>Conversation with RemoteUser345 at 5/15/2006 11:59:59 PM on LocalUser123 (aim)</h3>
<font color="#A82F2F"><font size="2">(5/15/2006 2:35:18 PM)</font> <b>Alice:</b></font> <html><span style='background: #ffffff;'>hello there</span></span></html><br/>
</body></html>
""".lstrip()),
            models.History(
                local_username='LocalUser123',
                remote_username='RemoteUser345',
                messages=[
                    models.Message(
                        sender='RemoteUser345',
                        timestamp=datetime.datetime(2006, 5, 15, 14, 35, 18),
                        contents='hello there'),
                ]))

    def test_handles_messages_with_many_contents_results(self):
        self.assertEqual(
            parser.Parser().parse("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>Conversation with remoteuser123@example.com at 4/9/2007 2:45:36 AM on localuser567@example.com/Home (jabber)</title></head><body><h3>Conversation with remoteuser123@example.com at 4/9/2007 2:45:36 AM on localuser567@example.com/Home (jabber)</h3>
<font color="#A82F2F"><font size="2">(2:45:36 AM)</font> <b>Gabe:</b></font> <body>we need a &apos;bigger fish to fry&apos; poster</body><br/>
</body></html>
""".lstrip()),
            models.History(
                local_username='localuser567@example.com',
                remote_username='remoteuser123@example.com',
                messages=[
                    models.Message(
                        sender='remoteuser123@example.com',
                        timestamp=datetime.datetime(2007, 4, 9, 2, 45, 36),
                        contents='we need a \'bigger fish to fry\' poster'),
                ]))

    def test_raises_exception_when_title_has_unexpected_format(self):
        with self.assertRaises(parser.InvalidMetadata):
            parser.Parser().parse("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>BADTITLE BADTITLE BADTITLE BADTITLE</title></head><body><h3>Conversation with RemoteUser345 at 12/20/2006 12:18:08 PM on LocalUser123 (aim)</h3>
</body></html>
""".lstrip())
