import datetime
import json


class Serializer(json.JSONEncoder):
    """Serializes list of History objects to JSON."""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return _timestamp_to_string(obj)
        return json.JSONEncoder.default(self, obj)

    def encode(self, obj):
        if isinstance(obj, list):
            return json.JSONEncoder.encode(self,
                                           _history_list_to_list_of_dicts(obj))
        return json.JSONEncoder.encode(self, obj)


def _history_list_to_list_of_dicts(history_list):
    return [_history_to_dict(h) for h in history_list]


def _history_to_dict(history):
    return {
        'localUsername': history.local_username,
        'remoteUsername': history.remote_username,
        'messages': _messages_to_list_of_dicts(history.messages)
    }


def _messages_to_list_of_dicts(messages):
    return [_message_to_dict(m) for m in messages]


def _message_to_dict(message):
    return {
        'sender': message.sender,
        'timestamp': message.timestamp,
        'contents': message.contents,
    }


def _timestamp_to_string(timestamp):
    return timestamp.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
