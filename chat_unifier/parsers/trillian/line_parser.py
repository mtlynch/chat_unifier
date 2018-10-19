import collections
import datetime
import urllib
from xml.dom import minidom

SessionStartLine = collections.namedtuple(
    'SessionStartLine',
    field_names=['timestamp', 'medium', 'sender', 'recipient'])

SessionStopLine = collections.namedtuple(
    'SessionStopLine',
    field_names=['timestamp', 'medium', 'sender', 'recipient'])

OutgoingPrivateMessageLine = collections.namedtuple(
    'OutgoingPrivateMessageLine',
    field_names=[
        'timestamp', 'medium', 'sender', 'sender_display', 'recipient',
        'contents'
    ])


def parse(line):
    document = minidom.parseString(line)
    node = document.childNodes[0]
    tag_name = node.tagName
    attributes = dict(node.attributes.items())
    if tag_name == 'session':
        return _parse_session_attributes(attributes)
    elif tag_name == 'message':
        return _parse_message_attributes(attributes)


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


def _parse_message_attributes(attributes):
    if attributes[u'type'] == u'outgoing_privateMessage':
        return _parse_outgoing_message(attributes)
    else:
        return _parse_incoming_message(attributes)


def _parse_outgoing_message(attributes):
    return OutgoingPrivateMessageLine(
        timestamp=_parse_timestamp_attribute(attributes[u'time']),
        medium=attributes[u'medium'],
        sender=attributes[u'from'],
        sender_display=attributes[u'from_display'],
        recipient=attributes[u'to'],
        contents=_decode_message_text(attributes[u'text']))


def _parse_incoming_message(attributes):
    raise NotImplementedError('Incoming messages not yet supported')


def _decode_message_text(text):
    return urllib.unquote(text)


def _parse_timestamp_attribute(timestamp_attribute):
    return datetime.datetime.utcfromtimestamp(int(timestamp_attribute))
