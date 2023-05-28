import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

## uncertainty threshold = 0.3, Chat temperature = 0.0

threshold = [i/10 for i in range(0,11)]
x = [i for i in range(0,11)]

# 选取阈值所选list + revised, 待添加...
conll_ori = []
conll_th_balance=[]
conll_ori_rivised =[]


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
