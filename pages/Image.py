# importing relevant python packages
import streamlit as st

from pydub import AudioSegment
import speech_recognition as sr
import src.audio_utils as utils
from PIL import Image
import easyocr as ocr
import numpy as np

img_input = st.container()
img_capture = st.container()
model_results = st.container()

@st.cache
def load_model(): 
    reader = ocr.Reader(['en'],model_storage_directory='.')
    return reader 

reader = load_model() #load model

with img_input:
    st.write('Upload Image file')
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

        user_text = join_list

    else:
        user_text = None

with img_capture:
    picture = st.camera_input("Take a picture")
    if picture:
        st.image(picture)
        input_image = Image.open(picture) #read image
        result = reader.readtext(np.array(input_image))

        result_text = [] #empty list for results
        for text in result:
            result_text.append(text[1])

        user_text = " ".join(result_text)
        st.info(user_text)

    else:
        user_text = None


with model_results:
    if user_text:
        result = utils.get_prediction(user_text)
        st.write("Prediction:")
        st.write(result)
