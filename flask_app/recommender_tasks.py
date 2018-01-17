def print_top_url(df_similar):
    df_copy = df_similar.reset_index()
    for i in range(len(df_similar['url'])):
        print "{}, {}".format(df_copy['artist'][i].title(), df_copy['title'][i].title())
        print "http://open.spotify.com/album/{}".format(df_copy['album_uri'][i])
        print df_copy['url'][i]
        print "\n"

def get_similar(df, url, recommender):
    top_5_similar = recommender.get_similar_items([url], k=20)['similar']
    return df[(df['score'] > 7) &
               (df['url'].isin(top_5_similar))][['artist','title', 'score', 'url', 'danceability rounded',
                                                'valence rounded', 'energy rounded', 'acousticness rounded',
                                               'pub_year', 'spotify_match', 'album_uri']].head(10)

def get_url(df, artist, title):
    return df[(df['artist'] == artist) & (df['title'] == title)].iloc[0][7]

def get_links(df_similar):
    df_copy = df_similar.reset_index()
    all_info = []
    for i in range(len(df_similar['url'])):
        all_info.append((df_copy['artist'][i].title(),
                        df_copy['title'][i].title(),
                        "http://open.spotify.com/album/{}".format(df_copy['album_uri'][i]),
                        df_copy['url'][i]))
    return all_info
