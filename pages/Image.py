# importing relevant python packages
import streamlit as st

# creating page sections
camera_input = st.container()
model_results = st.container()

with camera_input:
    image = st.camera_input("Take a picture")

with model_results:
    if image:
        st.image(image)