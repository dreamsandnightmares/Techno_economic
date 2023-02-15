import numpy as np
import data_load
from EnergyManagementSystem import EMS_OnlyBT
import DeviceInstantiation
import LPSP
import economic
import math
import matplotlib.pyplot as plt




def load(fix_load):

    load = fix_load
    return fix_load
def H2_prices(price):
    H2_prices =price
    return price
def grid_prices(price):
    grid_prices = price
    return price



"[the ratio of plant revenue to plant cost]"
class gridConnectTE():
    def __init__(self,Price,PV,bt,E_max,h,project_time,time,pv_cap,bt_cap,el_cap,fc_cap,ht_cap,bt_model,el_model,ems_model):
        self.ems_model = ems_model
        self.Price = Price
        self.PV  =PV
        self.Bt = bt
        self.E_max =E_max
        self.H= h
        self.project_time = project_time
        self.time = time
        self.power_cost_storage = None
        self.energy_cost_storage =None


        self.dr = 0.08
        self.ir = 0.03
        self.d = None
        self.project_lifetime = 20
        self.energy_tot = 0
        'cost inv [yuan]'

        self.pre_inv_LeadBT = 1490
        self.pre_inv_Li_BT = 2300
        self.pre_inv_HT = 500
        self.pre_inv_PEM_EL = 6000
        self.pre_inv_alk_EL = 3000
        self.pre_inv_PEM_FC = 1190

        'cap'
        self.PV_cap = pv_cap
        self.BT_cap = bt_cap
        self.EL_cap = el_cap
        self.FC_cap = fc_cap
        self.HT_cap = ht_cap

        'model'
        self.BT_Model = bt_model
        self.EL_Model = el_model

        'cost om'
        self.pre_PV_OM = 130
        self.li_om_cost = 60
        self.lead_om_cost = 45
        self.pre_inv_pv =6965
        self.bt_num = 1

        self.HT_rep = 0
        self.lifetime_el =None
        self.lifetime_bt = None
        self.lifetime_fc =None
        self.r_tot =0



        pass
    def R_tot(self,time):
        'discoust reward: duo fang dian de bu fen sui time + er zengda '

        if self.ems_model == 'BT':


            if self.Bt.ch[time]>=0:

                self.r_tot += self.Price[time]*(self.PV.PVpower(time)-self.Bt.ch[time]/0.9)
            else:
                self.r_tot += self.Price[time] * (self.PV.PVpower(time) - self.Bt.ch[time] )
        elif self.ems_model == 'HT':
            self.r_tot += self.Price(time) * (self.PV(time) + self.FC.power(time) - self.EL.power(time))
        else:
            self.r_tot += self.Price(time) * (self.PV(time) + self.FC.power(time) - self.EL.power(time)+self.Bt.dis(time)-self.Bt.ch(time))
    def CRF(self,i=0.05,n=20):
        crf = i*math.pow((1+i),n)/(math.pow((1+i),n)-1)
        return crf


    def cost(self):


        C_inv_tot = self.C_inv()  # investment contribution incurred by the system


        C_NPC_OM_tot = self.C_NPC_OM()  # O&M contribution incurred by the system

        C_NPC_rep_tot = self.C_NPC_rep()  # replacement contribution incurred by the system

        # C_NPC_sal_tot = self.C_NPC_sal()  # salvage contribution incurred by the system
        # print(C_NPC_sal_tot ,'sal')
        C_NPC_tot = C_inv_tot + C_NPC_OM_tot
        # C_NPC_tot = C_inv_tot + C_NPC_OM_tot + C_NPC_rep_tot - abs(C_NPC_sal_tot)


        return C_NPC_tot

    def C_inv(self,):
        """
            The output of the investment contributions(equation 30)

            Arguments:
            C_inv -- (in €) correspond to the investment contributions referred to the i-th component for the j-th year.

            Returns:
            C_inv_tot -- investment contributions
        """

        C_inv_tot = 0

        C_inv_PV =self.PV_cap*self.pre_inv_pv

        self.PV_rep = 0

        C_inv_HT = self.HT_cap*self.pre_inv_HT
        self.HT_OM = C_inv_HT*0.02
        # self.HT_rep = C_inv_HT*0.267

        if self.ems_model == 'BT':
            if self.BT_Model == 'LeadAcid':
                C_inv_BT = self.BT_cap * self.pre_inv_LeadBT * self.bt_num
                # print(C_inv_BT,'bt')
                # print(self.BT_cap*self.pre_inv_LeadBT,'not num')
                # self.BT_OM = self.BT_cap * self.pre_Lead_BT_OM*self.project_life
                self.BT_OM = C_inv_BT * 0.005
            else:
                C_inv_BT = self.BT_cap * self.pre_inv_Li_BT * self.bt_num
                # print(self.bt_num)
                # self.BT_OM = self.BT_cap * self.pre_Li_BT_OM*self.project_life
                self.BT_OM = C_inv_BT * 0.005
                # print(C_inv_BT, 'bt')
                # print(self.BT_cap * self.pre_inv_LeadBT, 'not num')

            self.BT_rep = C_inv_BT * 0.5
            C_inv_tot =  C_inv_PV + + C_inv_BT
        elif self.ems_model == 'HT':
            if self.EL_Model == 'PEM':
                # C_inv_EL = self.EL_cap*self.pre_inv_PEM_EL
                C_inv_EL = self.EL_cap * self.pre_inv_PEM_EL
                # print('C_el:',C_inv_EL)
                self.EL_OM = C_inv_EL * 0.04
                self.EL_rep = C_inv_EL * 0.267

            else:
                # C_inv_EL = self.c_inv(self.EL_Model,self.EL_cap)
                C_inv_EL = self.EL_cap * self.pre_inv_alk_EL
                self.EL_OM = C_inv_EL * 0.04
                self.EL_rep = C_inv_EL * 0.267

            C_inv_FC = self.FC_cap * self.pre_inv_PEM_FC
            # print('C_el:', C_inv_FC)

            self.PEM_FC_OM = C_inv_FC * 0.04
            self.FC_rep = C_inv_FC * 0.267

            C_inv_tot = C_inv_HT + C_inv_FC + C_inv_PV + C_inv_EL
        else:

            if self.BT_Model =='LeadAcid':
                C_inv_BT =self.BT_cap*self.pre_inv_LeadBT*self.bt_num
                # print(C_inv_BT,'bt')
                # print(self.BT_cap*self.pre_inv_LeadBT,'not num')
                # self.BT_OM = self.BT_cap * self.pre_Lead_BT_OM*self.project_life
                self.BT_OM = C_inv_BT * 0.005

            else:
                C_inv_BT = self.BT_cap*self.pre_inv_Li_BT*self.bt_num
                # print(self.bt_num)
                # self.BT_OM = self.BT_cap * self.pre_Li_BT_OM*self.project_life
                self.BT_OM = C_inv_BT*0.005
                # print(C_inv_BT, 'bt')
                # print(self.BT_cap * self.pre_inv_LeadBT, 'not num')

            self.BT_rep = C_inv_BT*0.5




            if self.EL_Model =='PEM':
                # C_inv_EL = self.EL_cap*self.pre_inv_PEM_EL
                C_inv_EL = self.EL_cap * self.pre_inv_PEM_EL
                # print('C_el:',C_inv_EL)
                self.EL_OM = C_inv_EL * 0.04
                self.EL_rep = C_inv_EL * 0.267

            else:
                # C_inv_EL = self.c_inv(self.EL_Model,self.EL_cap)
                C_inv_EL = self.EL_cap*self.pre_inv_alk_EL
                self.EL_OM = C_inv_EL * 0.04
                self.EL_rep = C_inv_EL * 0.267

            C_inv_FC =self.FC_cap*self.pre_inv_PEM_FC
            # print('C_el:', C_inv_FC)

            self.PEM_FC_OM =C_inv_FC*0.04
            self.FC_rep = C_inv_FC*0.267

            C_inv_tot = C_inv_HT+C_inv_FC+C_inv_PV+C_inv_EL+C_inv_BT
        # print(C_inv_PV,'guangfu ')
        # print(C_inv_HT,'HT')
        # print(C_inv_FC,'fc')
        # print(C_inv_EL,'el')
        # print(C_inv_BT,'bt')


        return C_inv_tot

    def C_NPC_OM(self,):
        """
            The output of the O&M contribution(equation 31)

            Arguments:
            C_OM -- (in €) correspond to the OM contributions referred to the i-th component for the j-th year.


            Returns:
            C_NPC_OM_tot -- O&M contribution
        """
        if self.ems_model =='BT':
            C_NPC_OM_tot =  self.BT_OM +  self.pre_PV_OM
        elif self.ems_model == 'HT':
            C_NPC_OM_tot = self.PEM_FC_OM + self.EL_OM + self.HT_OM + self.pre_PV_OM
        else:

            C_NPC_OM_tot = self.PEM_FC_OM+self.BT_OM+self.EL_OM+self.HT_OM+self.pre_PV_OM

        # print(C_NPC_OM_tot,'C_NPC_OM_tot')


        # for j in range(self.project_life):
        #
        #     C_NPC_OM_tot += C_NPC_OM_tot / math.pow((1 + self.d), j)
        # print(self.PEM_FC_OM, self.BT_OM, self.EL_OM, self.HT_OM, self.pre_PV_OM)
        # print(C_NPC_OM_tot,'om')
        return C_NPC_OM_tot
    def C_NPC_rep(self, ):
        """
            The output of the replacement contributions(equation 32)

            Arguments:
            C_rep -- (in €) correspond to the replacement contributions referred to the i-th component for the j-th year.

            Returns:
            C_NPC_rep_tot -- replacement contributions
        """
        if self.ems_model =='BT':

            C_NPC_rep_tot = self.BT_rep+self.PV_rep
        elif self.ems_model =='HT':
            C_NPC_rep_tot = self.EL_rep + self.FC_rep  + self.PV_rep + self.HT_rep
        else:
            C_NPC_rep_tot = self.EL_rep + self.FC_rep + self.BT_rep + self.PV_rep + self.HT_rep



        # for j in range(self.project_life):
        #     C_NPC_rep_tot += C_NPC_rep_tot / math.pow((1 + self.d), j)


        return C_NPC_rep_tot
    def C_NPC_sal(self,):
        """
            The output of the salvage contributions(equation 33)

            Arguments:
            C_sal -- (in €) correspond to the salvage contributions referred to the i-th component for the j-th year.

            Returns:
            C_NPC_sal_tot -- salvage contributions
        """
        if self.ems_model =='BT':
            C_NPC_sal_bt = abs(self.BT_rep * ((self.lifetime_bt - 20) / 20))
            C_NPC_sal_tot =  C_NPC_sal_bt
        elif self.ems_model =='HT':
            C_NPC_sal_el = abs(self.EL_rep * (1 - self.lifetime_el / 40000))
            C_NPC_sal_fc = abs(self.FC_rep * (1 - self.lifetime_fc / 30000))
            C_NPC_sal_tot = C_NPC_sal_el  + C_NPC_sal_fc
        else:




            C_NPC_sal_el  =abs(self.EL_rep*(1-self.lifetime_el/40000))
            C_NPC_sal_fc = abs(self.FC_rep*(1-self.lifetime_fc/30000))
            C_NPC_sal_bt = abs(self.BT_rep*((self.lifetime_bt-20)/20))

            C_NPC_sal_tot = C_NPC_sal_el+C_NPC_sal_bt+C_NPC_sal_fc




        # C_NPC_sal_tot = C_NPC_sal_tot / math.pow((1 + self.d), self.project_life)


        return C_NPC_sal_tot
    def C_BT(self):
        if self.BT_Model == 'LeadAcid':
            C_inv_BT = self.BT_cap * self.pre_inv_LeadBT * self.bt_num
            # print(C_inv_BT,'bt')
            # print(self.BT_cap*self.pre_inv_LeadBT,'not num')
            # self.BT_OM = self.BT_cap * self.pre_Lead_BT_OM*self.project_life
            self.BT_OM = C_inv_BT * 0.005
        else:
            C_inv_BT = self.BT_cap * self.pre_inv_Li_BT * self.bt_num
            # print(self.bt_num)
            # self.BT_OM = self.BT_cap * self.pre_Li_BT_OM*self.project_life
            self.BT_OM = C_inv_BT * 0.005
            # print(C_inv_BT, 'bt')
            # print(self.BT_cap * self.pre_inv_LeadBT, 'not num')
        return C_inv_BT

