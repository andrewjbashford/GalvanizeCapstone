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
#Reviews containing the following words are reissued albums

def parse_content_for_reissue(df, list_of_words):
    df['reissue'] = 0
    for each in list_of_words:
        df['reissue'] = df['reissue'] + df['abstract'].str.contains(each).astype('int')
    df['reissue'] = df['reissue'] + df['best_new_reissue'].astype('int')
    df['reissue'] = df['reissue'].astype(bool).astype(int)

#Reviews that were reviewed years after their release are classic albums
def reissue_columns(df):
    df['num_years_since_release'] = df.pub_year - df.year
    df['new_album'] = ((df['reissue'] == 0) & (df['num_years_since_release'] <= 1)).astype(int)
    return df


#Remove unusual characters from content and abstract

def remove_weird_char(string):
    return re.sub('[^A-Za-z0-9]+', ' ', string)


#Add columns of adjectives and adverbs used in review content and abstract

def parse_for_adj(df, column, new_column_name):
    prop_noun_parse = []
    for i in range(len(df[column])):
        non_PN = []
        blob = nlp(unicode(df[column][i]))
        for each in blob:
            if each.tag_ == u'ADJ' or each.tag_ == u'JJ':
                non_PN.append(str(each))
        prop_noun_parse.append((df['reviewid'][i], " ".join(non_PN)))

    df_new = pd.DataFrame(prop_noun_parse, columns =['reviewid', new_column_name])
    return df.merge(df_new)


#Adding Sentiment Scores with TextBlob of content and abstract adjectives/adverbs. This will come in handy later.
def add_sentiment(df, column, new_col_pol, new_col_subj):
    sentiments = []
    for each in range(len(df['reviewid'])):
        sentiments.append((df['reviewid'].iloc[each], TextBlob(df['content_adj'][each]).sentiment[0], TextBlob(df['content_adj'][each]).sentiment[1]))
    #                           TextBlob(df_mid['content'][each], analyzer=NaiveBayesAnalyzer()).sentiment))

    df_cont_sent = pd.DataFrame(sentiments, columns=['reviewid', new_col_pol, new_col_subj])
    return df.merge(df_cont_sent)



#Add a few additional columns for more NLP and bins for scores
def add_columns(df):
    df['word_count'] = df['content'].str.count('\w+')
    df['adj_count'] = df['content_adj'].str.count('\w+')
    df['adj_freq'] = df['adj_count'] / df['word_count']
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
    df = parse_for_adj(df, 'abstract', 'abstract_adj')
    print 'abs adj done'
    df = parse_for_adj(df, 'content', 'content_adj')
    print 'content adj done'
    df = add_sentiment(df, 'content_adj', 'cont_polarity', 'cont_subjectivity')
    print 'sentiment content done'
    df = add_sentiment(df, 'abstract_adj', 'abs_polarity', 'abs_subjectivity')
    print 'sentiment abs done'
    df = add_columns(df)

    # save CSV one level up so that it doesn't go to github
    df.to_csv('../pitchfork2.csv')
