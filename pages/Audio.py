# importing relevant python packages
import streamlit as st
import pandas as pd
import pickle
import cv2
import os
# preprocessing
import re
import nltk
import string
from io import StringIO
import speech_recognition as sr
import src.audio_utils as utils
from src.load_css import local_css

# creating page sections
audio_input = st.container()
audio_recorder = st.container()
model_results = st.container()
# sentiment_analysis = st.container()

local_css("templates/button_css.css")

with audio_input:
    st.header('Is Your Audio Considered Hate Speech?')
    flag1 = True
    t = "<div class='demo-5 one-edge-shadow'> Upload Audio file</div"
    st.markdown(t, unsafe_allow_html=True)
    user_audio_file = st.file_uploader("", type = [".wav", ".mp3"])
    if user_audio_file:
        user_text = utils.get_text_from_audio(user_audio_file)   
        if user_text == "":
            st.write("No text found")
        else:
            st.info(user_text)

    else:
        user_text = None
        flag1 = False

with audio_recorder:
    for i in range(8):
        st.write("")

    flag1=True
    t = "<div class='demo-5 one-edge-shadow'> Audio recorder</div"
    st.markdown(t, unsafe_allow_html=True)
    user_text, ret = utils.record_audio()
    print("check2:", ret)
    print("check: ", user_text)
    if user_text == "":
            st.write("No text found !!")
    else:
        if user_text:
            if ret:
                st.info(user_text)           
        else:
            flag1  = False

with model_results:
    for i in range(7):
        st.write("")

    t = "<div class='demo-5-pred'>Prediction</div"
    st.markdown(t, unsafe_allow_html=True)
    
    for i in range(2):
        st.write("")
        
    if st.button('Check for Hate Speech'):
        if not flag1:
            t = "<div><span class='highlight grey blink'>Please upload or record audio<span class='bold'></span></div>"
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