class gridConnectonlyBT():
    def __init__(self,Price,PV,bt,E_max,h,project_time,pv_cap,bt_cap,bt_model,ems_model):
        self.ems_model = ems_model
        self.Price = Price
        self.PV  =PV
        self.Bt = bt
        self.E_max =E_max
        self.H= h
        self.project_time = project_time

        self.power_cost_storage = None
        self.energy_cost_storage =None


        self.dr = 0.08
        self.ir = 0.03
        self.d = None
        self.project_lifetime = 20
        self.energy_tot = 0
        'cost inv [yuan]'

        # self.pre_inv_LeadBT = C_storage
        # self.pre_inv_LeadBT_power = C_power
        self.pre_inv_Li_BT = 2300
        self.pre_inv_HT = 500
        self.pre_inv_PEM_EL = 6000
        self.pre_inv_alk_EL = 3000
        self.pre_inv_PEM_FC = 1190

        'cap'
        self.PV_cap = pv_cap
        self.BT_cap = bt_cap

        'model'
        self.BT_Model = bt_model


        'cost om'
        self.pre_PV_OM = 130
        self.li_om_cost = 60
        self.lead_om_cost = 45
        self.pre_inv_pv =6965
        self.bt_num = 1



        self.lifetime_bt = None

        self.r_tot =0




    def R_tot(self,time):
        'discoust reward: duo fang dian de bu fen sui time + er zengda '

        if self.ems_model == 'BT':


            if self.Bt.ch[time]>=0:

                self.r_tot += self.Price[time]*(self.PV.PVpower(time)-self.Bt.ch[time]/0.9)
            else:
                self.r_tot += self.Price[time] * (self.PV.PVpower(time) - self.Bt.ch[time] )
        elif self.ems_model == 'HT':
            self.r_tot += self.Price(time) * (self.PV(time) + self.FC.power(time) - self.EL.power(time))
        else:
            self.r_tot += self.Price(time) * (self.PV(time) + self.FC.power(time) - self.EL.power(time)+self.Bt.dis(time)-self.Bt.ch(time))
    def CRF(self,i=0.05,n=20):
        crf = i*math.pow((1+i),n)/(math.pow((1+i),n)-1)
        return crf


    def cost(self):


        C_inv_tot = self.C_inv()  # investment contribution incurred by the system


        C_NPC_OM_tot = self.C_NPC_OM()  # O&M contribution incurred by the system

        C_NPC_rep_tot = self.C_NPC_rep()  # replacement contribution incurred by the system

        # C_NPC_sal_tot = self.C_NPC_sal()  # salvage contribution incurred by the system
        # print(C_NPC_sal_tot ,'sal')
        C_NPC_tot = C_inv_tot + C_NPC_OM_tot
        # C_NPC_tot = C_inv_tot + C_NPC_OM_tot + C_NPC_rep_tot - abs(C_NPC_sal_tot)


        return C_NPC_tot

    def C_inv(self,):
        """
            The output of the investment contributions(equation 30)

            Arguments:
            C_inv -- (in €) correspond to the investment contributions referred to the i-th component for the j-th year.

            Returns:
            C_inv_tot -- investment contributions
        """

        C_inv_tot = 0

        C_inv_PV =self.PV_cap*self.pre_inv_pv

        self.PV_rep = 0


        if self.ems_model == 'BT':
            if self.BT_Model == 'LeadAcid':
                C_inv_BT = self.BT_cap * self.pre_inv_LeadBT * self.bt_num
                self.BT_OM = C_inv_BT * 0.005
            else:
                C_inv_BT = self.BT_cap * self.pre_inv_Li_BT * self.bt_num
                self.BT_OM = C_inv_BT * 0.005
            self.BT_rep = C_inv_BT * 0.5
            C_inv_tot =  C_inv_PV + + C_inv_BT

        return C_inv_tot

    def C_NPC_OM(self,):
        """
            The output of the O&M contribution(equation 31)

            Arguments:
            C_OM -- (in €) correspond to the OM contributions referred to the i-th component for the j-th year.


            Returns:
            C_NPC_OM_tot -- O&M contribution
        """

        C_NPC_OM_tot =  self.BT_OM +  self.pre_PV_OM

        return C_NPC_OM_tot
    def C_NPC_rep(self, ):
        """
            The output of the replacement contributions(equation 32)

            Arguments:
            C_rep -- (in €) correspond to the replacement contributions referred to the i-th component for the j-th year.

            Returns:
            C_NPC_rep_tot -- replacement contributions
        """

        C_NPC_rep_tot = self.BT_rep+self.PV_rep




        # for j in range(self.project_life):
        #     C_NPC_rep_tot += C_NPC_rep_tot / math.pow((1 + self.d), j)


        return C_NPC_rep_tot
    def C_NPC_sal(self,):
        """
            The output of the salvage contributions(equation 33)

            Arguments:
            C_sal -- (in €) correspond to the salvage contributions referred to the i-th component for the j-th year.

            Returns:
            C_NPC_sal_tot -- salvage contributions
        """

        C_NPC_sal_bt = abs(self.BT_rep * ((self.lifetime_bt - 20) / 20))
        C_NPC_sal_tot =  C_NPC_sal_bt





        # C_NPC_sal_tot = C_NPC_sal_tot / math.pow((1 + self.d), self.project_life)


        return C_NPC_sal_tot
    def C_BT(self):
        if self.BT_Model == 'LeadAcid':
            C_inv_BT = self.BT_cap * self.pre_inv_LeadBT * self.bt_num
            self.BT_OM = C_inv_BT * 0.005
        else:
            C_inv_BT = self.BT_cap * self.pre_inv_Li_BT * self.bt_num
            self.BT_OM = C_inv_BT * 0.005
        return C_inv_BT

    def C_inv_gen(self):
        C_inv_gen = (self.PV_cap * self.pre_inv_pv +self.pre_PV_OM*self.PV_cap)/self.PV_cap

        return C_inv_gen

    def C_power_storage(self):
        pass

















