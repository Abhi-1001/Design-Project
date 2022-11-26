# importing relevant python packages
import streamlit as st
st.set_page_config(initial_sidebar_state="auto")
import pandas as pd

# preprocessing
from src.utils import check_hate_speech

# sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# creating page sections
text_input = st.container()
model_results = st.container()
sentiment_analysis = st.container()

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

with text_input:
    st.header('Is Your Text Considered Hate Speech?')
    st.write("""*Please note that this prediction is based on how the model was trained, so it may not be an accurate representation.*""")
    # user input here
    user_text = st.text_area('Enter Tweet', max_chars=280) # setting input as user_text

    st.button('Check for Hate Speech')

with model_results:
    # processing user_text
    if user_text:
        with st.spinner("Please wait......."):
            prediction = check_hate_speech(user_text)
            
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