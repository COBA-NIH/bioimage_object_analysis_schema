import json
import os
import sys

import streamlit as st

sys.path.append('..')
from bioimage_object_analysis_schema.utils import load_schema


"""
# Tell us about your data

(please note that not all questions are added yet. Stay tuned! Last updated April 22nd 2023)
"""

json_q_dict = load_schema(from_master=True,rewrite_master=False)
count_list = count_list = list(json_q_dict.keys())

setting_dict = {}

for eachcount in count_list:
    question = json_q_dict[eachcount]
    if question["short_name"]=='3D': #some answers will be different in 2D vs 3D
        is_3D_question = eachcount
    if question['select_all']:
        setting_dict[eachcount] = st.multiselect(question['full_name'],list(question['options'].keys()),
                                                 help=question['long_description'])
    elif question['slider']:
        setting_dict[eachcount] = st.select_slider(question['full_name'],list(question['options'].keys()),
                                                   value=list(question['options'].keys())[question["default_option_index"]],
                                                   help=question['long_description'])
    else:
        setting_dict[eachcount] = st.selectbox(question['full_name'],list(question['options'].keys()),
                                               index=question["default_option_index"],
                                               help=question['long_description'])

is_3D = setting_dict[is_3D_question] == "Yes"

by_name_dict = {json_q_dict[x]['full_name']:setting_dict[x] for x in count_list}
st.download_button('Download my answers as a json file',json.dumps(by_name_dict),'dataset_description.json')

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

(please note that not all question combinations have recommendations yet. Stay tuned! Last updated April 22nd 2023)
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
    
