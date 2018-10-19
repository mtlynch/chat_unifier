from __future__ import absolute_import

from chat_unifier import models
from chat_unifier.parsers.trillian import line_parser


class Parser(object):

    def parse(self, log_contents):
        messages = []
        lines = [x for x in log_contents.split('\n') if x]
        for line in lines:
            parsed_line = line_parser.parse(line)
            if _is_message_line(parsed_line):
                messages.append(
                    models.Message(
                        sender=parsed_line.sender,
                        timestamp=parsed_line.timestamp,
                        contents=parsed_line.contents))
        return models.History(sessions=[models.Session(messages=messages)])


def _is_message_line(parsed_line):
    return (isinstance(parsed_line, line_parser.OutgoingPrivateMessageLine) or
            isinstance(parsed_line, line_parser.IncomingPrivateMessageLine))
