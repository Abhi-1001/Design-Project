# importing relevant python packages
import streamlit as st
import pandas as pd
import moviepy.editor
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
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pydub.silence import split_on_silence
from sklearn.feature_extraction.text import CountVectorizer
# modeling
from sklearn import svm
# sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# creating page sections
video_input = st.container()
model_results = st.container()
sentiment_analysis = st.container()

# initialize the recognizer
speech_to_text_convertor = sr.Recognizer()

# func to save BytesIO on a drive
def write_bytesio_to_file(filename, bytesio):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet. 
    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())

with video_input:
    # user input here
    uploaded_file = st.file_uploader("Choose a file", type=['mp4'])
    
    if uploaded_file is not None:
        # save uploaded video to disc
        with st.spinner("Please wait......."):
            temp_file_to_save = 'temp_file_1.mp4'
            write_bytesio_to_file(temp_file_to_save, uploaded_file)

            video = moviepy.editor.VideoFileClip("temp_file_1.mp4")

            audio = video.audio

            audio.write_audiofile("temp_audio_file.wav")

            sound = AudioSegment.from_wav("temp_audio_file.wav")

            audio_chunks = split_on_silence(sound,
                min_silence_len=500,
                silence_thresh=sound.dBFS-14,
                keep_silence=500,
                )

            folder_name = "audio_chunks"

            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)

            whole_text = ""

            for i, audio_chunk in enumerate(audio_chunks, start=1):
                chunk_file = os.path.join(folder_name, f"chunk{i}.wav")

                audio_chunk.export(chunk_file, format="wav")

                with sr.AudioFile(chunk_file) as source:
                    audio_listened = speech_to_text_convertor.record(source)

                    try:
                        text = speech_to_text_convertor.recognize_google(audio_listened, pfilter=0)

                    except sr.UnknownValueError as e:
                        print("Error: ", str(e))

                    else:
                        text = f"{text}"
                        print(chunk_file, ":", text)
                        whole_text += text

            st.write("Converted Speech to Text")
            st.write(whole_text)

            
