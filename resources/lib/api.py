# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Implements VRT MAX GraphQL API functionality"""

from __future__ import absolute_import, division, unicode_literals

from helperobjects import TitleItem
from kodiutils import colour, get_setting_bool, get_setting_int, get_url_json, localize, url_for
from utils import shorten_link

GRAPHQL_URL = 'https://www.vrt.be/vrtnu-api/graphql/v1'


def generate_plot(plot, region, product_placement, mpaa, offtime, permalink):
    """Generate plot"""
    from datetime import datetime
    import dateutil.parser
    import dateutil.tz

    # Add additional metadata to plot
    plot_meta = ''
    # Only display when a video disappears if it is within the next 3 months
    # Show the remaining days/hours the episode is still available
    if offtime:
        now = datetime.now(dateutil.tz.tzlocal())
        remaining = offtime - now
        if remaining.days / 365 > 5:
            pass  # If it is available for more than 5 years, do not show
        elif remaining.days / 365 > 2:
            plot_meta += localize(30202, years=int(remaining.days / 365))  # X years remaining
        elif remaining.days / 30.5 > 3:
            plot_meta += localize(30203, months=int(remaining.days / 30.5))  # X months remaining
        elif remaining.days > 1:
            plot_meta += localize(30204, days=remaining.days)  # X days to go
        elif remaining.days == 1:
            plot_meta += localize(30205)  # 1 day to go
        elif remaining.seconds // 3600 > 1:
            plot_meta += localize(30206, hours=remaining.seconds // 3600)  # X hours to go
        elif remaining.seconds // 3600 == 1:
            plot_meta += localize(30207)  # 1 hour to go
        else:
            plot_meta += localize(30208, minutes=remaining.seconds // 60)  # X minutes to go

    if region == 'BE':
        if plot_meta:
            plot_meta += '  '
        plot_meta += localize(30201)  # Geo-blocked

    # Add product placement
    if product_placement is True:
        if plot_meta:
            plot_meta += '  '
        plot_meta += '[B]PP[/B]'

    # Add film rating
    if mpaa:
        if plot_meta:
            plot_meta += '  '
        plot_meta += '[B]{}[/B]'.format(mpaa)

    if plot_meta:
        plot = '{}\n\n{}'.format(plot_meta, plot)

    permalink = shorten_link(permalink)
    if permalink and get_setting_bool('showpermalink', default=False):
        plot = '{}\n\n[COLOR={{highlighted}}]{}[/COLOR]'.format(plot, permalink)
    return colour(plot)


def get_paginated_list(list_id, page_size, end_cursor=''):
    """Get paginated list of episodes from GraphQL API"""
    from tokenresolver import TokenResolver
    access_token = TokenResolver().get_token('vrtnu-site_profile_at')
    data_json = {}
    if access_token:
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json',
        }
        graphql_query = """
            query ListedEpisodes(
              $listId: ID!
              $endCursor: ID!
              $pageSize: Int!
            ) {
              list(listId: $listId) {
                __typename
                ... on PaginatedTileList {
                  paginated: paginatedItems(first: $pageSize, after: $endCursor) {
                    edges {
                      node {
                        __typename
                        ...ep
                      }
                    }
                    pageInfo {
                      startCursor
                      endCursor
                      hasNextPage
                      hasPreviousPage
                      __typename
                    }
                  }
                }
              }
            }
            fragment ep on EpisodeTile {
              __typename
              id
              title
              episode {
                __typename
                id
                name
                available
                whatsonId
                title
                description
                subtitle
                permalink
                logo
                brand
                brandLogos {
                  type
                  mono
                  primary
                }
                image {
                  alt
                  templateUrl
                }

                ageRaw
                ageValue

                durationRaw
                durationValue
                durationSeconds

                episodeNumberRaw
                episodeNumberValue
                episodeNumberShortValue

                onTimeRaw
                onTimeValue
                onTimeShortValue

                offTimeRaw
                offTimeValue
                offTimeShortValue

                productPlacementValue
                productPlacementShortValue

                regionRaw
                regionValue
                program {
                  title
                  id
                  programType
                  description
                  shortDescription
                  subtitle
                  announcementType
                  announcementValue
                  whatsonId
                  image {
                    alt
                    templateUrl
                  }
                  posterImage {
                    alt
                    templateUrl
                  }
                }
                season {
                  id
                  titleRaw
                  titleValue
                  titleShortValue
                }
                analytics {
                  airDate
                  categories
                  contentBrand
                  episode
                  mediaSubtype
                  mediaType
                  name
                  pageName
                  season
                  show
                  }
                primaryMeta {
                  longValue
                  shortValue
                  type
                  value
                  __typename
                }
                secondaryMeta {
                  longValue
                  shortValue
                  type
                  value
                  __typename
                }
                watchAction {
                  avodUrl
                  completed
                  resumePoint
                  resumePointProgress
                  resumePointTitle
                  episodeId
                  videoId
                  publicationId
                  streamId
                }
              }
            }
        """
        # FIXME: Find a better way to change GraphQL typename
        if 'static:/' in list_id:
            graphql_query = graphql_query.replace('on PaginatedTileList', 'on StaticTileList')

        payload = dict(
            operationName='ListedEpisodes',
            variables=dict(
                listId=list_id,
                endCursor=end_cursor,
                pageSize=page_size,
            ),
            query=graphql_query,
        )
        from json import dumps
        data = dumps(payload).encode('utf-8')
        data_json = get_url_json(url=GRAPHQL_URL, cache=None, headers=headers, data=data, raise_errors='all')
    return data_json


def convert_episodes(api_data, destination):
    """Convert paginated list of episodes to Kodi list items"""
    import dateutil.parser
    episodes = []
    for item in api_data.get('data').get('list').get('paginated').get('edges'):
        episode = item.get('node').get('episode')
        video_id = episode.get('watchAction').get('videoId')
        publication_id = episode.get('watchAction').get('publicationId')
        path = url_for('play_id', video_id=video_id, publication_id=publication_id)
        tvshowtitle = episode.get('program').get('title')
        label = '[B]{}[/B] - {}'.format(tvshowtitle, episode.get('title'))
        mpaa = episode.get('ageRaw') or ''
        offtime = dateutil.parser.parse(episode.get('offTimeRaw'))
        product_placement = True if episode.get('productPlacementShortValue') == 'pp' else False
        region = episode.get('regionRaw')
        permalink = episode.get('permalink')
        plot = episode.get('description')
        plot = generate_plot(plot, region, product_placement, mpaa, offtime, permalink)
        plotoutline = episode.get('program').get('subtitle')
        duration = int(episode.get('durationSeconds'))
        episode_no = int(episode.get('episodeNumberRaw') or 0)
        season_no = int(''.join(i for i in episode.get('season').get('titleRaw') if i.isdigit()) or 0)
        studio = episode.get('brand').title() if episode.get('brand') else 'VRT'
        aired = dateutil.parser.parse(episode.get('analytics').get('airDate')).strftime('%Y-%m-%d')
        dateadded = dateutil.parser.parse(episode.get('onTimeRaw')).strftime('%Y-%m-%d %H:%M:%S')
        year = int(dateutil.parser.parse(episode.get('onTimeRaw')).strftime('%Y'))
        tag = [tag.title() for tag in episode.get('analytics').get('categories').split(',') if tag]

        # Art
        fanart = episode.get('program').get('image').get('templateUrl')
        poster = episode.get('program').get('posterImage').get('templateUrl')
        thumb = episode.get('image').get('templateUrl')

        episodes.append(
            TitleItem(
                label=label,
                path=path,
                art_dict=dict(
                    thumb=thumb,
                    poster=poster,
                    banner=fanart,
                    fanart=fanart,
                ),
                info_dict=dict(
                    title=label,
                    tvshowtitle=tvshowtitle,
                    aired=aired,
                    dateadded=dateadded,
                    episode=episode_no,
                    season=season_no,
                    plot=plot,
                    plotoutline=plotoutline,
                    mpaa=mpaa,
                    tagline=plotoutline,
                    duration=duration,
                    studio=studio,
                    year=year,
                    tag=tag,
                    thumb=thumb,
                    fanart=fanart,
                    poster=poster,
                    mediatype='episode',
                ),
                is_playable=True,
            )
        )
    # Paging
    page_info = api_data.get('data').get('list').get('paginated').get('pageInfo')
    if page_info.get('hasNextPage'):
        end_cursor = page_info.get('endCursor')
        # Add 'More...' entry at the end
        episodes.append(
            TitleItem(
                label=colour(localize(30300)),
                path=url_for(destination, end_cursor=end_cursor),
                art_dict=dict(thumb='DefaultInProgressShows.png'),
                info_dict={},
            )
        )
    return episodes


def get_continue_episodes(end_cursor=''):
    """Get continue episodes"""
    page_size = get_setting_int('itemsperpage', default=50)
    list_id = 'dynamic:/vrtnu.model.json@resume-list-video'
    api_data = get_paginated_list(list_id=list_id, page_size=page_size, end_cursor=end_cursor)
    episodes = convert_episodes(api_data, destination='resumepoints_continue')
    return episodes


def get_recent_episodes(end_cursor=''):
    """Get continue episodes"""
    page_size = get_setting_int('itemsperpage', default=50)
    list_id = 'static:/vrtnu/kijk.model.json@par_list_copy_copy_copy'
    api_data = get_paginated_list(list_id=list_id, page_size=page_size, end_cursor=end_cursor)
    episodes = convert_episodes(api_data, destination='resumepoints_continue')
    return episodes
