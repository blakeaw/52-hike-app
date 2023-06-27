import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


st.title("52 Hike Challenge Data App")

cs1, cs2, cs3 = st.columns(3)

# cs1.image("https://media.pagefly.io/file/get/52hiketm-final-medjpg-1546517799959.jpg",
#            width=100)
cs2.image("https://media.pagefly.io/file/get/52hiketm-final-medjpg-1546517799959.jpg",
          width=100)


# st.image("https://media.pagefly.io/file/get/52hiketm-final-medjpg-1546517799959.jpg",
#            width=100)

st.divider()

with st.expander("How To Use This App"):

    st.markdown("If it's not already open, open the Sidebar (little `>` in the top left corner) and input the sharing link for the Google Sheet with your hike data. The link should have the format:")
    st.markdown("`https://docs.google.com/spreadsheets/d/SHEETID/edit?usp=sharing`")
    st.markdown("Click the **Load Data** button.")
    st.markdown("##### Data Format")
    st.markdown("The Google Sheet is expected to have the following columns and formats:")
    df_sample = pd.DataFrame({'Hike #':[1],
                            'Location':['Cool Park'],
                            'Trail(s)':['Goat Alley'],
                            'Date':['01-01-2023'],
                            'Distance (mi)':[1.0],
                            'Elevation Gain (ft)':[100],
                            'Duration (minutes)':[60],
                            'Avg. Pace (minutes)':[60],
                            'Steps':[1000],
                            'Calories':[100],
                            'Active Zone Minutes':[10],
                            'AllTrails Rating':['Easy'],
                            'Season':['Winter']})
    st.dataframe(df_sample, hide_index=True)
    st.write(" ")
    st.markdown("If you update the Google Sheet you can click the **Load Data** button again in the sidebar.")


st.divider()

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
            if 'Hike #' not in df_hike.columns:
                hike_num = np.arange(len(df_hike)) + 1
                df_hike['Hike #'] = hike_num
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

    with st.expander("Data table"):
        st.write(df_hike)  

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
        if y in df_hike.columns:
            with st.expander(y):
                bar_stats(st, df_hike, x, y)

    cols_need = pd.Series(['Distance (mi)', 'Duration (minutes)', 'AllTrails Rating', 'Elevation Gain (ft)'])
    if cols_need.isin(df_hike.columns).all():
        with st.expander('Relplot - Duration vs. Distance - Rating and Elevation Gain'):
            #figp1 = sns.pairplot(df_hike.loc[:, 'Distance (mi)':], hue='AllTrails Rating')
            figp1 = sns.relplot(x='Distance (mi)', y='Duration (minutes)',
                                hue='AllTrails Rating', size='Elevation Gain (ft)',
                                alpha=0.5, palette="colorblind", data=df_hike)
            st.pyplot(figp1)
    
    cols_need = pd.Series(['Distance (mi)', 'Duration (minutes)', 'Season', 'Calories'])
    if cols_need.isin(df_hike.columns).all():            
        with st.expander('Relplot - Duration vs. Distance - Season and Calories'):
            #figp2 = sns.pairplot(df_hike.loc[:, 'Distance (mi)':], hue='Season')
            figp2 = sns.relplot(x='Distance (mi)', y='Duration (minutes)',
                        hue='Season', size='Calories',
                        alpha=0.5, palette="colorblind", data=df_hike)
            st.pyplot(figp2) 
    # with st.expander("Season Breakdown"):
    #     figp3 = sns.catplot(data=df_hike, y="Season", color='slategrey', kind='bar')       
    #     st.pyplot(figp3)    