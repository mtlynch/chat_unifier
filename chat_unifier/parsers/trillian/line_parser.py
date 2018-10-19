import collections
import datetime
import urllib
from xml.dom import minidom


class Error(Exception):
    pass


class InvalidSessionType(Error):
    pass


class InvalidMessageType(Error):
    pass


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

IncomingPrivateMessageLine = collections.namedtuple(
    'IncomingPrivateMessageLine',
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
    try:
        session_type = attributes[u'type']
    except KeyError:
        raise InvalidSessionType('Session element has no \'type\' attribute')

    if session_type == u'start':
        return _parse_session_start(attributes)
    elif session_type == u'stop':
        return _parse_session_stop(attributes)
    else:
        raise InvalidSessionType('Unrecognized session type: %s' % session_type)


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
    try:
        message_type = attributes[u'type']
    except KeyError:
        raise InvalidMessageType('Message element has no \'type\' attribute')

    if message_type == u'outgoing_privateMessage':
        return _parse_outgoing_message(attributes)
    elif message_type == u'incoming_privateMessage':
        return _parse_incoming_message(attributes)
    else:
        raise InvalidMessageType('Unrecognized message type: %s' % message_type)


def _parse_outgoing_message(attributes):
    return OutgoingPrivateMessageLine(
        timestamp=_parse_timestamp_attribute(attributes[u'time']),
        medium=attributes[u'medium'],
        sender=attributes[u'from'],
        sender_display=attributes[u'from_display'],
        recipient=attributes[u'to'],
        contents=_decode_message_text(attributes[u'text']))


def _parse_incoming_message(attributes):
    return IncomingPrivateMessageLine(
        timestamp=_parse_timestamp_attribute(attributes[u'time']),
        medium=attributes[u'medium'],
        sender=attributes[u'from'],
        sender_display=attributes[u'from_display'],
        recipient=attributes[u'to'],
        contents=_decode_message_text(attributes[u'text']))


def _decode_message_text(text):
    return urllib.unquote(text)


def _parse_timestamp_attribute(timestamp_attribute):
    return datetime.datetime.utcfromtimestamp(int(timestamp_attribute))
