import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

st.title("52 Hike Challenge Data App")

df = None
with st.sidebar:
    # Load the Google sheet with data into a pandas 
    # DataFrame. Adpated from Ken Arnold's answer at:
    # https://stackoverflow.com/questions/19611729/getting-google-spreadsheet-csv-into-a-pandas-dataframe
    st.header("Load Data from Google Sheet")
    sheet_share = st.text_input("Sheet Sharing Link: ")
    #tab_name = st.text_input("Tab Name: ")
    if st.button("Load Data"):
        try:
            sheet_export = sheet_share.replace('/edit?usp=sharing', '/export?format=csv')
            df = pd.read_csv(sheet_export)
        except:
            if sheet_share is None:
                st.write('Please provide a sharing link to the Google Sheet.')
            else:
                st.write('Unable to load the sheet. Make sure the link is correct or is accessible by everyone with the link.')  

if df is not None:
    st.write(df)                      