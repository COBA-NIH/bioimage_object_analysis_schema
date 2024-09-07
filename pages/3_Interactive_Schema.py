import json
import os
import sys

import streamlit as st

st.set_page_config(page_title='Bioimage Object Analysis Questions - BOAQ')

sys.path.append('..')
from bioimage_object_analysis_schema.utils import display_interactive_schema


json_q_dict,setting_dict,is_3D = display_interactive_schema()