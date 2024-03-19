import numpy as np
import pandas as pd
from scipy.optimize import least_squares

from ..utils import spacing
from ..utils.lle_scanner import estimate_lle_from_gmix


class LLE:
    def __init__(self, actmodel):
        self.mix = actmodel.mix
        self.model  = actmodel

    def fobj_binodal(self, x1, T):
        # Equilibrium: Isoactivity criterion (aL1 - aL2 = 0)
        x = np.array([x1, 1-x1])
        activity = self.model.activity(T, x)
        equilibrium = np.diff(activity, axis=1)
        return equilibrium.ravel() # reshape from (2,1) --> (2,)

    def fobj_spinodal(self, x1):
        T = 0
        x = np.array([x1, 1-x1])
        return self.model.thermofac(T, x)

    def binodal(self, T, x0=None):
        if x0 is None:
            x0 = [0.1, 0.999]    # 1_N2_Ethan
        kwargs = dict(bounds=(0,1), ftol=1e-15, xtol=1e-15)
        res = least_squares(self.fobj_binodal, x0, args=(T,), **kwargs)
        return res.x

    def spinodal(self, x0=None):
        if x0 is None:
            x0 = self.binodal()
        return least_squares(self.fobj_spinodal, x0).x

# =============================================================================
#
# =============================================================================
    def approx_init_x0(self, T):
        x1 = spacing(0,1,51,'poly',n=3)
        gmix = self.model.gmix(T, x1)
        xL, xR, yL, yR = estimate_lle_from_gmix(x1, gmix, rough=True)
        return xL, xR

    def solve_lle(self, T, x0, info=True):
        binodal_x = self.binodal(T, x0)
        binodal_w = self.model._convert(binodal_x)
        formatted_w_binodal = [f"wL{i+1}={value:.4f}" for i, value in enumerate(binodal_w)]
        formatted_x_binodal = [f"xL{i+1}={value:.6f}" for i, value in enumerate(binodal_x)]
        msg = ('LLE: ', f"{T=:.2f}", *formatted_w_binodal, *formatted_x_binodal)
        if info:
            print(*msg)
            return binodal_x, binodal_w
        return binodal_x, binodal_w, msg

    def miscibility(self, T, x0=None, max_gap=0.1, max_T=500, dT=25):
        print()
        print("Calculating LLE...")
        res = []

        if x0 is None:
            print("...searching for suitable initial value...")
            x0 = self.approx_init_x0(T)
        binodal_x, binodal_w, msg = self.solve_lle(T, x0, info=False)

        # Check if initial guess is reasonalble - otherwise increase T
        while binodal_x[0] < x0[0] and T <= max_T:
            print('LLE: ', f"{T=:.2f}", "...no feasbible initial value found.")
            T += 10  # Increase T by 10
            x0 = self.approx_init_x0(T)
            binodal_x, binodal_w, msg = self.solve_lle(T, x0, info=False)
        print("Suitable initial value found! Proceed with calculating LLE...")
        print(*msg)
        gap = np.diff(binodal_w)[0]
        res.append((T, *binodal_w, *binodal_x))

        exponent = 2.1
        while gap > max_gap and T <= max_T:
            T += dT * gap**exponent
            x0 = binodal_x
            binodal_x, binodal_w = self.solve_lle(T, x0)
            gap = np.diff(binodal_w)[0]
            res.append((T, *binodal_w, *binodal_x))

        columns = ['T', 'wL1', 'wL2', 'xL1', 'xL2']
        res = pd.DataFrame(res, columns=columns)
        return res
