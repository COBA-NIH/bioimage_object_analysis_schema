"""
Pages
- One with nice expanded answers - done
- Generic interactive page - done, but would be nice to load saved jsons
- Recommender pages - 
-- CellProfiler - done
- one with chart (charts.py) - TODO
-- mermaid chart maybe? 
-- https://docs.bokeh.org/en/latest/docs/examples/topics/categorical/periodic.html
-- just matplotlib sub-charts (https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subfigures.html) with text boxes(https://matplotlib.org/stable/gallery/text_labels_and_annotations/fancytextbox_demo.html#sphx-glr-gallery-text-labels-and-annotations-fancytextbox-demo-py)), 

It's all just tiny text files so it should be fine, but if need to cache- https://docs.streamlit.io/library/api-reference/performance/st.cache_data
Embedded in a webpage at BOAQ.org, thanks to https://giswqs.medium.com/add-a-custom-domain-to-your-streamlit-web-app-daed6d11dd72
"""

"""
# Welcome to the home page for the "Twenty Questions of Bioimage Object Analysis" project!

This schema is currently under develeopment; stay tuned for more updates.
Previous versions of this schema are currently best found on [Zenodo](https://doi.org/10.5281/zenodo.7654937)

Last updated - April 24, 2023

Made by Beth Cimini, Broad Institute, 2023, as part of the Center for Open Bioimage Analysis

[Check out this app's source on GitHub](https://github.com/COBA-NIH/bioimage_object_analysis_schema)
"""
import json
import streamlit as st

from utils import load_schema,make_fig

load_schema(from_master=False,rewrite_master=True)

st.write(json.load(open('bioimage_object_analysis_questions.json')))

st.download_button('Download these questions and answers as a json file',open('bioimage_object_analysis_questions.json'),'bioimage_object_analysis_questions.json')
st.download_button('Download these questions and answers as a csv file',open('bioimage_object_analysis_questions.csv'),'bioimage_object_analysis_questions.csv')

make_fig()

st.image('figure.png')