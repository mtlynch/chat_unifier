import collections

Message = collections.namedtuple(
    'Message', field_names=['sender', 'timestamp', 'contents'])
