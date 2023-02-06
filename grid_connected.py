import numpy as np
import data_load
import EnergyManagementSystem
import DeviceInstantiation
import LPSP
import economic
import math
import matplotlib.pyplot as plt


PV_cap = 260

FC_cap = 45

EL_cap =160
EL_model = 'PEM'

BT_caph =645
BT_model = 'LI'

HT_caph =3160
HT_eta_fc =0.5
HT_eta_el = 0.8


power_data,pv_data_T,pv_data_dir,pv_data_dif,pv_data_hor  =data_load.data_load()

PV_Instantiate = DeviceInstantiation.PV_System(PV_cap)
PV = PV_Instantiate.PV_Instantiate()

BT_Instantiate =DeviceInstantiation.BT_System(BT_caph,BT_model)
BT =BT_Instantiate.BT_Instantiate()

HT_Instantiate =DeviceInstantiation.HT_System(HT_caph,HT_eta_el,HT_eta_fc)
HT = HT_Instantiate.HT_Instantiate()

FC_Instantiate = DeviceInstantiation.FC_System(cap=FC_cap)
FC = FC_Instantiate.FC_Instantiate()
FC_st_lifetime =FC_Instantiate.lifetime

EL_Instantiate =DeviceInstantiation.EL_System(EL_model,cap=EL_cap)
EL = EL_Instantiate.EL_Instantiate()
EL_st_litetime = EL_Instantiate.lifetime

EMS = EnergyManagementSystem.EMS_pbe(PV,BT,EL,FC,HT)
time_load = 8640

def load(fix_load):

    load = fix_load
    return fix_load
def H2_prices(price):
    H2_prices =price
    return price
def grid_prices(price):
    grid_prices = price
    return price


if __name__ == '__main__':
    fix_load = load(100)
    diff =[]
    for i in range(8640):
        x  =PV.PVpower(i)+42 -fix_load
        diff.append(x)


    h2_price = H2_prices(20)
    x_diff = list(range(len(diff)))
    plt.plot(x_diff,diff)
    plt.show()