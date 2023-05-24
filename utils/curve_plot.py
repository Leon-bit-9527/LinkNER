import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

## uncertainty threshold = 0.3, Chat temperature = 0.0

threshold = [i/10 for i in range(0,11)]
x = [i for i in range(0,11)]

# 选取阈值所选list + revised
conll_ori = [0.9200,0.8307, 0.7142, 0.6378, 0.5721, 0.5577, 0.5512, 0.5170, 0.4715, 0.3600, 0.0000] 
conll_th_balance=[0.8539, 0.6812, 0.6492,0.6217,0.6068,0.6067,0.6151,0.6140,0.6333,0.6154,0.7500]
conll_ori_rivised =[0.9313 ,0.8436 ,0.7430 ,0.6813 ,0.6333 ,0.6360 ,0.6537 ,0.6602 ,0.6909 ,0.6612 ,0.8571]

# typos
conll_typos = [0.8269, 0.7121,0.5993,0.5587,0.5151,0.4707,0.4389,0.4165,0.3653,0.3220, 0.1702]
conll_typos_revised = [0.8384, 0.8304, 0.7221, 0.6208, 0.5888, 0.5825, 0.5702, 0.5601, 0.5648, 0.5828, 0.6189, 0.7037]
# oov
conll_oov = [0.6861,0.6446, 0.5678, 0.5248, 0.4911, 0.4382, 0.4159, 0.3892, 0.3424, 0.3424, 0.2857] 
conll_oov_revised = [0.7229, 0.6972, 0.6517, 0.6339, 0.6180, 0.6152, 0.6187, 0.6306, 0.6321, 0.6321, 0.5895] 

# wiki
wiki_ori = [0.8109,0.7625, 0.6947, 0.6549, 0.6226, 0.5960, 0.5607, 0.5491, 0.5247, 0.4387, 0.5714] 
wiki_revised = [0.8232,0.7773, 0.7185, 0.6860, 0.6734, 0.6597, 0.6506, 0.6479, 0.6488, 0.6382, 0.8000]

# wnut17
wnut17_ori =  [0.4833, 0.5212, 0.4648, 0.4666, 0.4361, 0.4304, 0.4314, 0.4116, 0.4178, 0.3761, 0.0000] 
wnut17_th_balance = [0.6674, 0.6318, 0.6140, 0.6063, 0.5937, 0.5806, 0.5648, 0.5401, 0.5152, 0.4846, 0.4833]
wnut17_revised = [0.6674, 0.7914, 0.7635, 0.7692, 0.7658, 0.7616, 0.7699, 0.7855, 0.7795, 0.7591, 1.0000]

# Ontonote 5
Onto_ori = [0.8870, 0.8827, 0.8179, 0.7476, 0.6822, 0.6042, 0.5040, 0.3566, 0.2703]
Onto_th_balance = [0.7641, 0.7498, 0.6845, 0.6427, 0.6298, 0.6294, 0.6490, 0.5957, 0.6939] 
Onto_revised = [0.8916, 0.8969, 0.8251, 0.7502, 0.6822, 0.6299, 0.6490, 0.5957, 0.6939] 

f, axs = plt.subplots(1,1)
f.set_size_inches([6,6])
axs.spines['left'].set_linewidth(2.0)
axs.spines['right'].set_linewidth(2.0)
axs.spines['top'].set_linewidth(2.0)
axs.spines['bottom'].set_linewidth(2.0)

axs.plot(Onto_ori, c='royalblue',marker='+')
axs.plot(Onto_th_balance, c='orange',marker='*')

axs.set_title('Ontonote 5')
axs.set_xlabel('Uncertainty')
axs.set_ylabel('F1-scores')
axs.legend(['NER','LinkNER'], loc='upper right')
ticks = axs.set_xticks(x) # 设置刻度
axs.set_xticklabels(threshold)

plt.grid(linestyle = '--', linewidth = 0.5)

plt.savefig('figures/Onto_th.pdf')

plt.show()