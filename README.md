# Is Pitchfork Losing Its Edge?
An Analysis of Pitchfork Reviews Since Its 2015 Acquisition by Condé Nast & Pitchfork Review Recommendation System

# Background & Motivation

Pitchfork is an online music publication with a reputation for being opinionated, a little snobby, but usually right. Below is a satiric article published by the Onion that says it all:

<img src="powerpoint%20images/onion%20article.png" height=40%  width=40%  alt="Onion Article">


In 2015, they were acquired by the large media company Conde Nast, leaving fans skeptical of the future of Pitchfork’s reputation. Here's an excerpt from a recent AMA that Pitchfork conducted on Reddit:


<img src="powerpoint%20images/reddit_logo.png" height=15%  width=15%  alt="Reddit AMA">
<img src="powerpoint%20images/reddit%20example.png" height=100%  width=100%  alt="Reddit AMA">

Do Pitchfork's more critical fans have any basis to claim that Pitchfork has become more 'vanilla' over time? 

I conducted statistical analysis on their **scoring methodology** and used natural language processing techniques on the **content of reviews** in search of evidence that **Pitchfork has measurably changed since they were acquired.**

# Data Collection

First, I scraped Pitchfork’s archives to gather over 19,000 reviews since 1999. I started with code from Nolan Conaway's GitHub, but had to make several adjustments to accomodate changes to Pitchfork's HTML and adding important features.

Reissues and older album reviews are not clearly marked on Pitchfork. I used RegEx to categorize any albums containing 'reissue', 'collector', 'box set' etc. as reviews that are not for the first release. Pitchfork tends to score these albums higher, so they were removed from my dataset for the analysis of scores.


# Scoring Distribution

I broke down Pitchfork reviews into five major buckets:

1. Before the launch of Best New Music in 2003 
2. Before the launch of Pitchfork Music Festival in 2006 (the first time Pitchfork had an incentive to promote specific artists)
3. Before the major website redesign in 2011
4. Before the Conde Nast acquisition in 2015
5. After the acquisition

The spread of scores given to albums has tightened with each major event.

Next, I evaluated if Pitchfork is still willing to gamble on new artists. In 2004, they gave Arcade Fire a 9.7 for their first release, putting them on the map. But, since then, they have only given an album a 9.0 or above 8 times when the artist is being reviewed for the first time… and zero times since 2010.

# Natural Language Processing

I used SpaCy to tag all 14 million words from reviews with their part of speech, counting up the words that are most likely to be descriptive (adjectives, adverbs and certain tenses of verbs). I then used TextBlob to get a subjectivity score for each review, measuring how opinionated or objective the author was. 

I found that since 2003, Pitchfork reviews are getting less descriptive. The boxplots have notches indicating a 95% confidence interval of the median, showing that these changes are statistically significant. I also found that, while the content of the reviews has become more objective, the one-to-two sentence abstract at the top of the review has become more subjective. The subjectivity of the content and the abstract are converging together, giving the reader a more consistent account of Pitchfork’s opinion.

# Summary

Has Pitchfork changed its scoring methodology and review content since its acquisition?

- The spread of the score distribution has tightened
- Pitchfork doesn’t gamble big on new artists
- Pitchfork’s language has become less descriptive and more objective
- Pitchfork has become more consistent in the Abstract 

# Pitchfork Review Recommendation System:

System Requirements:
- GraphLab
- Python
- Flask

# Data Cleanup

I have included a CSV of the Pitchfork data that does not include any of the columns created doing NLP analysis.

Running data_cleanup.py will create a CSV with all data in the directory above wherever you clone this repo. You will need to install TextBlob and spaCy for that to run. Note that it takes ~30 minutes to run.


# Technology Stack

Data Collection / Visualization:
- Python
- BeautifulSoup
- pandas/numpy
- matplotlib/seaborn

Natural Language Processing:
- spaCy
- TextBlob
- scikit-learn

Spotify Data:
- R

Pitchfork Review Recommender:
- GraphLab


# Acknowledgments

Starter code for my webscraper:
https://github.com/nolanbconaway/pitchfork-data

Github repo used to get Spotify data into R:
https://github.com/charlie86/spotifyr
