import streamlit as st
import streamlit.components.v1 as components

# Include Google Analytics tracking code
with open("../google_analytics.html", "r") as f:
    html_code = f.read()
    components.html(html_code, height=0)

st.image('figure.png')
