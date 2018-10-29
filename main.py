#!/usr/bin/python2

import argparse
import json
import os
import logging

from chat_unifier import json_serializer
from chat_unifier import history_merger
from chat_unifier.parsers.trillian_xml import parser as trillian_parser
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
    for log_dir in args.trillian:
        logger.info('Searching for logs in %s', log_dir)
        for log_path in trillian_xml_iterator.iterate_files(log_dir):
            with open(log_path) as log_handle:
                parser = trillian_parser.Parser()
                merger.add(parser.parse(log_handle.read()))
                logger.info('Parsed %s', os.path.basename(log_path))
    print json.dumps([h for h in merger],
                     indent=2,
                     sort_keys=True,
                     cls=json_serializer.Serializer)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Chat Unifier',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--trillian', action='append', help='Trillian XML log root')
    main(parser.parse_args())
