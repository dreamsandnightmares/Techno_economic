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

'cap parameter'
PV_cap = 260
E_max = 1
E_max_ra = np.arange(0, 5, 0.5)
h_ra = np.arange(0, 5, 0.5)

h = 4
time_load = 8640
project_life =20
BT_cap = PV_cap*E_max*h
ch_energy =[]
dc_energy =[]
storage_eff = 0.9
bt_action = None
BT_model  ='LI'
ems_model = 'BT'
print('PV_cap:',PV_cap)
print('E_max:',E_max)
print('h',h)
price =[]
'pv_data price_data'
power_data,pv_data_T,pv_data_dir,pv_data_dif,pv_data_hor  =data_load.data_load()
for i in range(time_load):
    price.append(GridPrice.grid_price(i))




'''
Device Instantiation
'''
PV_Instantiate = DeviceInstantiation.PV_System(PV_cap)
PV = PV_Instantiate.PV_Instantiate()

BT_Instantiate =DeviceInstantiation.BT_System(BT_cap,BT_model)
BT =BT_Instantiate.BT_Instantiate()

'''
EMS
'''
EMS = EnergyManagementSystem.EMS_grid_connect_only_bt(price,PV,BT,E_max,h,pv_cap=PV_cap)
EMS.Energy_Storage_initializa()
OPT = grid_connected.gridConnectonlyBT(price,PV,BT,E_max,h,project_life,PV_cap,BT_cap,BT_model,ems_model)
R =0
for i in range(time_load):

    RT_power_data = float(power_data[i])
    RT_PV_data = (PV.PVpower(i))
    if price[i]<=0.6:
        bt_action ='ch'
    else:
        bt_action='dis'

    EMS.Energy_evaluate(bt_action,RT_PV_data)
    dc_all ,ch_all = EMS.Energy_storage_mode(RT_PV_data,i)
    dc_energy.append(dc_all)
    ch_energy.append(ch_all)
    R += price[i]*(RT_PV_data+dc_all-ch_all/storage_eff)






LT = BT.lifetime()
BT_AT = EMS.BT_peryear_AT()
BT_lifetime = LT/BT_AT
EMS.read_energy()
if BT_lifetime < project_life:
    OPT.bt_num = 2
    print(OPT.bt_num)
    OPT.lifetime_bt = BT_lifetime * 2
cost = OPT.cost()

CRF = OPT.CRF()
X  =grid_connected.x_test(R,cost,E_max,h,CRF)

print(X)










