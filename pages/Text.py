# importing relevant python packages
import streamlit as st
import pandas as pd
import numpy as np
import pickle
# preprocessing
import re
import nltk
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
# modeling
from sklearn import svm
# sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# creating page sections
text_input = st.container()
model_results = st.container()
sentiment_analysis = st.container()
stopword = set(stopwords.words('english'))
stemmer = nltk.SnowballStemmer("english")

def clean(text):
    text = str (text). lower()
    text = re.sub('[.?]', '', text)
    text = re.sub('https?://\S+|www.\S+', '', text)
    text = re.sub('<.?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w\d\w', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text= " ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text= " ".join(text)
    return text

with text_input:
    st.header('Is Your Tweet Considered Hate Speech?')
    st.write("""*Please note that this prediction is based on how the model was trained, so it may not be an accurate representation.*""")
    # user input here
    user_text = st.text_input('Enter Tweet', max_chars=280) # setting input as user_text

with model_results:
    # processing user_text
    if user_text:
        with st.spinner("Please wait......."):
            data = pd.read_csv("/home/abhi1001/personal_projects/Design-Project/src/twitter.csv")
            data["labels"] = data["class"]. map({0: "Hate Speech", 1: "Offensive Speech", 2: "No Hate and Offensive Speech"})
            data = data[["tweet", "labels"]]

            data["tweet"] = data["tweet"].apply(clean)
            x = np.array(data["tweet"])
            cv = CountVectorizer()
            cv.fit_transform(x)

            with open('/home/abhi1001/personal_projects/Design-Project/pickle/final_model.pkl', 'rb') as file:
                model = pickle.load(file)

            # Predicting the outcome
            input = cv.transform([user_text]).toarray()
            prediction = model.predict(input)

            prediction = ' '.join(prediction).capitalize()
            print(prediction)

            prediction = 'Prediction: ' + prediction
            
            st.subheader(prediction)
            st.text('')

with sentiment_analysis:
    if user_text:
        st.header('Sentiment Analysis with VADER')
        
        # explaining VADER
        st.write("""*VADER is a lexicon designed for scoring social media. More information can be found [here](https://github.com/cjhutto/vaderSentiment).*""")
        # spacer
        st.text('')
    
        # instantiating VADER sentiment analyzer
        analyzer = SentimentIntensityAnalyzer() 
        # the object outputs the scores into a dict
        sentiment_dict = analyzer.polarity_scores(user_text) 
        if sentiment_dict['compound'] >= 0.05 : 
            category = ("**Positive ✅**")
        elif sentiment_dict['compound'] <= - 0.05 : 
            category = ("**Negative 🚫**") 
        else : 
            category = ("**Neutral ☑️**")

        # score breakdown section with columns
        breakdown, graph = st.columns(2)
        with breakdown:
            # printing category
            st.write("Your Tweet is rated as", category) 
            # printing overall compound score
            st.write("**Compound Score**: ", sentiment_dict['compound'])
            # printing overall compound score
            st.write("**Polarity Breakdown:**") 
            st.write(sentiment_dict['neg']*100, "% Negative") 
            st.write(sentiment_dict['neu']*100, "% Neutral") 
            st.write(sentiment_dict['pos']*100, "% Positive") 
        with graph:
            sentiment_graph = pd.DataFrame.from_dict(sentiment_dict, orient='index').drop(['compound'])
            st.bar_chart(sentiment_graph) 