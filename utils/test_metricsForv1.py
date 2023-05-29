import json
import os
import re
import time
# import openai
from tqdm import tqdm

def save_res(result):
    file = open("ori_results_unc0.1.txt", "a+")
    for data in result:
        line = ' '.join(data) + '\n'
        file.write(line)

label = "\n Location\n Person\n Organization\n Miscellaneous\n Non-entity"
label_list = ['LOC','PER','ORG','Non']

def link(result, th):
    
    unc_count = 0
    pos_count = 0
    tp = 0
    tmp_pred_cnt = 0
    tmp_label_cnt = 0
    
    trup_sent = len(result)
    if trup_sent > 1:
        context = result[0]
        for idx in(result[1:]):
            if '<Context>' not in idx[0]:
                idx = idx[0].split(' ')
                if(float(idx[-2]))>=th:
                    unc_count += 1
                    
                    if str(idx[-7]) == str(idx[-6]):
                        tp += 1
                        pos_count += 1
                    if str(idx[-7]) != 'O':
                        tmp_label_cnt += 1
                    if str(idx[-6]) != 'O':
                        tmp_pred_cnt += 1
                else:
                    pass

    return unc_count, pos_count, tp, tmp_pred_cnt, tmp_label_cnt     

def metrics(file_dir):
    print('Threshold: ', 'Precision. ','Recall ','F1 ','Acc ', 'Num. ')

    stage2_result = []
    Acc = []
    # Open the file in read mode
    th = 0.0
    while th < 1:
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
                        unc_co, pos_co, tp, tmp_pred_cnt, tmp_label_cnt  = link(stage2_result, th)
                        unc_count += unc_co
                        pos_count += pos_co
                        TP += tp
                        TPC += tmp_pred_cnt
                        TLC += tmp_label_cnt
                        
                        stage2_result = []
                        stage2_result.append(sentence)

                    else:
                        stage2_result.append(sentence)
                else:
                    stage2_result.append(sentence) 
            unc_co, pos_co, tp, tmp_pred_cnt, tmp_label_cnt = link(stage2_result, th)
            TP += tp
            TPC += tmp_pred_cnt
            TLC += tmp_label_cnt
            unc_count += unc_co
            pos_count += pos_co
            

            precision = TP/(TPC + 1e-5)
            recall = TP/(TLC+1e-5)
            f1 = 2*precision*recall/(precision+recall+1e-5)
            
            print(th, precision, recall, f1, pos_count/(unc_count+1e-5),unc_count)
            th += 0.1
            Acc.append(th)
           

metrics('')
