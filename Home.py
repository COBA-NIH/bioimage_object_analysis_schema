"""
It's all just tiny text files so it should be fine, but if need to cache- https://docs.streamlit.io/library/api-reference/performance/st.cache_data
v1 was Embedded in a webpage at BOAQ.org, thanks to https://giswqs.medium.com/add-a-custom-domain-to-your-streamlit-web-app-daed6d11dd72

Current analytics approach thanks to https://discuss.streamlit.io/t/google-analytics-integration/41412/2
"""
import streamlit as st
import streamlit.components.v1 as components

# Include Google Analytics tracking code
with open("google_analytics.html", "r") as f:
    html_code = f.read()
    components.html(html_code, height=0)

st.set_page_config(layout='wide')

"""
# Welcome to the home page for the "Twenty Questions of Bioimage Object Analysis" project!

This website is associated with the paper "The Twenty Questions of Bioimage Object Analysis" by Beth A. Cimini and Kevin W. Eliceiri, available at Nature Methods [here](https://rdcu.be/dgAYI).

This schema is currently under development; stay tuned for more updates.
Previous versions of this schema are currently best found on [Zenodo](https://doi.org/10.5281/zenodo.7654937)

Last updated - September 7, 2024

App made by Beth Cimini, Broad Institute, 2023, as part of the Center for Open Bioimage Analysis

[Check out this app's source on GitHub](https://github.com/COBA-NIH/bioimage_object_analysis_schema)

[![DOI](https://zenodo.org/badge/629135528.svg)](https://zenodo.org/badge/latestdoi/629135528) (Source code DOI)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7654937.svg)](https://doi.org/10.5281/zenodo.7654937) (Original schema DOI)
"""
import json

from utils import load_schema

load_schema(from_master=True,rewrite_master=False)

st.write(json.load(open('bioimage_object_analysis_questions.json')))

st.download_button('Download these questions and answers as a json file',open('bioimage_object_analysis_questions.json'),'bioimage_object_analysis_questions.json')
st.download_button('Download these questions and answers as a csv file',open('bioimage_object_analysis_questions.csv'),'bioimage_object_analysis_questions.csv')