# def x_test(R_all,cost_all,E_max,h,crf):
#     X = R_all / ((cost_all + E_max * (100 + h * 100)) * crf)
#     return X


def x_test(R_all,E_max,h,crf):
    X = R_all / ((1 + E_max * (100 + h * 100)) * crf)
    return X

def grid_price(time):
    price = 0
    if 5 <= int(time/(30*24))<9 or int(time/(30*24)) ==10 :
        if 12<=time%24 <14:
            price =2
            pass
        elif 8<= time%24<12 or 14<=time%24<15 or 18<=time%24<21:
            price =1.3
            pass
        elif 6<= time%24<8 or 15<=time%24<18 or 21<=time%24<22:
            price =0.6
            pass
        elif 0<= time%24<6 or 22<=time%24<24:
            price =0.3
    elif int(time/(30*24))==9 :
        if 8<=time%24 <15 or 18<=time%24 <21 :
            price= 1.3
        elif 6<=time%24 <8 or 15<=time%24 <18 or 21<=time%24 <22:
            price = 0.6
        elif 0<=time%24 <6 or 22<=time%24 <24:
            price = 0.3
    elif int(time/(30*24)) ==12 or int(time/30/24)==1:
        if  19<=time%24 <21:
            price = 2
        elif  8<=time%24 <11 or 18<=time%24 <19:
            price = 1.3
        elif   6<=time%24 <8 or 11<=time%24 <18 or  21<=time%24 <22:
            price = 0.6
        elif 0<=time%24 <6 or 22<=time%24 <24:
            price = 0.3
    else:
        if 8 <= time % 24 < 11 or   18<=time%24 <19:
            price = 1.3
        elif 6 <= time % 24 < 8 or   11<=time%24 <18 or 21<=time%24 <22 :
            price = 0.6
        else:
            price = 0.3
    return price













