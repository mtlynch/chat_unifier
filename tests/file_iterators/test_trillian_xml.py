import os
import unittest

import mock

from chat_unifier.file_iterators import trillian_xml


class TrillianXmlFileIteratorTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_picks_correct_trillian_log_files(self):
        with mock.patch.object(os, 'walk') as mock_walk:
            mock_walk.return_value = [
                ('/logs', ('AIM', 'junk'), ('README.txt',)),
                ('/logs/AIM', ('Query',), ()),
                ('/logs/AIM/Query', (),
                 ('DummyBuddy123.xml', 'DummyBuddy123-assets.xml',
                  'DummyBuddy123.log', 'DummyBuddy234.xml',
                  'DummyBuddy234-assets.xml', 'DummyBuddy234.log')),
                ('/logs/junk', (), ('junk.png',)),
            ]
            self.assertEqual([
                '/logs/AIM/Query/DummyBuddy123.xml',
                '/logs/AIM/Query/DummyBuddy234.xml'
            ], [f for f in trillian_xml.iterate_files('/logs')])
