from weather.usgs import list_state_sources, GAGE_HEIGHT
from weather.dataset import save_data

sites = list_state_sources(state='CT')
save_data('data/usgs/all.sites', sites)

print('SAVE ALL SITES/VARS')
print('count: {}'.format(len(sites)))
lats = [float(s.latitude) for s, v in sites]
print('latitude range: {} to {}'.format(min(lats), max(lats)))
longs = [float(s.longitude) for s, v in sites]
print('logitude range: {} to {}'.format(min(longs), max(longs)))

def pick_site(s, v):
    # need Gage Height data
    if not v.code == GAGE_HEIGHT:
        return False
    # bound to square around airpoirt
    if not abs(float(s.longitude)) > 72.84:
        return False
    if not float(s.latitude) < 41.72:
        return False
    if not float(s.latitude) > 41.35:
        return False
    return True

sites = [(s, v) for s, v in sites if pick_site(s, v)]
keys = list(set([s.key for s, v in sites]))
new_sites = []
# remove duplicates
for k in keys:
    for s, v in sites:
        if s.key == k:
            new_sites.append((s, v))
            break
sites = new_sites
print()
print('SAVE SELECTED SITES/VARS')
save_data('data/usgs/selected.sites', sites)

print('count: {}'.format(len(sites)))
lats = [float(s.latitude) for s, v in sites]
print('latitude range: {} to {}'.format(min(lats), max(lats)))
longs = [float(s.longitude) for s, v in sites]
print('logitude range: {} to {}'.format(min(longs), max(longs)))

print(keys)
for s, v in sites:
    print()
    print(s)
    print(v)
