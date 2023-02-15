import math

class EMS_pbe():
    def __init__(self,pv,bt,el,fc,ht):
        self.pv  =pv
        self.bt = bt
        self.el =el
        self.fc= fc
        self.ht= ht
        self.offEnergy =[]



        self.offLoad =0
        self.energyToPower =0
        self.bt_eta_ch  = self.bt.readEta_ch()
        self.bt_eta_dc  =self.bt.readEta_dc()
        self.bt_conv  =self.bt.readEta_conv()





    def DC_DC_converter(self,x):
        return x*0.965
    def DC_AC_converter(self,x):
        return x*0.955

    def Energy_Storage_initializa(self):

        self.offlaod = []
        self.offLoad =0
        self.energyToPower =0


        self.BT_lifetime = 0
        self.EL_lifetime = 0
        self.FC_lifetime = 0
        self.HT_lifetime = 0
        self.BT_AT = 0
    def Energy_storage_mode(self,power_data,pv_power):

        'main bus'
        RT_power = self.DC_DC_converter(pv_power)

        'main bus energy'
        energy =RT_power - power_data/0.955

        Battery_SOC = self.bt.readSoc()
        Battery_SOC_max =self.bt.max_soc()
        Battery_SOC_min = self.bt.min_soc()

        Hydrogen_SOC  =self.ht.Loh_t()
        Hydrogen_SOC_max = self.ht.max_loh()
        Hydrogen_SOC_min =self.ht.min_loh()

        if energy ==0:
            self.energyToPower += power_data
        elif energy >0:
            'charge model'
            Battery_SOC = self.bt.readSoc()
            if Battery_SOC < Battery_SOC_max:
                bt_max_charge_energy = self.bt.max_charge()
                if self.DC_DC_converter(energy) <= bt_max_charge_energy:
                    self.bt.SOC(P_ch=self.DC_DC_converter(energy),P_dc=0)
                    self.BT_AT+= self.DC_DC_converter(energy)*self.bt_eta_ch*self.bt_conv
                    self.energyToPower+=power_data
                    self.BT_lifetime +=1
                    self.BT_AT += self.DC_DC_converter(energy)*self.bt_eta_ch*self.bt_conv
                else:
                    self.bt.SOC(P_ch=bt_max_charge_energy,P_dc=0)
                    self.BT_AT += bt_max_charge_energy * self.bt_eta_ch * self.bt_conv
                    self.energyToPower+=power_data
                    self.BT_lifetime += 1
                    self.BT_AT += bt_max_charge_energy * self.bt_eta_ch * self.bt_conv

                    energyToel = self.DC_DC_converter((self.DC_DC_converter(energy)-bt_max_charge_energy)/0.965)
                    H2Tank_max_ch = self.ht.max_charge()
                    if energyToel <= H2Tank_max_ch:

                        eff_el  =self.el.efficiency()

                        self.ht.LevelOfHydrogen(P_el=energyToel,P_fc=0,eff_el=eff_el,eff_fc=0)



                        self.EL_lifetime+=1
                        self.HT_lifetime +=1
                    else:
                        self.energyToPower +=power_data
                        eff_el  =self.el.efficiency()
                        self.ht.LevelOfHydrogen(P_el=H2Tank_max_ch,P_fc=0,eff_el=eff_el,eff_fc=0)
                        self.EL_lifetime+=1
                        self.HT_lifetime+=1

                        offEnergy = (energyToel-H2Tank_max_ch)/0.965/0.965
                        self.offEnergy.append(offEnergy)

            else:
                H2Tank_max_ch = self.ht.max_charge()
                energyToel = self.DC_DC_converter(energy)
                if energyToel <= H2Tank_max_ch:
                    self.energyToPower+=power_data
                    eff_el = self.el.efficiency()
                    self.ht.LevelOfHydrogen(P_el=energyToel, P_fc=0, eff_el=eff_el, eff_fc=0)

                    self.EL_lifetime+=1
                    self.HT_lifetime+=1

                else:
                    self.energyToPower += power_data
                    eff_el =self.el.efficiency()
                    self.ht.LevelOfHydrogen(P_el=H2Tank_max_ch, P_fc=0, eff_el=eff_el, eff_fc=0)

                    self.EL_lifetime+=1
                    self.HT_lifetime += 1

                    offEnergy = (energyToel-H2Tank_max_ch)/0.965/0.965
                    self.offEnergy.append(offEnergy)
        else:
            Battery_SOC = self.bt.readSoc()
            if Battery_SOC >Battery_SOC_min:
                bt_max_discharge_energy = self.bt.max_discharge()

                BtToLoad_max = (self.DC_DC_converter(bt_max_discharge_energy))

                if abs(energy)<=BtToLoad_max:
                    self.bt.SOC(P_ch=0,P_dc=self.DC_DC_converter(abs(energy)))
                    self.BT_AT += self.DC_DC_converter(abs(energy)) /(self.bt_eta_dc * self.bt_conv)
                    self.energyToPower +=power_data

                    self.BT_lifetime+=1
                else:
                    self.bt.SOC(P_ch=0,P_dc=(bt_max_discharge_energy))
                    self.BT_AT += bt_max_discharge_energy / (self.bt_eta_dc * self.bt_conv)
                    H2ToPower = (abs(energy) - self.DC_DC_converter(bt_max_discharge_energy))/0.965
                    self.BT_lifetime += 1
                    H2ToPower_max = self.ht.max_dischage()

                    if H2ToPower <=H2ToPower_max:
                        eff_fc =self.fc.efficiency()
                        self.ht.LevelOfHydrogen(P_el=0, P_fc=H2ToPower, eff_el=0, eff_fc=eff_fc)
                        self.FC_lifetime+=1
                        self.HT_lifetime+=1
                        self.energyToPower+=power_data
                    else:
                        eff_fc = self.fc.efficiency()
                        self.ht.LevelOfHydrogen(P_el=0, P_fc=H2ToPower_max, eff_el=0, eff_fc=eff_fc)
                        self.FC_lifetime += 1
                        self.HT_lifetime += 1
                        self.energyToPower += self.DC_AC_converter(self.DC_DC_converter(H2ToPower_max))
                        self.offLoad +=self.DC_AC_converter(abs(energy)-self.DC_DC_converter(H2ToPower_max))
            else:
                H2ToPower_max = self.ht.max_dischage()
                if abs(energy)<= self.DC_DC_converter(H2ToPower_max):
                    eff_fc = self.fc.efficiency()
                    self.ht.LevelOfHydrogen(P_el=0, P_fc=abs(energy), eff_el=0, eff_fc=eff_fc)
                    self.energyToPower += power_data
                    self.FC_lifetime+=1
                    self.HT_lifetime += 1
                else:
                    eff_fc = self.fc.efficiency()
                    self.ht.LevelOfHydrogen(P_el=0, P_fc=H2ToPower_max, eff_el=0, eff_fc=eff_fc)
                    self.energyToPower += self.DC_AC_converter(self.DC_DC_converter(H2ToPower_max))
                    self.FC_lifetime += 1
                    self.HT_lifetime += 1
                    self.offLoad+= self.DC_AC_converter(abs(energy)-self.DC_DC_converter(H2ToPower_max))


    def offload(self):
        return self.offLoad
    def offenergy(self):
        return sum(self.offEnergy)
    def engrgyToPower(self):
        return self.energyToPower
    def FC_worktime(self):
        return self.FC_lifetime
    def EL_worktime(self):
        return self.EL_lifetime
    def HT_worktime(self):
        return self.HT_lifetime
    def BT_worktime(self):
        return self.BT_lifetime
    def readAt(self):
        return self.BT_AT



