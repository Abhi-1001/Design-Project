# importing relevant python packages
import streamlit as st
st.set_page_config(initial_sidebar_state="auto")
import moviepy.editor
import shutil
import os

# preprocessing
from pydub import AudioSegment
import speech_recognition as sr
from src.utils import check_hate_speech
from src.utils import write_bytesio_to_file
from pydub.silence import split_on_silence

# creating page sections
video_input = st.container()
model_results = st.container()

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# initialize the recognizer
speech_to_text_convertor = sr.Recognizer()

with video_input:
    st.header('Is Your Video Considered Hate Speech?')
    st.write("""*Please note that this prediction is based on how the model was trained, so it may not be an accurate representation.*""")
    # user input here
    uploaded_file = st.file_uploader("Choose a file", type=['mp4'])
    
    if uploaded_file is not None:
        # save uploaded video to disc
        with st.spinner("Please wait....... Extracting audio........"):
            temp_file_to_save = 'temp_video_file.mp4'
            write_bytesio_to_file(temp_file_to_save, uploaded_file)

            video = moviepy.editor.VideoFileClip("temp_video_file.mp4")

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

            st.write("Converted Audio to Text")
            st.write(whole_text)
            
            # remove the media files
            os.remove('/home/abhi1001/personal_projects/Design-Project/temp_audio_file.wav')
            os.remove('/home/abhi1001/personal_projects/Design-Project/temp_video_file.mp4')
            shutil.rmtree('/home/abhi1001/personal_projects/Design-Project/audio_chunks')

with model_results:
    if st.button('Check for Hate Speech'):
        with st.spinner("Please wait......."):
            prediction = check_hate_speech(whole_text)
            
            prediction = 'Prediction: ' + prediction

            st.subheader(prediction)
            st.text('')
