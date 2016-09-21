import numpy as np
from datetime import datetime

fema_declaration = "./data/data.gov.FEMADeclarations.8.26.16.csv"
major_disaster = "./data/major_disaster.csv"
updated_major_disaster = "./data/updated_major_disaster.csv"

map = {} # {id, (start, end)}
data = np.loadtxt(fema_declaration, dtype= str, delimiter=',', usecols = (0,9,10), skiprows=1)

for i in range(data.shape[0]):
    id = data[i][0]
    if not map.has_key(id):
        map[id] = (data[i][1], data[i][2])


file_out = open(updated_major_disaster, 'w')
data_d = np.loadtxt(major_disaster, dtype = 'str', delimiter='\",\"', skiprows=1)
for i in range(data_d.shape[0]):
    id = data_d[i][0].strip('\"')
    print map[id]
    start_date = datetime.strptime(map[id][0], "%m/%d/%Y")
    end_date = datetime.strptime(map[id][1], "%m/%d/%Y")
    diff =  abs((end_date - start_date).days)
    print diff
    file_out.write('\",\"'.join(data_d[i]) + ',\"' + '\",\"'.join([str(map[id][0]), str(map[id][1]), str(diff + 1)]) + '\" \n')
file_out.close()