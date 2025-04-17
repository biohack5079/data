import numpy as np

class Cell:
    def __init__(self, initial_membrane_potential=-65):
        self.membrane_potential = initial_membrane_potential
        self.m = 0.05  # Activation gate for Na+
        self.h = 0.6   # Inactivation gate for Na+
        self.n = 0.32  # Activation gate for K+
    
    def initialize(self):
        """
        Initialize the cell's state.
        """
        self.membrane_potential = -65  # Reset to default resting potential
        self.m = 0.05
        self.h = 0.6
        self.n = 0.32

    def update(self, I):
        """
        Update the cell's state based on the input current I.
        """
        dV, dm, dh, dn = self.hh_model(self.membrane_potential, self.m, self.h, self.n, I)
        self.membrane_potential += dV
        self.m += dm
        self.h += dh
        self.n += dn

    def hh_model(self, V, m, h, n, I):
        """
        Hodgkin-Huxley model equations for membrane potential and gating variables.
        """
        C = 1.0  # Membrane capacitance
        g_Na = 120  # Maximum conductance for Na+
        g_K = 36    # Maximum conductance for K+
        g_L = 0.3   # Leak conductance
        E_Na = 50   # Equilibrium potential for Na+
        E_K = -77   # Equilibrium potential for K+
        E_L = -54.4 # Equilibrium potential for leak

        # 安全な指数関数の計算
        def safe_exp(x):
            return np.exp(np.clip(x, -50, 50))  # xを-100から100の範囲に制限
        
        dV = (I - g_Na * m**3 * h * (V - E_Na) - g_K * n**4 * (V - E_K) - g_L * (V - E_L)) / C
        dm = 0.1 * (25 - V) / (safe_exp((25 - V) / 10) - 1) * (1 - m) - 4 * safe_exp(-V / 18) * m
        dh = 0.07 * safe_exp(-V / 20) * (1 - h) - h / (safe_exp((30 - V) / 10) + 1)
        dn = 0.1 * (10 - V) / (safe_exp((10 - V) / 10) - 1) * (1 - n) - 0.125 * safe_exp(-V / 80) * n
        return dV, dm, dh, dn

    def get_state(self):
        """
        Return the current state of the cell.
        """
        return {
            "membrane_potential": self.membrane_potential,
            "m": self.m,
            "h": self.h,
            "n": self.n
        }