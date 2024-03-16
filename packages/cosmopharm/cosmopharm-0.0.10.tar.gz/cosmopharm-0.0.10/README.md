# COSMOPharm

<p align="center">
  <img src="https://github.com/ivanantolo/cosmopharm/raw/main/TOC.png" alt="TOC Figure" width="400"/>
</p>

<img src="https://github.com/ivanantolo/cosmopharm/raw/main/TOC.png" alt="TOC Figure" width="400"/>

![TOC Figure](https://raw.githubusercontent.com/ivanantolo/cosmopharm/main/TOC.png)

<img src="https://raw.githubusercontent.com/ivanantolo/cosmopharm/main/TOC.png" alt="TOC Figure" width="400"/>

<!-- <p align="center"> -->
![TOC Figure](https://raw.githubusercontent.com/ivanantolo/cosmopharm/main/TOC.png)
<!-- </p> -->


Welcome to the COSMOPharm repository, accompanying [our paper in *J. Chem. Theory Comput.*](https://dx.doi.org/10.1021/acs.jctc.9b01016). This project and its associated publication offer insights and a practical toolkit for researching drug-polymer and drug-solvent systems, aiming to provide the scientific community with the means to reproduce our findings and further the development of COSMO-SAC-based models.

## About 

COSMOPharm is a Python package designed to streamline the predictive modeling of drug-polymer compatibility, crucial for the development of pharmaceutical amorphous solid dispersions. Apart from that, it can also be used for the miscibility/solubility of drugs with/in common solvents. Leveraging the COSMO-SAC (Conductor-like Screening Model Segment Activity Coefficient) model, COSMOPharm offers a robust platform for scientists and researchers to predict solubility, miscibility, and phase behavior in drug formulation processes.

## Features

- **Compatibility Prediction**: Utilize open-source COSMO-SAC model for prediction of drug-polymer compatibility.
- **Solubility Calculation**: Calculate drug-polymer solubilities to guide the selection of suitable polymers for drug formulations.
- **Miscibility and Phase Behavior Analysis**: Analyze the miscibility of drug-polymer pairs and understand their phase behavior under various conditions.
- **User-friendly Interface**: Easy-to-use functions and comprehensive documentation to facilitate research and development in pharmaceutical sciences.

## Installation

### Quick Installation
For most users, the quickest and easiest way to install COSMOPharm is via pip, which will manage all dependencies for you. Ensure you have already installed the cCOSMO library by following the instructions on the [COSMOSAC GitHub page](https://github.com/usnistgov/COSMOSAC).

Once cCOSMO is installed, you can install COSMOPharm directly from [PyPI](https://pypi.org/project/cosmopharm/):

```
pip install cosmopharm
```

### Advanced Installation Options

For users who need more control over the installation process (e.g., for development purposes or when integrating with other projects), COSMOPharm can also be installed by cloning the repository and installing manually. 

#### Step 1: Clone the Repository

First, clone the COSMOPharm repository:
```
git clone https://github.com/ivanantolo/cosmopharm
```

#### Step 2: Navigate to the Repository Directory

```
cd cosmopharm
```

#### Option 1: Using pip to Install from Local Source

This method installs COSMOPharm and manages all dependencies efficiently:

```
pip install .
```


#### Option 2: Using setup.py for Installation

Alternatively, you can run the setup script directly:

```
python setup.py install
```

While this method is straightforward, using `pip` is generally preferred for its dependency management capabilities.

Please note: Before proceeding with either advanced installation option, ensure the cCOSMO library is installed as described at the beginning of this section.

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