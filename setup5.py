from weather.dataset import save_data
from weather.models import WeatherModel
from weather.usgs import GAGEHEIGHT_TEMPLATE
import weather.source as wsrc

# https://maps.waterdata.usgs.gov/mapper/nwisquery.html?URL=https://waterdata.usgs.gov/usa/nwis/uv?referred_module=sw&state_cd=ct&site_tp_cd=OC&site_tp_cd=OC-CO&site_tp_cd=ES&site_tp_cd=LK&site_tp_cd=ST&site_tp_cd=ST-CA&site_tp_cd=ST-DCH&site_tp_cd=ST-TS&format=sitefile_output&sitefile_output_format=xml&column_name=agency_cd&column_name=site_no&column_name=station_nm&range_selection=days&period=7&begin_date=2019-12-09&end_date=2019-12-16&date_format=YYYY-MM-DD&rdb_compression=file&list_of_search_criteria=state_cd%2Csite_tp_cd%2Crealtime_parameter_selection&column_name=site_tp_cd&column_name=dec_lat_va&column_name=dec_long_va&column_name=agency_use_cd

print('LOAD ALL DATA')

data, length = wsrc.get_full_dataset()
sites = wsrc.get_selected_river_sites()
airports = wsrc.get_airports()
proj = wsrc.build_projection(sites)
rmap = wsrc.build_rivermapper(proj)

latlong_list = wsrc.get_latlong_list(sites)
latlong_list = proj.on_points(latlong_list)
h, w = proj.get_dim()

def to_input(i):
    results = []
    for k, v in zip([GAGEHEIGHT_TEMPLATE.format(s.key) for s, v in sites], latlong_list):
        results.append((v[0], v[1], data[k][i]))
    return results

airports_latlong = {'OXFORD': (41.4795, 73.1359)}
print(airports_latlong)

print('MAP RIVERS TO GRID')
emmissions = [rmap.map_to_grid(to_input(i)) for i in range(length)]

print('MODEL PER AIRPORT')
for a in airports:
    print(a)
    latlong_a = proj.on_points([airports_latlong[a]])[0]
    emmissions_a = [m[latlong_a[0], latlong_a[1]] for m in emmissions]
    
    for k in ['HourlySkyConditions', 'HourlyWindDirection', 'HourlyWindSpeed', 'HourlyPrecipitation']:
        field = '{}_{}'.format(a, k)
        print(field)
        states = data[field]
        model = WeatherModel.build_hmm(emmissions_a, states, k)
        save_data('data/models/{}.hmm'.format(field), model)
