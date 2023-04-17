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

for question in range(len(q_questions)):
    st.write(globals()[f'option_{question}'])