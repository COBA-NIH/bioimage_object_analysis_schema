import json
import os

import pandas

def load_schema(from_master = True, rewrite_master = False, master_file = 'jsons/master_schema.json', short_master_file = 'jsons/master_schema_short.json'):
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

