import json
from collections import defaultdict
import re
from tqdm import tqdm
import os
import string
import argparse

def span2bio(input_dir, output_dir):
    punctuation = ",.\"!?:'"
    sentence_dic = defaultdict(list)
    f_write=open(output_dir,"w")
    
    file = open('input_dir', 'r')
    js = file.read()
    dic = json.loads(js)
    data_length = (len(dic))
    context_len = 0
    for i in range(data_length):
        data = dic[i]
        context = data['new_data']
        label = data['Label']
        new_label={}
        for p in punctuation:
            context = context.replace(p, " "+p)
        context = context.split(' ')
        context_len += len(context)
        for idx in (context):
            idx = idx.replace('\n','')

            for key in label.keys():
                key1 = key.split(' ')
                if len(key1)>=2:
                    count = 0
                # print(label[key])
                    for idy in key1:
                        if count == 0:
                            new_label[idy.lower()] = 'B-'+label[key]
                        else:
                            new_label[idy.lower()] = 'I-'+label[key]
                        count += 1
                else:
                    for idy in key1:
                        new_label[idy.lower()] = 'B-'+label[key]

            # print(new_label)

            if idx.lower() in new_label.keys():
                if 'B-' not in new_label[idx.lower()]:
                    if pre_label != 'O':
                        f_write.write(idx+" "+new_label[idx.lower()]+'\n')
                        pre_label = new_label[idx.lower()]
                    if pre_label == 'O':
                        pass
                elif 'B-' in new_label[idx.lower()]:
                    pre_label = 'B-'
                    f_write.write(idx+" "+new_label[idx.lower()]+'\n')
                    pre_label = new_label[idx.lower()]

            elif idx != '\n' and idx != ' ':
                f_write.write(idx+" "+'O'+'\n')
                pre_label = 'O'

        f_write.write('\n')

    print("句子平均长度:", context_len/data_length)  
    
span2bio(input_dir, output_dir)


