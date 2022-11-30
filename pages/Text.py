# importing relevant python packages
import streamlit as st
st.set_page_config(initial_sidebar_state="auto")
import pandas as pd

# preprocessing
from src.video_utils import check_hate_speech
import src.audio_utils as utils
from src.load_css import local_css


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
    flag1 = True
    st.header('Is Your Text Considered Hate Speech?')
        # user input here
    user_text = st.text_area('Enter Tweet', max_chars=280) # setting input as user_text

    if user_text == "":
            st.write("No text found")
            flag1 = False
    else:
        st.write(user_text)



with model_results:
    st.header("Prediction:")
    local_css("templates/button_css.css")
    if st.button('Check for Hate Speech'):
        if not flag1:
            t = "<div><span class='highlight grey blink'>Please enter text<span class='bold'></span></div>"
            # st.write("Please enter text")
            st.markdown(t, unsafe_allow_html=True)
        else:
            with st.spinner("Please wait......."):
                prediction = utils.get_prediction(user_text)
                
                if prediction == "Hatespeech":
                    t = "<div><span class='highlight red'>" + prediction + "<span class='bold'></span></div>"
                else:
                    t = "<div><span class='highlight green'>" + prediction + "<span class='bold'></span></div>"
                st.markdown(t, unsafe_allow_html=True)
                st.text('')

