import pickle
import streamlit as st
import pandas as pd
from PIL import Image

#load demo result
result = pd.read_pickle('pages/result.pkl')
result_2022 = pd.read_pickle('pages/result2022.pkl')
stock_code ='' 

def view_result_2022(stock_name):
    if stock_name not in list(result_2022['Stock_name'].unique()):
        info = 'No data available!'
        return info
    else:
        stock_code_info = result_2022.loc[result_2022['Stock_name']== stock_name]
        company_name = stock_code_info['Company_Name'].item()
        exchange_name = stock_code_info['Exchange_name'].item()
        year = int(stock_code_info['Establish_Year'].item())
        industry = stock_code_info['Industry'].item()
        website = stock_code_info['Website'].item()
        predict = stock_code_info['Predicted Dividend Policy'].item()

        if predict == 0:
            policy = 'NOT PAY'
            predict_prob = round((stock_code_info['Probability of Not Paying Dividend'].item())*100,2)
        else: 
            policy = 'PAY'
            predict_prob =round((stock_code_info['Probability of Paying Dividend'].item())*100,2)

        info = [company_name, year, industry, website, policy, predict_prob, exchange_name]

        return info


@st.cache_data(experimental_allow_widgets=True)
  
# this is the main function in which we define our webpage  
def main():

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
            >DIVIDEND POLICY PREDICTOR</
        h1>
        <h2 
            style ="
                font-family:'Baskerville ', serif;
                color:black;
                text-align:center;
                font-size: 1.4em
                "
            >Our predictions about dividend policy of public companies in Vietnam</
        h2>
        <h2 
            style ="
                font-family:'Baskerville ', serif;
                color:black;
                text-align:center;
                font-size: 1.4em
                "
            >We have collected 2022 financial data of 920 companies from <br> HOSE, HNX, and UPCOM.</
        h2>
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

    # Predict 2022
    intro_2022 = '<p style="font-family:Baskerville; color:Black; font-size: 1.2em; font-weight:normal;">👉 Our expectation for the overall coming dividend policy:  <br> </p>'
    st.markdown(intro_2022, unsafe_allow_html= True)
    predict_2022 = Image.open("C:/Users/Tan Phuoc/Desktop/Coding Stuff/Portfolio 2023/Graduation Thesis_Dividend Forecast/Streamlit_deploy/pages/prediction_2022.png")
    st.image(predict_2022, caption= 'The expectation for coming dividend policy of public companies in Vietnam')

    option_2022 = '<p style="font-family:Baskerville; color:Black; font-size: 1.2em; font-weight:normal;"> 👉 Find our 2022 dividend policy prediction of a specific:   <br> </p>'
    st.markdown(option_2022, unsafe_allow_html= True)
    stock_code= st.text_input('Enter the company stock code:', max_chars= 3)

    if st.button("Enter"): 
        enter_result_2022 = view_result_2022(stock_code.upper())
        if  enter_result_2022 == 'No data available!':
            st.success(enter_result_2022)
        else: 
            st.success('Stock name: {0}'.format(stock_code.upper()))
            st.success('Stock Exchange: {0}'.format(enter_result_2022[6]))
            st.success('Company name: {0}'.format(enter_result_2022[0]))
            st.success('Establish year: {0}'.format(enter_result_2022[1]))
            st.success('Industry: {0}'.format(enter_result_2022[2]))
            st.success('Website: {0}'.format(enter_result_2022[3]))
            st.success('We expect that this company will {0} dividend for 2022 with the probability is: {1}%'.format(enter_result_2022[4], enter_result_2022[5]))

    option_2022 = '<p style="font-family:Baskerville; color:Black; font-size: 1.2em; font-weight:normal;"> Find our 2022 dividend policy prediction of a specific:   <br> </p>'
     
if __name__ =='__main__': 
    main()
