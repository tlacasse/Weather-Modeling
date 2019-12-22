import requests
import json

# https://waterservices.usgs.gov/rest/DV-Test-Tool.html

GAGE_HEIGHT = '00065'
GAGEHEIGHT_TEMPLATE = '{}_GageHeight'

def request_txt(uri):
    r = requests.get(uri, allow_redirects=True)
    return str(r.content, 'utf-8')

def request_json(uri):
    return json.loads(request_txt(uri))  

def list_state_sources(state='CT'):
    # search list of dicts for type
    def get_site_type(info):
        for i in info['siteProperty']:
            if i['name'] == 'siteTypeCd':
                return i['value']
        return None
    
    def get_site(site):
        info = site['sourceInfo']
        return USGSSite(name=info['siteName'], 
                        number=info['siteCode'][0]['value'], 
                        site_type=get_site_type(info),
                        latitude=info['geoLocation']['geogLocation']['latitude'],
                        longitude=info['geoLocation']['geogLocation']['longitude'],
                        metadata=info)
        
    def get_var(site):
        var = site['variable']
        return USGSVariable(name=var['variableDescription'],
                            code=var['variableCode'][0]['value'],
                            metadata=var)
    
    uri = 'https://waterservices.usgs.gov/nwis/dv/?stateCd={}&format=json'
    r = request_json(uri.format(state))
    sites = r['value']['timeSeries']
    result = []
    for site in sites:
        result.append((get_site(site), get_var(site)))
    return result

class USGSVariable:
    
    def __init__(self, name, code, metadata=''):
        self.name = name
        self.code = code
        self.metadata = metadata
        
    def __str__(self):
        return "USGSVariable(name='{}', code='{}')".format(self.name, self.code)
        
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash(self.code)
    
    def __eq__(self, other):
        return hash(self) == hash(other)
 
class USGSSite:
    
    def __init__(self, name, number, site_type, latitude, longitude, metadata=''):
        self.name = name
        self.number = number
        self.site_type = site_type
        self.latitude = latitude
        self.longitude = longitude
        self.metadata = metadata
        self.key = ''.join([w[:2] for w in self.name.split(' ')])[:-2]
        
    def __str__(self):
        return "USGSSite(name='{}', number='{}', site_type='{}', latitude='{}', longitude='{}')".format(
                self.name, self.number, self.site_type, self.latitude, self.longitude)
        
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash(self.key)
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def get_data(self, begin_date, end_date, var_code, out_format='rdb'):
        uri = 'https://nwis.waterdata.usgs.gov/usa/nwis/uv/?'
        uri += 'cb_{}=on&format={}&site_no={}&period=&begin_date={}&end_date={}'
        return request_txt(uri.format(var_code, out_format, self.number, begin_date, end_date))