if __name__ == '__main__':

    PV_cap = 260

    FC_cap = 45

    EL_cap = 160
    EL_model = 'PEM'

    BT_caph = 400
    BT_model = 'LI'

    HT_caph = 3160
    HT_eta_fc = 0.5
    HT_eta_el = 0.8
    project_life = 20

    power_data, pv_data_T, pv_data_dir, pv_data_dif, pv_data_hor = data_load.data_load()

    PV_Instantiate = DeviceInstantiation.PV_System(PV_cap)
    PV = PV_Instantiate.PV_Instantiate()

    BT_Instantiate = DeviceInstantiation.BT_System(BT_caph, BT_model)
    BT = BT_Instantiate.BT_Instantiate()

    HT_Instantiate = DeviceInstantiation.HT_System(HT_caph, HT_eta_el, HT_eta_fc)
    HT = HT_Instantiate.HT_Instantiate()

    FC_Instantiate = DeviceInstantiation.FC_System(cap=FC_cap)
    FC = FC_Instantiate.FC_Instantiate()
    FC_st_lifetime = FC_Instantiate.lifetime

    EL_Instantiate = DeviceInstantiation.EL_System(EL_model, cap=EL_cap)
    EL = EL_Instantiate.EL_Instantiate()
    EL_st_litetime = EL_Instantiate.lifetime

    time_load = 8640


    price= []
    fix_load = load(100)
    diff =[]
    for i in range(8640):
        x  =PV.PVpower(i)+42 -fix_load
        diff.append(x)
        price.append(grid_price(i))


    h2_price = H2_prices(20)
    x_diff = list(range(len(price)))
    EMS = gridConnectTE(Price=price,PV=PV,bt=BT,E_max=1,h=4,project_time=20,time=time_load,pv_cap=PV_cap,
                         bt_cap=BT_caph,el_cap=EL_cap,fc_cap=FC_cap,ht_cap=HT_caph,el_model=EL_model,bt_model=BT_model,ems_model='BT')
    ems = EMS_OnlyBT(bt=BT,pv=PV)
    E_max_ra = np.arange(0, 5, 0.5)
    h = np.arange(0, 5, 0.5)
    x_e, Y = np.meshgrid(E_max_ra, h)


    for j in range(project_life):
        ems.Energy_Storage_initializa()
        power_all = []
        R = 0
        R_all = []
        for i in range(time_load):
            RT_PV_data = (PV.PVpower(i))
            RT_power_data = float(power_data[i])
            ems.Energy_storage_mode(power_data=RT_power_data,pv_power=RT_PV_data)
            EMS.lifetime_bt =  ems.BT_worktime()

        for i in range(time_load):
            EMS.R_tot(i)

    Re = EMS.r_tot
    E_max_ra = np.arange(0, 5, 0.5)
    h = np.arange(0, 5, 0.5)
    x_e, Y = np.meshgrid(E_max_ra, h)
    cost = EMS.cost()
    cost_bt = EMS.C_BT()




    crf = EMS.CRF()
    print(Re/20)

    Z = 1*x_e+2*Y
    ctf = plt.contourf(Y,x_e , Z, 15, cmap='RdGy')

    # ct = plt.contour(x_e, Y, Z, 15, colors='k')  # 等高线设置成黑色
    # plt.clabel(ct, inline=True, fontsize=10)  # 添加标签
    # plt.pcolormesh(X, Y, Z)     # 绘制分类背景图
    plt.colorbar()  # 添加cbar
    plt.xlabel(('storage time'))  # 去掉x标签
    plt.ylabel(('storage ratio'))  # 去掉y标签
    plt.show()
    Z = []
    Z_X = []
    for i in range(len(E_max_ra)):
        Z_X =[]
        for j in range(len(h)):

            Z_X.append(1*E_max_ra[i]+2*h[j])
        Z.append(Z_X)

    ctf = plt.contourf(x_e, Y, Z, 15, cmap='RdGy')
    plt.colorbar()  # 添加cbar
    plt.xlabel(('storage time'))  # 去掉x标签
    plt.ylabel(('storage ratio'))  # 去掉y标签
    plt.show()




















