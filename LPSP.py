class LPSP:
    def __init__(self,power_data,offload,delta_t=1):
        self.delta_t = delta_t
        self.power_data = power_data
        self.offload = offload
    def lpsp(self):
        """
            The output of the reliability of the off-grid system in covering the electrical load(equation 22)

            Arguments:
            delta_t -- is the time step (in h)

            Returns:
            LPSP -- reliability of the off-grid system in covering the electrical load
        """
        lpsp =  self.offload*self.delta_t/self.power_data*self.delta_t
        return lpsp