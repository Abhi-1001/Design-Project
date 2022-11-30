import speech_recognition as sr
import pathlib
import tempfile
from pydub import AudioSegment
import io
import os
import pandas as pd
import numpy as np
import soundfile as sf
from scipy.io.wavfile import write
from audiorecorder import audiorecorder
import src.audio_utils as utils
import json
import librosa
import soundfile as sf
from googleapiclient import discovery

API_KEY = 'AIzaSyA4KlnJP1r-u7USC3ITpsOEgHWFOfP_6tg'

import re
import nltk
import pickle
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

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

def check_hate_speech(user_text):
        # removing punctuation
    user_text = re.sub('[%s]' % re.escape(string.punctuation), '', user_text)


    client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
    cache_discovery = False
    )

    attributes = ["TOXICITY","INSULT", 'SEVERE_TOXICITY','PROFANITY', 'THREAT', 'IDENTITY_ATTACK']
    analyze_request = {
    'comment': { 'text': user_text },
    'requestedAttributes': {'TOXICITY': {}, 'INSULT':{}, 'SEVERE_TOXICITY':{}, 'IDENTITY_ATTACK':{}, 'THREAT':{}, 'PROFANITY':{}}
    }

    response = client.comments().analyze(body=analyze_request).execute()
    result = json.loads(json.dumps(response))

    threshold = 0.6
    for each in attributes:
        score_value = result["attributeScores"][each]['summaryScore']['value']
        print(each, score_value)
        if score_value >= threshold:
            return "Hatespeech"

    return "Not HateSpeech"

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