# importing relevant python packages
import streamlit as st

from pydub import AudioSegment
import speech_recognition as sr
import src.audio_utils as utils
from PIL import Image
import easyocr as ocr
import numpy as np

from src.load_css import local_css

img_input = st.container()
img_capture = st.container()
model_results = st.container()

@st.cache
def load_model(): 
    reader = ocr.Reader(['en'],model_storage_directory='.')
    return reader 

reader = load_model() #load model

local_css("templates/button_css.css")

with img_input:
    # local_css()
    flag1 = True
    st.header('Is Your Image text Considered Hate Speech?')
    t = "<div class='demo-5 one-edge-shadow'> Upload Image file</div"
    st.markdown(t, unsafe_allow_html=True)
    user_img_file = st.file_uploader("", type =['png','jpg','jpeg'])
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

        user_text = join_list
        if user_text == "":
            st.write("No text found")
        else:
            st.info(user_text)

    else:
        user_text = None
        flag1 = False

with img_capture:
    flag1 = True
    for i in range(8):
        st.write("")

    t = "<div class='demo-5 one-edge-shadow'> Take a picture</div"
    st.markdown(t, unsafe_allow_html=True)
    picture = st.camera_input("")
    if picture:
        st.image(picture)
        input_image = Image.open(picture) #read image
        result = reader.readtext(np.array(input_image))

        result_text = [] #empty list for results
        for text in result:
            result_text.append(text[1])

        user_text = " ".join(result_text)
        if user_text == "":
            st.write("No text found")
        else:
            st.info(user_text)

    else:
        user_text = None
        flag1 = False


with model_results:
    # if user_text:
    #     result = utils.get_prediction(user_text)
    #     st.write("Prediction:")
    #     st.write(result)
    for i in range(7):
        st.write("")

    t = "<div class='demo-5-pred'>Prediction</div"
    st.markdown(t, unsafe_allow_html=True)
    
    for i in range(2):
        st.write("")

    # st.header("Prediction:")
    if st.button('Check for Hate Speech'):
        if not flag1:
            t = "<div><span class='highlight grey blink'> Please upload or capture image<span class='bold'></span></div>"
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
