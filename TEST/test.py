from sympy import *
import numpy as np
import data_load
import EnergyManagementSystem
import DeviceInstantiation
import LPSP
import economic
import math
import matplotlib.pyplot as plt
import GridPrice
import grid_connected
import Pvsystem
import pandas as pd

from scipy import optimize as op
pv_cap =150
pv = Pvsystem.PVSystem(P_PV_rated=pv_cap)
# 'cap parameter'
# PV_cap = 260
# # E_max = 1
# E_max_ra = np.arange(0, 5, 0.5)
# h_ra = np.arange(0, 5, 0.5)
# time_load = 8640
# project_life =20
# ch_energy =[]
# dc_energy =[]
# storage_eff = 0.9
# bt_action = None
# BT_model  ='LI'
# ems_model = 'BT'
# price =[]
# power_data,pv_data_T,pv_data_dir,pv_data_dif,pv_data_hor  =data_load.data_load()
# for i in range(time_load):
#     price.append(GridPrice.grid_price(i))
# x_e, Y = np.meshgrid(E_max_ra, h_ra)
#
# def cost_all(e,h):
#     PV_Instantiate = DeviceInstantiation.PV_System(PV_cap)
#     PV = PV_Instantiate.PV_Instantiate()
#     BT_cap = PV_cap * e * h
#     BT_Instantiate = DeviceInstantiation.BT_System(BT_cap, BT_model)
#     BT = BT_Instantiate.BT_Instantiate()
#
#     EMS = EnergyManagementSystem.EMS_grid_connect_only_bt(price, PV, BT, x_e, Y, pv_cap=PV_cap)
#     EMS.Energy_Storage_initializa()
#
#     OPT = grid_connected.gridConnectonlyBT(price, PV, BT, x_e, Y, project_life, PV_cap, BT_cap, BT_model, ems_model)
#     R = 0
#     for i in range(time_load):
#
#         RT_power_data = float(power_data[i])
#         RT_PV_data = (PV.PVpower(i))
#         if price[i] <= 0.6:
#             bt_action = 'ch'
#         else:
#             bt_action = 'dis'
#
#         EMS.Energy_evaluate(bt_action, RT_PV_data)
#         dc_all, ch_all = EMS.Energy_storage_mode(RT_PV_data, i)
#         dc_energy.append(dc_all)
#         ch_energy.append(ch_all)
#         R += price[i] * (RT_PV_data + dc_all - ch_all / storage_eff)
#
#     LT = BT.lifetime()
#     BT_AT = EMS.BT_peryear_AT()
#     BT_lifetime = LT / BT_AT
#     EMS.read_energy()
#     if BT_lifetime < project_life:
#         OPT.bt_num = 2
#         print(OPT.bt_num)
#         OPT.lifetime_bt = BT_lifetime * 2
#     cost = OPT.cost()
#
#     CRF = OPT.CRF()
#     X = grid_connected.x_test(R, cost, e, h, CRF)
#     return X

def CRF(i=0.05, n=20):
    crf = i * math.pow((1 + i), n) / (math.pow((1 + i), n) - 1)
    return crf

def x (R,crf,E_max,h):
    x = R /((1.05+E_max*(1743+h*1190))*crf)
    return x


# z = np.array([1,-0.9])
#
# A_ub = np.array([[-1,1],[1,-1]])
# b_ub =np.array([1,0])
# bounds =[0,1],[0,min(0.9,0.24)]
# res = op.linprog(-z,A_ub,b_ub,bounds=bounds)
# print(f"目标函数的最大值z={-res.fun:.2f}，此时目标函数的决策变量为{res.x.round(2)}")
# print(-res.fun)






df_load  = pd.read_csv('/home/wch/Downloads/RECO_data/hrl_load_metered-RECO.csv')
print(df_load['mw'])
o =df_load['mw'].tolist()
dist = list(range(len(o)))
plt.plot(dist,o)
plt.show()

df_









