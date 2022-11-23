# importing relevant python packages
import streamlit as st
from PIL import Image

# creating page sections
site_header = st.container()
business_context = st.container()
data_desc = st.container()
performance = st.container()
contact = st.container()

with site_header:
    st.title('Hate Speech Detection')
    st.write("""
    This project aims to **automate content moderation** to identify hate speech using **machine learning binary classification algorithms.** 
    
    Baseline models included Random Forest, Naive Bayes, Logistic Regression and Support Vector Machine (SVM). The final model was a **Logistic Regression** model that used Count Vectorization for feature engineering. It produced an F1 of 0.3958 and Recall (TPR) of 0.624.  
        
    Check out the project repository [here](https://github.com/sidneykung/twitter_hate_speech_detection).
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

with performance:
    description, conf_matrix = st.columns(2)
    with description:
        st.header('Final Model Performance')
        st.write("""
        These scores are indicative of the two major roadblocks of the project:
        - The massive class imbalance of the dataset
        - The model's inability to identify what constitutes as hate speech
        """)
    with conf_matrix:
        st.image(Image.open('visualizations/normalized_log_reg_countvec_matrix.png'), width = 400)

with contact:
    st.markdown("---")
    st.header('For More Information')
    st.text('')
    st.write("""

    **Check out the project repository [here](https://github.com/sidneykung/twitter_hate_speech_detection).**

    Contact Sidney Kung via [sidneyjkung@gmail.com](mailto:sidneyjkung@gmail.com).
    """)

    st.subheader("Let's Connect!")
    st.write("""
    
    [LinkedIn](https://www.linkedin.com/in/sidneykung/) | [Github](https://github.com/sidneykung)  |  [Medium](https://medium.com/@sidneykung)  |  [Twitter](https://twitter.com/sidney_k98)


    """)
