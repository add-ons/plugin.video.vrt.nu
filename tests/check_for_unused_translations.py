#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Quick and dirty way to check if all translations might be used. """

# pylint: disable=invalid-name,superfluous-parens

import subprocess
import sys

import polib

error = 0

# Load all python code from git
code = subprocess.check_output(['git', 'grep', '', '--', 'resources/*.py', 'resources/settings.xml']).decode('utf-8')

# Load po file
po = polib.pofile('resources/language/resource.language.en_gb/strings.po')
for entry in po:
    # Extract msgctxt
    msgctxt = entry.msgctxt.lstrip('#')

    if msgctxt not in code:
        print('No usage found for translation:')
        print(entry)
        error = 1

sys.exit(error)
