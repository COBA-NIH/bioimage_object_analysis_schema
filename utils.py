import json
import os

import pandas
import streamlit as st

def load_schema(from_master = True, rewrite_master = False, master_file = 'jsons/master_schema.json', short_master_file = 'bioimage_object_analysis_questions.json'):
    if from_master:
        master_schema_dict = json.load(open(master_file))
    else:
        json_q_dict = {json.load(open(f"jsons/{x}"))['index']:json.load(open(f"jsons/{x}")) for x in os.listdir('jsons') if '.json' in x if 'master_schema' not in x}
        count_list = list(json_q_dict.keys()) 
        count_list = [x for x in count_list if x >= 0] #allow for dummy files with an index of -1
        count_list.sort()

        master_schema_dict = {}
        for eachcount in count_list:
            master_schema_dict[eachcount]=json_q_dict[eachcount]
        
        if rewrite_master == True:
            with open(master_file,'w') as mf:
                json.dump(master_schema_dict,mf)
            master_schema_short = {}
            for eachcount in count_list:
                question = json_q_dict[eachcount]
                master_schema_short[question['full_name']]=list(question['options'].keys())
                with open(short_master_file,'w') as mfs:
                    json.dump(master_schema_short,mfs)
            max_val = max([len(val) for val in master_schema_short.values()])
            short_schema_padded = {k:v+['']*(max_val - len(v)) for k,v in master_schema_short.items()}
            df = pandas.DataFrame(short_schema_padded)
            df.to_csv('bioimage_object_analysis_questions.csv',index=False)

    return master_schema_dict

def display_interactive_schema():
    st.write("# Tell us about your data")
    st.write("")
    st.write("please note that these questions are not finalized and questions and answers may be edited or removed. Last updated April 24th 2023")

    json_q_dict = load_schema(from_master=True,rewrite_master=False)
    count_list = count_list = list(json_q_dict.keys())

    setting_dict = {}

    section_start_text = {
        "0":"### Questions about your images that may affect preprocessing before segmentation happens",
        "9":"### Questions about your objects that may affect specific settings during segmentation",
        "18":"### Questions about which measurements must be made of your objects"
        }

    for eachcount in count_list:
        if eachcount in list(section_start_text.keys()):
            st.write(section_start_text[eachcount])
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
    return json_q_dict,setting_dict,is_3D
