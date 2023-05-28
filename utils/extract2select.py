import json
from collections import defaultdict
import re
from tqdm import tqdm
import os
import random
import argparse

# Twitter labels
label_map = {"LOC": "Loction", "ORG": "Organization", "PER": "Person", "OTHER": "Other"}
label = "\n Location\n Person\n Organization\n Other\n Non-entity"
label_list = ['PER', 'LOC', 'OTHER', 'ORG', 'Non']

def ext2sel(input_dir, output_dir):
    sentence_dic = defaultdict(list)

    file = open(input_dir, 'r')
    js = file.read()
    dic = json.loads(js)
    data_length = (len(dic))
    context_len = 0
    all_datas = []

    for i in range(data_length):
        data = dic[i]
        context = data['context']
        label = data['Label']
        for idx in label.keys():
            query = "<Context>:" + context + "\n Select the entity type of "+str(idx)+" in this context, and only need to output the entity type."
            answer = "\nAnswer:" + label_map[label[idx]]
            example ={
                "question": query,
                "answer": answer
                }
            all_datas.append(example)

    with open(output_dir, "w") as f:
        json.dump(all_datas, f, ensure_ascii=False, indent=2)
        
def sample_example(dic, shot):
    data_length = (len(dic))
    example = []
    
    count = 0
    if shot<=0:
        return []
    else:
        set_example = (len(label_list) - 1)

    for i in range (shot):
        label = []
        while len(label)<set_example:
            idx = random.randint(0,data_length)
            data = dic[idx]
            if data['answer'] not in label:
                count += 1
                example.append("Example"+":\n"+data['question']+data['answer']+"\n")
                label.append(data['answer'])
            else:
                pass
    return("".join(example))

ext2sel("", "")

file = open("twitter/select.dev", 'r')
js = file.read()
dic = json.loads(js)
shot = 1

print(sample_example(dic, shot))
