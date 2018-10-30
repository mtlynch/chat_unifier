from __future__ import absolute_import

import datetime
import re

from chat_unifier import models
from chat_unifier.parsers.pidgin import html_reader

_TITLE_PATTERN = re.compile(
    r'^Conversation with (?P<remote_username>.+) at (?P<start_date>\d{1,2}/\d{1,2}/\d{4}) (?P<start_time>\d{1,2}:\d{1,2}:\d{1,2}) (?P<am_pm>[AP]M) on (?P<local_username>.+) \((?P<medium>.+)\)$'
)


class Error(Exception):
    pass


class UnexpectedResultType(Error):
    pass


class UnexpectedMessageDirection(Error):
    pass


class InvalidMetadata(Error):
    pass


class Parser(object):

    def parse(self, log_contents):
        reader = html_reader.Reader()
        reader.feed(log_contents)
        converter = _ResultsToHistoryConverter(reader.results)
        return converter.convert()


class _ResultsToHistoryConverter(object):

    def __init__(self, results):
        self._results = results
        self._metadata = None
        self._last_timestamp = None

    def convert(self):
        self._process_metadata()
        return models.History(
            local_username=self._metadata['local_username'],
            remote_username=self._metadata['remote_username'],
            messages=self._process_messages())

    def _process_metadata(self):
        title = self._pop_result_with_type(html_reader.RESULT_TYPE_TITLE)
        self._metadata = _metadata_from_title(title)
        self._last_timestamp = self._metadata['start_timestamp']

    def _process_messages(self):
        messages = []
        while self._results:
            messages.append(self._process_next_message())
        return messages

    def _process_next_message(self):
        message_direction = self._pop_result_with_type(
            html_reader.RESULT_TYPE_MESSAGE_START)
        timestamp_raw = self._pop_result_with_type(
            html_reader.RESULT_TYPE_TIMESTAMP)
        # TODO(mtlynch): Save the display name.
        self._pop_result_with_type(html_reader.RESULT_TYPE_DISPLAY_NAME)
        contents = self._pop_result_with_type(
            html_reader.RESULT_TYPE_MESSAGE_CONTENTS)

        return models.Message(
            sender=self._sender_from_message_direction(message_direction),
            timestamp=self._parse_message_timestamp(timestamp_raw),
            contents=contents)

    def _sender_from_message_direction(self, message_direction):
        if message_direction == html_reader.MESSAGE_DIRECTION_OUTGOING:
            return self._metadata['local_username']
        elif message_direction == html_reader.MESSAGE_DIRECTION_INCOMING:
            return self._metadata['remote_username']
        else:
            raise UnexpectedMessageDirection(
                'Unrecognized message direction: %s' % message_direction)

    def _parse_message_timestamp(self, time_string):
        # Strip parens from timestamp.
        time_string = time_string[1:-1]
        if _timestamp_includes_date(time_string):
            timestamp = datetime.datetime.strptime(time_string,
                                                   '%m/%d/%Y %I:%M:%S %p')
        else:
            datetime_string = (
                self._last_timestamp.strftime('%m/%d/%Y') + ' ' + time_string)
            timestamp = datetime.datetime.strptime(datetime_string,
                                                   '%m/%d/%Y %I:%M:%S %p')
            if self._timestamp_rolled_over_to_next_day(timestamp):
                timestamp += datetime.timedelta(days=1)

        self._last_timestamp = timestamp
        return timestamp

    def _timestamp_rolled_over_to_next_day(self, timestamp):
        return timestamp < self._last_timestamp

    def _pop_result_with_type(self, result_type_expected):
        result_type, result_value = self._results.pop(0)
        if result_type != result_type_expected:
            raise UnexpectedResultType(
                'Expected result type %s, but got %s:%s' %
                (result_type_expected, result_type, result_value))
        return result_value


def _metadata_from_title(title):
    match = _TITLE_PATTERN.match(title)
    if not match:
        raise InvalidMetadata('Unexpected metadata format: %s' % title)
    local_username = _strip_username_suffix(match.group('local_username'))
    return {
        'local_username':
        local_username,
        'remote_username':
        match.group('remote_username'),
        'medium':
        match.group('medium'),
        'start_timestamp':
        _parse_timestamp_parts(
            match.group('start_date'), match.group('start_time'),
            match.group('am_pm')),
    }


def _strip_username_suffix(username):
    if '/' in username:
        return username.split('/')[0]
    return username


def _timestamp_includes_date(timestamp):
    return '/' in timestamp


def _parse_timestamp_parts(date_string, time_string, am_pm):
    timestamp_string = '%s %s %s' % (date_string, time_string, am_pm)
    return datetime.datetime.strptime(timestamp_string, '%m/%d/%Y %I:%M:%S %p')
