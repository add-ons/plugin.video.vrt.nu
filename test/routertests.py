# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

from resources.lib import router

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')


class TestRouter(unittest.TestCase):

    def test_main_menu(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', ''])

    # LISTING_FAVORITES = 'favorites'
    def test_favorites(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=favorites'])
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingaztvshows&use_favorites=True'])
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingrecent&use_favorites=True'])
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingrecent&use_favorites=True&page=2'])
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingoffline&use_favorites=True'])

    # LISTING_AZ_TVSHOWS = 'listingaztvshows'
    def test_az_menu(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingaztvshows'])

    # LISTING_EPISODES = 'listingepisodes'
    def test_episodes_menu(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingepisodes&video_url=/vrtnu/a-z/het-journaal.relevant/'])

    # LISTING_ALL_EPISODES = 'listingallepisodes'
    def test_all_episodes_menu(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingallepisodes&video_url=/vrtnu/a-z/thuis.relevant/'])

    # LISTING_CATEGORIES = 'listingcategories'
    def test_categories_menu(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingcategories'])

    # LISTING_CATEGORY_TVSHOWS = 'listingcategorytvshows'
    def test_categories_tvshow_menu(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingcategorytvshows&category=docu'])

    # LISTING_CHANNELS = 'listingchannels'
    def test_channels_menu(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingchannels'])

    # LISTING_LIVE = 'listinglive'
    def test_livetv_menu(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listinglive'])

    # LISTING_RECENT = 'listingrecent'
    def test_recent_menu(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingrecent'])
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingrecent&page=2'])

    # LISTING_OFFLINE = 'listingoffline'
    def test_offline_menu(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingoffline'])

    # LISTING_TVGUIDE = 'listingtvguide'
    def test_tvguide_date_menu(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingtvguide'])
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingtvguide&date=today'])
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=listingtvguide&date=today&channel=canvas'])

    # SEARCH = 'search'
    def test_search_menu(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=search'])
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=search&query=dag'])
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=search&query=dag&page=2'])

    # FOLLOW = 'follow'
    def test_follow_action(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=follow&program=Thuis&path=thuis'])

    # UNFOLLOW = 'unfollow'
    def test_unfollow_action(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=unfollow&program=Thuis&path=thuis'])

    # CLEAR_COOKIES = 'deletetokens'
    def test_clear_cookies_action(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=deletetokens'])

    # INVALIDATE_CACHES = 'invalidatecaches'
    def test_invalidate_caches_action(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=invalidatecaches'])

    # REFRESH_FAVORITES = 'refreshfavorites'
    def test_refresh_favorites_action(self):
        router.router(['plugin://plugin.video.vrt.nu', '0', '?action=refreshfavorites'])


if __name__ == '__main__':
    unittest.main()
