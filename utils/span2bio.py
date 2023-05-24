import json
from collections import defaultdict
import re
from tqdm import tqdm
import os
import string
import argparse

def BIO(input_file, output_file):
    with open(input_file,'r') as in_file:
        fins = in_file.readlines()
    fout = open(output_file,'w')
    words = []
    labels = []
    for line in fins:
        if len(line) < 3:
            sent_len = len(words)
            for idx in range(sent_len):
                if "I-" in labels[idx]:
                    label_type = labels[idx].split('-')[-1]
                    if (idx == 0) or (labels[idx-1] == "O") or (label_type != labels[idx-1].split('-')[-1]):
                        fout.write(words[idx]+" B-"+label_type+"\n")
                    else:
                        fout.write(words[idx]+" "+labels[idx]+"\n")
                else:
                    fout.write(words[idx]+" "+labels[idx]+"\n")
            fout.write('\n')
            words = []
            labels = []
        else:
            pair = line.strip('\n').split()
            words.append(pair[0])
            labels.append(pair[-1].upper())
    fout.close()
    print("BIO file generated:", output_file)

punctuation = ",.\"!?:'"
sentence_dic = defaultdict(list)
f_write=open("bio_newData.train","w")

# with tqdm(total = os.path.getsize('new_data.train')) as pbar:
#     with open('new_data.train', 'r') as f:
#         for line in f.readlines():
#             line = line.strip('\n') 
#             print(line)     
#             if "new_data" in line:
                
#                 sentence_dic[new_data] = 
            
            
#             pbar.update(len(line)) 
#             pass
file = open('new_data.train', 'r')
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
        #     print(label[key])
        # print(data['Label'])
    
    # print(idx['new_data'])


