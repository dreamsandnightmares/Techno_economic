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
PV_cap = 100
# E_max = 1
E_max_ra = np.arange(0.1, 4, 0.25)
h_ra = np.arange(0.1, 4, 0.25)
time_load = 100
project_life =20
ch_energy =[]
dc_energy =[]
storage_eff = 0.9
bt_action = None
BT_model  ='LI'
ems_model = 'BT'
price =[]
power_data,pv_data_T,pv_data_dir,pv_data_dif,pv_data_hor  =data_load.data_load()
for i in range(time_load):
    price.append(GridPrice.grid_price(i))
x_e, Y = np.meshgrid(E_max_ra, h_ra)
Z = []
Z_X =[]
RT_pv_data_all = []
def cost_all(e,h):
    PV_Instantiate = DeviceInstantiation.PV_System(PV_cap)
    PV = PV_Instantiate.PV_Instantiate()
    BT_cap = PV_cap * e * h
    BT_Instantiate = DeviceInstantiation.BT_System(BT_cap, BT_model)
    BT = BT_Instantiate.BT_Instantiate()

    EMS = EnergyManagementSystem.EMS_grid_connect_only_bt(price, PV, BT, e, h, pv_cap=PV_cap)
    EMS.Energy_Storage_initializa()

    OPT = grid_connected.gridConnectonlyBT(price, PV, BT, e, h, project_life, PV_cap, BT_cap, BT_model, ems_model)
    R = 0
    for i in range(time_load):

        RT_power_data = float(power_data[i])
        RT_PV_data = (PV.PVpower(i))
        RT_pv_data_all.append(RT_PV_data)

        if price[i] <= 0.6:
            bt_action = 'ch'
        else:
            bt_action = 'dis'

        EMS.Energy_evaluate(bt_action, RT_PV_data)
        dc_all, ch_all = EMS.Energy_storage_mode(RT_PV_data, i)
        dc_energy.append(dc_all)
        ch_energy.append(ch_all)
        R += price[i] * (RT_PV_data + dc_all - ch_all / storage_eff)
    R = R/ (sum(RT_pv_data_all)+sum(dc_energy)-sum(ch_energy)/storage_eff)

    LT = BT.lifetime()
    BT_AT = EMS.BT_peryear_AT()
    BT_lifetime = LT / BT_AT
    EMS.read_energy()
    if BT_lifetime < project_life:
        OPT.bt_num = 2
        print(OPT.bt_num)
        OPT.lifetime_bt = BT_lifetime * 2
    cost = OPT.cost()

    CRF = OPT.CRF()
    X = grid_connected.x_test(R, e, h, CRF)
    return X
for i in range(len(E_max_ra)):
    Z_X =[]
    for j in range(len(h_ra)):

        Z_X.append(cost_all(E_max_ra[i],h_ra[j]))
    Z.append(Z_X)




ctf = plt.contourf( Y,x_e, Z, 10, cmap='RdGy')


plt.colorbar()  # 添加cbar
plt.xlabel(('storage time'))  # 去掉x标签
plt.ylabel(('storage ratio'))  # 去掉y标签
plt.show()
print(Z)






# def x_cum(e,h):
#     x_all = []
#     for i in range(8064):
#         price = 0
#         X_gen =0
#         for j in range(504):
#             price +=GridPrice.grid_price(i+j)
#             X_gen += GridPrice.grid_price(i+j)*pv.PVpower(i+j)
#
#
#         per_x_gen = X_gen/pv_cap/price
#         z = np.array([1, -0.9])
#         A_ub = np.array([[-1, 1], [1, -1]])
#         b_ub = np.array([e*h, 0])
#         bounds = [0, e], [0, min(0.9*e, per_x_gen)]
#         res = op.linprog(-z, A_ub, b_ub, bounds=bounds)
#         x_rel = (-res.fun+per_x_gen)*price
#         x_all.append(x_rel)
#
#         i +=336
#
#     return sum(x_all)/len(x_all)
# E_max_ra = np.arange(0.1, 4, 0.25)
# h_ra = np.arange(2, 3, 0.5)
# Z = []
# for i in range(len(E_max_ra)):
#     Z_X =[]
#     for j in range(len(h_ra)):
#         R = x_cum(E_max_ra[i],h_ra[j])
#
#         Z_X.append(x(R,crf=CRF(),E_max=E_max_ra[i],h=h_ra[j]))
#     Z.append(Z_X)
# Z = np.array(Z)
# z = Z.T
# z = z.tolist()
# ctf = plt.contourf( h_ra,E_max_ra, z, 10, cmap='RdGy')
#
#
# plt.colorbar()  # 添加cbar
# plt.xlabel(('storage time'))  # 去掉x标签
# plt.ylabel(('storage ratio'))  # 去掉y标签
# plt.show()
# print(Z)







