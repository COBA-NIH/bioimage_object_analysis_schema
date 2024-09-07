import json
import os
import sys

import streamlit as st

sys.path.append('..')
from bioimage_object_analysis_schema.utils import display_interactive_schema


json_q_dict,setting_dict,is_3D = display_interactive_schema()

def follow_answer_tree(json_q_dict,eachkey,setting_dict,is_3D):
    if json_q_dict[eachkey]["changes_based_on_3d"]:
        if type(setting_dict[eachkey]) == list:
            for eachsubkey in setting_dict[eachkey]:
                answer = json_q_dict[eachkey]['options'][eachsubkey]["cellprofiler_suggester"][f"3D_{is_3D}"]
                if answer:#just don't show anything if we haven't written the rec yet
                    st.write(answer)
        else:
            answer = json_q_dict[eachkey]['options'][setting_dict[eachkey]]["cellprofiler_suggester"][f"3D_{is_3D}"]
            if answer: #just don't show anything if we haven't written the rec yet
                st.write(answer)              

    else:
        if type(setting_dict[eachkey]) == list:
            for eachsubkey in setting_dict[eachkey]:
                answer = json_q_dict[eachkey]['options'][eachsubkey]["cellprofiler_suggester"]
                if answer:#just don't show anything if we haven't written the rec yet
                    st.write(answer)
        else:
            answer = json_q_dict[eachkey]['options'][setting_dict[eachkey]]["cellprofiler_suggester"]
            if answer: #just don't show anything if we haven't written the rec yet
                st.write(answer)   

"""
# CellProfiler pipeline recommendations

See below for pipeline suggestions based on the answers to your questions. Note that some "best-case-scenario answers" where therefore no special handling is needed will not generate suggestions, so the number of suggestions may not match the number of questions.

Last updated July 11 2023
"""

"""
## CellProfiler pipeline recommendations - image preprocessing
"""
for eachkey in setting_dict.keys():
    if json_q_dict[eachkey]["section"] == 'image':
        follow_answer_tree(json_q_dict,eachkey,setting_dict,is_3D)

"""
## CellProfiler pipeline recommendations - object specifications
"""

for eachkey in setting_dict.keys():
    if json_q_dict[eachkey]["section"] == 'object':
        follow_answer_tree(json_q_dict,eachkey,setting_dict,is_3D)


"""
## CellProfiler pipeline recommendations - measurement specifications
"""

for eachkey in setting_dict.keys():
    if json_q_dict[eachkey]["section"] == 'measurement':
        follow_answer_tree(json_q_dict,eachkey,setting_dict,is_3D)
    
