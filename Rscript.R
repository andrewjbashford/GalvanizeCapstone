library(spotifyr)

Sys.setenv(SPOTIFY_CLIENT_ID = 'c38e0bb028ff450ab8f452671c484d97')
Sys.setenv(SPOTIFY_CLIENT_SECRET = 'a522513473a04a9ba5cd7d45bf87f0b2')

access_token <- get_spotify_access_token()
library(tidyverse)
beatles <- get_artist_audio_features('the beatles', access_token = get_spotify_access_token())
The Beatles
count(beatles, key_mode, sort = T)


artists <- get_artists('radiohead')
albums <- get_albums(artists$artist_uri[1])
tracks <- get_album_tracks(albums)
radiohead_audio_features <- get_track_audio_features(tracks)


library(tidyverse)
library(spotifyr)
library(stringr)
library(stringdist)
# import keys
# source('data_aquisition_scripts/spotify_keys.R')
Sys.setenv(SPOTIFY_CLIENT_ID = 'c38e0bb028ff450ab8f452671c484d97')
Sys.setenv(SPOTIFY_CLIENT_SECRET = 'a522513473a04a9ba5cd7d45bf87f0b2')

access_token <- spotifyr::get_spotify_access_token()

get_artist_audio_features <- function(artist_name, access_token = get_spotify_access_token(), return_closest_artist = TRUE) {
  
  artists <- get_artists(artist_name)
  
  if (nrow(artists) > 0) {
    if (return_closest_artist == TRUE) {
      string_distances <- stringdist(artist_name, artists$artist_name, method = 'cosine')
      min_distance_index <- which(string_distances == min(string_distances))
      selected_artist <- artists$artist_name[min_distance_index]
      message(paste0('Selecting artist "', selected_artist, '"', '. Choose return_closest_artist = FALSE to interactively choose from all the artist matches on Spotify.'))
    } else {
      cat(paste0('We found the following artists on Spotify matching "', artist_name, '":\n\n\t', paste(artists$artist_name, collapse = '\n\t'), '\n\nPlease type the name of the artist you would like:'), sep  = '')
      selected_artist <- readline()
    }
    
    artist_uri <- artists$artist_uri[artists$artist_name == selected_artist]
  } else {
    stop(paste0('Cannot find any artists on Spotify matching "', artist_name, '"'))
  }
  
  albums <- get_albums(artist_uri)
  
  if (nrow(albums) > 0) {
    albums <- select(albums, -c(base_album_name, base_album, num_albums, num_base_albums, album_rank))
  } else {
    stop(paste0('Cannot find any albums for "', selected_artist, '" on Spotify'))
  }
  
  album_popularity <- get_album_popularity(albums)
  tracks <- get_album_tracks(albums)
  track_features <- get_track_audio_features(tracks)
  track_popularity <- get_track_popularity(tracks)
  
  tots <- albums %>%
    left_join(album_popularity, by = 'album_uri') %>%
    left_join(tracks, by = 'album_name') %>%
    left_join(track_features, by = 'track_uri') %>%
    left_join(track_popularity, by = 'track_uri')
  
  return(tots)
}
radiohead_features <- get_artist_audio_features('radiohead')

radiohead_features %>% 
  group_by(album_name) %>% 
  summarize(avg_valance = mean(valence))

read_csv()
getwd()
