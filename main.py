#!/usr/bin/python2

import argparse
import os
import logging

from chat_unifier import debug_print
from chat_unifier import history_merger
from chat_unifier.parsers.trillian import parser as trillian_parser

logger = logging.getLogger(__name__)


def configure_logging():
    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-15s %(levelname)-4s %(message)s',
        '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)


def main(args):
    configure_logging()
    logger.info('Started runnning')
    merger = history_merger.Merger()
    for log_dir in args.log_dirs:
        for filename in os.listdir(log_dir):
            if not filename.endswith('xml'):
                continue
            full_path = os.path.join(log_dir, filename)
            with open(full_path) as log_handle:
                parser = trillian_parser.Parser()
                merger.add(parser.parse(log_handle.read()))
                logger.info('Parsed %s', filename)
    for history in merger:
        debug_print.print_history(history)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Chat Unifier',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'log_dirs', nargs='+', help='Directory containing log files')
    main(parser.parse_args())
