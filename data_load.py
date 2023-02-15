import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import  os

def data_load():


    # 'PV_DATA'
    #
    df_pv1  = pd.read_csv('/home/wch/Downloads/data/weather_data.csv')
    print(df_pv1)

    pv_data_T = df_pv1['AT_temperature']
    #
    # pv_data_rad_dir = df_pv['AT_radiation_direct_horizontal']
    #
    # pv_data_rad_dif = df_pv['AT_radiation_diffuse_horizontal']
    #
    # year_pv_data_T  =pv_data_T.iloc[341880:].tolist()
    #
    # year_pv_data_red_dir  = pv_data_rad_dir.iloc[341880:].tolist()
    #
    # year_pv_data_red_dif = pv_data_rad_dif.iloc[341880:].tolist()
    df_pv = pd.read_csv('/home/wch/Downloads/XIHE_Meteorological_Data_1675306464.csv',encoding='gb18030')
    df_pv_new = df_pv.iloc[8:]
    # print(df_pv_new)
    year_pv_data_T = pv_data_T.iloc[341857:].tolist()
    pv_data_dir = df_pv_new['Unnamed: 3'].tolist()
    pv_data_dif = df_pv_new['Unnamed: 4'].tolist()
    pv_data_hor = df_pv_new['Unnamed: 2'].tolist()
    pv_data_hor2  =list(map(float,pv_data_hor))




    'POWER DATA'

    df_power  = pd.read_csv('/home/wch/Downloads/data/household_data_60min_singleindex.csv')

    power= df_power[['DE_KN_industrial3_area_room_1','DE_KN_industrial3_area_room_2','DE_KN_industrial3_area_room_3','DE_KN_industrial3_area_room_4','DE_KN_industrial3_cooling_pumps',
        'DE_KN_industrial3_machine_1','DE_KN_industrial3_machine_2','DE_KN_industrial3_machine_3','DE_KN_industrial3_machine_4','DE_KN_industrial3_machine_5','DE_KN_industrial3_dishwasher','DE_KN_industrial3_cooling_aggregate','DE_KN_industrial3_compressor','DE_KN_industrial3_ev','DE_KN_industrial3_refrigerator','DE_KN_residential1_dishwasher'\
                     ,'DE_KN_residential1_freezer','DE_KN_residential1_heat_pump','DE_KN_residential1_washing_machine','DE_KN_residential2_circulation_pump','DE_KN_residential2_dishwasher','DE_KN_residential2_freezer']]

    power_office = power.iloc[9248:18032]

    power_office['sum'] = power_office[['DE_KN_residential2_circulation_pump','DE_KN_residential2_dishwasher','DE_KN_residential1_freezer','DE_KN_residential1_heat_pump','DE_KN_residential1_washing_machine','DE_KN_residential2_circulation_pump','DE_KN_residential2_dishwasher','DE_KN_industrial3_area_room_1','DE_KN_industrial3_refrigerator','DE_KN_industrial3_machine_5','DE_KN_industrial3_cooling_pumps','DE_KN_industrial3_machine_2',
         ]].sum(axis=1)


    pds  =power_office['sum'].diff()

    power_data = pds[1:].tolist()


    # print(len(power_data))


    year_list =list(range(len(power_data)))
    'load'
    # plt.plot(year_list,power_data)
    # plt.legend()
    # plt.title('Electrical load [KW]')
    # plt.xlabel('Hour [h]')
    # plt.show()

    'T'
    # plt.plot(year_list,year_pv_data_T)
    # plt.legend()
    # plt.title('Temperature [°C]')
    # plt.xlabel('Hour [h]')
    # plt.show()
    'radiation'
    # plt.plot(year_list,pv_data_hor2)
    # plt.legend()
    # plt.title('Radiation [W/m²]')
    # plt.xlabel('Hour [h]')
    # plt.show()

    # print(sum(power_data))
    # plt.plot(year_list,year_pv_data_T)
    # plt.plot(year_list,year_pv_data_red_dif)
    return power_data,year_pv_data_T,pv_data_dir,pv_data_dif,pv_data_hor

if __name__ == '__main__':
    a =data_load()






