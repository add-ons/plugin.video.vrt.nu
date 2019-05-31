# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

''' This is the actual VRT NU video plugin entry point '''

from __future__ import absolute_import, division, unicode_literals
import sys

from resources.lib import router

if __name__ == '__main__':
    router.router(sys.argv)
