# importing relevant python packages
import streamlit as st
st.set_page_config(initial_sidebar_state="auto", layout="wide")
from PIL import Image

video_html = """
		<style>
            #myVideo {
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100%; 
            min-height: 100%;
            }

            .content {
            position: fixed;
            bottom: 0;
            background: rgba(0, 0, 0, 0.9);
            color: #f1f1f1;
            width: 100%;
            padding: 20px;
            }
		</style>

		<video autoplay muted loop id="myVideo">
		  <source src="https://static.streamlit.io/examples/star.mp4">
		  Your browser does not support HTML5 video.
		</video>
        """

st.markdown(video_html, unsafe_allow_html=True)

# creating page sections
site_header = st.container()
business_context = st.container()
data_desc = st.container()
performance = st.container()
contact = st.container()

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

with site_header:
    st.title('Hate Speech Detection')
    st.write("""
    This project intends to use machine learning techniques to automate content filtering to
    detect hate speech. It supports various modes of input to detect hate Speech.
    """)

# with business_context:
#     st.header('The Problem of Content Moderation')
#     st.write("""
#     **Human content moderation exploits people by consistently traumatizing and underpaying them.** In 2019, an [article](https://www.theverge.com/2019/6/19/18681845/facebook-moderator-interviews-video-trauma-ptsd-cognizant-tampa) on The Verge exposed the extensive list of horrific working conditions that employees faced at Cognizant, which was Facebook’s primary moderation contractor. Unfortunately, **every major tech company**, including **Twitter**, uses human moderators to some extent, both domestically and overseas.
    
#     Hate speech is defined as **abusive or threatening speech that expresses prejudice against a particular group, especially on the basis of race, religion or sexual orientation.**  Usually, the difference between hate speech and offensive language comes down to subtle context or diction.
#     """)
with business_context:
    st.header('What is Hate Speech')
    st.write("""
            Hate speech is described as abusive or threatening speech that conveys prejudice against
            a certain group, often based on race, religion, or sexual orientation. Hate speech and
            abusive language can typically be distinguished by slight nuances in context or diction.
            Although there is no precise definition of hate speech, in general it is speech that targets
            a person’s distinctive values and is designed not just to humiliate or mock the target but
            also to harass and create enduring harm. \n
            Hatebase created a multilingual dictionary of words used in hate speech, has the fol-
            lowing criteria for identifying hate speech:
            - It is addressed to a specific group of people (ethnicity, nationality, religion, sexuality, disability or class)
            - There is a malicious intent
            """)

    st.header("Labels Predicted")
    st.write("""
            - Hate Speech
            - Not Hate Speech
            """)

