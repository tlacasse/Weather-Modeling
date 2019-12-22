
CONDITIONS = ['CLR', 'FEW', 'SCT', 'BKN', 'OVC', 'VV']

def condition_index(c):
    def get_name(c):
        i = c.find(':')
        if i >= 0:
            name = c[(i-3):i]
            name2 = c[(i-2):i]
            if (name2 == 'VV'):
                return 'VV'
            else:
                return name if len(name) == 3 else ''
        else:
            return ''
    try:
        return CONDITIONS.index(get_name(c))
    except:
        return -1
