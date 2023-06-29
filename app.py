import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# Set custom Page Configs.
st.set_page_config(
    page_title="52 Hike App",
    page_icon=":hiking_boot:",
    initial_sidebar_state="expanded",
    menu_items={
        "Report a Bug": "https://github.com/blakeaw/52-hike-app/issues",
    },
)

st.title("52 Hike Challenge Data App")

cs1, cs2, cs3 = st.columns(3)

cs1.image(
    "https://media.pagefly.io/file/get/52hiketm-final-medjpg-1546517799959.jpg",
    width=100,
)
# cs2.image("https://media.pagefly.io/file/get/52hiketm-final-medjpg-1546517799959.jpg",
#          width=100)
cs3.markdown(" A Streamlit web app by [@blakeaw](https://github.com/blakeaw)")

# st.image("https://media.pagefly.io/file/get/52hiketm-final-medjpg-1546517799959.jpg",
#            width=100)

st.markdown(
    "Welcome to my 52 Hike Challenge Data App powered by Streamlit. This app can load hike data from a Google Sheet via its sharing link. It will then highlight your progress, try to generate some graphs from data like the distance and duration, as well as highlight important 52 Hike Challenge milestones."
)
st.write(" ")
st.markdown(
    "Feel free to give it a try! You can see more detailed instructions in the **How To Use This App** dropdown below."
)
st.divider()

with st.expander("How To Use This App"):
    st.markdown(
        "If it's not already open, open the Sidebar (little `>` in the top left corner) and input the sharing link for the Google Sheet with your hike data. The link should have the format:"
    )
    st.markdown("`https://docs.google.com/spreadsheets/d/SHEETID/edit?usp=sharing`")
    st.markdown("Click the **Load Data** button.")
    st.markdown("##### Data Format")
    st.markdown("The Google Sheet may have the following columns and formats:")
    df_sample = pd.DataFrame(
        {
            "Hike #": [1],
            "Location": ["Cool Park"],
            "Trail(s)": ["Goat Alley"],
            "Date": ["01-01-2023"],
            "Distance (mi)": [1.0],
            "Elevation Gain (ft)": [100],
            "Duration (minutes)": [60],
            "Avg. Pace (minutes)": [60],
            "Steps": [1000],
            "Calories": [100],
            "Active Zone Minutes": [10],
            "AllTrails Rating": ["Easy"],
            "Season": ["Winter"],
        }
    )
    st.dataframe(df_sample, hide_index=True)
    st.write(" ")
    st.markdown(
        "However, your data doesn't neccesarily need to include all of these columns. For example, `Active Zone Minutes` is a Fitbit-specific metric that you won't have if you track your hikes with some other device or app. Plots will only be generated for those columns you include in your data's Google Sheet."
    )
    st.markdown(
        "You can include additional data columns in your Sheet. They just won't be used here in this app for plots."
    )
    st.write(" ")
    st.markdown("##### Update The Data")
    st.markdown(
        "If you update the Google Sheet you can click the **Load Data** button again in the sidebar to update the data here."
    )
    st.write(" ")
    st.markdown("##### Sample Data")
    st.markdown(
        "You can also try out the app using this sample Data Sheet: https://docs.google.com/spreadsheets/d/1xegpV0HuWQElmTdrAFjF2_Fcz2qxUo-QYucreuXXBcE/edit?usp=sharing"
    )

st.divider()


def load_gsheet(sharing):
    sheet_export = sheet_share.replace("/edit?usp=sharing", "/export?format=csv")
    df = pd.read_csv(sheet_export)
    return df


if "is_loaded" not in st.session_state:
    st.session_state.is_loaded = False
if "df_hike" not in st.session_state:
    st.session_state.df_hike = None
# if "has_changed" not in st.session_state:


with st.sidebar:
    # Load the Google sheet with data into a pandas
    # DataFrame. Adpated from Ken Arnold's answer at:
    # https://stackoverflow.com/questions/19611729/getting-google-spreadsheet-csv-into-a-pandas-dataframe
    st.header("Load Data from Google Sheet")
    sheet_share = st.text_input("Sheet Sharing Link: ")
    # tab_name = st.text_input("Tab Name: ")
    if st.button("Load Data"):
        try:
            df_hike = load_gsheet(sheet_share)
            if "Hike #" not in df_hike.columns:
                hike_num = np.arange(len(df_hike)) + 1
                df_hike["Hike #"] = hike_num
            st.session_state.is_loaded = True
            st.session_state.df_hike = df_hike
        except:
            st.session_state.is_loaded = False
            st.session_state.df_hike = None
            if sheet_share is None:
                st.warning("Please provide a sharing link to the Google Sheet.")
                st.stop()
            else:
                st.warning(
                    "Unable to load the sheet. Make sure the link is correct or is accessible by everyone with the link."
                )
                st.stop()
# st.markdown('------')


