import pickle

data = {}
names = []
with open('data/2010-11-09_2019-11-09_hourly.csv', 'r') as file:
    first = True
    j = 0
    for line in file:
        j += 1
        line = line.split(',')
        if first:
            first = False
            for c in line:
                c = c.strip()
                names.append(c)
                data[c] = []
        else:
            i = 0
            for n in names:
                c = None
                if len(line[i]) > 0 and line[i][0] == '"':
                    j = i
                    while not line[i][-1] == '"':
                        i += 1
                    c = ','.join(line[j:i+1])
                else:
                    c = line[i]
                data[n].append(c.strip())
                i += 1

with open('data/hourly.names', 'wb') as file:
    pickle.dump(names, file)
with open('data/hourly.data', 'wb') as file:
    pickle.dump(data, file)
