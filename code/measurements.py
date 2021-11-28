#!/usr/bin/env python

import pandas as pd
import geopandas as gpd

out_file='../hackathon4good2021/data/measurements_Mg.csv'

csv_files=['../data/IM_Metingen_2020/IM-Metingen_2020_1_mnd01tm-04.csv','../data/IM_Metingen_2020/IM-Metingen_2020_2_mnd05tm-07.csv','../data/IM_Metingen_2020/IM-Metingen_2020_3_mnd08tm-09.csv','../data/IM_Metingen_2020/IM-Metingen_2020_4_mnd10tm-12.csv']

df=pd.read_csv(csv_files.pop(), sep=';')
for csv_file in csv_files:
	df=df.append(pd.read_csv(csv_file, sep=';'))

df_ft=df.query("`Parameter.code`=='Mg'")[['Waterbeheerder.omschrijving', 'Meetobject.code', 'Parameter.code', 'Numeriekewaarde']]
del df_ft['Parameter.code']

df_ml=pd.read_csv('../data/Meetlocaties_2020/Meetlocaties_2020.csv', sep=';')
df_merged=pd.merge(df_ft, df_ml[['Meetobject.code','xcoordinate','ycoordinate']], right_index=False)

df_mean=df_merged.groupby(by=['Waterbeheerder.omschrijving', 'Meetobject.code', 'xcoordinate', 'ycoordinate']).mean().reset_index()
gdf=gpd.GeoDataFrame(df_mean[['Waterbeheerder.omschrijving', 'Meetobject.code', 'Numeriekewaarde']], geometry=gpd.points_from_xy(df_mean['xcoordinate'],df_mean['ycoordinate'], crs='EPSG:28992'))

df_csv=pd.DataFrame(list(map(lambda e: {'time': datetime.now().isoformat()+'Z', 'latitude': e[1]['geometry'].y, 'longitude': e[1]['geometry'].x, 'mag': e[1]['Numeriekewaarde']}, gdf.to_crs('EPSG:4326').iterrows())))

df_csv.to_csv(out_file, index=False)

