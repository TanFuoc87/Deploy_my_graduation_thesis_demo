import streamlit as st
from PIL import Image
      
  
# this is the main function in which we define our webpage  
def main():

    st.set_page_config(
    page_title="Welcome to Dividend Policy Predictor",
    page_icon=":wave:",
    layout="centered",
    initial_sidebar_state="auto"
)

    # front end elements of the web page 
    html_temp = """ 
    <div 
        style ="
            border-style: groove;
            border-color: #207d6c;
            border-width: 4px;
            background-color:rgba(178, 235, 237, 0.53);
            padding:10px;
            opacity: 0.9;
            border-radius: 15px
            "> 
        <h1 
            style = "
                font-family:'Helvetica ', sans-serif;
                color:black;
                text-align:center;
                font-size: 2.8em
                "
            >WELCOME TO <br> DIVIDEND POLICY PREDICTOR</
        h1>
        <h2 
            style ="
                font-family:'Baskerville ', serif;
                color:black;
                text-align:center;
                font-size: 1.8em;
                "
            >-- About us --</
        h2>  
        <h4 
            style ="
                font-family:'Baskerville ', serif;
                color:black;
                text-align:justify;
                font-size: 1.4em;
                font-weight:normal;
                "
            >''' The Well-Performed Machine Learning  model that has been trained to predict "Dividend Policy" based on financial-statement data from over 1000 public companies in Vietnam. With its high accuracy, this model is expected to be a helpful tool for investors and financial professionals looking to make informed decisions about their investments. By leveraging the power of Machine Learning, our model can analyze a vast amount of data, identify patterns, and predict dividend policies with unparalleled accuracy. Whether you're an experienced investor or a newcomer to the world of finance, our model can help you make smarter investment decisions and maximize your returns. Let's try and experience yourself!!! '''</
        h4>
        <h6 
            style ="
                color:black;
                text-align:right;
                font-size: 1.2em;
                font-style:oblique;
                font-weight:normal
                "
            >Made by: Phan Tấn Phước <br> Supervisor: MSc. Phan Huy Tâm</
        h6>
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 


    # Background
    background = """
    <style>
    [data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1493957988430-a5f2e15f39a3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    }
    </style>
    """

    st.markdown(background, unsafe_allow_html = True) 

    subheader = '<p style="font-family:Baskerville; color:Black; font-size: 1.4em; font-weight:normal;">👉 The Predictor has been optimized for predicting the dividend policy of public companies Vietnam. Here are results we achieved:</p>'
    st.markdown(subheader, unsafe_allow_html=True)

    hose_text = '<p style="font-family:Baskerville; color:Black; font-size: 1.2em; font-weight:normal;"> 1️⃣ HOSE <br> </p>'
    st.markdown(hose_text, unsafe_allow_html=True)
    hose = Image.open("pages/model_performance_HOSE.png")
    st.image(hose, caption= 'Efficiency of predicting dividend policy of companies belonging to HOSE')

    hnx_text = '<p style="font-family:Baskerville; color:Black; font-size: 1.2em; font-weight:normal;"> 2️⃣ HNX <br> </p>'
    st.markdown(hnx_text, unsafe_allow_html=True)
    hnx = Image.open("pages/model_performance_HNX.png")
    st.image(hnx, caption= 'Efficiency of predicting dividend policy of companies belonging to HNX')
    
    upcom_text = '<p style="font-family:Baskerville; color:Black; font-size: 1.2em; font-weight:normal;"> 3️⃣ UPCOM <br> </p>'
    st.markdown(upcom_text, unsafe_allow_html=True)
    upcom = Image.open("pages/model_performance_UPCOM.png")
    st.image(upcom, caption= 'Efficiency of predicting dividend policy of companies belonging to UPCOM')

     
if __name__ =='__main__': 
    main()
