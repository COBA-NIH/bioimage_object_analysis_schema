"""
Can plan to do this multipage - https://docs.streamlit.io/library/get-started/multipage-apps
- one with chart (charts.py), 
- one with nice expanded answers 
-- mermaid chart maybe? 
-- https://docs.bokeh.org/en/latest/docs/examples/topics/categorical/periodic.html
-- just matplotlib sub-charts (https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subfigures.html) with text boxes(https://matplotlib.org/stable/gallery/text_labels_and_annotations/fancytextbox_demo.html#sphx-glr-gallery-text-labels-and-annotations-fancytextbox-demo-py)), 
- one with CellProfiler suggestions.
Need also a util data loader function, pull all the jsons and put them into (likely a few) master dicts with the right components
It's all just tiny text files so it should be fine, but https://docs.streamlit.io/library/api-reference/performance/st.cache_data
Embed in webpage rather than webpage forwarding - https://giswqs.medium.com/add-a-custom-domain-to-your-streamlit-web-app-daed6d11dd72
"""

"""
# Welcome to the home page for the "Twenty Questions of Bioimage Object Analysis" project!

This is the part of the schema currently loaded into our "CellProfiler Suggester" tool; stay tuned for more updates.

Last updated - April 22, 2023

Made by Beth Cimini, Broad Institute
"""
import json
import streamlit as st

st.write(json.load(open('jsons/master_schema_short.json')))