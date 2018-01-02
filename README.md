## Is Pitchfork losing its edge?

Pitchfork.com gained a reputation in the past 18 years for its ability to pick artists out of obscurity and put them in the mainstream, and for its ability to destroy the rise of an artist with one scathing review, and generally for its pretentiousness. As it has gained popularity, and especially after it was acquired by Condé Nast in 2015, I’ve observed that the reviews have gotten ‘softer’, perhaps in an attempt to appeal to a broader base of readers, and gain traffic through keyword search by doing reviews for more established artists.

### Here is what I plan to do:

    1. Determine if Pitchfork has made an objective change to their review criteria since being acquired by Conde Nast
    2. Determine if reviewers successfully defend the scores given to albums
    3. Develop a recommendation system to recommend albums to readers

I’m not the first person to analyze data from Pitchfork:

    1. https://opendatascience.com/blog/processing-the-language-of-pitchfork-part-1/
    - This article analyzes the reading level of Pitchfork’s reviews -- they are using similar methodology to what I anticipate doing, but solving a different problem
    2. https://nlp.stanford.edu/courses/cs224n/2011/reports/cadander-esegel-jepense.pd
    - This study extracts the important phrases and words from music reviews across the web to create a shorter descriptive snippet
    3. https://rstudio-pubs-static.s3.amazonaws.com/286186_b58494562ee64d0bb7da79dcfa7e5186.html
    - This study does meandering EDA on the same dataset I will be using.
    4.https://github.com/nolanbconaway/pitchfork-data/tree/master/notebooks
    - This investigates distribution of Best New Music assignments and evaluates independence / autocorrelation between reviewers / albums from same artists

## Why does this matter?
Pitchfork's reputation for discovering artists and being the leading opinion on music is important. Conde Nast / Pitchfork editorial staff have a vested interest, and a better understanding of the review critera could help lead to improvements for readers. Clustering artists and reviews into different genre-bending groups would help readers discover new music based on the reviews they are choosing to read.

Pitchfork markets itself as the most trusted voice in music. To preserve that reputation, they need to be on the cutting edge of discovering new, relevant artists, and take a firm stance on what its readers should be listening to.


## Next Steps
### Determine if Pitchfork has made an objective change to their review criteria since being acquired by Conde Nast

We can gain some information about ‘if Pitchfork is losing its edge’ by doing some descriptive statistical analysis of reviews over the past 20 years.

Important Inflection Points:

    1. Before/after acquisition by Conde Nast in 2015
    2. 2011 major website redesign,
    3. Launch of Pitchfork Music Festival in 2006. Each of these events could be motives for the editorial staff to change the criterion for reviewing records

   ![alt text](https://github.com/andrewjbashford/GalvanizeCapstone/blob/master/images/All.png "Logo Title Text 1")

### Determine if reviewers successfully defend the scores given to albums

How has the range of album scores changed over time? By staff reviewers?

Analyze sentiment of reviews
    
    - Are the reviews of late less biting? More ‘mainstream’? Less pretentious?
    - Do some reviewers tend to write with anger? joy? Different writing styles for different genres or artist types?
      Has this changed over time?
    - Scores are often determined at the time of assignment by the editorial staff. 
      Does the sentiment of the reviewer always line up with the score given to the album?
    - Do reviewers change their language when writing about less established artists? 
      Does the level of persuasiveness change based on album score?
    - Build and evaluate models that predicts album scores / predict Best New Music based on NLP of review content. 
      Can this be done with a relatively high level of accuracy?
      
### Has sentiment of reviews changed over time?

Have Pitchfork writers changed the severity of their tone since the Conde Nast acquisition? Do positive reviews have a more/less positive sentiment? Do negative reviews have a more/less negative sentiment?

Have Pitchfork writers become more objective or subjective in their tone? A more objective stance suggests that writers are less willing to take risks in the reviews they are writing.

### Has Pitchfork launched the careers of any artists since the Conde Nast acquisition?

Using Google Trends, we can get a broad sense of how many people were searching for an artist before or after Pitchfork published a review of their new album. Using Arcade Fire and Clap Your Hands Say Yeah! as a baseline, have there been other very obscure artists that had their first spike in Google searches after Pitchfork posted a review?

 ![alt text](https://github.com/andrewjbashford/GalvanizeCapstone/blob/master/images/arcade%20fire%20searches.png "Logo Title Text 1")


### Develop a recommendation system to recommend albums to readers

Use mentions of other artists, similar types of describer words, and similar scores to recommended further reading.

## Anticipated Hurdles and Scope of Project

How to handle reissues? Pitchfork often reviews reissues of notable albums as a chance to update album scores while incorporating the artists’ longevity. These reviews should be removed from the corpus when evaluating Pitchfork’s treatments of new music.

I anticipate that I will be able to find conclusive evidence to evaluate if / how their criteria has changed for scoring albums using statistical analysis and NLP techniques, as well as develop a basic content-based recommender to suggest similar reviews for readers (based on language used within the review and Pitchfork-described artist communities)

Since Pitchfork reviews are written and scored subjectively, I anticipate measuring the effectiveness of any models, recommenders and analysis I do will be difficult.

## Data
Review Data through Jan 2017
https://www.kaggle.com/nolanbconaway/pitchfork-data/data

 ![alt text](https://github.com/andrewjbashford/GalvanizeCapstone/blob/master/images/data_sample.png "Logo Title Text 1")

Over the holidays, I'll scrape 2017 reviews myself, and I'll get data about initial album release from Music Brainz to deal with reissues.

 ![alt text](https://github.com/andrewjbashford/GalvanizeCapstone/blob/master/images/pipeline1.png "Logo Title Text 1")

## Additional Thoughts

Pitchfork was previously known for launching the careers of unknown artists (Arcade Fire, Bon Iver, Clap Your Hands Say Yeah all attribute Pitchfork’s favorable reviews to the rise of their careers). In years past, they would often forgo writing reviews for popular artists that they didn’t deem as essential -- whether or not an album got a review was itself an editorial statement on its OWN for the album’s quality.

Ex. Taylor Swift’s music was previously ignored, but now Pitchfork will review artists like her even if the album being reviewed generates an average / unremarkable rating
