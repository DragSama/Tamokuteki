anime_search_query = """
query ($id: Int, $search: String) {
  Media(id: $id, type: ANIME, search: $search) {
    id
    title {
      romaji
      english
      native
    }
    description
    startDate {
      year
    }
    episodes
    season
    type
    format
    status
    duration
    studios {
      nodes {
        name
      }
    }
    trailer {
      id
      site
      thumbnail
    }
    averageScore
    genres
  }
}
"""

manga_query = """
query ($id: Int,$search: String) {
      Media (id: $id, type: MANGA,search: $search) {
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          type
          format
          status
          siteUrl
          averageScore
          genres
      }
    }
"""

__type__ = "IGNORE"
