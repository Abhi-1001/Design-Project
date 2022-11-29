""" 


    PLEASE NOTE:

    This is an interactive web app created with StreamLit.

    It's hosted on Heroku here:
    https://hate-speech-predictor.herokuapp.com/

    If you use any of this code, please credit with a link to my website:
    https://www.sidneykung.com/


""" 

# importing relevant python packages
import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image
from audiorecorder import audiorecorder
import tempfile
import wave
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import pydub
import queue
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
# preprocessing
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from sklearn.feature_extraction.text import CountVectorizer
# modeling
from sklearn import svm
# sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import streamlit.components.v1 as components
import os
from io import BytesIO
from pydub import AudioSegment
import scipy
import easyocr as ocr
from PIL import Image 
# import cv2

import src.audio_utils as utils

# from src.sound import sound
# from src.settings import DURATION, get_recorded_audio_file

# creating page sections
site_header = st.container()
business_context = st.container()
data_desc = st.container()
performance = st.container()
tweet_input = st.container()
model_results = st.container()
sentiment_analysis = st.container()
contact = st.container()

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


@st.cache
def load_model(): 
    reader = ocr.Reader(['en'],model_storage_directory='.')
    return reader 

reader = load_model() #load model

with tweet_input:
    st.header('Is Your Tweet Considered Hate Speech?')
    st.write("""*Please note that this prediction is based on how the model was trained, so it may not be an accurate representation.*""")
    # user input here
    user_text = st.text_input('Enter Tweet', max_chars=500) # setting input as user_text


    ###########################################################################################################################
    # FOR UPLOADING AUDIO FILE

    user_audio_file = st.file_uploader("upload audio file", type = [".wav", ".mp3"])
    if user_audio_file:
        user_text = utils.get_text_from_audio(user_audio_file)   
        st.info(user_text)
    



    # FOR RECORDING FILE
    st.write("Audio Recorder")
    # webrtc_ctx = webrtc_streamer(
    #     key="sendonly-audio",
    #     mode=WebRtcMode.SENDONLY,
    #     audio_receiver_size=256,
    #     client_settings=ClientSettings(
    #         rtc_configuration={
    #             "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    #         },
    #         media_stream_constraints={
    #             "audio": True,
    #         },
    #     ),
    # )

    # if "audio_buffer" not in st.session_state:
    #     st.session_state["audio_buffer"] = pydub.AudioSegment.empty()

    # status_indicator = st.empty()

    # while True:
    #     if webrtc_ctx.audio_receiver:
    #         try:
    #             audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
    #         except queue.Empty:
    #             status_indicator.write("No frame arrived.")
    #             continue

    #         status_indicator.write("Running. Say something!")

    #         sound_chunk = pydub.AudioSegment.empty()
    #         for audio_frame in audio_frames:
    #             sound = pydub.AudioSegment(
    #                 data=audio_frame.to_ndarray().tobytes(),
    #                 sample_width=audio_frame.format.bytes,
    #                 frame_rate=audio_frame.sample_rate,
    #                 channels=len(audio_frame.layout.channels),
    #             )
    #             sound_chunk += sound

    #         if len(sound_chunk) > 0:
    #             st.session_state["audio_buffer"] += sound_chunk
    #     else:
    #         status_indicator.write("AudioReciver is not set. Abort.")
    #         break

    # audio_buffer = st.session_state["audio_buffer"]

    # if not webrtc_ctx.state.playing and len(audio_buffer) > 0:
    #     st.info("Writing wav to disk")
    #     tmp_audio_file = tempfile.NamedTemporaryFile(delete = False, mode = "w+b")
    #     audio_buffer.export(tmp_audio_file.name, format="wav")
    #     user_text = utils.get_text_from_audio(tmp_audio_file)

    #     # Reset
    #     st.session_state["audio_buffer"] = pydub.AudioSegment.empty()

    ############################################################################################################

    # if st.button('Record'):
    #     with st.spinner(f'Recording for {DURATION} seconds ....'):
    #         sound.record()
    #     st.success("Recording completed")


    # st.sidebar.title("Duration")
    # duration = st.sidebar.slider("Recording duration", 0.0, 3600.0, 3.0)
    # duration = 10

    # if st.button("Start Recording"):
    #     with st.spinner("Recording..."):
    #         user_audio_record = utils.record_audio(duration)

    #     user_text = utils.get_text_from_audio(user_audio_record)

    ############################################################################################

    # parent_dir = os.path.dirname(os.path.abspath(__file__))
    # # Custom REACT-based component for recording client audio in browser
    # build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
    # # specify directory and initialize st_audiorec object functionality
    # st_audiorec = components.declare_component("st_audiorec", path=build_dir)

    # # TITLE and Creator information
    # st.title('streamlit audio recorderss')
    # st.write('\n\n')


    # # STREAMLIT AUDIO RECORDER Instance
    # val = st_audiorec()
    # # web component returns arraybuffer from WAV-blob
    # st.write('Audio data received in the Python backend will appear below this message ...')

    # if isinstance(val, dict):  # retrieve audio data
    #     with st.spinner('retrieving audio-recording...'):
    #         ind, val = zip(*val['arr'].items())
    #         ind = np.array(ind, dtype=int)  # convert to np array
    #         val = np.array(val)             # convert to np array
    #         sorted_ints = val[ind]
    #         stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))

    #     # tmp_audio_file = tempfile.NamedTemporaryFile(suffix=".wav", mode = "b+x")
    #     buffer = stream.getbuffer()
    #     with open("stream.mp3", "w+b") as file:
    #         file.write(buffer)

    #         user_text = utils.get_text_from_audio(file)   
    #         st.info(user_text)


    #     tmp_audio_file = "tmp_file.wav"
    #     output = utils.convert_bytearray_to_wav_ndarray(input_bytearray=stream.read())
    #     scipy.io.wavfile.write(tmp_audio_file, 16000, output)

    #     # tmp_audio_file.write(stream.read())
    #     # audio = AudioSegment.from_raw(stream, sample_width = é, frame_rate = 44100, channels = 1).export(tmp_audio_file.name, format='wav')
        
    #     audio = wave.open(tmp_audio_file, "r")

    #     ####################################################################################################################################
        # wav_bytes contains audio data in format to be further processed
        # display audio data as received on the Python side
        # st.audio(wav_bytes, format='audio/wav')
        # print("this2: ",)

        # audio = get_recorded_audio_file()
    user_text = utils.record_audio()
    if user_text:
        st.info(user_text)

    #############################################################################################################
    # audio_file = open("Welcome.wav", mode = "r+b")
    # user_text = utils.get_text_from_audio(audio_file)
    # st.info(user_text)
    # st.audio(audio_file)



    # UPLOADING PICTURE
    user_img_file = st.file_uploader("upload img file", type =['png','jpg','jpeg'])
    if user_img_file:
        input_image = Image.open(user_img_file) #read image
        st.image(input_image) #display image

        result = reader.readtext(np.array(input_image))

        result_text = [] #empty list for results
        for text in result:
            result_text.append(text[1])

        # st.write(result_text)
        # print("res", result_text)
        join_list = " ".join(result_text)

        # FOR WHOLE PARAGRAPH
        # user_text = join_list

        # For each sentence
        if "." in join_list:
            sentence_list = join_list.split(".")[:-1]
        else:
            sentence_list = [join_list]
        st.info(sentence_list)

        user_text = sentence_list

    # FOR CLICKING PICTURE

    # vid = cv2.VideoCapture( 'http://localhost:8501/video' )

    # st.title( 'Using Mobile Camera with Streamlit' )
    # frame_window = st.image( [] )
    # take_picture_button = st.button( 'Take Picture' )

    # while True:
    #     got_frame , frame = vid.read()
    #     frame = cv2.cvtColor( frame , cv2.COLOR_BGR2RGB )
    #     if got_frame:
    #         frame_window.image(frame)

    #     if take_picture_button:
    #         # Pass the frame to a model
    #         # And show the output here...
    #         break

    # vid.release()
    ##########################################################################################################################



print("user text: ", user_text)


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


with model_results:    
    st.subheader('Prediction:')
    if type(user_text) == list:
        for each in user_text:
            prediction = get_prediction(each)
            st.write("For text: ", each)
            if prediction == 0:
                st.write('**Not Hate Speech**')
            else:
                st.write('**Hate Speech**')
            st.text('')

    elif type(user_text) == str:
    # processing user_text
        try:
            prediction = get_prediction(user_text)

            if prediction == 0:
                st.subheader('**Not Hate Speech**')
            else:
                st.subheader('**Hate Speech**')
            st.text('')
        except:
            print("error")