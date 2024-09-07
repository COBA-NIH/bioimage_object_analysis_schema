import json
import os
import sys

import streamlit as st
import streamlit.components.v1 as components

# Include Google Analytics tracking code
with open("../google_analytics.html", "r") as f:
    html_code = f.read()
    components.html(html_code, height=0)

sys.path.append('..')
from bioimage_object_analysis_schema.utils import display_interactive_schema


json_q_dict,setting_dict,is_3D = display_interactive_schema()
