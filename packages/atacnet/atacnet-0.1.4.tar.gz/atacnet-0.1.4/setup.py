# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atacnet']

package_data = \
{'': ['*'], 'atacnet': ['pyquic/*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'numpy>=1.25.0,<2.0.0',
 'pandas>=2.1.1,<3.0.0',
 'rich>=10.12.0,<11.0.0',
 'scanpy>=1.8.1,<2.0.0',
 'scikit-learn>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'atacnet',
    'version': '0.1.4',
    'description': 'Package for building co-accessibility networks from ATAC-seq data.',
    'long_description': '# AtacNet\n\n\n## Description\nThis repo contains a python package for inferring co-accessibility networks from single-cell ATAC-seq data, using [skggm](https://www.github.com/skggm/skggm) for the graphical lasso and [scanpy](https://www.github.com/theislab/scanpy) for data processing.\n\nIt is based on the pipeline and hypotheses presented in the manuscript "Cicero Predicts cis-Regulatory DNA Interactions from Single-Cell Chromatin Accessibility Data" by Pliner et al. (2018). The original R package [Cicero](https://cole-trapnell-lab.github.io/cicero-release/) is available [here](https://www.github.com/cole-trapnell-lab/cicero-release).\n\nResults may vary between both packages, notably due to the different implementations of graphical lasso. \n<br> Currently, scores seem proportional but absolute values differs slightly. (cf comparison plots below)\n\n\n## Installation\nThe package can be installed using pip:\n\n```\npip install atacnet\n```\n\n and from github\n```\npip install "git+https://github.com/r-trimbour/atacnet.git"\n```\n\n## Minimal example\n```\nimport anndata as ad\nimport atacnet as an\n\natac = ad.read_h5ad(\'atac_data.h5ad\')\nan.add_region_infos(atac)\nan.compute_atac_network(atac)\nan.extract_atac_links(atac)\n```\n\n## Comparison to Cicero R package\n### Toy dataset 1: \n<br> *On the same metacells obtained from Cicero code.*\n- Pearson correlation coefficient: 0.99\n- Spearman correlation coefficient: 0.98\n<img src="Figures/correlation_toy_dataset1.png" align="center" width="480"/>\n\n### Coming:\n\n_Add stats on similarity on large datasets._\n<br>\n_Add stats on runtime, memory usage._\n<br>\n_This package can be run on multiple cores._\n\n## Usage\nIt is currently developped to work with AnnData objects. Check Example1.ipynb for a simple usage example.\n\n',
    'author': 'Rémi Trimbour',
    'author_email': 'remi.trimbour@pasteur.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.13',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
