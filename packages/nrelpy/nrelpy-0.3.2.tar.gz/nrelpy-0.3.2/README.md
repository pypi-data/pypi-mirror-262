[![Build Status](https://github.com/samgdotson/nrelpy/actions/workflows/python-app.yml/badge.svg)](https://github.com/samgdotson/nrelpy/actions/workflows/python-app.yml)
# nrelpy
Simple API to interact with the National Renewable Energy Laboratory's Annual Technology Baseline

## Features and Datasets

`nrelpy` currently enables access to the following datasets:
* Annual Technology Baseline
    - Transportation (2020)
    - Electricity (2019 - 2022)
* GIS Renewable Energy Potential (state-level resolution)

### Installing

This package may be installed from [PyPI](https://pypi.org/project/nrelpy/) with 

`pip install nrelpy`

### Using

The motivation for this API is to relieve researchers of the need to carry datasets
in their repositories. Therefore, the most basic function of `nrelpy` returns a 
dataset as a pandas dataframe. This basic usage is shown below.


#### ATB
Users can access either the ATB datasets for both transportation and electricity
and interact with it as a `pandas.DataFrame`.

```py
import nrelpy.atb as ATB

year = 2022
database = 'electricity'

df = ATB.as_dataframe(year=year, database=database)
```

Alternatively, users can import the `ATBe` class for a simpler interface to the data.

```py
from nrelpy.atb import ATBe

atbe = ATBe(year=2022)

# Downloading NREL ATB electricity from 2022
# Download Successful.

atbe(technology='Nuclear',
     core_metric_parameter='LCOE',
     core_metric_case='R&D',
     scenario='Moderate',
     crpyears='60',
     ).head(5)
```
```bash
Out[3]: 
display_name          Nuclear - AP1000  Nuclear - Small Modular Reactor
core_metric_variable                                                   
2020                         65.987664                        65.665363
2021                         65.748826                        65.408952
2022                         65.520452                        65.163004
2023                         65.302550                        64.927528
2024                         64.205891                        64.681539
```

#### Renewable Potential

```py
import nrelpy.re_potential as REP

df = REP.as_dataframe()
```

### Testing

From the top-level `nrelpy` directory, run `pytest`.  

You can also check the testing coverage with

```bash
pytest --cov-config=.coveragerc --cov=nrelpy
coverage html
```
`coverage html` creates a nicely formatted html page with 
the entire coverage report. Simply open the `htmlcov/index.html` file in your browser.

### Contributing

Contributors should clone the repository and install an editable installation.

```bash
git clone https://github.com/samgdotson/nrelpy.git

cd nrelpy

pip install -e .
```

*All pull requests must include appropriate, passing, tests.*

Issues and feature requests are welcome.
