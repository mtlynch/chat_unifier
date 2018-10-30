import unittest

from chat_unifier.parsers.pidgin import html_reader


class HtmlReaderTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.reader = html_reader.Reader()

    def test_parse_log_with_simple_conversation(self):
        self.reader.feed("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>Conversation with RemoteUser345 at 12/20/2006 12:18:08 PM on LocalUser123 (aim)</title></head><body><h3>Conversation with RemoteUser345 at 12/20/2006 12:18:08 PM on LocalUser123 (aim)</h3>
<font color="#A82F2F"><font size="2">(12:18:08 PM)</font> <b>Alice:</b></font> <html><span style='background: #ffffff;'>how are you</span></span></html><br/>
<font color="#16569E"><font size="2">(12:18:37 PM)</font> <b>Bob:</b></font>good good<br/>
</body></html>
""".lstrip())
        self.assertEqual([
            (html_reader.RESULT_TYPE_TITLE,
             'Conversation with RemoteUser345 at 12/20/2006 12:18:08 PM on LocalUser123 (aim)'
            ),
            (html_reader.RESULT_TYPE_MESSAGE_START,
             html_reader.MESSAGE_DIRECTION_INCOMING),
            (html_reader.RESULT_TYPE_TIMESTAMP, '(12:18:08 PM)'),
            (html_reader.RESULT_TYPE_DISPLAY_NAME, 'Alice:'),
            (html_reader.RESULT_TYPE_MESSAGE_CONTENTS, 'how are you'),
            (html_reader.RESULT_TYPE_MESSAGE_START,
             html_reader.MESSAGE_DIRECTION_OUTGOING),
            (html_reader.RESULT_TYPE_TIMESTAMP, '(12:18:37 PM)'),
            (html_reader.RESULT_TYPE_DISPLAY_NAME, 'Bob:'),
            (html_reader.RESULT_TYPE_MESSAGE_CONTENTS, 'good good'),
        ], self.reader.results)

    def test_parse_log_with_simple_conversation_with_cr_lf_line_endings(self):
        self.reader.feed("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>Conversation with RemoteUser345 at 12/20/2006 12:18:08 PM on LocalUser123 (aim)</title></head><body><h3>Conversation with RemoteUser345 at 12/20/2006 12:18:08 PM on LocalUser123 (aim)</h3>
<font color="#A82F2F"><font size="2">(12:18:08 PM)</font> <b>Alice:</b></font> <html><span style='background: #ffffff;'>how are you</span></span></html><br/>
<font color="#16569E"><font size="2">(12:18:37 PM)</font> <b>Bob:</b></font>good good<br/>
</body></html>
""".lstrip().replace('\n', '\r\n'))
        self.assertEqual([
            (html_reader.RESULT_TYPE_TITLE,
             'Conversation with RemoteUser345 at 12/20/2006 12:18:08 PM on LocalUser123 (aim)'
            ),
            (html_reader.RESULT_TYPE_MESSAGE_START,
             html_reader.MESSAGE_DIRECTION_INCOMING),
            (html_reader.RESULT_TYPE_TIMESTAMP, '(12:18:08 PM)'),
            (html_reader.RESULT_TYPE_DISPLAY_NAME, 'Alice:'),
            (html_reader.RESULT_TYPE_MESSAGE_CONTENTS, 'how are you'),
            (html_reader.RESULT_TYPE_MESSAGE_START,
             html_reader.MESSAGE_DIRECTION_OUTGOING),
            (html_reader.RESULT_TYPE_TIMESTAMP, '(12:18:37 PM)'),
            (html_reader.RESULT_TYPE_DISPLAY_NAME, 'Bob:'),
            (html_reader.RESULT_TYPE_MESSAGE_CONTENTS, 'good good'),
        ], self.reader.results)

    def test_parse_log_with_no_closing_body_and_html_tags(self):
        self.reader.feed("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>Conversation with RemoteUser345 at 12/20/2006 12:18:08 PM on LocalUser123 (aim)</title></head><body><h3>Conversation with RemoteUser345 at 12/20/2006 12:18:08 PM on LocalUser123 (aim)</h3>
<font color="#A82F2F"><font size="2">(12:18:08 PM)</font> <b>Alice:</b></font> <html><span style='background: #ffffff;'>how are you</span></span></html><br/>
<font color="#16569E"><font size="2">(12:18:37 PM)</font> <b>Bob:</b></font>good good<br/>
""".lstrip())
        self.assertEqual([
            (html_reader.RESULT_TYPE_TITLE,
             'Conversation with RemoteUser345 at 12/20/2006 12:18:08 PM on LocalUser123 (aim)'
            ),
            (html_reader.RESULT_TYPE_MESSAGE_START,
             html_reader.MESSAGE_DIRECTION_INCOMING),
            (html_reader.RESULT_TYPE_TIMESTAMP, '(12:18:08 PM)'),
            (html_reader.RESULT_TYPE_DISPLAY_NAME, 'Alice:'),
            (html_reader.RESULT_TYPE_MESSAGE_CONTENTS, 'how are you'),
            (html_reader.RESULT_TYPE_MESSAGE_START,
             html_reader.MESSAGE_DIRECTION_OUTGOING),
            (html_reader.RESULT_TYPE_TIMESTAMP, '(12:18:37 PM)'),
            (html_reader.RESULT_TYPE_DISPLAY_NAME, 'Bob:'),
            (html_reader.RESULT_TYPE_MESSAGE_CONTENTS, 'good good'),
        ], self.reader.results)

    def test_allows_br_in_message_body(self):
        self.reader.feed("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>Conversation with RemoteUser345 at 12/20/2006 3:33:44 PM on LocalUser123 (aim)</title></head><body><h3>Conversation with RemoteUser345 at 12/20/2006 3:33:44 PM on LocalUser123 (aim)</h3>
<font color="#16569E"><font size="2">(3:33:44 PM)</font> <b>Bob:</b></font> <br/>PARKER<br/>I saw you last week and you weren't showing at all. Tell me Steve, what trimester are you in?<br/>
<font color="#16569E"><font size="2">(3:34:13 PM)</font> <b>Bob:</b></font> <br/>STEVE<br/>Well this baby's different Parker, because it's on a semester system<br/>
</body></html>
""".lstrip())
        self.assertEqual([
            (html_reader.RESULT_TYPE_TITLE,
             'Conversation with RemoteUser345 at 12/20/2006 3:33:44 PM on LocalUser123 (aim)'
            ),
            (html_reader.RESULT_TYPE_MESSAGE_START,
             html_reader.MESSAGE_DIRECTION_OUTGOING),
            (html_reader.RESULT_TYPE_TIMESTAMP, '(3:33:44 PM)'),
            (html_reader.RESULT_TYPE_DISPLAY_NAME, 'Bob:'),
            (html_reader.RESULT_TYPE_MESSAGE_CONTENTS,
             '\nPARKER\nI saw you last week and you weren\'t showing at all. Tell me Steve, what trimester are you in?'
            ),
            (html_reader.RESULT_TYPE_MESSAGE_START,
             html_reader.MESSAGE_DIRECTION_OUTGOING),
            (html_reader.RESULT_TYPE_TIMESTAMP, '(3:34:13 PM)'),
            (html_reader.RESULT_TYPE_DISPLAY_NAME, 'Bob:'),
            (html_reader.RESULT_TYPE_MESSAGE_CONTENTS,
             '\nSTEVE\nWell this baby\'s different Parker, because it\'s on a semester system'
            ),
        ], self.reader.results)

    def test_allows_nbsp_in_message_body(self):
        self.reader.feed("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>Conversation with RemoteUser345 at 12/20/2006 3:33:44 PM on LocalUser123 (aim)</title></head><body><h3>Conversation with RemoteUser345 at 12/20/2006 3:33:44 PM on LocalUser123 (aim)</h3>
<font color="#A82F2F"><font size="2">(12:47:11 PM)</font> <b>Alice:</b></font> &nbsp;yeah?<br/>
</body></html>
""".lstrip())
        self.assertEqual([
            (html_reader.RESULT_TYPE_TITLE,
             'Conversation with RemoteUser345 at 12/20/2006 3:33:44 PM on LocalUser123 (aim)'
            ),
            (html_reader.RESULT_TYPE_MESSAGE_START,
             html_reader.MESSAGE_DIRECTION_INCOMING),
            (html_reader.RESULT_TYPE_TIMESTAMP, '(12:47:11 PM)'),
            (html_reader.RESULT_TYPE_DISPLAY_NAME, 'Alice:'),
            (html_reader.RESULT_TYPE_MESSAGE_CONTENTS, u'\xa0yeah?'),
        ], self.reader.results)

    def test_parse_log_ignores_special_message_types(self):
        self.reader.feed("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>Conversation with RemoteUser345 at 12/20/2006 6:05:37 PM on LocalUser123 (aim)</title></head><body><h3>Conversation with RemoteUser345 at 12/20/2006 6:05:37 PM on LocalUser123 (aim)</h3>
<font color="#16569E"><font size="2">(6:05:37 PM)</font> <b>Bob:</b></font>heyo heyo<br/>
<font size="2">(6:07:32 PM)</font><b> Alice has signed off.</b><br/>
<font color="#FF0000"><font size="2">(6:05:38 PM)</font><b> Unable to send message: Not logged in</b></font><br/>
<font color="#062585"><font size="2">(6:05:39 PM)</font> <b>***Alice</b></font> smells good<br/>
<font color="#A82F2F"><font size="2">(6:06:58 PM)</font> <b>Alice:</b></font> <html><span style='background: #ffffff;'>wassup</span></span></html><br/>

</body></html>
""".lstrip())
        self.assertEqual([
            (html_reader.RESULT_TYPE_TITLE,
             'Conversation with RemoteUser345 at 12/20/2006 6:05:37 PM on LocalUser123 (aim)'
            ),
            (html_reader.RESULT_TYPE_MESSAGE_START,
             html_reader.MESSAGE_DIRECTION_OUTGOING),
            (html_reader.RESULT_TYPE_TIMESTAMP, '(6:05:37 PM)'),
            (html_reader.RESULT_TYPE_DISPLAY_NAME, 'Bob:'),
            (html_reader.RESULT_TYPE_MESSAGE_CONTENTS, 'heyo heyo'),
            (html_reader.RESULT_TYPE_MESSAGE_START,
             html_reader.MESSAGE_DIRECTION_INCOMING),
            (html_reader.RESULT_TYPE_TIMESTAMP, '(6:06:58 PM)'),
            (html_reader.RESULT_TYPE_DISPLAY_NAME, 'Alice:'),
            (html_reader.RESULT_TYPE_MESSAGE_CONTENTS, 'wassup'),
        ], self.reader.results)

    def test_decodes_html_encoded_entities_in_message_contents(self):
        self.reader.feed("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>Conversation with remoteuser123@example.com at 4/9/2007 2:45:36 AM on localuser567@example.com/Home (jabber)</title></head><body><h3>Conversation with remoteuser123@example.com at 4/9/2007 2:45:36 AM on localuser567@example.com/Home (jabber)</h3>
<font color="#A82F2F"><font size="2">(2:45:36 AM)</font> <b>Gabe:</b></font> <body>we need a &apos;bigger fish to fry&apos; poster</body><br/>
</body></html>
""".lstrip())
        self.assertEqual([
            (html_reader.RESULT_TYPE_TITLE,
             'Conversation with remoteuser123@example.com at 4/9/2007 2:45:36 AM on localuser567@example.com/Home (jabber)'
            ),
            (html_reader.RESULT_TYPE_MESSAGE_START,
             html_reader.MESSAGE_DIRECTION_INCOMING),
            (html_reader.RESULT_TYPE_TIMESTAMP, '(2:45:36 AM)'),
            (html_reader.RESULT_TYPE_DISPLAY_NAME, 'Gabe:'),
            (html_reader.RESULT_TYPE_MESSAGE_CONTENTS,
             u'we need a \'bigger fish to fry\' poster'),
        ], self.reader.results)

    def test_decodes_html_encoded_entities_in_display_name(self):
        self.reader.feed("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>Conversation with RemoteUser987 at 7/4/2006 3:36:09 PM on LocalUser123 (aim)</title></head><body><h3>Conversation with RemoteUser987 at 7/4/2006 3:36:09 PM on LocalUser123 (aim)</h3>
<font color="#A82F2F"><font size="2">(3:36:09 PM)</font> <b>Alice &lt;AUTO-REPLY&gt;:</b></font> I am away from my computer right now.<br/>
</body></html>
""".lstrip())
        self.assertEqual([
            (html_reader.RESULT_TYPE_TITLE,
             'Conversation with RemoteUser987 at 7/4/2006 3:36:09 PM on LocalUser123 (aim)'
            ),
            (html_reader.RESULT_TYPE_MESSAGE_START,
             html_reader.MESSAGE_DIRECTION_INCOMING),
            (html_reader.RESULT_TYPE_TIMESTAMP, '(3:36:09 PM)'),
            (html_reader.RESULT_TYPE_DISPLAY_NAME, 'Alice <AUTO-REPLY>:'),
            (html_reader.RESULT_TYPE_MESSAGE_CONTENTS,
             ' I am away from my computer right now.'),
        ], self.reader.results)

    def test_decodes_html_encoded_char_refs_in_message_contents(self):
        self.reader.feed("""
<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"><title>Conversation with remoteuser123@example.com at 4/9/2007 2:45:36 AM on localuser567@example.com/Home (jabber)</title></head><body><h3>Conversation with remoteuser123@example.com at 4/9/2007 2:45:36 AM on localuser567@example.com/Home (jabber)</h3>
<font color="#A82F2F"><font size="2">(2:45:36 AM)</font> <b>Gabe:</b></font> <body>we need a &#39;bigger fish to fry&apos; poster</body><br/>
</body></html>
""".lstrip())
        self.assertEqual([
            (html_reader.RESULT_TYPE_TITLE,
             'Conversation with remoteuser123@example.com at 4/9/2007 2:45:36 AM on localuser567@example.com/Home (jabber)'
            ),
            (html_reader.RESULT_TYPE_MESSAGE_START,
             html_reader.MESSAGE_DIRECTION_INCOMING),
            (html_reader.RESULT_TYPE_TIMESTAMP, '(2:45:36 AM)'),
            (html_reader.RESULT_TYPE_DISPLAY_NAME, 'Gabe:'),
            (html_reader.RESULT_TYPE_MESSAGE_CONTENTS,
             u'we need a \'bigger fish to fry\' poster'),
        ], self.reader.results)
