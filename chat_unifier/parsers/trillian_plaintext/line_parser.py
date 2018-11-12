import collections


# TODO(mtlynch): Move these to a common module so we can share between Trillian
# XML parser and Trillian plaintext parser.
SessionStartLine = collections.namedtuple(
    'SessionStartLine',
    field_names=['timestamp', 'medium', 'local_username', 'remote_username'])

SessionStopLine = collections.namedtuple(
    'SessionStopLine',
    field_names=['timestamp', 'medium', 'local_username', 'remote_username'])

InformationalMessageLine = collections.namedtuple(
    'InformationalMessageLine', field_names=['timestamp', 'medium', 'contents'])

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
    raise NotImplementedError('Still need to write this')
