import json
import os
import sys

import streamlit as st

st.set_page_config(page_title='Bioimage Object Analysis Questions - BOAQ - Schema Definitions')

sys.path.append('..')
from bioimage_object_analysis_schema.utils import load_schema

json_q_dict = load_schema(from_master=True,rewrite_master=False)

"""
# Explanation of each of the question in the schema

Please note that questions and answers may be edited or removed in future versions of the schema. Last updated July 11th 2023
"""

for _,values in json_q_dict.items():
    st.write(f"## {values['full_name']}")
    st.write(f"  _{values['long_description']}_")
    st.write(f"  **Workflow step category**: {values['section']}")
    st.write(f"  **Current possible answers in the schema**: {' | '.join(list(values['options'].keys()))}")
