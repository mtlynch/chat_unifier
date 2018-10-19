import collections
import datetime
from xml.dom import minidom

SessionStartLine = collections.namedtuple(
    'SessionStartLine',
    field_names=['timestamp', 'medium', 'sender', 'recipient'])


def parse(line):
    document = minidom.parseString(line)
    return _parse_session_start(dict(document.childNodes[0].attributes.items()))


def _parse_session_start(attributes):
    timestamp = datetime.datetime.fromtimestamp(int(attributes[u'time']))

    return SessionStartLine(
        timestamp=timestamp,
        medium=attributes[u'medium'],
        sender=attributes[u'from'],
        recipient=attributes[u'to'])
