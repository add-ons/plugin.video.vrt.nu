# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=invalid-name,missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import statichelper


class HelperTests(unittest.TestCase):

    def test_url_to_episode(self):
        url = '//www.vrt.be/vrtnu/a-z/buck/1/buck-s1a32/'
        episode = '/vrtnu/a-z/buck/1/buck-s1a32/'
        self.assertEqual(episode, statichelper.url_to_episode(url))

    def test_url_to_program(self):
        url = '//www.vrt.be/vrtnu/a-z/buck/1/buck-s1a32/'
        program = 'buck'
        self.assertEqual(program, statichelper.url_to_program(url))

        url = '/vrtnu/a-z/buck/1/buck-s1a32/'
        program = 'buck'
        self.assertEqual(program, statichelper.url_to_program(url))


if __name__ == '__main__':
    unittest.main()
