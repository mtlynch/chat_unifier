from chat_unifier import models


class Merger(object):

    def __init__(self):
        self._histories = {}

    def __iter__(self):
        for v in self._histories.itervalues():
            yield v

    def add(self, history):
        key = _key_for_history(history)
        if key in self._histories:
            existing_history = self._histories[key]
            self._histories[key] = _merge_histories(existing_history, history)
        else:
            self._histories[key] = history


def _key_for_history(history):
    return '%s:%s' % (history.local_username, ','.join(
        history.remote_usernames))


def _merge_histories(a, b):
    messages = sorted(a.messages + b.messages, key=lambda m: m.timestamp)
    return models.History(
        local_username=a.local_username,
        remote_usernames=a.remote_usernames,
        messages=messages)
