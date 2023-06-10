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
    st.write("#### When analyzing multiple kinds of objects, these set of questions should be independently answered for each object to be segmented.")
    st.write("")
    st.write("Please note that questions and answers may be edited or removed in future versions of the schema. Last updated June 10th 2023")

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

def make_fig():
    # much of this stolen from https://github.com/mwaskom/seaborn/blob/bf0cfec0627bee4b757f033ff504c0a520a3cd5b/doc/sphinxext/tutorial_builder.py#L130
    # subplot wrapping from https://gist.github.com/dneuman/90af7551c258733954e3b1d1c17698fe
    import json
    import matplotlib as mpl
    import matplotlib.text as mtext
    from matplotlib.patches import FancyBboxPatch
    import matplotlib.pyplot as plt
    import seaborn as sns

    qs=json.load(open('jsons/master_schema.json'))
    categories = ['Measurement','Object','Image']

    dict_for_plotting = {'Question':[x['full_name'] for x in qs.values()],
                        'Category':[x['section'].title() for x in qs.values()],
                        'Answers':[list(x['options'].keys()) for x in qs.values()],
                        }
    class WrapText(mtext.Text):
        """
        WrapText(x, y, s, width, widthcoords, **kwargs)
        x, y       : position (default transData)
        text       : string
        width      : box width
        widthcoords: coordinate system (default screen pixels)
        **kwargs   : sent to matplotlib.text.Text
        Return     : matplotlib.text.Text artist
        """
        def __init__(self,
                    x=0, y=0, text='',
                    width=0,
                    widthcoords=None,
                    **kwargs):
            mtext.Text.__init__(self,
                    x=x, y=y, text=text,
                    wrap=True,
                    clip_on=False,
                    **kwargs)
            if not widthcoords:
                self.width = width
            else:
                self.width = widthcoords.transform_point((width,0))[0]

        def _get_wrap_line_width(self):
            return self.width

    mpl.rcParams['figure.subplot.wspace']=mpl.rcParams['figure.subplot.hspace']=0.001
    fig = plt.figure(figsize=[10,12],dpi=300)
    with sns.axes_style("white"):
        axes = fig.subplots(ncols=4,nrows=5,sharex=True,sharey=True)
    deep = sns.color_palette("colorblind")
    colors ={"Image":deep[0], "Object":deep[1], "Measurement":deep[2]}
    dark = sns.color_palette("dark")
    text_colors = {"Image":dark[0], "Object":dark[1], "Measurement":dark[2]}
    pad = 0.04
    for eachq in range(20):
        x = eachq %4
        y = int(eachq /4)
        color = colors[dict_for_plotting['Category'][eachq]]+(.25,)
        text_color = text_colors[dict_for_plotting['Category'][eachq]]
        ax = axes[y][x]
        ax.set_axis_off()
        ax.set(xlim=(0, 1), ylim=(0, 1))
        ax.add_artist(FancyBboxPatch(
            (0.05, 0.78), 0.89, 0.15, f"round,pad={pad}",
            linewidth=1, edgecolor=text_color, facecolor=color,
        ))
        wtxt = WrapText(
            0.5, 0.85, f"{eachq+1}) {dict_for_plotting['Question'][eachq]}",width=550, widthcoords=None,
            ha="center", va='center',ma="center", size=7, color=text_color
        )
        ax.add_artist(wtxt)
        answers = dict_for_plotting['Answers'][eachq]
        pad2 = 0.01
        h = (0.72-(3*pad2*len(answers)))/(len(answers))
        color2 = colors[dict_for_plotting['Category'][eachq]]+(.15,)
        for eachanswer in range(len(answers)):
            y = 0.75-((h+(3*pad2))*(eachanswer+1))
            ax.add_artist(FancyBboxPatch(
            (0.1, y), 0.8, h, f"round,pad={pad2}",
            linewidth=1, edgecolor=text_color, facecolor=color2,))
            wtxt = WrapText(
            0.5, y+(0.5*h), f"{answers[eachanswer]}",width=430, widthcoords=None,
            ha="center", va='center',ma="center", size=7, color=text_color,linespacing=1)
            ax.add_artist(wtxt)
    plt.savefig('figure.png',dpi=300,bbox_inches='tight')

#on import of this, which will be on app reboot/rebuild, remake everything to ensure stuff is up to date
load_schema(from_master=False,rewrite_master=True)
make_fig()