class EMS_OnlyBT():
    def __init__(self,pv,bt,):
        self.pv  =pv
        self.bt = bt
        self.offEnergy =[]

        self.offLoad = 0
        self.energyToPower = 0
        self.bt_eta_ch = self.bt.readEta_ch()
        self.bt_eta_dc = self.bt.readEta_dc()
        self.bt_conv = self.bt.readEta_conv()
    def DC_DC_converter(self,x):
        return x*0.965
    def DC_AC_converter(self,x):
        return x*0.955

    def Energy_Storage_initializa(self):



        self.BT_lifetime = 0
        self.BT_AT = 0
        self.offLoad =0
        self.energyToPower =0
        self.bt.soc = 0.5
    def Energy_storage_mode(self,power_data,pv_power):

        'main bus'
        RT_power = self.DC_DC_converter(pv_power)

        'main bus energy'
        energy =RT_power - power_data/0.955

        Battery_SOC = self.bt.readSoc()
        Battery_SOC_max =self.bt.max_soc()
        Battery_SOC_min = self.bt.min_soc()
        if energy == 0:
            self.energyToPower += power_data
        elif energy > 0:
            'charge model'
            Battery_SOC = self.bt.readSoc()
            if Battery_SOC < Battery_SOC_max:
                bt_max_charge_energy = self.bt.max_charge()

                if self.DC_DC_converter(energy) <= bt_max_charge_energy:
                    self.bt.SOC(P_ch=self.DC_DC_converter(energy), P_dc=0)
                    self.bt.ch.append(self.DC_DC_converter(energy))
                    self.BT_AT += self.DC_DC_converter(energy) * self.bt_eta_ch * self.bt_conv
                    self.energyToPower += power_data
                    self.BT_lifetime += 1
                    self.BT_AT += self.DC_DC_converter(energy) * self.bt_eta_ch * self.bt_conv
                else:
                    self.bt.SOC(P_ch=bt_max_charge_energy, P_dc=0)
                    self.bt.ch.append(self.DC_DC_converter(energy))
                    self.BT_AT += bt_max_charge_energy * self.bt_eta_ch * self.bt_conv
                    self.energyToPower += power_data
                    self.BT_lifetime += 1
                    self.BT_AT += bt_max_charge_energy * self.bt_eta_ch * self.bt_conv
                    offEnergy = self.DC_AC_converter(energy-self.DC_DC_converter(bt_max_charge_energy))

                    self.offEnergy.append(offEnergy)
            else:
                offEnergy = energy
                self.offEnergy.append(offEnergy)
                self.bt.ch.append(0)
        else:
            Battery_SOC = self.bt.readSoc()
            if Battery_SOC > Battery_SOC_min:
                bt_max_discharge_energy = self.bt.max_discharge()

                BtToLoad_max = (self.DC_DC_converter(bt_max_discharge_energy))
                if abs(energy)<=BtToLoad_max:
                    self.bt.SOC(P_ch=0,P_dc=self.DC_DC_converter(abs(energy)))
                    self.bt.ch.append(-self.DC_DC_converter(abs(energy)))
                    self.BT_AT += self.DC_DC_converter(abs(energy)) /(self.bt_eta_dc * self.bt_conv)
                    self.energyToPower +=power_data

                    self.BT_lifetime+=1
                else:
                    self.bt.SOC(P_ch=0,P_dc=(bt_max_discharge_energy))
                    self.bt.ch.append(-self.DC_DC_converter(abs(energy)))
                    self.BT_AT += bt_max_discharge_energy / (self.bt_eta_dc * self.bt_conv)

                    self.BT_lifetime += 1
                    self.offLoad+=self.DC_AC_converter(abs(energy)-self.DC_DC_converter(bt_max_discharge_energy))
            else:
                self.bt.ch.append(0)
    def offload(self):
        return self.offLoad
    def offenergy(self):
        return sum(self.offEnergy)
    def engrgyToPower(self):
        return self.energyToPower

    def BT_worktime(self):
        return self.BT_lifetime
    def readAt(self):
        return self.BT_AT


