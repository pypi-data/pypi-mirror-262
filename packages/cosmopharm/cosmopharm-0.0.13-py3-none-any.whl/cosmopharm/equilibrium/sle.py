import pandas as pd
import numpy as np
from scipy.optimize import fsolve, root
from typing import Literal

from ..components import Component
from ..utils.spacing import spacing

class SLE:
    def __init__(self, solute, solvent, actmodel):
        self.mix = [solute, solvent]
        self.model = actmodel
        self.solute, self.solvent = solute, solvent

    def solubility(self,
                   solute: Component = None, solvent: Component = None,
                   args=None, init=None, data=None,
                   vary: Literal['T', 'w', 'auto'] = 'auto',
                   mix: Literal['ideal', 'real'] = 'real',
                   solver: Literal['root', 'fsolve'] = 'root'):
        ''' Calculate solubility curve of solute in solvent.'''
        self.solute = solute or self.solute
        self.solvent = solvent or self.solvent
        self.vary, self.mix_type = vary, mix
        if self.vary == 'auto':
            gen = self.auto_solve(solver)
        else:
            self._vary = self.vary
            if args is None or init is None:
                args, init = self.initialize(init=init, data=data)
            gen = self.solve_sle(args, init, solver)
        res = [k for k in gen]
        res = pd.DataFrame(res, columns=['T', 'x', 'vary', 'w'])
        res = res[['T', 'w', 'x', 'vary']]
        return res


# =============================================================================
# MATHEMATICS
# =============================================================================
    def solve_sle(self, args, init, solver='root'):
        is_iterable = hasattr(init, "__len__") and len(init) > 1
        key, lock = ['T', 'x'] if self._vary == 'T' else ['x', 'T']
        solve = self.set_solver(solver=solver)
        x0 = init
        args, pure_component = self._handle_pure_component(args)
        if pure_component: # no need to calculate pure component
            yield pure_component

        for i, arg in enumerate(args):
            x0 = init[i] if is_iterable else x0
            out = float(solve(x0, arg))
            x0 = out if not is_iterable else x0
            res = {key: arg, lock: out, 'vary': self._vary}
            res['w'] = self.model._convert(res['x'])[0]
            text = (f"T={res['T']:.2f}", f"w={res['w']:.4f}", f"x={res['x']:.4f}")
            print(f'SLE ({self.mix_type}): ', *text)
            yield res

    def auto_solve(self, solver: Literal['root', 'fsolve'] = 'root'):
        print()
        print(f"Calculating SLE ({self.mix_type})...")
        # Start with varying 'w' until dTdw > THRESHOLD
        self._vary = 'w'
        args, x0 = self.initialize()
        gen = self.solve_sle(args, x0, solver)
        previous = None
        for i, current in enumerate(gen):
            yield current
            if self._should_stop_generator(i, previous, current):
                break  # This will end the generator
            previous = current
        # Switch to varying 'T'
        self._vary = 'T'
        T0, x0 = current['T'], current['x']
        # # (Deprecated): If last dT>5, make the next dT=5 (from old version)
        # T1 = previous['T']; dT = T0 - T1
        # T0 += dT if abs(dT) < 5 else np.sign(dT) * 5
        args = self.set_args(xmax=T0)[1:]  # exclude initial point (redundant)
        gen = self.solve_sle(args, x0)
        yield from gen


