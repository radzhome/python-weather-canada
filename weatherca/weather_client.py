"""
The data for city weather is from:
https://dd.weather.gc.ca/citypage_weather/xml/
https://eccc-msc.github.io/open-data/msc-datamart/readme_en/
Icons - https://dd.weather.gc.ca/citypage_weather/docs/Current_Conditions_Icons-Icones_conditions_actuelles.pdf
- https://weather.gc.ca/weathericons/01.gif through https://weather.gc.ca/weathericons/48.gif
Github - https://github.com/ECCC-MSC
Cities per province:
https://weather.gc.ca/forecast/canada/index_e.html?id=AB

City, town data is from:
https://www.nrcan.gc.ca/earth-sciences/geography/download-geographical-names-data/9245

"""
import xmltodict

import requests

CITY_LIST_URL = 'https://dd.weather.gc.ca/citypage_weather/xml/siteList.xml'
CITY_URL = f'https://dd.weather.gc.ca/citypage_weather/xml/{{province_code}}/{{city_code}}_e.xml'  # city code = @code
CITY_FR_URL = 'https://dd.weather.gc.ca/citypage_weather/xml/{province_code}/{city_code}}_f.xml'  # French version

# TODO: convert the TWN region code to the city code as per this (need mapping)


# TODO: based on data/ for canada map each location to closest weather station/data from api

# png, svg
IMAGE_MAPPING = {
    'hp_w_i_l': 'n/a',
    # 'hp_w-iln_l': 'rain_cloud_night', # - in here, moon
    # 'hp_w-ian_l': 'moon_rain_cloud',  # night # - in here
    # 'hp_w_ia_l': 'sun_rain_cloud',  # day
    'hp_w_ib_l': 'sun_cloud',  # part sun blocked
    'hp_w_ibn_l': 'moon_cloud',
    'hp_w_ic_l': 'sun',
    'hp_w_icn_l': 'moon',  # clear
    'hp_w_id_l': 'sun_clouds',  # more cloudy
    'hp_w_idn_l': 'moon_clouds',  # more cloudy
    'hp_w_if_l': 'wind',
    'hp_w_ifn_l': 'wind_night',
    'hp_w_ig_l': 'rain_snow_cloud',
    'hp_w_ign_l': 'rain_snow_cloud_night',
    'hp_w_ih_l': 'more_sun_cloud',  # sun is out, but cloud
    'hp_w_ihn_l': 'more_moon_cloud',  # moon is out, but cloud
    'hp_w_ii_l': 'rain_snow_cloud',  # exact same - hp_w_ig_l
    'hp_w_iin_l': 'rain_snow_cloud_night',  # exact same - hp_w_ign_l
    'hp_w_ij_l': 'sun_cloud',  # exact same - hp_w_ib_l
    'hp_w_ijn_l': 'moon_cloud',  # exact same - hp_w_ib_l
    'hp_w_ik_l': 'sun_clouds',  # exact same - hp_w_id_l
    'hp_w_ikn_l': 'moon_clouds',  # exact same
    'hp_w_il_l': 'moon_clouds',  # exact same
    'hp_w_im_l': 'sun_rain_snow_cloud',
    'hp_w_imn_l.': 'moon_rain_snow_cloud',
    'hp_w_in_l': 'sun_snow_cloud',
    'hp_w_inn_l': 'night_snow_cloud',  # no moon
    'hp_w_io_l': 'cloud',
    'hp_w_ion_l': 'moon_cloud',  # party moon blocked i.e. cloudy night
    'hp_w_ip_l': 'snow_wind_cloud',
    'hp_w_ipn_l': 'snow_wind_cloud_night',
    'hp_w_iq_l': 'rain_thunder_cloud',
    'hp_w_iqn_l': 'rain_thunder_cloud_night',
    'hp_w_ir_l': 'rain_cloud',
    'hp_w_irn_l': 'night_rain_cloud',
    'hp_w_is_l': 'more_sun_cloud',  # same as hp_w_ih_l
    'hp_w_isn_l': 'more_moon_cloud',  # same as hp_w_ihn_l
    'hp_w_it_l': 'sun_rain_thunder_cloud',
    'hp_w_itn_l': 'rain_thunder_cloud_night',
    'hp_w_iu_l': 'more_sun_cloud',  # same
    'hp_w_iun_l': 'more_moon_cloud',  # same
    'hp_w_iunknown_l': 'unknown',
    'hp_w_iv_l': 'snow_cloud',
    'hp_w_ivn_l': 'snow_cloud_night',
    'hp_w_iw_l': 'more_snow_cloud',  # lg snowflakes
    'hp_w_iwn_l.': 'more_snow_cloud_night',  # lg snowflakes
    'hp_w_ix_l': 'blank',  # nothing, same as unknown?
    'hp_w_iy_l': 'more_snow_cloud',  # same
    'hp_w_iyn_l': 'more_snow_cloud_night',  # same
    'hp_w_iz_l': 'ice_rain_cloud',
    'hp_w_izn_l': 'ice_rain_cloud_night',
}


def get_cities_list():
    """
    Gets cities list from the api
    """
    cities = requests.get(CITY_LIST_URL).content
    cities = xmltodict.parse(cities)
    cities = cities.get('siteList') or {}
    cities = cities.get('site') or []  # list of cities w/ keys ['@code', 'nameEn', 'nameFr', 'provinceCode']
    return cities


def load_cities_list():
    """
    City config mapping load
    """
    cities = get_cities_list()
    city_mapping = {}
    for city in cities:
        city_mapping[city['@code']] = {'name': city['nameEn'], 'province_code': city['provinceCode']}
    return city_mapping


def get_city_forecast(province_code='AB', city_code='s0000001'): # TODO: Get province_code form cities_list ?
    """
    Get city weather
    """
    city_url = CITY_URL.format(province_code=province_code, city_code=city_code)
    city_weather = requests.get(city_url).content
    city_weather = city_weather.decode('utf-8').replace("Int\'l", "International")  # I.e. Macdonald-Cartier Int\'l
    city_weather = xmltodict.parse(city_weather)
    city_weather = city_weather.get('siteData') or {}
    city_weather.pop('@xsi:noNamespaceSchemaLocation', None)
    city_weather.pop('@xmlns:xsi', None)
    city_weather.pop('license', None)
    return city_weather

# TODO: need today current, then this evening, tonight, next morning, next afternoon (last 4)
# TODO: 4 day forecast
