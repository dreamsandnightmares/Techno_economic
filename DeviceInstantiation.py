import Pvsystem
from Battery_system.Battery import Li_ionBattery,Lead_acid_battert
from Hydrogen_system.Hydrogen import PEMelectrolyzer,Alkelectrolyzer,HydrogenTank,PEM_fuelCell

class PV_System:
    def __init__(self,cap):
        self.cap = cap
        self.lifetime = 0

    def PV_Instantiate(self):
        PV_rata = self.cap
        #光伏额定功率
        return Pvsystem.PVSystem(P_PV_rated=PV_rata)

class EL_System:
    def __init__(self,model,cap):
        self.cap =cap
        self.model = model
        self.lifetime = None

    def EL_Instantiate(self):
        if self.model =='PEM':
           self.lifetime = 30000
           return PEMelectrolyzer(self.cap)

        else:
            self.lifetime =76923
            return Alkelectrolyzer(self.cap)
    def lifetime(self):
        if self.model =='PEM':
            self.lifetime = 30000
        else:
            self.lifetime =76923
        return self.lifetime
class FC_System:
    def __init__(self,cap):
        self.cap = cap
        self.lifetime =30000
    def FC_Instantiate(self):
        PEM_fuelCell(self.cap)
    def lifetime(self):
        return self.lifetime


class BT_System:
    def __init__(self,cap,model):
        self.cap =cap

        self.model =model


    def BT_Instantiate(self):

        BT_Model = self.model

        if  BT_Model == "Lead":
            BT =Lead_acid_battert(self.cap)
            BT.BattertInitializa()
            return BT

        else:
            BT = Li_ionBattery(self.cap)
            BT.BattertInitializa()
            return BT
class HT_System:
    def __init__(self,cap,eta_fc,eta_el):
        self.cap =cap
        self.eta_fc= eta_fc
        self.eta_el =eta_el

        self.lifetime =40000



    def HT_Instantiate(self):
        Cap_h2 = self.cap
        eta_FC = self.eta_fc
        eta_EL = self.eta_el

        return  HydrogenTank(Cap_h2,eta_EL,eta_FC)
    def lifetime(self):
        return self.lifetime