class Li_ionBattery():
    def __init__(self,cap):
        self.SocMax = 0.8
        self.SocMin = 0.2
        self.B_t = 0.05/30/24
        self.soc =0
        self.cap = cap
        self.time =1
        self.eta_BT_ch = 0.95
        self.eta_BT_dc = 0.95
        self.eta_BT_conv = 0.9
        self.done =False
        self.num = 1

        self.ch = []



    def BattertInitializa(self):
        self.soc = 0.5


    def SOC(self,P_ch,P_dc):
         self.soc = self.soc*(1-self.B_t)+P_ch*self.time*self.eta_BT_ch*self.eta_BT_conv/self.cap-P_dc*self.time/(self.eta_BT_dc*self.eta_BT_conv*self.cap)

    def max_charge(self):
        energy = ((self.SocMax-self.soc*(1-self.B_t))*self.cap/(self.time*self.eta_BT_ch*self.eta_BT_conv))
        return energy
    def max_discharge(self):
        energy = (abs(self.SocMin-self.soc*(1-self.B_t))*self.eta_BT_dc*self.eta_BT_conv*self.cap)/self.time
        return energy
    def readSoc(self):
        return self.soc
    def check(self):
        if self.soc <=self.SocMax and self.soc >=self.SocMin:
            pass
        else:
            self.done = True
            print('error: Battery cap  SOC =', self.soc)

    def lifetime(self):
        DOD =[50,70,80]
        CTF = [5000,3000,2500]
        LT =0
        for i in range(len(DOD)):
            LT +=2*self.cap*DOD[i]*CTF[i]/len(DOD)
        return LT
    def max_soc(self):
        return self.SocMax
    def min_soc(self):
        return self.SocMin
    def readEta_ch(self):
        return self.eta_BT_ch
    def readEta_dc(self):
        return self.eta_BT_dc
    def readEta_conv(self):
        return self.eta_BT_conv
    def readenergy(self):
        return self.ch








class Lead_acid_battert():
    def __init__(self,cap):
        self.SocMax = 1
        self.SocMin = 0.5
        self.B_t = 0.025 / 30 / 24
        self.soc = 0
        self.cap = cap
        self.time = 1
        self.eta_BT_ch = 0.85
        self.eta_BT_dc = 0.85
        self.eta_BT_conv = 0.9
        self.done = False
        self.num =1
    def BattertInitializa(self):
        self.soc = 0.5
    def SOC(self,P_ch,P_dc):
         self.soc = self.soc*(1-self.B_t)+P_ch*self.time*self.eta_BT_ch*self.eta_BT_conv/self.cap-P_dc*self.time/(self.eta_BT_dc*self.eta_BT_conv*self.cap)

    def max_charge(self):
        energy = (self.SocMax-self.soc*(1-self.B_t)*self.cap/(self.time*self.eta_BT_ch*self.eta_BT_conv))
        return energy
    def max_discharge(self):
        energy = (abs(self.SocMin-self.soc*(1-self.B_t))*self.eta_BT_dc*self.eta_BT_conv*self.cap)/self.time
        return energy
    def readSoc(self):
        return self.soc
    def check(self):
        if self.soc <=self.SocMax and self.soc >=self.SocMin:
            pass
        else:
            self.done = True
            print('error: Battery cap  SOC =', self.soc)
    def lifetime(self):
        DOD =[10,25,35,50,60,70,80,90]
        CTF = [5700,2100,1470,1000,830,700,600,450]
        LT =0
        for i in range(len(DOD)):
            LT +=2*self.cap*DOD[i]*CTF[i]/len(DOD)
        return LT

    def max_soc(self):
        return self.SocMax
    def min_soc(self):
        return self.SocMin

    def readEta_ch(self):
        return self.eta_BT_ch
    def readEta_dc(self):
        return self.eta_BT_dc
    def readEta_conv(self):
        return self.eta_BT_conv












