import speech_recognition as sr
import pathlib
from pydub import AudioSegment
import io
import pickle
import re
import string
import wave

import numpy as np
import soundfile as sf
from scipy.io.wavfile import write
from audiorecorder import audiorecorder
from pydub.silence import split_on_silence
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from sklearn.feature_extraction.text import CountVectorizer
import subprocess
import shutil
import librosa
import soundfile as sf
from googleapiclient import discovery
import json

stopword = set(stopwords.words('english'))
stemmer = nltk.SnowballStemmer("english")

API_KEY = 'AIzaSyA4KlnJP1r-u7USC3ITpsOEgHWFOfP_6tg'


# from hatesonar import Sonar
# sonar_model = Sonar()


nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


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



def convert_mp3_to_wav(inp_file, op_file):
    try:
        sound = AudioSegment.from_file(inp_file.name, format = "mp3")
    except:
        sound = Audiosegment.from_file(inp_file.name, format="mp4")
    sound.export(op_file, format="wav")
    return open(op_file)


def get_text_from_audio(file_uploaded, already_exist = False):
    # if file_uploaded
    print("this:",file_uploaded.name)
    input_file = file_uploaded
    tmp_wav_file = "generated_files/tmp_wav_file.wav"
    if pathlib.Path(file_uploaded.name).suffix == ".mp3":
        # input_file = convert_mp3_to_wav(file_uploaded)

        if not already_exist:
            tmp_mp3_file = "generated_files/tmp_mp3_file.mp3"
            with open(tmp_mp3_file, "w+b") as f:
                f.write(file_uploaded.getbuffer())
            input_file = convert_mp3_to_wav(tmp_mp3_file, tmp_wav_file)
        else:
            input_file = file_uploaded
    else:
        if not already_exist:
            temp_wav_file = "generated_files/tmp_wav_file.wav"
            write_bytesio_to_file(temp_wav_file, input_file)
            input_file = open(temp_wav_file)
        else:
            input_file = file_uploaded

    sound = AudioSegment.from_wav(input_file.name)

    audio_chunks = split_on_silence(sound,
                min_silence_len=500,
                silence_thresh=sound.dBFS-14,
                keep_silence=500,
                )

    folder_name = "audio_chunks"
    if os.path.isdir(folder_name):
        # os.unlink(folder_name)
        shutil.rmtree(folder_name)

    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    whole_text = ""

    for i, audio_chunk in enumerate(audio_chunks, start=1):
        chunk_file = os.path.join(folder_name, f"chunk{i}.wav")

        audio_chunk.export(chunk_file, format="wav")

        with sr.AudioFile(chunk_file) as source:
            audio_listened = speech_to_text_convertor.record(source)

            try:
                text = speech_to_text_convertor.recognize_google(audio_listened)

            except sr.UnknownValueError as e:
                print("Error: ", str(e))

            else:
                text = f"{text}"
                print(chunk_file, ":", text)
                whole_text += text

    
    return whole_text


def record_audio():
    audio = audiorecorder("Click to record", "Click to stop recording")

    if len(audio) > 0:       
        # To save audio to a file:
        # tmp_audio_file = tempfile.NamedTemporaryFile(delete = False, mode = "w+b", suffix = ".mp3")
        file_path = "generated_files/temp_audio_record1.wav"
        tmp_audio_file = open(file_path, mode = "w+b")
        tmp_audio_file.write(audio.tobytes())

        file_path_op = "generated_files/temp_audio_record.wav"
        x,_ = librosa.load(file_path, sr=16000)
        sf.write(file_path_op, x, 16000)

        final_audio_file = open(file_path_op)

        # final_audio_file = wave.open(file_path_op)
        user_text = get_text_from_audio(final_audio_file, already_exist= True)

        return user_text
    
    return None




def get_prediction(user_text):
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