import collections
import datetime
from xml.dom import minidom

SessionStartLine = collections.namedtuple(
    'SessionStartLine',
    field_names=['timestamp', 'medium', 'sender', 'recipient'])

SessionStopLine = collections.namedtuple(
    'SessionStopLine',
    field_names=['timestamp', 'medium', 'sender', 'recipient'])


def parse(line):
    document = minidom.parseString(line)
    return _parse_session_attributes(
        dict(document.childNodes[0].attributes.items()))


def _parse_session_attributes(attributes):
    if attributes[u'type'] == u'start':
        return _parse_session_start(attributes)
    else:
        return _parse_session_stop(attributes)


def _parse_session_start(attributes):
    return SessionStartLine(
        timestamp=_parse_timestamp_attribute(attributes[u'time']),
        medium=attributes[u'medium'],
        sender=attributes[u'from'],
        recipient=attributes[u'to'])


def _parse_session_stop(attributes):
    return SessionStopLine(
        timestamp=_parse_timestamp_attribute(attributes[u'time']),
        medium=attributes[u'medium'],
        sender=attributes[u'from'],
        recipient=attributes[u'to'])


def _parse_timestamp_attribute(timestamp_attribute):
    return datetime.datetime.utcfromtimestamp(int(timestamp_attribute))