class EMS_OnlyH2():
    def __init__(self,pv,el,fc,ht):
        self.pv  =pv
        self.el =el
        self.fc= fc
        self.ht= ht
        self.offEnergy =[]
        self.offLoad =0
        self.energyToPower =0
    def DC_DC_converter(self,x):
        return x*0.965
    def DC_AC_converter(self,x):
        return x*0.955

    def Energy_Storage_initializa(self):
        self.offlaod = []
        self.offLoad = 0
        self.energyToPower = 0


        self.EL_lifetime = 0
        self.FC_lifetime = 0
        self.HT_lifetime = 0

    def Energy_storage_mode(self, power_data, pv_power):

            'main bus'
            RT_power = self.DC_DC_converter(pv_power)

            'main bus energy'
            energy = RT_power - power_data / 0.955



            Hydrogen_SOC = self.ht.Loh_t()
            Hydrogen_SOC_max = self.ht.max_loh()
            Hydrogen_SOC_min = self.ht.min_loh()

            if energy == 0:
                self.energyToPower += power_data
            elif energy > 0:
                if Hydrogen_SOC <Hydrogen_SOC_max:
                    H2Tank_max_ch = self.ht.max_charge()
                    if energy <= H2Tank_max_ch:
                        eff_el = self.el.efficiency()
                        self.ht.LevelOfHydrogen(P_el=energy, P_fc=0, eff_el=eff_el, eff_fc=0)

                        self.EL_lifetime+=1
                        self.energyToPower += power_data
                    else:
                        eff_el = self.el.efficiency()
                        self.ht.LevelOfHydrogen(P_el=H2Tank_max_ch, P_fc=0, eff_el=eff_el, eff_fc=0)

                        self.EL_lifetime+=1
                        self.HT_lifetime+=1
                        self.energyToPower +=self.DC_AC_converter(self.DC_DC_converter(H2Tank_max_ch) )
                        self.offEnergy+=(energy - self.DC_DC_converter(H2Tank_max_ch))/0.965
                else:
                    self.offEnergy+=energy/0.965
            else:
                H2ToPower_max = self.ht.max_dischage()
                if abs(energy)<= self.DC_DC_converter(H2ToPower_max):
                    eff_fc = self.fc.efficiency()
                    self.ht.LevelOfHydrogen(P_el=0, P_fc=abs(energy), eff_el=0, eff_fc=eff_fc)
                    self.energyToPower += power_data
                    self.FC_lifetime+=1
                    self.HT_lifetime += 1
                else:
                    eff_fc = self.fc.efficiency()
                    self.ht.LevelOfHydrogen(P_el=0, P_fc=H2ToPower_max, eff_el=0, eff_fc=eff_fc)
                    self.energyToPower += self.DC_AC_converter(self.DC_DC_converter(H2ToPower_max))
                    self.FC_lifetime += 1
                    self.HT_lifetime += 1
                    self.offLoad+= self.DC_AC_converter(abs(energy)-self.DC_DC_converter(H2ToPower_max))

    def offload(self):
        return self.offLoad

    def offenergy(self):
        return sum(self.offEnergy)

    def engrgyToPower(self):
        return self.energyToPower

    def FC_worktime(self):
        return self.FC_lifetime

    def EL_worktime(self):
        return self.EL_lifetime

    def HT_worktime(self):
        return self.HT_lifetime

