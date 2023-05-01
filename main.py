import streamlit as st
import pandas as pd

header = st.container()
dataset = st.container()
distribution = st.container()
top_companies = st.container()


with header:
    st.title("Web Scraping Project")
    st.write("In a nutshell, web scraping is the process of extracting data from websites. In this project I am scraping the UK job list dataset.")

with dataset:
    st.header("UK Job List Dataset")
    st.write("The UK Job List Dataset can be found [here](https://docs.google.com/spreadsheets/d/1ZaLWbzOeFXAJWte6p8pPy745KLyAH0RCA1YgGgNrto0/htmlview#).")

    with open("datafile.py") as f:
        exec(f.read())

    if 'jobs' not in st.session_state:
            st.session_state.jobs = get_data()
    st.write(st.session_state.jobs.head())


with distribution:
    st.header("Distribution of Data")
    st.write("The bar chart given below shows the top 10 items in each category. Select a category from the dropdown list.")
    col_name = st.selectbox("Which column distribution would you like to explore?", options = ['City', 'County', 'Type', 'Route'])
    dist = pd.DataFrame(st.session_state.jobs[col_name].value_counts())
    st.write("Number of elements:", len(dist))
    st.bar_chart(dist[:10], height=500)


with top_companies:
    st.header("List of companies")

    st.write("Below you can filter companies based on the top values in each category.")
    sel_col, disp_col = st.columns(2)
    with sel_col:
        city = st.selectbox("Select City", options = st.session_state.jobs['City'].value_counts().index.tolist()[:10])
        route = st.selectbox("Select Route", options = st.session_state.jobs['Route'].value_counts().index.tolist()[:6])
        type = st.selectbox("Select Type", options = st.session_state.jobs['Type'].value_counts().index.tolist()[:5])


    with disp_col:
        df_companies = st.session_state.jobs.loc[(st.session_state.jobs['City'] == city) & (st.session_state.jobs['Route'] == route) & (st.session_state.jobs['Type']== type)]
        st.text("No of companies that satisfy given criteria:")
        st.write(len(df_companies))
        st.write(df_companies['Company'])
