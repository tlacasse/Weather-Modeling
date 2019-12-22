import pickle

def parse_data_csv(file_name):
    data = {}
    names = []
    with open('data/{}.csv'.format(file_name), 'r') as file:
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
    save_data('data/{}.names'.format(file_name), names)
    save_data('data/{}.data'.format(file_name), data)

def save_data(filename, obj):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)

def open_data(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

class Column:
    
    def __init__(self, heading):
        self.heading = heading
        self.filter_func = (lambda _: True)
        self.process_func = (lambda _: _)
        self.preprocess_func = (lambda _: _)
    
    def set_preprocess(self, preprocess_func):
        self.preprocess_func = preprocess_func
        return self
    
    def set_filter(self, filter_func):
        self.filter_func = filter_func
        return self
    
    def set_process(self, process_func):
        self.process_func = process_func
        return self
        
    def preprocess(self, x):
        return self.preprocess_func(x)
        
    def should_include(self, x):
        return self.filter_func(self.preprocess(x))
    
    def process(self, x):
        return self.process_func(self.preprocess(x))
    
    def __str__(self):
        return self.heading
    
    def __repr__(self):
        return self.heading
    
class IntColumn(Column):
    
    def __init__(self, heading):
        super().__init__(heading)
        def _filter_func(x):
            try:
                int(x)
                return True
            except:
                return False
        self.filter_func = _filter_func
        self.process_func = (lambda x: int(x))
     
class FloatColumn(Column):
    
    def __init__(self, heading):
        super().__init__(heading)
        def _filter_func(x):
            try:
                float(x)
                return True
            except:
                return False
        self.filter_func = _filter_func
        self.process_func = (lambda x: float(x))    

def clean_dataset(src, columns):
    fails = {c.heading: [] for c in columns}
    
    def get_columns_at(i):
        return [src[c.heading][i] for c in columns]
    
    def is_valid_row(row):
        results = [columns[i].should_include(row[i]) for i in range(len(row))]
        for i in range(len(row)):
            if not results[i]:
                fails[columns[i].heading].append(row[i])
        return all(results)

    def process_row(row):
        return [columns[i].process(row[i]) for i in range(len(row))]
        
    rows = len(src[columns[0].heading])

    data = [get_columns_at(i) for i in range(rows)]
    data = [process_row(row) for row in data if is_valid_row(row)]
    
    transposed = {}
    for i, c in enumerate(columns):
        c = c.heading
        transposed[c] = [row[i] for row in data]

    return transposed, fails

def group(by, values):
    def add_dict_list(d, k, v):
        if not k in d:
            d[k] = []
        d[k].append(v)
    both = zip(by, values)
    groups = {}
    for k, v in both: 
        add_dict_list(groups, k, v)  
    return groups
