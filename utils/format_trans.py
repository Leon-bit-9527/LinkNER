import json
import os
import re
import time
from tqdm import tqdm


def save_res(result):
    file = open("ori_transfotmat.txt", "a+")
    for data in result:
        line = ' '.join(data) + '\n'
        file.write(line)

stage2_result = []
final_result = []
# Open the file in read mode
with tqdm(total = os.path.getsize('ori_result9120.txt')) as pbar:
    with open('ori_result9120.txt', 'r') as f:
        count = 0
        count_ex = 0
        all_datas = []
        for line in f.readlines():
            line = line.strip('\t\n')
            line = str(line)
            sentence = re.split(':: |\t|"', line)
            ## 判断是否是句子，[]
            if '<Context>' in sentence[0]:
                count += 1
                if count > 1:
                    save_res(stage2_result)

                    stage2_result = []
                    stage2_result.append(sentence)

                else:
                    stage2_result.append(sentence)
            else:
                stage2_result.append(sentence) 
            pbar.update(len(line)) 
            pass
        save_res(stage2_result)
