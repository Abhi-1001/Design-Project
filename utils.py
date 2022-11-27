import speech_recognition as sr
import pathlib
from pydub import AudioSegment
import io
import pickle
import re
import string

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

from hatesonar import Sonar
sonar_model = Sonar()


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
    sound = AudioSegment.from_mp3(inp_file)
    sound.export(op_file, format="wav")
    return open(op_file)


def get_text_from_audio(file_uploaded):
    # if file_uploaded
    print("this:",file_uploaded.name)
    input_file = file_uploaded
    tmp_wav_file = "generated_files/tmp_wav_file.wav"
    if pathlib.Path(file_uploaded.name).suffix == ".mp3":
        # input_file = convert_mp3_to_wav(file_uploaded)

        tmp_mp3_file = "generated_files/tmp_mp3_file.mp3"
        with open(tmp_mp3_file, "w+b") as f:
            f.write(file_uploaded.getbuffer())

        input_file = convert_mp3_to_wav(tmp_mp3_file, tmp_wav_file)
    else:
        temp_wav_file = "generated_files/tmp_wav_file.wav"
        write_bytesio_to_file(temp_wav_file, input_file)
        input_file = open(temp_wav_file)

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

def convert_bytearray_to_wav_ndarray(input_bytearray: bytes, sampling_rate=16000):
    bytes_wav = bytes()
    byte_io = io.BytesIO(bytes_wav)
    write(byte_io, sampling_rate, np.frombuffer(input_bytearray, dtype=np.int16))
    output_wav = byte_io.read()
    output, samplerate = sf.read(io.BytesIO(output_wav))
    return output


def record_audio():
    audio = audiorecorder("Click to record", "Click to stop recording")

    if len(audio) > 0:       
        # To save audio to a file:
        # tmp_audio_file = tempfile.NamedTemporaryFile(delete = False, mode = "w+b", suffix = ".mp3")
        tmp_audio_file = open("generated_files/temp_audio.mp3", "w+b")
        tmp_audio_file.write(audio.tobytes())

        user_text = get_text_from_audio(tmp_audio_file)

        # tmp_audio_file.close()
        # os.remove(tmp_audio_file.name)
        return user_text
    
    return None

def get_prediction(user_text):
    # removing punctuation
    user_text = re.sub('[%s]' % re.escape(string.punctuation), '', user_text)
    # tokenizing
    stop_words = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(user_text)
    # removing stop words
    stopwords_removed = [token.lower() for token in tokens if token.lower() not in stop_words]
    # taking root word
    lemmatizer = WordNetLemmatizer() 
    lemmatized_output = []
    for word in stopwords_removed:
        lemmatized_output.append(lemmatizer.lemmatize(word))
    print("lemma: ", lemmatized_output)

    result = sonar_model.ping(text = user_text)

    res_class = result['top_class']

    return res_class




    # instantiating count vectorizor
    count = CountVectorizer(stop_words=stop_words)
    X_train = pickle.load(open('pickle/X_train_2.pkl', 'rb'))
    X_test = lemmatized_output
    X_train_count = count.fit_transform(X_train)
    X_test_count = count.transform(X_test)

    # loading in model
    final_model = pickle.load(open('pickle/final_log_reg_count_model.pkl', 'rb'))

    # apply model to make predictions
    prediction = final_model.predict(X_test_count[0])

    return prediction