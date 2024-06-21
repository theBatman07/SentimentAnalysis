import streamlit as st
import streamlit.components.v1 as components
import requests
from PIL import Image
import text2emotion as te
import plotly.graph_objects as go

def plotPie(labels, values):
    fig = go.Figure(
        go.Pie(
        labels = labels,
        values = values,
        hoverinfo = "label+percent",
        textinfo = "value"
    ))
    st.plotly_chart(fig)

def getSentiments(userText, type):
    if(type == 'Positive/Negative/Neutral - TextBlob'):
        response = requests.post("http://127.0.0.1:5000/upload", files={'file': userText})
        if response.status_code == 200:
            result = response.json()
            polarity = result['sentiment']['polarity']
            subjectivity = result['sentiment']['subjectivity']
            status = result['sentiment']['sentiment']
            if status == "Positive":
                image = Image.open('./images/positive.PNG')
            elif status == "Negative":
                image = Image.open('./images/negative.PNG')
            else:
                image = Image.open('./images/neutral.PNG')
            col1, col2, col3 = st.columns(3)
            col1.metric("Polarity", polarity, None)
            col2.metric("Subjectivity", subjectivity, None)
            col3.metric("Result", status, None)
            st.image(image, caption=status)
        else:
            st.write("Error:", response.json().get('error', 'Unknown error'))
    elif(type == 'Happy/Sad/Angry/Fear/Surprise - text2emotion'):
        emotion = dict(te.get_emotion(userText))
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Happy 😊", emotion['Happy'], None)
        col2.metric("Sad 😔", emotion['Sad'], None)
        col3.metric("Angry 😠", emotion['Angry'], None)
        col4.metric("Fear 😨", emotion['Fear'], None)
        col5.metric("Surprise 😲", emotion['Surprise'], None)
        plotPie(list(emotion.keys()), list(emotion.values()))

def renderPage():
    st.title("Sentiment Analysis 😊😐😕")
    components.html("""<hr style="height:3px;border:none;color:#333;background-color:#333; margin-bottom: 10px" /> """)
    st.subheader("User Input Text Analysis")
    st.text("Analyzing call transcripts given by the user and find sentiments within it.")
    st.text("")
    uploaded_file = st.file_uploader("Choose a file")
    st.text("")
    type = st.selectbox(
     'Type of analysis',
     ('Positive/Negative/Neutral - TextBlob', 'Happy/Sad/Angry/Fear/Surprise - text2emotion'))
    st.text("")
    if st.button('Predict'):
        if uploaded_file is not None and type:
            st.text("")
            components.html("""
                <h3 style="color: #0284c7; font-family: Source Sans Pro, sans-serif; font-size: 28px; margin-bottom: 10px; margin-top: 50px;">Result</h3>
                """, height=100)
            content = uploaded_file.read().decode('utf-8')
            getSentiments(content, type)

if __name__ == '__main__':
    renderPage()
