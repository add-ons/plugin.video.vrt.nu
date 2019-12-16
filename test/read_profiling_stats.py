#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Process profiling stats"""

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import pstats

STATS = pstats.Stats(sys.argv[1])
STATS.sort_stats('name').print_stats()
STATS.sort_stats('cumulative').print_stats(20)
