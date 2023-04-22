import json
import os


def load_schema(from_master = True, rewrite_master = False, master_file = 'master_schema.json', short_master_file = 'master_schema_short.json'):
    if from_master:
        master_schema_dict = json.load(open(master_file))
    else:
        json_q_dict = {json.load(open(x))['index']:json.load(open(x)) for x in os.listdir('.') if '.json' in x if 'master_schema' not in x}
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

    return master_schema_dict

