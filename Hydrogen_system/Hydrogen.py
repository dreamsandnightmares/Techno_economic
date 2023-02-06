import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

class HydrogenTank(object):
    'P_el/P_fc  electrolyzer and fuel cell operating power (at the DC bus level)'
    def __init__(self,cap_h2,t,eff_el,eff_fc):

        self.LOH_max = 1
        self.LOH_min = 0
        self.tank_cap = cap_h2
        self.eff_el = eff_el
        self.eff_fc = eff_fc
        self.time = t
        self.LOH =None
        self.done = None

    def initializa(self):
        self.LOH_t = 0.5

    def LevelOfHydrogen(self,P_el,P_fc):

        self.LOH = self.LOH+P_el*self.time*self.eff_el/self.tank_cap - P_fc*self.time/self.eff_fc*self.tank_cap

        return self.LOH

    def check(self):
        if self.LOH>=self.LOH_min and self.LOH<=self.LOH_max:
            pass
        else:
            self.done =True
            print('error: tank cap  LOH =',self.LOH)
    def Loh_t(self):
        return  self.LOH

    def max_charge(self):
        energy = abs((self.LOH_max -self.LOH)*self.tank_cap/(self.time*self.eff_el))
        return energy
    def max_dischage(self):
        energy  =abs((self.LOH-self.LOH_min)*self.eff_fc*self.tank_cap/(self.time))
        return energy

class Alkelectrolyzer(object):
    def __init__(self,cap):
        'Ru :[j/mol/K]'
        'F : [C/mol]'
        'P_act/an is the anode/cathode operating pressure :[bar]'
        'P_v_koh is the vapor pressure of the KOH so-lution'
        'a_h2o_koh is the water activity of the KOH solution.'

        self.cap = cap
        self.Ru = 8.314
        self.F = 96485
        self.P_act =30
        self.P_v_koh =None
        self.P_an =30
        self.a_h2o_koh = None
        self.m =57*1.3

        self.T = 70
        self.T0 = 70
        self.T_ref = 298.15

        self.a_an = 0.99
        self.a_cat =0.92
        self.i = 0.35
        self.i0_an =None
        self.i0_cat =None
        self.i0_an_ref =9.83*10**(-8)
        self.i0_cat_ref = 7.32*10**(-3)
        self.E_a_act_an = 82.27
        self.E_a_act_cat =32.76

        self.theta =None

        self.y_m_an = 2.5
        self.y_m_cat = 1.5


        self.k_el = 2*10**(-5)
        self.l_an_s = 0.125
        self.l_cat_s = 0.125
        self.b_an = 0.045
        self.b_cat = 0.045
        self.t_s = 2.18

        self.x_s = 0.05
        self.w_s =0.85
        self.e_s = 0.42

        self.A_s = 300
        self.A_e = 300

        self.f1 = 250
        self.f2= 0.96
        self.j = 100
        self.j0 = 300
        self.A = 30
        'cm2'






    def volt_rev(self,  ):
        a = -0.0151*self.m-1.6788*10**(-3)*self.m**2+2.2588*10**(-5)**self.m**3
        b =1-1.2062*10**(-3)*self.m+5.6024*10**(-4)*self.m**2-7.8228*self.m**3*10**(-6)
        P_v_h2o = math.exp(81.6179-7699.68/(self.T+273.15)-10.9*math.log(self.T+273.15)+9.5891*10**(-3)*(self.T+273.15))

        self.P_v_koh = math.exp(2.302*a + b*math.log(P_v_h2o))

        self.a_h2o_koh = math.exp(-0.05192*self.m+0.003302*self.m**2+(3.177*self.m-2.131*self.m**2)/(self.T+273.15))

        volt_rev_0 =1.5184 - 1.5421*10**(-3)*(self.T+273.15)+9.526*10**(-5)*(self.T+273.15)*math.log(self.T+273.15)+9.84*10**(-8)*(self.T+273.15)**2
        volt_rev = volt_rev_0+ self.Ru*self.T/(2*self.F)*math.log((self.P_act - self.P_v_koh)*(self.P_an-self.P_v_koh)**0.5/self.a_h2o_koh)
        return volt_rev

    def volt_act_an(self):
        self.theta = (-97.25+182*self.T/self.T0-84*(self.T/self.T0)**2)*(self.j/self.j0)**(0.3)

        self.i0_an  = self.y_m_an*self.i0_an_ref*math.exp(-self.E_a_act_an*10**(3)/self.Ru*(1/(self.T+273.15)-1/self.T_ref))


        volt_act_an = self.Ru*self.T/(self.a_an*self.F)*math.asinh(self.i/2*self.i0_an*(1-self.theta))
        return volt_act_an

    def volt_act_cat(self):
        self.theta = (-97.25 + 182 * self.T / self.T0 - 84 * (self.T / self.T0) ** 2) * (self.j / self.j0) ** (0.3)

        self.i0_cat = self.y_m_cat * self.i0_cat_ref * math.exp(
            -self.E_a_act_cat * 10 ** (3) / self.Ru * (1 / (self.T + 273.15) - 1 / self.T_ref))
        volt_act_an = self.Ru * self.T / (self.a_cat * self.F) * math.asinh(self.i / 2 * self.i0_cat * (1 - self.theta))

        return volt_act_an

    def volt_ohm(self):
        self.theta = (-97.25 + 182 * self.T / self.T0 - 84 * (self.T / self.T0) ** 2) * (self.j / self.j0) ** (0.3)

        ASR_kohsol  = self.m/(1+self.k_el*(self.T+273.15 -self.T_ref))*((self.l_an_s-self.b_an)/self.A_e+1/(1-self.theta)**(3/2)*(self.b_an/self.A_e)+(self.l_cat_s-self.b_cat)/self.A_e+1/(1-self.theta)**(3/2)*(self.b_cat/self.A_e))


        ASR_mem = self.m*(self.t_s)**2*self.x_s/(self.w_s*self.e_s*self.A_s)


        ASR_ohm = 0.17+ASR_kohsol+ASR_mem

        volt_ohm = ASR_ohm*self.i
        return volt_ohm


    def faraday(self):

        n_f = self.i**2/(self.f1+self.i**2)*self.f2
        return n_f

    def volt_cell(self):
        'Volt : [v]'
        self.volt_act = self.volt_act_cat()+self.volt_act_an()
        self.volt_ohm = self.volt_ohm()
        self.volt_rev =self.volt_rev()
        self.volt_diff =0


        volt_cell = self.volt_rev + self.volt_act + self.volt_ohm + self.volt_diff
        return volt_cell



