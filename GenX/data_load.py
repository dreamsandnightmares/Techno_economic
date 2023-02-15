import os
import pandas as pd
import re
import matplotlib.pyplot as plt

path = r"/home/wch/Downloads/RECO_data/"
FileNames =os.listdir(path)

def data_load():
    x = pd.DataFrame()
    for name in  FileNames:

        if re.search('Load',name):
            full_name =os.path.join(path,name)
            pd_load =pd.read_csv(full_name,encoding='utf-8')
            pd_load = pd_load['mw'].tolist()
        elif re.search('jcpl',name):
            full_name = os.path.join(path, name)
            data = pd.read_csv(full_name,encoding='utf-8')
            x= pd.concat([x,data])
            pd_price= x['JCPL'].tolist()
            for i in  range(len(x)):
                if float(pd_price[i].strip("$")) >100:
                    pd_price[i]  =100
                else:
                    pd_price[i] = float(pd_price[i].strip("$"))
        else:
            full_name = os.path.join(path,name)

            pd_wea = pd.read_csv(full_name,encoding='utf-8')
            pd_wea_T = pd_wea['气温℃'].tolist()
            pd_wea_G_dir = pd_wea['直接辐射W/m^2'].tolist()
            pd_wea_G_diff = pd_wea['散射辐射W/m^2'].tolist()
            pd_wea_wind = pd_wea['地面风速m/s'].tolist()
    return pd_load,pd_price,pd_wea_wind,pd_wea_G_dir,pd_wea_G_diff,pd_wea_T

if __name__ == '__main__':
    pd_load,pd_price,pd_wea_wind,pd_wea_G_dir,pd_wea_G_diff,pd_wea_T = data_load()

    dist_price = list(range(len(pd_price)))

    fig,(axs1,axs2,axs3,axs4,axs5) = plt.subplots(5,1)
    axs1.plot(dist_price,pd_price)
    axs1.set_xlabel('time')
    axs1.set_ylabel('price')


    dist_load = list(range(len(pd_load)))
    axs2.plot(dist_load,pd_load)
    axs2.set_xlabel('time')
    axs2.set_ylabel('load')

    dist_G_dir = list(range(len(pd_wea_G_dir)))
    axs3.plot(dist_G_dir,pd_wea_G_dir)
    axs3.set_xlabel('time')
    axs3.set_ylabel('solar irradiance dir')

    dist_G_dif = list(range(len(pd_wea_G_diff)))
    axs4.plot(dist_G_dif,pd_wea_G_diff)
    axs4.set_xlabel('time')
    axs4.set_ylabel('solar irradiance diff')


    dist_wind = list(range(len(pd_wea_wind)))
    axs5.plot(dist_wind,pd_wea_wind)
    axs5.set_xlabel('time')
    axs5.set_ylabel('wind speed')

    fig.subplots_adjust(hspace=2)

    plt.show()
