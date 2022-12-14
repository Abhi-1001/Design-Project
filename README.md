# Design-Project - Hate Speech Detection

## *Can Content Moderation Be Automated?*

## Overview

This project aims to **automate content moderation** to identify hate speech using **machine learning binary classification algorithms.**

## Business Problem
**Human content moderation exploits people by consistently traumatizing and underpaying them.** In 2019, an [article](https://www.theverge.com/2019/6/19/18681845/facebook-moderator-interviews-video-trauma-ptsd-cognizant-tampa) on The Verge exposed the extensive list of horrific working conditions that employees faced at Cognizant, Facebook’s former moderation contractor. Unfortunately, **every major tech company**, including **Twitter**, uses human moderators to some extent, both domestically and overseas.

Hate speech is defined as **abusive or threatening speech that expresses prejudice against a particular group, especially on the basis of race, religion or sexual orientation.** Usually, the difference between hate speech and offensive language comes down to subtle context or diction. 

**Warning:** All notebooks contain offensive language from the dataset.

## Data Sourcing
The dataset for this capstone project was sourced from a study called *Automated Hate Speech Detection and the Problem of Offensive Language* conducted by Thomas Davidson and a team at Cornell University in 2017. The GitHub repository can be found [here](https://github.com/t-davidson/hate-speech-and-offensive-language). 

- The dataset is a `.csv` file with **24,802** text posts from Twitter where **6% of the tweets were labeled as hate speech**
- The labels on this dataset were voted on by crowdsource and **determined by majority-rules**
- To prepare the data for binary classification, labels were manually replaced by changing existing 1 and 2 values to 0, and changing 0 to 1 to indicate hate speech

### Cleaned Dataset Columns

| Column Name | Description |
|-|-|
| total_votes | number of CrowdFlower users who coded each tweet (minimum is 3, sometimes more users coded a tweet when judgments were determined to be unreliable by CF) |
| hate_speech_votes | number of CF users who judged the tweet to be hate speech |
| other_votes | number of CF users who judged the tweet to be offensive language or neither |
| label | class label for majority of CF user votes. 1 - hate speech 0 - not hate speech |
| tweet | raw tweets |
| clean_tweet | tweets filtered through NLP data cleaning process |

## Data Understanding

### 1. What are the linguistic differences between hate speech and offensive language?

![img1](./visualizations/label_word_count_y.png)

Linguistically, it's important to note that the difference between hate speech and offensive language often comes down to how it targets marginalized communities, often in threatening ways.

- Although the labels have very similar frequently occurring words, only 20% of the "Hate Speech" label is unique overall
- For instance, Hate Speech typically contains the N-word with the hard 'R' 
- **The use of this slur could indicate malicious intent, which goes beyond possibly using the word as cultural slang**

Examples like that one demonstrate the nuances of English slang and the fine line between Hate Speech and offensive language. **Because of the similarities of each label’s vocabulary, it could be difficult for machine learning algorithms to differentiate between them and determine what counts as hate speech.**

### 2. What are the most popular hashtags of each tweet type?

![img2](./visualizations/censored_top_hashtags.png)

We can see some more parallels and differences between what is classified as hate speech or not. 

- #tcot stands for "Top Conservatives On Twitter” and it appears in both groups
- #teabagger, which refers to those who identify with the Tea Party, that is primarily (but not exclusively) associated with the Republican Party, only appears in the “Not Hate Speech” cloud
- Both hashtags are used among Alt-Right communities
- #r**skins, the former Washington NFL team name, only appears in the Not Hate Speech cloud
    - This hashtag demonstrates how similar "offensive language" could be to "Hate Speech"

From this, it's recommended that **Twitter should closely monitor those top hashtags for potential posts containing hate speech** or even regular offensive language.


### 3. What is the overall polarity of the tweets?

![img3](./visualizations/compound_polarity_score.png)

The compound polarity score is a metric that calculates the sum of all the [lexicon ratings](https://github.com/cjhutto/vaderSentiment/blob/master/vaderSentiment/vader_lexicon.txt) which have been normalized between -1 and +1. With -1 being extreme negative and +1 being extreme positive. **This score encompasses the overall sentiment of this corpus.**

- Hate Speech tweets on average have a compound score of -0.363
- Non Hate Speech tweets on average have a compound score of -0.263

According to this metric, both classes of tweets have pretty negative sentiments because their normalized compound scores are less than the threshold of -0.05. 

Additionally from this graph, we can see that tweets classified as Hate Speech are especially negative. This further emphasizes how slim the difference between the two labels are.

## Next Steps

To further develop this project, here are some immediate next steps that anyone could execute.

- Collect more potential "Hate Speech" data to be labeled by CrowdFlower voting system
- Improve final model with different preprocessing techniques, such as removing offensive language as stop words
- Evaluate model with new tweets or other online forum data to see if it can generalize well
- LDA Topic Modeling with Gensim

## Repository Contents
```bash
.
├── models                             # contains model iterations
├── pages                              # contains all webpages for different input formats
├── pickle                             # contains cleaned data
│   └── final_model.pkl                # pickled final model
├── preprocessing                      # contains all data preparation iterations and EDA
├── src                                # source folder
│   └── twitter.csv                    # raw dataset
│   └── utils.py                       # contains utility functions
├── visualizations                     # contains visualizations and local images
├── README.md                          # public-facing preview process
└── Home.py                            # interactive dashboard to host project
```

## For More Information

- See the [full project overview](https://github.com/sidneykung/twitter_hate_speech_detection/blob/master/final_notebook.ipynb) in the `final_notebook.ipynb` Jupyter Notebook.

## References

**Data Source**

- Davidson, T., Warmsley, D., Macy, M. and Weber, I., 2017. Automated Hate Speech Detection and the Problem of Offensive Language. ArXiv,.

**Packages**

- Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
