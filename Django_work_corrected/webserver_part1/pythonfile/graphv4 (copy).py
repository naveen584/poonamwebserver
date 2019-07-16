import numpy as np
import re
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import matplotlib.lines as mlines
import matplotlib.ticker as ticker
import pandas as pd 
import csv

def delete_column(self):
 
# Instantiating a Workbook object by excel file path
    workbook = self.Workbook(self.dataDir + 'Book1.xls')
 
# Accessing the first worksheet in the Excel file
    worksheet = workbook.getWorksheets().get(0)
 
# Deleting a column from the worksheet at 2nd position
    worksheet.getCells().deleteColumns(1,1,True)
 
# Saving the modified Excel file in default (that is Excel 2003) format
    workbook.save(self.dataDir + "Delete Column.xls")





f = open('hmm_output').read()
data = f[f.find('    -'):f.find('\n\n\n')].split('\n')[3:]
all_data = []
for line in data:
    if 'threshold' not in line:
        line = line.strip()
        all_data.append(list(map(float, re.split(r'\s+', line)[0:2])))
        
        
    else:
        break



with open('all_data.csv', 'wb') as f:
    np.savetxt(f, all_data, fmt='%.2e %.2f', delimiter=',')
read_data = np.genfromtxt('all_data.csv')
x = list(x for x in range(read_data.shape[0]))
y1 = [np.log10(x) for x in read_data[:, 0]]
y2 = read_data[:, 1]

xnew = np.linspace(min(x), max(x), 30)

spl1 = make_interp_spline(x, y1, k=3)
spl2 = make_interp_spline(x, y2, k=3)

y1_new = spl1(xnew)
y2_new = spl2(xnew)

fig, ax1 = plt.subplots()

color = 'r'
ax1.set_ylabel('score', color=color)
ax1.plot(xnew, y2_new, color=color, linewidth=5)
ax1.tick_params(axis='y', labelcolor=color)
ax1.xaxis.set_ticks(np.arange(0, 460, 40))

ax2 = ax1.twinx()  

color = 'k'
ax2.set_ylabel('E-value', color=color)  
ax2.plot(xnew, y1_new, color=color, linewidth=5)
ax2.tick_params(axis='y', labelcolor=color)

y_labels = ax2.get_yticks()
ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0e'))


e_val = mlines.Line2D([], [], color='k',
                      marker='_', linestyle='None',
                      markersize=10, label='E-Value')

score = mlines.Line2D([], [], color='r',
                      marker='_', linestyle='None',
                      markersize=10, label='Score')

plt.legend(handles=[e_val, score])
plt.show()
all_data1 = []

f = open('hmm_output').read()
data1 = f[f.find('    -'):f.find('\n\n\n')].split('\n')[3:]

for line in data1:
    if 'threshold' not in line:
        line = line.strip()
        all_data1.append(list(map(float, re.split(r'\s+', line)[0:1])))
        all_data1.append(list(map(float, re.split(r'\s+', line)[1:2])))
        all_data1.append(list( re.split(r'\s+', line)[8:9]))
        
    else:
        break
    




np_array = np.reshape(np.array(all_data1), (-1, 3))    
pd.DataFrame(np_array).to_csv("./all_data1.csv")
#print(np_array)
import pandas as pd
df = pd.read_csv("all_data1.csv")
# If you know the name of the column skip this
first_column = df.columns[0]
# Delete first
df = df.drop([first_column], axis=1)
df.to_csv('all_data1.csv', index=False)
