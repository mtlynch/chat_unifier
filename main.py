#!/usr/bin/python2

import argparse
import json
import os
import logging

from chat_unifier import json_serializer
from chat_unifier import history_merger
from chat_unifier.parsers.pidgin import parser as pidgin_parser
from chat_unifier.parsers.trillian_xml import parser as trillian_parser
from chat_unifier.file_iterators import pidgin as pidgin_iterator
from chat_unifier.file_iterators import trillian_xml as trillian_xml_iterator

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
    processors = [
        (args.trillian, trillian_xml_iterator, trillian_parser.Parser()),
        (args.pidgin, pidgin_iterator, pidgin_parser.Parser()),
    ]
    for dir_roots, file_iterator, log_parser in processors:
        if dir_roots:
            _process_log_dirs(dir_roots, file_iterator, log_parser, merger)
    print json.dumps([h for h in merger],
                     indent=2,
                     sort_keys=True,
                     cls=json_serializer.Serializer)


def _process_log_dirs(dir_roots, file_iterator, log_parser, merger):
    for dir_root in dir_roots:
        _process_log_dir(dir_root, file_iterator, log_parser, merger)


def _process_log_dir(dir_root, file_iterator, log_parser, merger):
    logger.info('Searching for logs in %s', dir_root)
    for log_path in file_iterator.iterate_files(dir_root):
        logger.info('Parsing %s', log_path)
        with open(log_path) as log_handle:
            try:
                merger.add(log_parser.parse(log_handle.read()))
            except Exception as ex:
                logger.error('Failed to parse: %s', ex.message)
            logger.info('Parsed %s', os.path.basename(log_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Chat Unifier',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--trillian', action='append', help='Trillian XML log root')
    parser.add_argument('--pidgin', action='append', help='Pidgin log root')
    main(parser.parse_args())
