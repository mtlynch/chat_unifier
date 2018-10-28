import collections

Message = collections.namedtuple(
    'Message', field_names=['sender', 'timestamp', 'contents'])

History = collections.namedtuple(
    'History', field_names=['local_username', 'remote_username', 'messages'])
