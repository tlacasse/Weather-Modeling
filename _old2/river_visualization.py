from weather.usgs import BRADLEY_RIVERS_DATA, BRADLEY_RIVERS
from weather.dataset import DataSet
import cv2
import numpy as np
# https://maps.waterdata.usgs.gov/mapper/nwisquery.html?URL=https://waterdata.usgs.gov/usa/nwis/uv?referred_module=sw&state_cd=ct&site_tp_cd=AT&site_tp_cd=GL&site_tp_cd=OC&site_tp_cd=OC-CO&site_tp_cd=ES&site_tp_cd=LK&site_tp_cd=ST&site_tp_cd=ST-CA&site_tp_cd=ST-DCH&site_tp_cd=ST-TS&site_tp_cd=SP&site_tp_cd=GW&site_tp_cd=GW-CR&site_tp_cd=GW-EX&site_tp_cd=GW-HZ&site_tp_cd=GW-IW&site_tp_cd=GW-MW&site_tp_cd=GW-TH&site_tp_cd=SB&site_tp_cd=SB-CV&site_tp_cd=SB-GWD&site_tp_cd=SB-TSM&site_tp_cd=SB-UZ&site_tp_cd=WE&site_tp_cd=LA&site_tp_cd=LA-EX&site_tp_cd=LA-OU&site_tp_cd=LA-SNK&site_tp_cd=LA-SH&site_tp_cd=LA-SR&site_tp_cd=FA&site_tp_cd=FA-CI&site_tp_cd=FA-CS&site_tp_cd=FA-DV&site_tp_cd=FA-FON&site_tp_cd=FA-GC&site_tp_cd=FA-HP&site_tp_cd=FA-QC&site_tp_cd=FA-LF&site_tp_cd=FA-OF&site_tp_cd=FA-PV&site_tp_cd=FA-SPS&site_tp_cd=FA-STS&site_tp_cd=FA-TEP&site_tp_cd=FA-WIW&site_tp_cd=FA-SEW&site_tp_cd=FA-WWD&site_tp_cd=FA-WWTP&site_tp_cd=FA-WDS&site_tp_cd=FA-WTP&site_tp_cd=FA-WU&site_tp_cd=AW&site_tp_cd=AG&site_tp_cd=AS&format=sitefile_output&sitefile_output_format=xml&column_name=agency_cd&column_name=site_no&column_name=station_nm&range_selection=days&period=7&begin_date=2019-12-03&end_date=2019-12-10&date_format=YYYY-MM-DD&rdb_compression=file&list_of_search_criteria=state_cd%2Csite_tp_cd%2Crealtime_parameter_selection&column_name=site_tp_cd&column_name=dec_lat_va&column_name=dec_long_va&column_name=agency_use_cd
dataset = DataSet([r[5:] for r in BRADLEY_RIVERS_DATA.data], BRADLEY_RIVERS_DATA.get_column_names()[5:])

print(dataset.get_column_names())
pos = [[r.lat_coord(), r.long_coord()] for r in BRADLEY_RIVERS]
print(pos)
pos = [[int((70 - y - 8)), int((70 - x - 20))] for y, x in pos]
print(pos)
maxs = [max([a[i] for a in dataset.data]) for i in range(4)]
print(maxs)
limit = max(maxs)

cols = [dataset.get_column(k) for k in dataset.get_column_names()]

for i in range(len(cols[0])):
    img = np.zeros((13, 23), dtype='uint8')
    
    for r in range(4):
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                img[pos[r][0]+x, pos[r][1]+y] = min(int((cols[r][i] / maxs[r]) * 300) - 1, 255)
                
    img = cv2.resize(img, (1150, 650), interpolation=cv2.INTER_NEAREST)#
    
    
    cv2.imshow('GageHeight', img)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
    