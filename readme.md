# Weather Modeling Visualization

### Setup

Requires numpy, matplotlib, pomegranate, opencv.

### Runnning

All data files are already built and included in the repository. To recreate, run `setup1.py` to `setup5.py`.

Run `main.py` to see the visualization of weather. 

### Useful Links

[NOAA documents](noaa_documents).

[NOAA data](https://www.ncdc.noaa.gov/cdo-web/datatools/lcd).

[USGS data](https://waterdata.usgs.gov/nwis/uv/?referred_module=sw).

[USGS map](https://maps.waterdata.usgs.gov/mapper/nwisquery.html?URL=https://waterdata.usgs.gov/usa/nwis/uv?referred_module=sw&state_cd=ct&site_tp_cd=OC&site_tp_cd=OC-CO&site_tp_cd=ES&site_tp_cd=LK&site_tp_cd=ST&site_tp_cd=ST-CA&site_tp_cd=ST-DCH&site_tp_cd=ST-TS&format=sitefile_output&sitefile_output_format=xml&column_name=agency_cd&column_name=site_no&column_name=station_nm&range_selection=days&period=7&begin_date=2019-12-09&end_date=2019-12-16&date_format=YYYY-MM-DD&rdb_compression=file&list_of_search_criteria=state_cd%2Csite_tp_cd%2Crealtime_parameter_selection&column_name=site_tp_cd&column_name=dec_lat_va&column_name=dec_long_va&column_name=agency_use_cd).

### Project Overview

Two datasets were used. The NOAA Local Climatological Data contains information about air, 
and the USGS Surface-Water Historical Data contains information about water bodies. 
The resulting idea was to model some connection between the two idea, mainly there should be 
some correlation between water flow and precipitation/clouds. The source data was taken from 2010-11-09 to 2019-11-09. 
A solid 10 years may be enough to have a reasonable amount of points, but at some point, going back farther in time 
limits the number of stations available. Also, hourly points were chosen for maximum available points, and reduce averaging.

The NOAA station sources are Connecticut airports. The Oxford airport was chosen due to its personal value and presence 
of surrounding USGS river gauges. The data contains multiple types of records (including daily and monthly summaries), 
but the hourly “METAR Aviation routine weather report” records were used here. Refer to the “LCD Dataset Documentation” 
for more details. The columns explored were as follows:

| Column Name | Notes |
| ----------- | ----- |
| HourlyAltimeterSetting | Float (.xx). <br> An appended “s” is a “suspect value” and was ignored. |
| HourlyDewPointTemperature	| Integer. <br> Ignored “s”. |
| HourlyDryBulbTemperature | Integer. <br> Ignored “s”. |
| HourlyPrecipitation | float (.xx). <br> A “T” means trace precipitation, and was treated as a 0. <br> Ignored “s”. |
| HourlyRelativeHumidity | Integer. |
| HourlySkyConditions | String xxx:nn nn.  <br>  Cloud description  <br>&nbsp;  CLR: clear sky  <br>&nbsp;  FEW: few clouds  <br>&nbsp;  SCT: scattered clouds  <br>&nbsp; BKN: broken clouds  <br>&nbsp; OVC: overcast  <br>&nbsp; VV: obscured sky  <br>  Up to 3 layers, last layer was used since it is the most representative of the sky conditions.  <br> Numbers were not used.  <br>  Ex: "BKN:07 13 OVC:08 49" -> "OVC" |
| HourlyWetBulbTemperature | Integer. |
| HourlyWindDirection | Integer.  <br>&nbsp; 0: calm winds  <br>&nbsp; 90: east  <br>&nbsp; 180: south  <br>&nbsp; 270: west  <br>&nbsp;  360: north  <br> "VRB", which is “variable wind direction”, was treated as 0. |
| HourlyWindSpeed | Integer. <br> Ignored “s”. |

The USGS river data is recorded in 15-minute intervals, with a variety of information, inconsistently present. “Discharge” and “Gage height” seemed 
to be the most common. “GageHeight” (float .xx) was chosen due to its higher correlation with NOAA values. This GageHeight should have some 
correlation to precipitation weather. River locations in CT with longitude greater than 72.84 and latitude between 41.35 and 41.72 were chosen 
(an arbitrary bounding box around the Oxford airport), and those with GageHeight data. 

All the data points (9 from NOAA and 11 from USGS) were aligned to each hour. Because the NOAA times were generally at hh:51, the USGS points at hh:45 were 
taken. All records that had any problems (at least one of the columns did not fit the common format determined of that column) were completely removed. This 
created discontinuities, and the broken data should have been treated as separate sequences for training the models rather than one long sequence. The columns 
were analyzed for correlation using numpy’s “corrcoef” function. See [correlation script](correlation.py).

HourlySkyConditions, HourlyPrecipitation, HourlyWindDirection, HourlyWindSpeed were chosen to be modeled because of their positive correlation, 
ability to be visualized, and relation to precipitation/clouds that may should correlate with river GageHeight (the height should generally increase 
after rain). Despite being the highest positive correlation relatively, they are not absolutely correlated, showing the difficulty in modeling this 
data. See [histogram script](histogram.py).

Next is to find a value of GageHeight at the position of the airport, where there is not a river source. The latitude and longitude of the river gauges are 
mapped to a low resolution “image” and scaled based on its max value, where a kernel is then applied, a linear amplifying kernel.

The linear choice is arbitrary for simplicity, other types (such as Gaussian) would presumably not have any noticeable change, and the amplification 
is to scale up the small GageHeight values to the full grayscale range and reinforce its values, and allow it to “spread” to where there is no data. 
The low resolution helps the “spread” without too large of a kernel, and encourages spatially more general data. This happens at each discrete time step (hour). 

The coordinates of the airport can then be mapped down to these same dimensions (approximately the center) to obtain values for GageHeight. A separate HMM is 
created for each of the four weather columns as hidden states, and each using the same estimated airport GageHeight as the observable emissions. The source 
GageHeight values are remapped to the reduced and filtered image and generated weather using predictions of the HMMs are visualized on top of the grid. Each 
cell in the grid shows a collection of clouds based on the prediction of the “spread” GageHeight value in the cell. HourlySkyConditions is shown in the number 
of clouds, ranging from empty to full coverage. HourlyWindSpeed and HourlyWindDirection is shown as the speed and direction of those clouds. Calm winds (direction = 0) 
are treated as a speed of 0. The HourlyPrecipitation model was predicting precipitation constantly, so it was removed. 

The gray dots are the locations of the river gauges in the reduced image dimensions. The visualization clearly contains some artifacts of the reduce and “spread” method, 
such as the bottom left corner, which is always cloudy due to a lack of data. The resulting visualization is interesting nonetheless.

![visualization example](/images/final_visual.gif)

### Possible Future Work

- Make a more cohesive model.
- Include some river/city landmarks.
- Explore Markov Random Fields.
