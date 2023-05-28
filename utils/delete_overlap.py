import json
import os
import re
import time
# import openai
from tqdm import tqdm
import numpy as np
import operator

def check_fun(check_list, pr):

    if len(check_list) < 1:
        return False
    if len(check_list) == 1:
        return []
    a_list = sorted(check_list, key=lambda l: l[0])
    delet_index = []
    
    for i in range(0, len(a_list)-1):
        if a_list[i+1][0] <= a_list[i][1]:
            # print((str(a_list[i]), str(a_list[i+1])))
            a_list[i] = [ int(x) for x in a_list[i] ]
            a_list[i+1] = [ int(x) for x in a_list[i+1] ]

            delet_index.append((a_list[i]) if pr[i+1] >= pr[i] else (a_list[i+1]))
            # print((str(pr[i]), str(pr[i+1])))
            
    return delet_index

def save_res(result):
    file = open("detele_overlapUn0.1.txt", "a+")
    for data in result:
        line = ' '.join(data) + '\n'
        file.write(line)

label = "\n Location\n Person\n Organization\n Miscellaneous\n Non-entity"
label_list = ['LOC','PER','ORG','Non']

def link(result):
    probs = []
    overlap_index = []
    new_results = []
    trup_sent = len(result)
    if trup_sent > 1:
        context = result[0]
        new_results.append(context)
        for idx in(result[1:]):
            if '<Context>' not in idx[0]:
                idx = idx[0].split(' ')
                sidx, eidx = idx[-8].split(',')
                x = [int(sidx),int(eidx)] 
                pr = float(idx[-4])
                probs.append([pr])
                overlap_index.append(x)
                
        delet_index=(check_fun(overlap_index, probs))
                # print(delet_index)
                
        for idx in(result[1:]):
            if '<Context>' not in idx[0]:
                idx = idx[0].split(' ')
                sidx, eidx = idx[-8].split(',')
                
                if delet_index == []:
                    new_results.append(idx)
                elif [int(sidx), int(eidx)] != delet_index[0]:
                    new_results.append(idx)
        
        save_res(new_results)
    else:
        save_res(result)

def main(file_dir):

    stage2_result = []
    # Open the file in read mode
    with open(file_dir, 'r') as f:
        unc_count, pos_count = 0., 0.
        TP, TPC, TLC = 0, 0, 0
        count = 0
        for line in f.readlines():
            line = line.strip('\t\n')
            line = str(line)
            sentence = re.split(':: |\t|"', line)
            
            ## 判断是否是句子，[]
            if '<Context>' in line:
                count += 1
                if count > 1:
                    link(stage2_result)
                    stage2_result = []
                    stage2_result.append(sentence)

                else:
                    stage2_result.append(sentence)
            else:
                stage2_result.append(sentence) 
        link(stage2_result)
           

main('')
