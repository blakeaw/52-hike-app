import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

st.title("52 Hike Challenge Data App")

@st.cache_data
def load_gsheet(sharing):
    sheet_export = sheet_share.replace('/edit?usp=sharing', '/export?format=csv')
    df = pd.read_csv(sheet_export)
    return df

if "is_loaded" not in st.session_state:
    st.session_state.is_loaded = False
if "df_hike" not in st.session_state:
    st.session_state.df_hike = None

with st.sidebar:
    # Load the Google sheet with data into a pandas 
    # DataFrame. Adpated from Ken Arnold's answer at:
    # https://stackoverflow.com/questions/19611729/getting-google-spreadsheet-csv-into-a-pandas-dataframe
    st.header("Load Data from Google Sheet")
    sheet_share = st.text_input("Sheet Sharing Link: ")
    #tab_name = st.text_input("Tab Name: ")
    if st.button("Load Data"):
        try:
            df_hike = load_gsheet(sheet_share)
            st.session_state.is_loaded = True
            st.session_state.df_hike = df_hike            
        except:
            st.session_state.is_loaded = False
            st.session_state.df_hike = None 
            if sheet_share is None:
                st.write('Please provide a sharing link to the Google Sheet.')
            else:
                st.write('Unable to load the sheet. Make sure the link is correct or is accessible by everyone with the link.')  
#st.markdown('------')

def bar_stats(loc, df, x, y):
    figb, axb = plt.subplots()
    sns.barplot(df, x=x, y=y, ax=axb, color='slategrey')
    loc.write(y)
    avg = np.mean(df[y])
    max_val = np.max(df[y])
    min_val = np.min(df[y])
    loc.write("    Min: {:.2f}    Max: {:.2f}    Average {:.2f}".format(min_val, max_val, avg))
    loc.pyplot(figb)
    return

if st.session_state.is_loaded:
    df_hike = st.session_state.df_hike
    if st.checkbox("Show data table"):

        st.write(df_hike)                      
    n_hike = len(df_hike)
    t_ratio = '{}/52'.format(n_hike)
    #st.write(t_ratio)

    f_done = n_hike / 52
    f_remain = 1 - f_done
    sizes = [f_done, f_remain]
    labels = ['completed', 'remaining']
    # pie chart based circular progess bar adapted from
    # https://towardsdatascience.com/basics-of-donut-charts-with-pythons-matplotlib-100cf71b259d
    fig, ax = plt.subplots()
    #xv = np.ones(52)
    #ax.pie(xv, wedgeprops={'width':0.3, 'edgecolor':'k', 'linewidth':1})
    sizes = list()
    colors = list()
    for i in range(n_hike):
        sizes.append(1)
        colors.append('forestgreen')
    for i in range(52 - n_hike):
        sizes.append(1)
        colors.append('gainsboro')            
    ax.pie(sizes, #labels=labels,
           wedgeprops={'width':0.3, 'edgecolor':'k'},
           startangle=140,
           colors=colors)
    t_percent = '\n ------ \n {:.0f} %'.format(f_done*100)
    ax.text(0, -0.225, t_ratio + t_percent,
             fontsize='xx-large',
             color='white',
             ha='center')
    fig.set_facecolor('None')
    #fig.set_size_inches(2, 2)
    col1, col2, col3 = st.columns(3)
    col2.subheader("Progress")
    col2.pyplot(fig)
    st.markdown('------')
    if n_hike == 52:
        st.header("Congrats! You have completed the 52 Hike Challenge!")
        st.balloons()
        st.markdown('------')

    st.subheader("Hike Data and Stats")
    col1, col2 = st.columns(2)
    x = 'Hike #'
    expanded = ['Distance (mi)',
                'Duration (minutes)',
                'Elevation Gain (ft)',
                'Avg. Pace (minutes/mi)',
                'Calories', 
                'Active Zone Minutes']
    for y in expanded:
        with st.expander(y):
            bar_stats(st, df_hike, x, y)
    # with st.expander("Distance"):
    #     bar_stats(st, df_hike, x, 'Distance (mi)')
    # with st.expander("Duration"):
    #     bar_stats(st, df_hike, x, 'Duration (minutes)')
    # with st.expander("Elevation gain"):
    #         bar_stats(st, df_hike, x, 'Elevation Gain (ft)')
