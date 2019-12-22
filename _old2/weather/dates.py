from datetime import datetime, timedelta

# https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for d in range(int ((end_date - start_date).days)):
        for h in range(24):
            yield start_date + timedelta(days=d, hours=h, minutes=45)

def usgs_dates():
    def fix_zero(d):
        i = d.index(':')
        if d[i-2] == '0':
            return d[:i-2] + d[i-1:]
        else:
            return d
    return [d for d in daterange(datetime(2010, 11, 9, 0, 0), datetime(2019, 11, 9, 23, 45))]
   
     # https://stackoverflow.com/questions/5946236/how-to-merge-multiple-dicts-with-same-key