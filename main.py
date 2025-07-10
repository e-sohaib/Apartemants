import pandas as pd
from data.data_cleaner import clean
from kluster import kluster
from regression import regr , ploter
from map import mapit
from data.crawler import scroll_and_save_tokens , Clean_tokens , get_information
names = [
    'title', 'city', 'location_lat', 'location_lon', 'price_total',
    'meterage', 'build_year', 'room_count', 'price_per_meter',
    'floor_number', 'total_floors', 'age_of_building', 'has_elevator',
    'has_parking', 'has_anbari', 'balcony', 'floor_material', 'wc_type',
    'cooling', 'heating', 'water_heater', 'document_type', 'direction',
    'renovated', 'features_score'
]

#scroll_and_save_tokens(citynumber = ['1'] ,categoryName="apartment-sell")
#Clean_tokens("apartment-sell",['1'])
#get_information("apartment-sell",['1'])
datafaram = pd.read_csv("tehran.csv", header=None  ,names = names)
mapit(datafaram)
df = clean(datafaram)
df = kluster(df)
#mapit(df)
print(regr(df))