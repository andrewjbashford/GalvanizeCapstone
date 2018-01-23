# Is Pitchfork Losing Its Edge?
An Analysis of Pitchfork Reviews Since Its 2015 Acquisition by Condé Nast & Pitchfork Review Recommendation System

# Project Overview

# Key Findings

# Launching the Recommender:

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

Pitchfork Review Recommender:
- GraphLab


# Acknowledgments

Starter code for my webscraper:
https://github.com/nolanbconaway/pitchfork-data

Github repo used to get Spotify data into R:
https://github.com/charlie86/spotifyr
