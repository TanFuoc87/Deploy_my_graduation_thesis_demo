import pickle
import pandas as pd
import streamlit as st
import os.path

#Determine the current directory using os.path.dirname
current_directory = os.path.dirname(__file__)
#Determine the parent directory using os.path.split:
parent_directory = os.path.split(current_directory)[0] # Repeat as needed
#Join parent_directory with any sub-directories:
file_path = os.path.join(parent_directory, 'path', 'to', 'file')

# loading the trained model
pickle_in = open('dividend_policy_predictor.pkl', 'rb') 
predictor = pickle.load(pickle_in)

#load demo result
result = pd.read_pickle('pages/result.pkl')
result_2022 = pd.read_pickle('pages/result2022.pkl')
 
@st.cache_data()
  
# defining the function which will make the prediction using the data which the user inputs 
def prediction(Net_Income, Total_Equity, Total_Revenue, Current_Assets, Current_Liabilities, Total_Liabilities, Total_Assets, Stock_Price, 
               Cash_from_Operating_Activities, Net_Intangibles_Asset, Total_Common_Stock, Operating_Income, Net_Income_Before_Taxes,
               Cumulative_Net_Change_in_Cash, Retained_Earnings, Free_Cash_Flow, Dividend_in_3_latest_year):

    import numpy as np
    import pandas as pd

    Interest_Expense = Operating_Income - Net_Income_Before_Taxes
    Book_Value = Total_Assets - Net_Intangibles_Asset - Total_Liabilities
    Size = np.log(Total_Assets)
    Current_Ratio = Current_Assets/ Current_Liabilities
    ROA = Net_Income/ Total_Assets
    ROE = Net_Income/ Total_Equity
    Debt_on_Equity = Total_Liabilities/ Total_Equity
    Net_profit_margin = Net_Income/ Total_Revenue
    Cost_of_debt = Interest_Expense/ Total_Liabilities
    BVPS = Book_Value/ Total_Common_Stock
    Price_on_Book_Value =Stock_Price/ BVPS
    EPS = Net_Income / Total_Common_Stock
    Price_on_EPS =Stock_Price/ EPS
    Price_on_Operating_Cash_flow_per_Share =Stock_Price/(Cash_from_Operating_Activities/Total_Common_Stock)
    Operating_cash_flow_ratio = Cash_from_Operating_Activities/ Current_Liabilities
    Time_interest_earned = Operating_Income/ Interest_Expense
    Retained_Earnings = Retained_Earnings
    Cumulative_Net_Change_in_Cash = Cumulative_Net_Change_in_Cash
    FCF = Free_Cash_Flow 
    Dividend_in_3_latest_year = Dividend_in_3_latest_year  

    # Pre-processing user input    
    if Dividend_in_3_latest_year == "Yes":
        Dividend_in_3_latest_year = 1
    else:
        Dividend_in_3_latest_year = 0

    # Create a list of features of the needed-predict observation
    object = [Size, Current_Ratio, ROA, ROE, Debt_on_Equity, Net_profit_margin, Cost_of_debt, BVPS, 
              Price_on_Book_Value, Price_on_EPS, Price_on_Operating_Cash_flow_per_Share,
              Operating_cash_flow_ratio, Time_interest_earned, Retained_Earnings, 
              Cumulative_Net_Change_in_Cash, FCF, Dividend_in_3_latest_year]
 
    # Making predictions 
    predict = predictor.predict([object])
    
    prediction_proba = predictor.predict_proba([object])

    not_pay_prob = (prediction_proba[0,0])
    pay_prob = (prediction_proba[0,1])

    if predict == 0:
            policy = 'NOT PAY'
            predict_prob = not_pay_prob
            similar = result.loc[(result['Probability of Not Paying Dividend'] > (predict_prob -0.05) ) & (result['Probability of Not Paying Dividend'] < (predict_prob +0.05))]
            pay_dividend = similar.loc[similar['Actual Dividend Policy'] == 1]
            not_pay_dividend = similar.loc[similar['Actual Dividend Policy'] == 0]
            wrong = similar.loc[(similar['Actual Dividend Policy'] != similar['Predicted Dividend Policy'])]
            correct = similar.loc[(similar['Actual Dividend Policy'] == similar['Predicted Dividend Policy'])]
    else: 
            policy = 'PAY'
            predict_prob = pay_prob
            similar = result.loc[(result['Probability of Paying Dividend'] > (predict_prob -0.05) ) & (result['Probability of Paying Dividend'] < (predict_prob +0.05))]
            pay_dividend = similar.loc[similar['Actual Dividend Policy'] == 1]
            not_pay_dividend = similar.loc[similar['Actual Dividend Policy'] == 0]
            wrong = similar.loc[(similar['Actual Dividend Policy'] != similar['Predicted Dividend Policy'])]
            correct = similar.loc[(similar['Actual Dividend Policy'] == similar['Predicted Dividend Policy'])]

    pay_ratio = round(((len(pay_dividend)/ (len(similar)))*100), 2)
    correct_ratio = round(((len(correct)/ (len(similar)))*100), 2)
    similar_refer1 = f'There are {len(similar)} cases that have similar predicted probability with your input in our data'
    similar_refer2 = f'{pay_ratio}% PAID dividend'
    similar_refer3 = f'The model would correctly identify dividend policy of {len(correct)} cases - ({correct_ratio}%)'
     
    if int(predict) == 0:
        if not_pay_prob < 90:
            predicition_statement = f'It is possible that the company will NOT PAY dividend for stockholders - Probability of NOT PAYING dividend: {round(not_pay_prob*100,2)}%'
        else:
            predicition_statement = f'It is likely that the company will NOT PAY dividend for stockholders - Probability of NOT PAYING dividend: {round(not_pay_prob*100,2)}%'
    else:
        if pay_prob < 90:
            predicition_statement = f'It is possible that the company will PAY dividend for stockholders - Probability of PAYING dividend: {round(pay_prob*100,2)}%'
        else:
            predicition_statement = f'It is likely that the company will PAY dividend for stockholders - Probability of PAYING dividend: {round(pay_prob*100,2)}%'
    
    predict_result = [predicition_statement, similar_refer1, similar_refer2, similar_refer3]
    return predict_result

