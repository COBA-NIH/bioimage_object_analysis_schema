import pandas
import streamlit as st

q_dataframe = pandas.read_csv('bioimage_object_analysis_schema.csv')
q_questions = list(q_dataframe.columns)

with st.form(key='this_form'):
    for question in range(len(q_questions)):
        if 'all that apply' in q_questions[question]:
            globals()[f'option_{question}'] = st.multiselect(q_questions[question],q_dataframe[q_questions[question]].dropna())
        else:
            globals()[f'option_{question}'] = st.selectbox(q_questions[question],q_dataframe[q_questions[question]].dropna())

    submit_button = st.form_submit_button(label='Submit')

## TODO - rather than this lazy globals thing, make a nice dict, and use it above and below, so that we don't care when numbers change
## So that we aren't super sensitive to exact phrasing, think of using a fuzzy match or a unique string in

answer_dict = {
    0:{
    'Brightfield - unstained': "You said you're using unstained brightfield images. Consider using ilastik to create pseudo-fluorescent images or a tool like Cellpose for segmentation\
        otherwise try the 'EnhanceOrSuppressFeatures' module in 'Texture' mode",
    'Brightfield - histology stained': "You said you're using histologically stained images. You likely want to use the UnmixColors module to create pseudo-fluorescent images.",
    'Fluorescence':"You said you're using fluorescence images. This is CellProfiler's default mode and no special behavior is needed."
    },
    1:{
    'Yes': 'You said your images are 3D. Please make sure to select this in the NamesAndTypes module',
    'No': 'You said your images are 2D. Please make sure to select this in the NamesAndTypes module'
    },
    }


"""
# CellProfiler pipeline recommendations
"""

"""
## CellProfiler pipeline recommendations - image preprocessing
"""

answer_dict[1][option_1]
answer_dict[0][option_0]

"""
## CellProfiler pipeline recommendations - object specifications
"""

"""
## CellProfiler pipeline recommendations - measurement specifications
"""
