import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

import graphlab

pd.options.display.max_colwidth = 100

import sys
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    # Read in CSV of Pitchfork data and Spotify data
    df = pd.read_csv('data/pitchfork_no_nlp.csv')
    df_spotify = pd.read_csv('data/spotify_with_rank.csv')

    #Group by non-numeric features that we want to save, take the mean of everything else.
    #Spotify data is by track, so the mean will get the average for the tracks in an album
    df_spotify = df_spotify.groupby(['title', 'artist', 'album_uri']).mean().reset_index()

    #Merge DFs and drop duplicates
    df_merged = df.merge(df_spotify, how='left', on=['artist', 'title'])
    df_merged = df_merged.drop_duplicates(['title', 'artist', 'reviewid'], keep='first')


    # Remove stop words and vectorize review content using TF-IDF, add the vectors as
    # new feature
    vectorizer = TfidfVectorizer(stop_words='english', max_features=500, max_df=.4)
    X = vectorizer.fit_transform(df_merged['content'].values.astype('U'))
    df_merged['tf-idf'] = list(X.toarray())

    # Create new features rounding off spotify data, impute the mean scores for albums
    #lacking spotify data, and create feature indicating
    # whether or not the album was matched on spotify
    df_merged['danceability rounded'] = (df_merged['danceability mean']*10).round(1)
    df_merged['valence rounded'] = (df_merged['valence mean']*10).round(1)
    df_merged['energy rounded'] = (df_merged['energy mean']*10).round(1)
    df_merged['acousticness rounded'] = (df_merged['acousticness mean']*10).round(1)
    df_merged['score_bin_5'] = pd.cut(df_merged['score'], bins=5, labels=False)
    df_merged['score_bin_2'] = pd.cut(df_merged['score'], bins=2, labels=False)
    df_merged['danceability rounded'].fillna(value=df_merged['danceability rounded'].mean(), inplace=True)
    df_merged['valence rounded'].fillna(value=df_merged['valence rounded'].mean(), inplace=True)
    df_merged['energy rounded'].fillna(value=df_merged['energy rounded'].mean(), inplace=True)
    df_merged['acousticness rounded'].fillna(value=df_merged['acousticness rounded'].mean(), inplace=True)
    df_merged['spotify_match'] = np.where(df_merged['year sum'] > 0, 1, 0)

    #Drop any duplicates, keep the first title.
    df_merged.drop_duplicates(['title', 'artist'], keep='first')
    df_merged =df_merged.dropna(subset=['content'])

    #Create graphlab SFrames, one using spotify data and one using only Pitchfork data
    sf = graphlab.SFrame(df_merged[['url', 'tf-idf',
                                    'danceability rounded', 'valence rounded', 'energy rounded', 'acousticness rounded',
                                    'pub_year', u'genre_electronic', u'genre_experimental',
           u'genre_folk/country', u'genre_global', u'genre_jazz', u'genre_metal',
           u'genre_pop/r&b', u'genre_rap', u'genre_rock', 'new_album', 'spotify_match']])

    sf2 = graphlab.SFrame(df_merged[['url', 'tf-idf', 'pub_year', u'genre_electronic', u'genre_experimental',
           u'genre_folk/country', u'genre_global', u'genre_jazz', u'genre_metal',
           u'genre_pop/r&b', u'genre_rap', u'genre_rock']])

    #Create recommender systems using both SFrames. Ultimately, albums with spotify data will
    # have recommendations generated using the first, and albums lacking spotify data will have
    # recommendations using only TF-IDF and genre.
    recommender = graphlab.recommender.item_content_recommender.create(sf, item_id='url')
    recommender_tfidf = graphlab.recommender.item_content_recommender.create(sf2, item_id='url')

    #Save recommenders and DataFrame
    #Saved up one directory
    recommender.save('../recommender')

    recommender_tfidf.save('../recommender_tfidf')

    df_merged.to_csv('../recommender_df.csv')