# this is the main function in which we define our webpage  
def main():

    st.set_page_config(
    page_title="Predict your companies' dividend policy",
    page_icon=":mag:",
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
            >DIVIDEND POLICY PREDICTOR</
        h1>
        <h2 
            style ="
                font-family:'Baskerville ', serif;
                color:black;
                text-align:center;
                font-size: 1.6em
                "
            >Predict dividend policy by your own infomation</
        h2>
        <h2 
            style ="
                font-family:'Baskerville ', serif;
                color:black;
                text-align:left;
                font-size: 1.2em;
                font-weight:normal
                "
            >Give us some financial infomation below, we will do our best to predict the upcoming dividend policy!</
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

    # following lines create boxes in which user can enter data required to make prediction 

    Total_Assets = st.number_input("Total Assets (VND):")
    Current_Assets = st.number_input("Current Assets (VND):")
    Net_Intangibles_Asset = st.number_input("Net Intangibles Asset (VND):")
    Total_Liabilities = st.number_input("Total Liabilities (VND):")
    Current_Liabilities = st.number_input("Current Liabilities (VND):")
    Total_Equity = st.number_input("Total Equity (VND):")

    Total_Revenue = st.number_input("Total Revenue (VND):")
    Operating_Income = st.number_input("Operating Income (VND):")
    Net_Income_Before_Taxes = st.number_input("Net Income Before Taxes (EBT) (VND):")
    Net_Income = st.number_input("Net Income (VND):")
    
    Cash_from_Operating_Activities = st.number_input("Cash from Operating Activities (VND):")
    Cumulative_Net_Change_in_Cash = st.number_input("Cumulative Net Change in Cash (VND):")
    Free_Cash_Flow = st.number_input("Free Cash Flow (VND):")
    
    
    Retained_Earnings = st.number_input("Retained Earnings (VND):")
    Stock_Price = st.number_input("Stock Price (VND):")
    Total_Common_Stock = st.number_input("Total Common Stock:")
    
    Dividend_in_3_latest_year = st.radio("Have the companies paid dividend at least once in 3 latest years?: ",("Yes", "No"))

    
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        deploy_result = prediction(Net_Income, Total_Equity, Total_Revenue, Current_Assets, Current_Liabilities, Total_Liabilities, Total_Assets, 
                                   Stock_Price, Cash_from_Operating_Activities, Net_Intangibles_Asset, Total_Common_Stock, 
                                   Operating_Income, Net_Income_Before_Taxes, Cumulative_Net_Change_in_Cash, Retained_Earnings, Free_Cash_Flow, Dividend_in_3_latest_year) 
        st.success('{}'.format(deploy_result[0]))
        st.success('{}'.format(deploy_result[1]))
        st.success('{}'.format(deploy_result[2]))
        st.success('{}'.format(deploy_result[3]))
        print(deploy_result)
     
if __name__ =='__main__': 
    main()
