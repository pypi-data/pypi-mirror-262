import numpy as np
import numbers

from ..utils.convert import convert

class ActModel:

    def __init__(self, components: list = []):
        self.mix = components

    def lngamma(self, T, x):
        pass

    def dlngamma(self, T, x):
        # Only binary case
        def f(x1):
            x = np.array([x1, 1-x1])
            return self.lngamma(T, x)#[0]
        h, x = 0.0001, x[0]
        dy = (f(x+h)-f(x-h))/(2*h)
        # Revert direction of dy2_dx2 --> dy2_dx1
        dy[1] = dy[1][::-1]
        return f(x), dy

    def activity(self, T, x):
        act = np.log(x) + self.lngamma(T, x)
        act[(act == np.inf) | (act == -np.inf)] = np.nan
        return act

    def gmix(self, T, x):
        # Convert input as needed
        x = self._convert_input(x)
        # Create mask to identify columns that don't contain 0 or 1
        mask = np.any((x != 0) & (x != 1), axis=0)
        # Apply the mask to filter x
        _x = x[:, mask]
        # Calculate gmix for the  x values
        _gmix = _x * (np.log(_x) + self.lngamma(T, _x))
        _gmix = np.sum(_gmix, axis=0)
        # Initialize gmix array with zeros
        gmix = np.zeros(x.shape[1])
        # Fill gmix with calculated values where the mask is True
        gmix[mask] = _gmix
        return gmix


# =============================================================================
# Wrapper functions (Decorators)
# =============================================================================
    @staticmethod
    def vectorize(func):
        ''' Intended vor ActModels where only single mole fractions can be
        handled, like e.g. COSMO-SAC. This function vectorizes the lngamma()
        to make it work with arrays of mole fractions.
        '''
        def wrapper(self, T, x):
            # Convert input to appropriate format
            x = self._convert_input(x)
            # Process based on the dimensionality of x
            if x.ndim == 1:
                return func(self, T, x)
            elif x.ndim == 2:
                results = [func(self, T, x[:, col]) for col in range(x.shape[1])]
                return np.array(results).T
            else:
                raise ValueError("Input must be either a scalar, 0D, 1D or 2D array")
        return wrapper


# =============================================================================
# Auxilliary functions
# =============================================================================
    def _convert_input(self, x):
        """Converts input to a 1-dim ndarray if it's a number or 0-dim ndarray."""
        if isinstance(x, numbers.Number) or (isinstance(x, np.ndarray) and x.ndim == 0):
            return np.array([float(x), 1 - float(x)])
        elif isinstance(x, np.ndarray) and x.ndim == 1 and len(x) != len(self.mix):
            return np.array([x, 1 - x])
        return x

    def _convert(self, x, to='weight'):
        Mw = np.array([c.Mw for c in self.mix])
        return convert(x=np.array([x, 1-x]), Mw=Mw, to=to)[0]
