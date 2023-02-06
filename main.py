import numpy as np
import data_load
import EnergyManagementSystem
import DeviceInstantiation
import LPSP
import economic
import math
import matplotlib.pyplot as plt

def DC_DC_converter(X):
    return X*0.965
def DC_AC_converter(X):
    return X*0.955

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


LPSP_star = 0.09

project_life = 25

OPT = economic.Lcoe(PV_cap,BT_caph,EL_cap,FC_cap,HT_caph,BT_model,EL_model)
engry =0

if __name__ == '__main__':

    EMS.Energy_Storage_initializa()
    power_all =[]
    for j in range(project_life):
        d = OPT.real_d()
        for i in range(time_load):
            RT_power_data = float(power_data[i])

