import numpy as np
import pandas as pd
import sqlite3
import re
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def parse_content_for_reissue(df, list_of_words):
    """
    Takes in a DataFrame and a list of words that indicate if the albums
    to be reviewed is a reissue, box set, or any other release other than new
    """
    df['reissue'] = 0
    for each in list_of_words:
        df['reissue'] = df['reissue'] + df['abstract'].str.contains(each).astype('int')
    df['reissue'] = df['reissue'] + df['best_new_reissue'].astype('int')
    df['reissue'] = df['reissue'].astype(bool).astype(int)
#Reviews that were reviewed years after their release are classic albums
def reissue_columns(df):
    """
    Albums that were reviewed years after their release are classic albums
    """
    df['num_years_since_release'] = df.pub_year - df.year
    df['new_album'] = ((df['reissue'] == 0) & (df['num_years_since_release'] <= 1)).astype(int)
    return df

if __name__ == "__main__":
    #connect to databse
    nlp = spacy.load('en')
    conn = sqlite3.connect("../pitchfork-data/pitchfork_2017.db")
    #create dataframes for each table
    df = pd.read_sql_query("select * from reviews;", conn)
    df_reviews = pd.read_sql_query("select * from content", conn)
    df_years = pd.read_sql_query("select * from years;", conn)
    df_genres = pd.read_sql_query("select * from genres", conn)
    #create dummies to allow for multiple genres for each review
    df_genres = pd.get_dummies(df_genres, columns=['genre']).groupby('reviewid').sum().reset_index()

    #merge tables
    df = df.merge(df_years)
    df = df.merge(df_genres)
    df = df.merge(df_reviews).reset_index()
    print 'data merged'
    #Fill NA Values for Year, Drop any duplicates, drop any unimportant columns
    df.year.fillna(value=df.pub_year, inplace=True)
    df.drop_duplicates('reviewid',inplace=True)
    df.drop(['index'], axis=1, inplace=True)
    df.drop('author_type', axis=1, inplace=True)
    df.year = df.year.astype(int)
    df = df[df['pub_year'] < 2018]

    list_of_words = ['reissue', 'remaster', 'box set', 'collector', 'delux']
    parse_content_for_reissue(df, list_of_words)

    df = reissue_columns(df)
    df.reset_index(inplace=True)


    # save CSV one level up so that it doesn't go to github
    df.to_csv('../pitchfork_no_nlp.csv')
