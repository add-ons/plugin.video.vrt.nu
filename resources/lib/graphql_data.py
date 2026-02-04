# -*- coding: utf-8 -*-
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Implements VRT MAX GraphQL API functionality"""


EPISODE = """
    fragment episode on Episode {
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
        link
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
        catalogMemberType
        id
        navigationTitle
        numEpisodesRaw
        numEpisodesShortValue
        numEpisodesValue
        objectId
        programId
        programName
        programTitle
        programType
        titleRaw
        titleShortValue
        titleValue
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
      shareAction {
        url
      }
      favoriteAction {
        favorite
        id
        title
      }
    }
"""

PROGRAM_TILE = """
    fragment programTileFragment on ProgramTile {
      __typename
      objectId
      id
      link
      tileType
      image {
        alt
        templateUrl
      }
      title
      program {
        title
        id
        link
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
        favoriteAction {
          favorite
          id
          title
        }
      }
    }
"""


EPISODE_TILE = """
    fragment episodeTileFragment on EpisodeTile {
      id
      image {
        templateUrl
      }
      tileType
      title
      componentType
      description
      available
      action {
        ... on LinkAction {
          link
        }
      }
      chapterStart
      formattedDuration
      whatsonId
      primaryMeta {
        longValue
        shortValue
        type
        value
        __typename
      }
      progress {
        completed
        progressInSeconds
        durationInSeconds
        __typename
      }
      status {
        accessibilityLabel
        icon {
          __typename
        }
        text {
          small
          default
          __typename
        }
        __typename
      }
      __typename
    }
"""
