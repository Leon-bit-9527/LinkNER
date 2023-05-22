import json
import os
import re
import time
# import openai
from tqdm import tqdm

# openai.api_key = "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"

def save_res(result):
    file = open("ori_results_unc0.1.txt", "a+")
    for data in result:
        line = ' '.join(data) + '\n'
        file.write(line)

# def chatRes(content):
#     time.sleep(10)
#     response = openai.ChatCompletion.create(
#     model = "gpt-3.5-turbo",
#     temperature = 0.2,
#     max_tokens = 256,
#     messages = [{"role": "user", "content":content}]
#     )
#     return (response['choices'][0]['message']['content'])

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
                    # # print(idx[0])
                    # # print(float(idx[-2]))
                    # query = str(context[0]) + "\n Select the entity type of "+ str(idx[0]) +" in this Context, and only need to output the entity type:" + label
                    # # res = chatRes(query)
                    # # print(query)
                    # new_label = [i for i in label_list if i.lower() in res.lower()]
                    # new_label = ['O'] if new_label == [] else new_label
                    # new_label = ['O'] if new_label[0] == 'Non' else new_label
                    # stage1_res = idx[3]
                    # idx[3] = new_label[0]
                    # # print(new_label[0])
                    # # print(idx[2])
                    # if (str(new_label[0])==str(idx[2])) and (str(stage1_res)!=str(idx[2])):  
                    #     pos_count += float(idx[-1])
                    # idx[3] = '<replace>'
                else:
                    pass
    
    #     save_res(result)
    # else:
    #     save_res(result)

    return unc_count, pos_count, tp, tmp_pred_cnt, tmp_label_cnt     
    # acc = pos_count/unc_count
    
    # print(acc)

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
            
# metrics('typos8138_result9120.txt')
# metrics('oov6719_result9120.txt')
# metrics('ood7818_result9120.txt')
# metrics('test_result.txt')

metrics('ori_results_unc0.8.txt')