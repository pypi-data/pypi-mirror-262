# COSMOPharm

COSMOPharm is a Python package designed to streamline the predictive modeling of drug-polymer compatibility, crucial for the development of pharmaceutical amorphous solid dispersions. Leveraging the COSMO-SAC (Conductor-like Screening Model Segment Activity Coefficient) model, COSMOPharm offers a robust platform for scientists and researchers to predict solubility, miscibility, and phase behavior in drug formulation processes.

## Features

- **Compatibility Prediction**: Utilize open-source COSMO-SAC model for prediction of drug-polymer compatibility.
- **Solubility Calculation**: Calculate drug-polymer solubilities to guide the selection of suitable polymers for drug formulations.
- **Miscibility and Phase Behavior Analysis**: Analyze the miscibility of drug-polymer pairs and understand their phase behavior under various conditions.
- **User-friendly Interface**: Easy-to-use functions and comprehensive documentation to facilitate research and development in pharmaceutical sciences.

## Installation

Please note that COSMOPharm requires the manual installation of the cCOSMO library. Refer to the [COSMOSAC GitHub page](https://github.com/usnistgov/COSMOSAC) for detailed instructions.

Once cCOSMO is installed, you can install COSMOPharm using pip:

`pip install cosmopharm`

## Quick Start

Here's a quick example to get you started with COSMOPharm: [Example](https://github.com/ivanantolo/cosmopharm/blob/main/example_usage.py)

```python
# Example usage script: example_usage.py

import cCOSMO
from cosmopharm import SLE, LLE, COSMOSAC
from cosmopharm.utils import read_params, create_components

# Rest of the script...
```

## Contributing / Getting Help

Contributions to COSMOPharm are welcome! We accept contributions via pull requests to the [GitHub repository](https://github.com/ivanantolo/cosmopharm). 

For bugs, feature requests, or other queries, please [open an issue](https://github.com/ivanantolo/cosmopharm/issues) on GitHub.


## Citation

If you use COSMOPharm in your research, please consider citing it. You can find the citation format in [CITATION.md](https://github.com/ivanantolo/cosmopharm/CITATION.md).


## License

COSMOPharm is released under the MIT License. See the [LICENSE](https://github.com/ivanantolo/cosmopharm/LICENSE) file for more details.