from flask import render_template, request
from flask_app import app
import numpy as np
from textblob import TextBlob
import graphlab as gl
import pandas as pd
pd.options.display.max_colwidth = 100

recommender = gl.load_model('../recommender')
recommender_tfidf = gl.load_model('../recommender_tfidf')
df = pd.read_csv('../pitchfork_no_nlp.csv')
df_spotify = pd.read_csv('spotify_with_rank.csv')
df_spotify = df_spotify.groupby(['title', 'artist', 'album_uri']).mean().reset_index()

df_merged = df.merge(df_spotify, how='left', on=['artist', 'title'])
df_merged = df_merged.drop_duplicates(['title', 'artist', 'reviewid'], keep='first')
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

df_merged.drop_duplicates(['title', 'artist'], keep='first')
df_merged =df_merged.dropna(subset=['content'])

def get_links(df_similar):
    df_copy = df_similar.reset_index()
    all_info = []
    for i in range(len(df_similar['url'])):
        try:
            abstract = df_copy['abstract'][i].decode('utf-8')
        except:
            abstract = " "
        all_info.append((df_copy['artist'][i].title(),
                        df_copy['title'][i].title(),
                        "https://open.spotify.com/search/results/{}".format(df_copy['artist'][i].replace(" ", "%20")),
                        df_copy['url'][i],
                        df_copy['score'][i],
                        abstract,
                        df_copy['album_uri'][i],
                        df_copy['spotify_match'][i]))
    return all_info

def get_similar(df, url, recommender, recommender_tfidf):
    if df[df['url'] == url].iloc[0][-1] == 0:
        top_5_similar = recommender_tfidf.get_similar_items([url], k=20)['similar']
    else:
        top_5_similar = recommender.get_similar_items([url], k=20)['similar']
    return df[(df['score'] > 7) &
               (df['url'].isin(top_5_similar))][['artist','title', 'score', 'url', 'danceability rounded',
                                                'valence rounded', 'energy rounded', 'acousticness rounded',
                                               'pub_year', 'spotify_match', 'album_uri', 'abstract']]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Pitchfork Review Recommendation System', data=None)


@app.route('/make_recommendation', methods=['POST'])
def make_recommendation():
    url = request.form['text1']
    df_similar = get_similar(df_merged, url, recommender, recommender_tfidf)
    requested_artist = "{}, {}".format(df_merged[df_merged['url']==url].iloc[0][4].title(),
                                      df_merged[df_merged['url']==url].iloc[0][3].title())

    all_info = get_links(df_similar)

    return render_template('index.html', title='Similar Albums',
                            all_info=all_info, url=url, requested_artist=requested_artist)