class EMS_grid_connect_only_bt():
    'only depend price'

    def __init__(self,price,pv,bt,E_max,h,pv_cap):


        self.pv_cap =pv_cap
        self.pv  =pv
        self.bt = bt
        self.offEnergy =[]
        self.time = 1
        self.price= price

        self.E_max = E_max
        self.h = h
        self.Ture_energy = 0
        self.dc_energy = 0
        self.ch_energy =0


        self.offLoad = 0
        self.energyToPower = 0
        self.bt_eta_ch = self.bt.readEta_ch()
        self.bt_eta_dc = self.bt.readEta_dc()
        self.bt_conv = self.bt.readEta_conv()
    def DC_DC_converter(self,x):
        return x*0.965
    def DC_AC_converter(self,x):
        return x*0.955
    def Energy_Storage_initializa(self):



        self.BT_lifetime = 0
        self.BT_AT = 0
        self.offLoad =0
        self.energyToPower =0
        self.bt.soc = 0.5
        self.BT_AT = 0
        self.eta_BT_ch =0.95
        self.eta_BT_dc = 0.95
        self.eta_BT_conv=0.9

    def Energy_evaluate(self,bt_action,pv_power,):
        if bt_action =='ch':


            if min(self.DC_DC_converter(pv_power),self.pv_cap*self.bt_conv*self.E_max)  > self.bt.max_charge():
                energy = self.bt.max_charge()
            else:
                energy = self.DC_DC_converter(pv_power)
        else:
            if self.E_max* self.pv_cap <= self.bt.max_discharge() :
                energy = self.E_max* self.pv_cap
            else:
                energy = self.bt.max_discharge()
        return energy

    def Energy_DC_evalute(self,bt_action,True_energy):

        if bt_action =='ch':
            self.Ture_energy +=True_energy
        else:
            self.Ture_energy -= True_energy



    def Energy_storage_mode(self, pv_power,time):
        'main bus'
        RT_power = self.DC_DC_converter(pv_power)
        self.dc_energy = 0
        self.ch_energy =0

        'main bus energy'
        # energy = RT_power - power_data / 0.955
        #
        # Battery_SOC = self.bt.readSoc()
        # Battery_SOC_max = self.bt.max_soc()
        # Battery_SOC_min = self.bt.min_soc()

        if 5 <= int(time/(30*24))<9 or int(time/(30*24)) ==10 :

            'price = 2'
            if 12 <= time % 24 < 14:
                True_energy =self.Energy_evaluate(bt_action='dc',pv_power=RT_power)

                self.bt.SOC(P_dc=True_energy,P_ch=0)
                self.dc_energy=(True_energy)
                self.BT_lifetime += 1
                self.BT_AT +=(True_energy)/(self.eta_BT_dc*self.eta_BT_conv)
            elif 8<= time%24<12 or 14<=time%24<15 or 18<=time%24<21:
                True_energy = self.Energy_evaluate(bt_action='dc', pv_power=RT_power)

                self.bt.SOC(P_dc=True_energy,P_ch=0)
                self.dc_energy=(True_energy)
                self.BT_lifetime += 1
                self.BT_AT += (True_energy) / (self.eta_BT_dc * self.eta_BT_conv)

            elif 6<= time%24<8 or 15<=time%24<18 or 21<=time%24<22:
                True_energy = self.Energy_evaluate(bt_action='ch', pv_power=RT_power)
                self.bt.SOC(P_ch=True_energy, P_dc=0)
                self.ch_energy=(True_energy)
                self.BT_lifetime += 1
                self.BT_AT += True_energy * self.eta_BT_ch * self.eta_BT_conv

            elif 0 <= time % 24 < 6 or 22 <= time % 24 < 24:
                True_energy = self.Energy_evaluate(bt_action='ch', pv_power=RT_power)
                self.bt.SOC(P_ch=True_energy, P_dc=0)
                self.ch_energy=(True_energy)
                self.BT_lifetime += 1
                self.BT_AT += True_energy * self.eta_BT_ch * self.eta_BT_conv

        elif int(time/(30*24))==9 :
            if 8 <=time % 24 < 15 or 18 <= time % 24 < 21:
                True_energy = self.Energy_evaluate(bt_action='dc', pv_power=RT_power)
                self.bt.SOC(P_dc=True_energy, P_ch=0)
                self.dc_energy=(True_energy)
                self.BT_lifetime += 1
                self.BT_AT += (True_energy) / (self.eta_BT_dc * self.eta_BT_conv)

            elif 6 <= time % 24 < 8 or 15 <= time % 24 < 18 or 21 <= time % 24 < 22:
                True_energy = self.Energy_evaluate(bt_action='ch', pv_power=RT_power)
                self.bt.SOC(P_ch=True_energy, P_dc=0)
                self.ch_energy=(True_energy)
                self.BT_lifetime += 1
                self.BT_AT += True_energy * self.eta_BT_ch * self.eta_BT_conv
            elif 0<=time%24 <6 or 22<=time%24 <24:
                True_energy = self.Energy_evaluate(bt_action='ch', pv_power=RT_power)
                self.bt.SOC(P_ch=True_energy, P_dc=0)
                self.ch_energy=(True_energy)
                self.BT_lifetime += 1
                self.BT_AT += True_energy * self.eta_BT_ch * self.eta_BT_conv

        elif int(time / (30 * 24)) == 12 or int(time / 30 / 24) == 1:
            if 19 <= time % 24 < 21:
                True_energy = self.Energy_evaluate(bt_action='dc', pv_power=RT_power)
                self.bt.SOC(P_dc=True_energy, P_ch=0)
                self.dc_energy=(True_energy)
                self.BT_lifetime += 1
                self.BT_AT += (True_energy) / (self.eta_BT_dc * self.eta_BT_conv)
            elif  8<=time%24 <11 or 18<=time%24 <19:
                True_energy = self.Energy_evaluate(bt_action='dc', pv_power=RT_power)
                self.bt.SOC(P_dc=True_energy, P_ch=0)
                self.dc_energy=(True_energy)
                self.BT_lifetime += 1
                self.BT_AT += (True_energy) / (self.eta_BT_dc * self.eta_BT_conv)
            elif 6<=time%24 <8 or 11<=time%24 <18 or  21<=time%24 <22:
                True_energy = self.Energy_evaluate(bt_action='ch', pv_power=RT_power)
                self.bt.SOC(P_ch=True_energy, P_dc=0)
                self.ch_energy=(True_energy)
                self.BT_lifetime += 1
                self.BT_AT += True_energy * self.eta_BT_ch * self.eta_BT_conv
            elif 0<=time%24 <6 or 22<=time%24 <24:
                True_energy = self.Energy_evaluate(bt_action='ch', pv_power=RT_power)
                self.bt.SOC(P_ch= True_energy , P_dc=0)
                self.ch_energy=(True_energy)
                self.BT_lifetime += 1
                self.BT_AT += True_energy * self.eta_BT_ch * self.eta_BT_conv
        else:
            if 8 <= time % 24 < 11 or 18 <= time % 24 < 19:
                True_energy = self.Energy_evaluate(bt_action='dc', pv_power=RT_power)
                self.bt.SOC(P_dc=True_energy, P_ch=0)
                self.dc_energy=(True_energy)
                self.BT_lifetime += 1
                self.BT_AT += (True_energy) / (self.eta_BT_dc * self.eta_BT_conv)
            elif 6 <= time % 24 < 8 or   11<=time%24 <18 or 21<=time%24 <22 :
                True_energy = self.Energy_evaluate(bt_action='ch', pv_power=RT_power)
                self.bt.SOC(P_ch=True_energy, P_dc=0)
                self.ch_energy=(True_energy)
                self.BT_lifetime += 1
                self.BT_AT += True_energy * self.eta_BT_ch * self.eta_BT_conv
            else:
                True_energy = self.Energy_evaluate(bt_action='ch', pv_power=RT_power)
                self.bt.SOC(P_ch=True_energy, P_dc=0)
                self.ch_energy=(True_energy)
                self.BT_lifetime += 1
                self.BT_AT += True_energy * self.eta_BT_ch * self.eta_BT_conv
        return self.dc_energy,self.ch_energy



    def read_energy(self):
        if 0<=self.Ture_energy <= self.h*self.E_max:
            print('D/C energy ok')
        else:
            print('D/C energy error')

    def BT_worktime(self):
        return self.BT_lifetime
    def BT_peryear_AT(self):
        return self.BT_AT


class EMs_grid_connect_only_ht():

    def __init__(self,price,pv,el,fc,ht,E_max,h,pv_cap):


        self.pv_cap =pv_cap
        self.pv  =pv
        self.el = el
        self.fc = fc
        self.ht =ht
        self.offEnergy =[]
        self.time = 1
        self.price= price

        self.E_max = E_max
        self.h = h
        self.Ture_energy = 0
        self.dc_energy = 0
        self.ch_energy =0


        self.offLoad = 0
        self.energyToPower = 0
        self.el_eta_ch = self.el.readEta_ch()
        self.fc_eta_dc = self.fc.readEta_dc()
        self.sys_conv = self.el_eta_ch*self.fc_eta_dc

    def DC_DC_converter(self,x):
        return x*0.965
    def DC_AC_converter(self,x):
        return x*0.955






































































