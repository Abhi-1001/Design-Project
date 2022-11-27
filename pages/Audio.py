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
from pydub import AudioSegment
import speech_recognition as sr
import utils

# creating page sections
audio_input = st.container()
audio_recorder = st.container()
model_results = st.container()
# sentiment_analysis = st.container()

with audio_input:
    st.write("Audio Recorder")
    user_audio_file = st.file_uploader("upload audio file", type = [".wav", ".mp3"])
    if user_audio_file:
        user_text = utils.get_text_from_audio(user_audio_file)   
        st.info(user_text)
    else:
        user_text = None

with model_results:
    if user_text:
        result = utils.get_prediction(user_text)

        st.write(result)
