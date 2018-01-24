import numpy as np
import pandas as pd
import sqlite3
from textblob import TextBlob
import re
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


import spacy
nlp = spacy.load('en')


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



def remove_weird_char(string):
    """
    Remove unusual characters from content and abstract
    """
    return re.sub('[^A-Za-z0-9]+', ' ', string)



def parse_for_adj(df, column, new_column_name):
    """
    Add columns of adjectives and adverbs used in review content and abstract.
    Must pass through the new column name, as well as the column to be parsed.
    """
    prop_noun_parse = []
    for i in range(len(df[column])):
        non_PN = []
        blob = nlp(unicode(df[column][i]))
        for each in blob:
            if each.tag_ in [u'JJ', u'JJR', u'JJS', u'VBZ', u'VBG', u'RB', u'RBR', u'RBS']:
                non_PN.append(str(each))
        prop_noun_parse.append((df['reviewid'][i], " ".join(non_PN)))

    df_new = pd.DataFrame(prop_noun_parse, columns =['reviewid', new_column_name])
    return df.merge(df_new)


def add_sentiment(df, column, new_col_pol, new_col_subj):
    """
    Adding Sentiment Scores with TextBlob of content and abstract adjectives/adverbs.
    Must pass through the new column names for polarity and subjectivity, as well
    as the column to be parsed.
    """
    sentiments = []
    for each in range(len(df['reviewid'])):
        sentiments.append((df['reviewid'].iloc[each], TextBlob(df[column][each]).sentiment[0], TextBlob(df[column][each]).sentiment[1]))
    #                           TextBlob(df_mid['content'][each], analyzer=NaiveBayesAnalyzer()).sentiment))

    df_cont_sent = pd.DataFrame(sentiments, columns=['reviewid', new_col_pol, new_col_subj])
    return df.merge(df_cont_sent)



#Add a few additional columns for more NLP and bins for scores
def add_columns(df):
    """
    This function uses regex to add word counts for previously created columns,
    as well as a score_bin
    """
    df['word_count'] = df['content'].str.count('\w+')
    df['desc_count'] = df['content_desc'].str.count('\w+')
    df['desc_freq'] = df['desc_count'] / df['word_count']
    df['score_bin'] = (df['score'] // 1).astype(int)
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
    df['content'] = df['content'].map(remove_weird_char)
    df['abstract'] = df['abstract'].map(remove_weird_char)
    print 'beginning NLP parsing'
    df = parse_for_adj(df, 'abstract', 'abstract_desc')
    print 'abs adj done'
    df = parse_for_adj(df, 'content', 'content_desc')
    print 'content adj done'
    df = add_sentiment(df, 'content_desc', 'cont_polarity', 'cont_subjectivity')
    print 'sentiment content done'
    df = add_sentiment(df, 'abstract_desc', 'abs_polarity', 'abs_subjectivity')
    print 'sentiment abs done'
    df = add_columns(df)

    # save CSV one level up so that it doesn't go to github
    df.to_csv('../pitchfork4.csv')
