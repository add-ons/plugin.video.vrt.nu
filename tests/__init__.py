# -*- coding: utf-8 -*-
"""Add paths for unittest"""
from __future__ import absolute_import, division, unicode_literals

import os
import sys
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(PROJECT_PATH, 'resources/lib')
TESTS_PATH = os.path.join(PROJECT_PATH, 'tests')
sys.path.append(SOURCE_PATH)
sys.path.append(TESTS_PATH)
