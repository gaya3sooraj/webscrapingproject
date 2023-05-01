import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np



def get_data():
    #Create a URL object
    url = 'https://docs.google.com/spreadsheets/d/1ZaLWbzOeFXAJWte6p8pPy745KLyAH0RCA1YgGgNrto0/htmlview#'
    st.write("\nIt's going to take a few seconds. Please hang in there...")
    st.markdown(f'<p style="color:#008000;">{"Data scraping request sent..."}</p>', unsafe_allow_html=True)
    #Create object page
    page = requests.get(url)
    #parser-lxml = Change html to Python friendly format
    #Obtain page's information
    st.markdown(f'<p style="color:#008000;">{"Request granted!Extracting data from url..."}</p>', unsafe_allow_html=True)

    soup = BeautifulSoup(page.text, "html.parser")
    #Find previous element with id
    prev = soup.find('div',{'id':'1637882187'})
    table_element = prev.find_next('table')
    #Create list
    table_data=[]
    #Skip first row that contains column reference
    for t in table_element.find_all('tr')[1:]:
        data = t.find_all('td')
        table_row=[]
        for d in data[:5]:
            table_row.append(d.text)
        table_data.append(table_row)

    col = ['Company', 'City', 'County', 'Type', 'Route']
    jobs = pd.DataFrame(table_data[2:], columns=col)
    #Assign empty cells with Nan
    jobs = jobs.apply(lambda x: x.str.strip()).replace('', np.nan)
    #Remove empty rows
    jobs = jobs.dropna(how='all')
    #Normalise Town/city column
    #Convert to lowercase
    jobs['City'] = jobs['City'].str.lower()
    #Remove special characters
    jobs['City'] = jobs['City'].str.replace('\W', ' ')
    st.markdown(f'<p style="color:#008000;">{"Data successfully extracted and cleaned..."}</p>', unsafe_allow_html=True)
    return jobs
