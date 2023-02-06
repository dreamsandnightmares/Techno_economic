import math
class Lcoe:
    def __init__(self,pv_cap,bt_cap,el_cap,fc_cap,ht_cap,bt_model,el_model):

        self.dr = 0.08
        self.ir = 0.03
        self.d = None
        self.project_lifetime = 20
        self.energy_tot = 0
        'cost inv [yuan]'
        self.cost_per_pv = 6965
        self.cost_per_bt_lead = 1490
        self.cost_per_bt_li = 2300
        self.cost_per_ht =500
        self.cost_per_el_pem = 6000
        self.cost_per_el_alk =3000
        self.cost_per_fc = 1190

        'cap'
        self.pv_cap = pv_cap
        self.bt_cap =bt_cap
        self.el_cap = el_cap
        self.fc_cap =fc_cap
        self.ht_cap =ht_cap

        'model'
        self.bt_model = bt_model
        self.el_model = el_model

        'cost om'
        self.pv_om_cost = 130
        self.li_om_cost = 60
        self.lead_om_cost = 45








    def real_d(self):
        self.d = (self.dr-self.ir)/(self.ir+1)
        return self.d
    def lcoe(self,energy):

        for i in range(self.project_lifetime):
            self.energy_tot += energy/math.pow((self.d+1),i)

        C_inv_tot = self.C_inv_tot()

        C_NPC_om_tot = self.C_NPC_om_tot()



        self.C_NPC_tot = C_inv_tot +C_NPC_om_tot+C_NPC_rep_tot-C_NPC_sal_tot

        lcoe = self.C_NPC_tot/self.energy_tot

        return lcoe

    def C_inv_tot(self):
        C_inv_pv = self.cost_per_pv*self.pv_cap
        if self.el_model  =='PEM':
            C_inv_el = self.cost_per_el_pem *self.el_cap
        else:
            C_inv_el = self.cost_per_el_alk * self.el_cap
        if self.bt_model == 'lead' :
            C_inv_bt = self.cost_per_bt_lead * self.bt_cap
        else:
            C_inv_bt = self.cost_per_bt_li * self.bt_cap

        C_inv_fc = self.cost_per_fc * self.fc_cap
        C_inv_ht = self.cost_per_ht * self.ht_cap




        C_NPC_tot = C_inv_pv + C_inv_el + C_inv_fc + C_inv_bt + C_inv_ht
        return C_NPC_tot

    def C_NPC_om_tot(self):
        C_NPC_om = 0
        if self.bt_model == 'lead':

            C_om_tot = self.pv_om_cost * self.pv_cap + self.lead_om_cost * self.bt_cap
        else:
            C_om_tot = self.pv_om_cost * self.pv_cap + self.li_om_cost * self.bt_cap


        for i in range(self.project_lifetime):
            C_NPC_om += C_om_tot/math.pow((1+self.d),i)

        if self.el_model =='PEM':
            C_NPC_om_tot = C_NPC_om+ self.el_cap*self.cost_per_el_pem*0.04+self.fc_cap*self.cost_per_fc*0.04+self.ht_cap*self.cost_per_ht*0.02
        else:
            C_NPC_om_tot = C_NPC_om + self.el_cap * self.cost_per_el_alk * 0.04 + self.fc_cap * self.cost_per_fc * 0.04 + self.ht_cap * self.cost_per_ht * 0.02

        return  C_NPC_om_tot
    def C_NPC_rep_tot(self):
        C_NPC_rep_tot = 0
        return C_NPC_rep_tot
    def C_NPC_sal_tot(self):
        C_NPC_sal_tot = 0
        return C_NPC_sal_tot



