class PEMelectrolyzer(object):
    def __init__(self,cap):
        self.cap = cap
        self.T =60
        self.Ru = 8.314
        self.F = 96485
        self.p_cat  =30
        self.P_h2o =None
        self.i0_an_ref = 4.38*10**(-9)
        self.i0_cat_ref = 4.94*10*(-3)
        self.E_a_act_an = 59.95
        self.E_a_act_cat = 8.57
        self.E_a_mem = 10.32
        self.a_an = 0.69
        self.a_cat = 0.56
        self.b_mem_ref = 0.106
        self.T_ref = 298.15
        self.y_m_an = 2.5
        self.y_m_cat = 1.5
        self.i = 1.8
        self.ASR_electric = 7.48*10**(-2)
        self.ASR_mem =None
        self.b_thick = 0.0183
        self.b_mem = None
        self.i_l_an = 6
        self.N_o2= None
        self.N_h2 = None
        self.N = 2








        self.p_an = 30



        self.A = 25


    def volt_cell(self):
        self.volt_act = self.volt_act_cat()+self.volt_act_an()
        self.volt_rev = self.volt_rev()
        self.volt_ohm =self.volt_ohm()
        self.volt_diff = self.volt_diff()
        volt_cell  = self.volt_rev + self.volt_act + self.volt_ohm + self.volt_diff
        return volt_cell

    def volt_rev(self,):
        V0 = 1.229 - 0.009 * (self.T+273.15 - 298)
        self.P_h2o = 6.1078*10**(-3)*math.exp(17.2694*(self.T)/(self.T-34.85))
        volt_rev = V0+(self.T*self.Ru/self.F*2)*(math.log(((self.p_cat-self.P_h2o)*(self.p_an-self.P_h2o)**0.5)/self.P_h2o))
        return volt_rev

    def volt_act_an(self):

        self.i0_an = self.y_m_an * self.i0_an_ref * math.exp(
            -self.E_a_act_an * 10 ** (3) / self.Ru * (1 / (self.T + 273.15) - 1 / self.T_ref))

        volt_act_an = self.Ru * self.T / (self.a_an * self.F) * math.asinh(self.i / 2 * self.i0_an * (1))
        return volt_act_an
    def volt_act_cat(self):

        self.i0_cat = self.y_m_cat * self.i0_cat_ref * math.exp(
            -self.E_a_act_cat * 10 ** (3) / self.Ru * (1 / (self.T + 273.15) - 1 / self.T_ref))
        volt_act_an = self.Ru * self.T / (self.a_cat * self.F) * math.asinh(self.i / 2 * self.i0_cat * (1))


        return volt_act_an

    def volt_ohm(self):
        self.b_mem = self.b_mem_ref*math.exp((-self.E_a_mem*10**(3)/self.Ru)*(1/(self.T+273.15)-1/self.T_ref))
        self.ASR_mem  =self.b_thick/self.b_mem

        volt_ohm = (self.ASR_electric+self.ASR_mem)*self.i


        return volt_ohm
    def volt_diff(self):
        volt_diff = self.Ru*(self.T+273.15)/(4*self.F)*math.log(1-self.i/self.i_l_an)
        return  volt_diff

    def faraday(self):
        self.N_h2 = self.N*self.i*self.A/2*self.F
        self.N_o2 = self.N*self.i*self.A/4*self.F


        n =1-self.F*2/self.i*(self.N_h2+self.N_o2*2)

        return n

















