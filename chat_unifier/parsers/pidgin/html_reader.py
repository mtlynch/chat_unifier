from HTMLParser import HTMLParser

RESULT_TYPE_TITLE = 'title'
RESULT_TYPE_MESSAGE_START = 'message-start'
RESULT_TYPE_TIMESTAMP = 'timestamp'
RESULT_TYPE_DISPLAY_NAME = 'display-name'
RESULT_TYPE_MESSAGE_CONTENTS = 'message-contents'

MESSAGE_DIRECTION_INCOMING = 'incoming'
MESSAGE_DIRECTION_OUTGOING = 'outgoing'

_STATE_SEEKING_TITLE = 1
_STATE_PARSING_TITLE = 2
_STATE_SEEKING_NEXT_MESSAGE = 3
_STATE_PARSING_TIMESTAMP = 4
_STATE_SEEKING_DISPLAY_NAME = 5
_STATE_PARSING_DISPLAY_NAME = 6
_STATE_SEEKING_CONTENTS = 7
_STATE_PARSING_CONTENTS = 8


class Error(Exception):
    pass


class UnexpectedFontColor(Error):
    pass


def _is_local_user_font_color(color):
    return color == '#16569E'


def _is_remote_user_font_color(color):
    return color == '#A82F2F'


def _is_system_message_font_color(color):
    return color == '#FF0000'


def _is_pidgin_message_font_color(color):
    return color == '#062585'


class Reader(HTMLParser):
    """Read relevant elements from Pidgin HTML log file.

    Read a Pidgin HTML log file, pulling out the relevant elements with minimal
    parsing. This is meant only to scrape the screen and leave more complex
    parsing to other components.
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self._state = _STATE_SEEKING_TITLE
        self._results = _ResultSequence()

    @property
    def results(self):
        return [r for r in self._results]

    def feed(self, html):
        html_annotated = _annotate_html(html)
        HTMLParser.feed(self, html_annotated)

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'title':
            self._update_state(_STATE_PARSING_TITLE)
        elif ((self._state == _STATE_SEEKING_NEXT_MESSAGE) and (tag == 'font')):
            if 'color' in attrs_dict:
                font_color = attrs_dict['color']
                if _is_local_user_font_color(font_color):
                    self._results.append_message_start(
                        MESSAGE_DIRECTION_OUTGOING)
                    self._update_state(_STATE_PARSING_TIMESTAMP)
                elif _is_remote_user_font_color(font_color):
                    self._results.append_message_start(
                        MESSAGE_DIRECTION_INCOMING)
                    self._update_state(_STATE_PARSING_TIMESTAMP)
                elif (_is_system_message_font_color(font_color) or
                      _is_pidgin_message_font_color(font_color)):
                    pass
                else:
                    raise UnexpectedFontColor(
                        'Font color %s is unexpected' % font_color)
        elif ((self._state == _STATE_SEEKING_DISPLAY_NAME) and (tag == 'b')):
            self._update_state(_STATE_PARSING_DISPLAY_NAME)

    def handle_endtag(self, tag):
        if ((self._state == _STATE_PARSING_TITLE) and (tag == 'title')):
            self._update_state(_STATE_SEEKING_NEXT_MESSAGE)
        elif ((self._state == _STATE_PARSING_TIMESTAMP) and (tag == 'font')):
            self._update_state(_STATE_SEEKING_DISPLAY_NAME)
        elif ((self._state == _STATE_PARSING_DISPLAY_NAME) and (tag == 'b')):
            self._update_state(_STATE_SEEKING_CONTENTS)
        elif ((self._state == _STATE_SEEKING_CONTENTS) and (tag == 'font')):
            self._update_state(_STATE_PARSING_CONTENTS)

    def handle_startendtag(self, tag, attrs):
        if ((self._state == _STATE_PARSING_CONTENTS) and (tag == 'br')):
            self._results.append_message_contents('\n')
        elif ((self._state == _STATE_PARSING_CONTENTS) and
              (tag == 'message-end')):
            self._update_state(_STATE_SEEKING_NEXT_MESSAGE)

    def handle_data(self, data):
        if self._state == _STATE_PARSING_TITLE:
            self._results.append_title(data)
        elif self._state == _STATE_PARSING_TIMESTAMP:
            self._results.append_timestamp(data)
        elif self._state == _STATE_PARSING_DISPLAY_NAME:
            self._results.append_display_name(data)
        elif self._state == _STATE_PARSING_CONTENTS:
            if data.strip():
                self._results.append_message_contents(data.decode('utf8'))
            else:
                self._results.append_message_contents('')

    def handle_entityref(self, name):
        decoded = _decode_html_entity_ref(name)
        if self._state == _STATE_PARSING_CONTENTS:
            self._results.append_message_contents(decoded)
        elif self._state == _STATE_PARSING_DISPLAY_NAME:
            self._results.append_display_name(decoded)

    def handle_charref(self, name):
        decoded = _decode_html_char_ref(name)
        if self._state == _STATE_PARSING_CONTENTS:
            self._results.append_message_contents(decoded)
        elif self._state == _STATE_PARSING_DISPLAY_NAME:
            self._results.append_display_name(decoded)

    def _update_state(self, new_state):
        self._state = new_state


class _ResultSequence(object):

    def __init__(self):
        self._results = []

    def __iter__(self):
        for r in self._results:
            yield r

    def append_title(self, title):
        self._results.append((RESULT_TYPE_TITLE, title))

    def append_message_start(self, message_type):
        self._results.append((RESULT_TYPE_MESSAGE_START, message_type))

    def append_timestamp(self, timestamp):
        self._results.append((RESULT_TYPE_TIMESTAMP, timestamp))

    def append_display_name(self, display_name):
        self._append_or_coalesce_result(RESULT_TYPE_DISPLAY_NAME, display_name)

    def append_message_contents(self, message_contents):
        self._append_or_coalesce_result(RESULT_TYPE_MESSAGE_CONTENTS,
                                        message_contents)

    def _append_or_coalesce_result(self, result_type, result_value):
        if self._results:
            last_result_type, last_result_value = self._results[-1]
            if last_result_type == result_type:
                self._results.pop()
                result_value = last_result_value + result_value
        self._results.append((result_type, result_value))


def _annotate_html(html):
    # We need to specially mark line-terminating <br> tags otherwise there's
    # ambiguity in where the message ends (<br> can appear within messages).
    return html.replace('\r\n', '\n').replace('<br/>\n', '<message-end/>\n')


def _decode_html_entity_ref(entity_ref):
    return HTMLParser().unescape('&' + entity_ref + ';')


def _decode_html_char_ref(entity_ref):
    return HTMLParser().unescape('&#' + entity_ref + ';')
