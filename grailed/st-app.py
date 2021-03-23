import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import re
import time
import sys
import requests
import datefinder
import pickle
#selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
#bs4
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import streamlit as st
import altair as alt
import sel
import utils

DIRECTORY_PATH = r"C:\Users\ferdi\Downloads\projects\grailed"
FILE_PATH = "\supreme.csv" #edit
from pprint import pformat
#FUTURE PLANS:
#0: first thing to do after reading early docs: https://docs.streamlit.io/en/stable/tutorial/create_a_data_explorer_app.html

#1. github actions to automate changes?
#2. create cache where we store all past data and load in cache from user input (https://docs.streamlit.io/en/stable/api.html#streamlit.cache)
#3. long-term retention of testing the app: https://blog.streamlit.io/testing-streamlit-apps-using-seleniumbase/
#4. change theme and configuration through [theme] in https://docs.streamlit.io/en/stable/streamlit_configuration.html
#5. change plots that are in utils.

### TO DO:



## 1. ADD CATEGORIES SO CAN BE FILTERED, NEED TO BE SPLIT
######## INTRO AND HEADER ########

header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
    utils.img_to_bytes("header.jpg"))

st.markdown(header_html, unsafe_allow_html = True)

intro_markdown = utils.read_markdown_file("intro.md")

st.markdown(intro_markdown, unsafe_allow_html = True)

########### SIDE BAR ###############
st.sidebar.markdown("## Configuration")
st.sidebar.markdown("① ** What Listing or Brand to Analyze?**")
user_input = st.sidebar.text_input(label="Enter Product or Brand Name")
amount_scrape = st.sidebar.number_input(label = "Amount of Listings? (Integers Only!)")
#filters
st.sidebar.markdown("② **Apply Filters to Data**")
filter_options = ["Sold Only", "Unsold Only"]
help_list = ["Includes only listings that are sold", "Include only listings that are not sold"]
check_boxes = [st.sidebar.checkbox(option, key=option, help = help_option) for option,help_option in zip(filter_options, help_list)]
#disclaimer
st.sidebar.markdown("---")


#details
st.sidebar.markdown("ℹ️: ** Details **")
desc_check = st.sidebar.checkbox("Dataset Description")
desc_markdown = utils.read_markdown_file("data_description.md")
dict_check = st.sidebar.checkbox("Data Dictionary")
dict_markdown = utils.read_markdown_file("data_dictionary.md")

if desc_check:
    st.sidebar.markdown(desc_markdown, unsafe_allow_html=True)
if dict_check:
    st.sidebar.markdown(dict_markdown, unsafe_allow_html=True)
    st.sidebar.code(pformat(utils.colnames, indent=2))
st.sidebar.markdown("_")
#diosclaimer
st.sidebar.markdown(":warning: **Disclaimer:** The acceptable use policy for grailed.com [does not officially allow for web scrapers](https://www.grailed.com/acceptable). This app is purely for educational purposes to learn about underlying trends surrounding clothes.")
st.sidebar.markdown("*Please* use this app at your own discretion, especially for non-nefarious and non-profit purposes. ")


########## MAIN PAGE ##############
st.markdown("_")
faq = st.beta_expander("FAQ:")
faq_md = utils.read_markdown_file("faq.md")
faq.markdown(faq_md, unsafe_allow_html = True)
latest_iteration = st.empty()
st.markdown("\n")
st.markdown("\n")
col1, col2, col3 = st.beta_columns([1,1,1])

if check_boxes[0] and check_boxes[1]:
    st.header("** &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp&nbsp;&nbsp;&nbsp;Please check only one filter at a time!**")

elif len(user_input) > 0 and amount_scrape > 0 and amount_scrape < 500 and amount_scrape.is_integer():

    col1.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp; &nbsp;     :link:")
    #col3.write(":o:")
    st.markdown("\n")
    if col2.button("Click Here to Get Data!"):
        latest_iteration = st.empty()
        latest_iteration.markdown('Initiating Scraping... (this may take awhile so go ahead and get a snack :cookie:)')
        bar = st.progress(1)

        #scrape
        if check_boxes[0]:
            sold_df = sel.scrape_filter_sold(user_input, amount_scrape)
        elif check_boxes[1]:
            unsold_df = sel.scrape(user_input, amount_scrape)
        else:
            unsold_df = sel.scrape(user_input, amount_scrape)
            sold_df = sel.scrape_filter_sold(user_input, amount_scrape)

        for i in range(1, 100):
          latest_iteration.text(f'Getting data... {i+1}%')
          bar.progress(i + 1)
          time.sleep(.01)

        if not check_boxes[0] and not check_boxes[1]:
            #merge
            merged_df = sel.merge_df(user_input, unsold_df, sold_df)
            merge_iteration = st.empty()
            merge_bar = st.progress(0)

            for i in range(100):
              # Update the progress bar with each iteration.
              merge_iteration.text(f'Merging data... {i+1}%')
              merge_bar.progress(i + 1)
              time.sleep(.01)
            st.success("Data Retrieved!")

            first_listing_link = list(merged_df['Link'])[0]
            utils.display_picture(first_listing_link, 500, 400, False)

            st.subheader("Dataframe:")
            st.write(merged_df)

        elif check_boxes[0]:
            st.success("Data Retrieved!")

            first_listing_link = list(sold_df['Link'])[0]
            utils.display_picture(first_listing_link, 500, 400, True)

            st.subheader("Dataframe:")
            st.write(sold_df)
        else:
            st.success("Data Retrieved!")

            first_listing_link = list(unsold_df['Link'])[0]
            utils.display_picture(first_listing_link, 500, 400, False)

            st.subheader("Dataframe:")
            st.write(unsold_df)