def bar_stats(loc, df, x, y):
    figb, axb = plt.subplots()
    sns.barplot(df, x=x, y=y, ax=axb, color="slategrey")
    loc.write(y)
    avg = np.mean(df[y])
    max_val = np.max(df[y])
    min_val = np.min(df[y])
    loc.write(
        "    Min: {:.2f}    Max: {:.2f}    Average {:.2f}".format(min_val, max_val, avg)
    )
    loc.pyplot(figb)
    return


milestones = [[1, 10], [11, 20], [21, 30], [31, 40], [41, 50], [51, 52]]

if st.session_state.is_loaded:
    df_hike = st.session_state.df_hike

    n_hike = len(df_hike)
    t_ratio = "{}/52".format(n_hike)
    # st.write(t_ratio)

    f_done = n_hike / 52
    f_remain = 1 - f_done
    sizes = [f_done, f_remain]
    labels = ["completed", "remaining"]
    # pie chart based circular progess bar adapted from
    # https://towardsdatascience.com/basics-of-donut-charts-with-pythons-matplotlib-100cf71b259d
    fig, ax = plt.subplots()
    # xv = np.ones(52)
    # ax.pie(xv, wedgeprops={'width':0.3, 'edgecolor':'k', 'linewidth':1})
    sizes = list()
    colors = list()
    for i in range(n_hike):
        sizes.append(1)
        colors.append("forestgreen")
    for i in range(52 - n_hike):
        sizes.append(1)
        colors.append("gainsboro")
    ax.pie(
        sizes,  # labels=labels,
        wedgeprops={"width": 0.3, "edgecolor": "k"},
        startangle=140,
        colors=colors,
    )
    t_percent = "\n ------ \n {:.0f} %".format(f_done * 100)
    ax.text(
        0, -0.225, t_ratio + t_percent, fontsize="xx-large", color="white", ha="center"
    )
    fig.set_facecolor("None")
    # fig.set_size_inches(2, 2)
    col1, col2, col3 = st.columns(3)
    col2.subheader("Progress")
    col2.pyplot(fig)
    st.markdown("------")
    if n_hike == 52:
        st.success(
            "Congrats! You have completed the 52 Hike Challenge! \n If you haven't already, you can fill out the Finisher Form at: https://www.52hikechallenge.com/pages/finisher-form"
        )
        st.balloons()
        # st.markdown("If you haven't already, you can fill out the Finisher Form at: https://www.52hikechallenge.com/pages/finisher-form")
        st.markdown("------")
    else:
        # Check other milestones
        n_mile = len(milestones)
        for i in range(n_mile - 1):
            mile_i = milestones[i]
            mile_i1 = milestones[i + 1]
            if (n_hike >= mile_i[1]) and (n_hike < mile_i1[1]):
                out_text = "Congrats! You have completed the HIKES {}-{} milestone. \n If you haven't already, you can submit your milestone check-in by email at: https://www.52hikechallenge.com/pages/hikes-check-in".format(
                    mile_i[0], mile_i[1]
                )
                st.success(out_text)
                # st.markdown("If you haven't already, you can submit your milestone check-in by email at: https://www.52hikechallenge.com/pages/hikes-check-in")
                st.markdown("------")

    with st.expander("Data table"):
        st.dataframe(df_hike, hide_index=True)

    st.subheader("Hike Data and Stats")
    col1, col2 = st.columns(2)
    x = "Hike #"
    expanded = [
        "Distance (mi)",
        "Duration (minutes)",
        "Elevation Gain (ft)",
        "Avg. Pace (minutes/mi)",
        "Calories",
        "Active Zone Minutes",
    ]
    for y in expanded:
        if y in df_hike.columns:
            with st.expander(y):
                bar_stats(st, df_hike, x, y)

    st.divider()
    st.write("Create a customizable relational plot")
    num_accept = [
        "Distance (mi)",
        "Elevation Gain (ft)",
        "Duration (minutes)",
        "Avg. Pace (minutes/mi)",
        "Steps",
        "Calories",
        "Active Zone Minutes",
    ]
    cat_accept = [
        "Surface Type",
        "AllTrails Rating",
        "Season",
    ]
    num_avail = list()
    for item in num_accept:
        if item in df_hike.columns:
            num_avail.append(item)
    cat_avail = list()
    for item in cat_accept:
        if item in df_hike.columns:
            cat_avail.append(item)

    with st.form("Relplot_form"):
        st.write("Required:")
        cr1, cr2 = st.columns(2)
        xvar = cr1.selectbox("Select an x-variable:", num_avail)
        yvar = cr2.selectbox("Select a y-value:", num_avail, index=1)
        st.write("Optional:")
        co1, co2 = st.columns(2)
        huevar = co1.selectbox(
            "Select a category for coloring data points:", [None] + cat_avail
        )
        sizevar = co2.selectbox(
            "Select a variable to set the size of data points:", [None] + num_avail
        )
        # Every form must have a submit button.
        submitted = st.form_submit_button("Generate")
        if submitted:
            figrp = sns.relplot(
                data=df_hike,
                x=xvar,
                y=yvar,
                size=sizevar,
                hue=huevar,
                alpha=0.5,
                palette="colorblind",
            )
            st.pyplot(figrp)
