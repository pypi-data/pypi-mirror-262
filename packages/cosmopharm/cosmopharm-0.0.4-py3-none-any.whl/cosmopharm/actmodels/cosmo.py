import numpy as np
from .actmodel import ActModel

class COSMOSAC(ActModel):
    def __init__(self, COSMO, components: list, free_volume=False,
                 dispersion=False, combinatorial=True):
        self.COSMO = COSMO
        self.mix = components
        # Flexible assignment of 'get_lngamma_comb' and 'get_lngamma_dsp'
        # that changes dynamically if the values for 'free_volume', 'dispersion'
        # or "combinatorial" are changed after initialization of an instance.
        self._free_volume = free_volume
        self._dispersion = dispersion
        self._combinatorial = combinatorial

    @ActModel.vectorize
    def lngamma(self, T, x):
        resid = self.get_lngamma_resid(T, x)
        comb  = self.get_lngamma_comb(x)
        disp  = self.get_lngamma_disp(x)
        lngamma = resid + comb + disp
        return lngamma

    def get_lngamma_fv(self, x):
        """
        Calculates the free-volume term of the activity coefficient for a mixture.

        This implementation uses a formula to avoid numerical instability when
        `x_i` approaches zero, which is important in asymmetric API-polymer
        mixtures. The formula used is:

        ```
        phi_i^FV / x_i = v_i^F / sum_j(x_j * v_j^F)
        ```

        where
        - `phi_i^FV` is the free-volume fraction of component `i`,
        - `x_i` is the mole fraction of component `i`,
        - `v_i^F` is the free volume of component `i`,
        and the summation is over all components `j` in the mixture.

        Parameters
        ----------
        x : array_like
            Mole fractions of the components in the mixture.

        Returns
        -------
        np.ndarray
            Logarithm of the free-volume term of the activity coefficient.

        Note:
        Free-volume term of the activity coefficient according to Elbro et al.
        (can replace ln_gamma_comb of normal COSMO-SAC) - Kuo2013
        x, v_298, v_hc are 1D arrays (number of elements = number of components)
        """
        v_298 = np.array([c.v_298 for c in self.mix])
        v_hc = np.array([c.v_hc for c in self.mix])
        vf = v_298-v_hc
        sum_vf = np.sum(x*vf)
        phix = vf/sum_vf
        return np.log(phix) + 1 - phix

    def get_lngamma_sg(self, x):
        return self.COSMO.get_lngamma_comb(0, x)

    def get_lngamma_resid(self, T, x):
        return self.COSMO.get_lngamma_resid(T, x)

    def get_lngamma_comb(self, x):
        if not self._combinatorial:
            return np.zeros(len(x))
        elif self._free_volume:
            return self.get_lngamma_fv(x)
        else:
            return self.get_lngamma_sg(x)

    def get_lngamma_disp(self, x):
        if self._dispersion:
            return self.COSMO.get_lngamma_disp(x)
        else:
            return np.zeros(len(x))

    @property
    def free_volume(self):
        return self._free_volume

    @free_volume.setter
    def free_volume(self, value):
        self._free_volume = value

    @property
    def dispersion(self):
        return self._dispersion

    @dispersion.setter
    def dispersion(self, value):
        self._dispersion = value

    @property
    def combinatorial(self):
        return self._combinatorial

    @combinatorial.setter
    def combinatorial(self, value):
        self._combinatorial = value
