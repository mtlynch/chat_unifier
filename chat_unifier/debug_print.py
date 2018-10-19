def print_history(history):
    for session in history.sessions:
        print_session(session)


def print_session(session):
    for message in session.messages:
        print_message(message)


def print_message(message):
    print '%s (%s): %s' % (message.sender, _format_timestamp(message.timestamp),
                           message.contents)


def _format_timestamp(timestamp):
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')