# =============================================================================
# THERMODYNAMICS
# =============================================================================
    def ideal_mix(self, T):
        return np.exp(-self.gibbs_fusion(T))

    def real_mix(self, T, x):
        lngamma = self.model.lngamma(T, x)[0]
        return np.log(x) + lngamma + self.gibbs_fusion(T)

    # Gibbs energy of fusion, i.e., the right-hand side of the solubility equation:
    def gibbs_fusion(self, T):
        T_fus = self.solute.T_fus
        H_fus = self.solute.H_fus
        Cp_fus_A = self.solute.Cp_fus_A
        Cp_fus_BT = self.solute.Cp_fus_BT

        R  = 8.314                 # J/(mol K)
        RT = R*T                   # J/mol
        A, B = Cp_fus_A, Cp_fus_BT
        G1 = H_fus*(1-T/T_fus)     # J/mol
        G2 = A * (T-T_fus) + 0.5*B*(T**2-T_fus**2)
        G3 = -T * (A * np.log(T/T_fus) + B*(T-T_fus))
        G_fus = G1 + G2 + G3       # J/mol
        return G_fus/RT


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
    def initialize(self, xmin=None, xmax=None, dx=None, data=None, init=None):
        args = self.set_args(xmin, xmax, dx, data)
        x0 = self.set_x0(init)
        return args, x0

    def set_args(self, xmin=None, xmax=None, dx=None, data=None):
        vary = self._vary
        # Determine argument values based on input data or generate
        # them based on range and type
        defaults = {
            'T': {'min': 310, 'max': self.solute.T_fus, 'step': 10},
            'w': {'min': 0.01, 'max': 1, 'step': 0.08}
        }
        mi = defaults[vary]['min'] if xmin is None else xmin
        ma = defaults[vary]['max'] if xmax is None else xmax
        dx = defaults[vary]['step'] if dx is None else dx

        if data is None:
            if self.vary != 'auto':  # auto_vary == False
                args = np.arange(ma, mi-dx, -dx)
                args[-1] = np.maximum(args[-1], mi)
            elif vary == 'T':  # auto_vary == True
                num, dT = 16, 175  # How many data points in this T-range
                num = int((ma-mi)/dT*num)  # fraction of points if dT smaller
                num = max(6, num)
                kwargs = dict(reverse=True, n=1.5)
                args = spacing(ma, mi, num, 'poly', **kwargs)
            else:  # vary == 'w'
                num = 16 if self.mix_type == 'ideal' else 21
                args = spacing(ma, mi, num, 'quadratic')
        else:
            args = data
        return args if vary != 'w' else self.model._convert(args, to='mole')

    def set_x0(self, init=None):
        vary = self._vary
        # Set up initial values based on the type of variable ('T' or 'w')
        if vary == 'T':
            x0 = 1. if init is None else self.model._convert(init, to='mole')
        else:  # vary == 'w'
            x0 = self.solute.T_fus if init is None else init
        return x0

    def set_solver(self, solver: Literal['root', 'fsolve'] = 'root'):
        vary, mix = self._vary, self.mix_type
        # Define the objective function (fobj) and the solver function (solve)
        # based on the mixture type (mix) and the variable type (vary)
        if mix == 'ideal' and vary == 'T':
            def fobj(x, T): return self.ideal_mix(T)
            def solve(x0, args): return fobj(x0, args)
        else:
            if mix == 'ideal':
                def fobj(T, x): return x - self.ideal_mix(T)
            elif vary == 'T':  # mix != 'ideal'
                def fobj(x, T): return self.real_mix(T, x)
            else:  # vary == 'w'
                def fobj(T, x): return self.real_mix(T, x)
            kwargs = dict(method='krylov', options={'maxiter': 5, 'xtol': 1e-3})
            if solver == 'fsolve':
                def solve(x0, args): return fsolve(fobj, x0, args)
            else:
                def solve(x0, args): return root(fobj, x0, args, **kwargs).x
        # Problem: "fsolve" and "root" return different types of np.arrays
        # (1) fsolve returns (1,) 1D array
        # (2) root returns () 0D array
        # Therefore, it is necessary to use float(solve(...)) to extract the
        # single value from the array, since solve()[0] does not work for root.
        return solve


# =============================================================================
# AUXILLIARY FUNCTIONS
# =============================================================================
    def _should_stop_generator(self, i, previous, current):
        THRESHOLD = 60
        if i > 1:  # ensuring there was a previous result
            dT = current['T'] - previous['T']
            dw = current['w'] - previous['w']
            return (dT / dw) > THRESHOLD
        return False  # If not enough elements, continue the generator

    def _handle_pure_component(self, args):
        res = {'T': self.solute.T_fus, 'x': 1, 'vary': self._vary, 'w': 1}
        if self._vary == 'T' and self.solute.T_fus in args:
            args = args[args != self.solute.T_fus]
            return args, res
        elif self._vary == 'w' and 1 in args:
            args = args[args != 1]
            return args, res
        return args, None
