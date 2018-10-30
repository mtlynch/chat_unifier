import os
import unittest

import mock

from chat_unifier.file_iterators import pidgin


class PidginFileIteratorTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_picks_correct_log_files(self):
        with mock.patch.object(os, 'walk') as mock_walk:
            mock_walk.return_value = [
                ('/logs', ('aim',), ('README.txt',)),
                ('/logs/aim', ('LocalUser123',), ()),
                ('/log/aim/LocalUser123', ('RemoteUser345', 'RemoteUser456'),
                 ()),
                ('/log/aim/LocalUser123/RemoteUser345', (),
                 ('2007-02-24.020826-0500EST.html',
                  '2007-02-25.154550-0500EST.html')),
                ('/log/aim/LocalUser123/RemoteUser456', (),
                 ('2006-11-19.195755-0500EST.html',
                  '2006-11-22.112333-0500EST.html')),
            ]
            self.assertEqual([
                '/log/aim/LocalUser123/RemoteUser345/2007-02-24.020826-0500EST.html',
                '/log/aim/LocalUser123/RemoteUser345/2007-02-25.154550-0500EST.html',
                '/log/aim/LocalUser123/RemoteUser456/2006-11-19.195755-0500EST.html',
                '/log/aim/LocalUser123/RemoteUser456/2006-11-22.112333-0500EST.html',
            ], [f for f in pidgin.iterate_files('/logs')])

    def test_ignores_irc_log_files(self):
        with mock.patch.object(os, 'walk') as mock_walk:
            mock_walk.return_value = [
                ('/logs', ('aim', 'irc'), ('README.txt',)),
                ('/logs/aim', ('LocalUser123',), ()),
                ('/log/aim/LocalUser123', ('RemoteUser345',), ()),
                ('/log/aim/LocalUser123/RemoteUser345', (),
                 ('2007-02-24.020826-0500EST.html',
                  '2007-02-25.154550-0500EST.html')),
                ('/log/irc', ('localuser123@irc.freenode.net',), ()),
                ('/log/irc/localuser123@irc.freenode.net', ('#dummy.chat',),
                 ()),
                ('/log/irc/localuser123@irc.freenode.net/#dummy.chat', (),
                 ('2006-06-21.200806-0400EST.html',)),
            ]
            self.assertEqual([
                '/log/aim/LocalUser123/RemoteUser345/2007-02-24.020826-0500EST.html',
                '/log/aim/LocalUser123/RemoteUser345/2007-02-25.154550-0500EST.html',
            ], [f for f in pidgin.iterate_files('/logs')])

    def test_ignores_system_log_files(self):
        with mock.patch.object(os, 'walk') as mock_walk:
            mock_walk.return_value = [
                ('/logs', ('aim',), ()),
                ('/logs/aim', ('LocalUser123',), ()),
                ('/log/aim/LocalUser123', ('RemoteUser345', '.system'), ()),
                ('/log/aim/LocalUser123/RemoteUser345', (),
                 ('2007-02-24.020826-0500EST.html',
                  '2007-02-25.154550-0500EST.html')),
                ('/log/aim/LocalUser123/.system', (),
                 ('2007-03-05.231324-0500EST.html',)),
            ]
            self.assertEqual([
                '/log/aim/LocalUser123/RemoteUser345/2007-02-24.020826-0500EST.html',
                '/log/aim/LocalUser123/RemoteUser345/2007-02-25.154550-0500EST.html',
            ], [f for f in pidgin.iterate_files('/logs')])
