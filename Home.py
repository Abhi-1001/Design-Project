# importing relevant python packages
import streamlit as st
st.set_page_config(initial_sidebar_state="auto", layout="wide")

from PIL import Image

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
    This project aims to **automate content moderation** to identify hate speech using **machine learning algorithms.**
    """)

with business_context:
    st.header('The Problem of Content Moderation')
    st.write("""
    **Human content moderation exploits people by consistently traumatizing and underpaying them.** In 2019, an [article](https://www.theverge.com/2019/6/19/18681845/facebook-moderator-interviews-video-trauma-ptsd-cognizant-tampa) on The Verge exposed the extensive list of horrific working conditions that employees faced at Cognizant, which was Facebook’s primary moderation contractor. Unfortunately, **every major tech company**, including **Twitter**, uses human moderators to some extent, both domestically and overseas.
    
    Hate speech is defined as **abusive or threatening speech that expresses prejudice against a particular group, especially on the basis of race, religion or sexual orientation.**  Usually, the difference between hate speech and offensive language comes down to subtle context or diction.
    """)

with data_desc:
    understanding, venn = st.columns(2)
    with understanding:
        st.text('')
        st.write("""
        The **data** for this project was sourced from a Cornell University [study](https://github.com/t-davidson/hate-speech-and-offensive-language) titled *Automated Hate Speech Detection and the Problem of Offensive Language*.
        
        The `.csv` file has **24,802 rows** where **6% of the tweets were labeled as "Hate Speech".**

        Each tweet's label was voted on by crowdsource and determined by majority rules.
        """)
    with venn:
        st.image(Image.open('visualizations/word_venn.png'), width = 400)
