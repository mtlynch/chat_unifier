from HTMLParser import HTMLParser

RESULT_TYPE_TITLE = 'title'
RESULT_TYPE_MESSAGE_START = 'message-start'
RESULT_TYPE_TIMESTAMP = 'timestamp'
RESULT_TYPE_DISPLAY_NAME = 'display-name'
RESULT_TYPE_MESSAGE_CONTENTS = 'message-contents'

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
        self._results = []

    @property
    def results(self):
        return self._results

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'title':
            self._update_state(_STATE_PARSING_TITLE)
        if ((self._state == _STATE_SEEKING_NEXT_MESSAGE) and (tag == 'font')):
            if 'color' in attrs_dict:
                font_color = attrs_dict['color']
                if _is_local_user_font_color(font_color):
                    self._add_message_start('local')
                    self._update_state(_STATE_PARSING_TIMESTAMP)
                elif _is_remote_user_font_color(font_color):
                    self._add_message_start('remote')
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
            self._update_state(_STATE_SEEKING_NEXT_MESSAGE)

    def handle_data(self, data):
        if self._state == _STATE_PARSING_TITLE:
            self._add_title(data)
        elif self._state == _STATE_PARSING_TIMESTAMP:
            self._add_timestamp(data)
        elif self._state == _STATE_PARSING_DISPLAY_NAME:
            self._add_display_name(data)
        elif self._state == _STATE_PARSING_CONTENTS:
            if not data.strip():
                return
            self._add_message_contents(data)

    def _add_title(self, title):
        self.results.append((RESULT_TYPE_TITLE, title))

    def _add_message_start(self, message_type):
        self.results.append((RESULT_TYPE_MESSAGE_START, message_type))

    def _add_timestamp(self, timestamp):
        self.results.append((RESULT_TYPE_TIMESTAMP, timestamp))

    def _add_display_name(self, display_name):
        self.results.append((RESULT_TYPE_DISPLAY_NAME, display_name))

    def _add_message_contents(self, message_contents):
        self.results.append((RESULT_TYPE_MESSAGE_CONTENTS, message_contents))

    def _update_state(self, new_state):
        self._state = new_state
