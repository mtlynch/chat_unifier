import collections

Message = collections.namedtuple(
    'Message', field_names=['sender', 'timestamp', 'contents'])

Session = collections.namedtuple('Session', field_names=['messages'])

History = collections.namedtuple('History', field_names=['sessions'])
