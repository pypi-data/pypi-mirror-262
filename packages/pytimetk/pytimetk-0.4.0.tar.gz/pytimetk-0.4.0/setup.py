# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytimetk',
 'pytimetk.core',
 'pytimetk.crossvalidation',
 'pytimetk.datasets',
 'pytimetk.feature_engineering',
 'pytimetk.finance',
 'pytimetk.plot',
 'pytimetk.utils']

package_data = \
{'': ['*']}

install_requires = \
['adjusttext>=0.8,<0.9',
 'holidays>=0.33,<0.34',
 'matplotlib>=3.8.0,<4.0.0',
 'pandas-flavor>=0.6.0,<0.7.0',
 'pandas>=1.5.0',
 'pathos>=0.3.1,<0.4.0',
 'plotly>=5.17.0,<6.0.0',
 'plotnine>=0.12.3,<0.13.0',
 'polars>=0.20.7,<0.21.0',
 'pyarrow>=13.0.0,<14.0.0',
 'statsmodels>=0.14.0,<0.15.0',
 'tqdm>=4.66.1,<5.0.0',
 'tsfeatures>=0.4.5,<0.5.0',
 'xarray<=2023.10.1']

setup_kwargs = {
    'name': 'pytimetk',
    'version': '0.4.0',
    'description': 'The time series toolkit for Python.',
    'long_description': '<div align="center">\n<img src="docs/logo-timetk.png" width="30%"/>\n</div>\n\n<div align="center">\n  <a href="https://github.com/business-science/pytimetk/actions">\n  <img alt="Github Actions" src="https://github.com/business-science/pytimetk/actions/workflows/timetk-checks.yaml/badge.svg"/>\n  </a>\n  <a href="https://pypi.python.org/pypi/pytimetk">\n  <img alt="PyPI Version" src="https://img.shields.io/pypi/v/pytimetk.svg"/>\n  </a>\n  <a href="https://business-science.github.io/pytimetk/contributing.html">\n  <img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"/>\n  </a>\n</div>\n\n# pytimetk\n\n> Time series easier, faster, more fun. Pytimetk.\n\n[**Please ⭐ us on GitHub (it takes 2-seconds and means a lot).**](https://github.com/business-science/pytimetk)\n\n# Introducing pytimetk: Simplifying Time Series Analysis for Everyone\n\nTime series analysis is fundamental in many fields, from business forecasting to scientific research. While the Python ecosystem offers tools like `pandas`, they sometimes can be verbose and not optimized for all operations, especially for complex time-based aggregations and visualizations.\n\nEnter **pytimetk**. Crafted with a blend of ease-of-use and computational efficiency, `pytimetk` significantly simplifies the process of time series manipulation and visualization. By leveraging the `polars` backend, you can experience speed improvements ranging from 3X to a whopping 3500X. Let\'s dive into a comparative analysis.\n\n| Features/Properties | **pytimetk**                  | **pandas (+matplotlib)**               |\n|---------------------|-------------------------------|---------------------------------------|\n| **Speed**           | 🚀 3X to 3500X Faster          | 🐢 Standard                           |\n| **Code Simplicity** | 🎉 Concise, readable syntax    | 📜 Often verbose                      |\n| `plot_timeseries()` | 🎨 2 lines, no customization  | 🎨 16 lines, customization needed    |\n| `summarize_by_time()` | 🕐 2 lines, 13.4X faster     | 🕐 6 lines, 2 for-loops               |\n| `pad_by_time()`     | ⛳ 2 lines, fills gaps in timeseries        | ❌ No equivalent    |\n| `anomalize()`       | 📈 2 lines, detects and corrects anomalies  | ❌ No equivalent    |\n| `augment_timeseries_signature()` | 📅 1 line, all calendar features    | 🕐 29 lines of `dt` extractors |\n| `augment_rolling()` | 🏎️ 10X to 3500X faster     | 🐢 Slow Rolling Operations |\n\nAs evident from the table, **pytimetk** is not just about speed; it also simplifies your codebase. For example, `summarize_by_time()`, converts a 6-line, double for-loop routine in `pandas` into a concise 2-line operation. And with the `polars` engine, get results 13.4X faster than `pandas`!\n  \nSimilarly, `plot_timeseries()` dramatically streamlines the plotting process, encapsulating what would typically require 16 lines of `matplotlib` code into a mere 2-line command in **pytimetk**, without sacrificing customization or quality. And with `plotly` and `plotnine` engines, you can create interactive plots and beautiful static visualizations with just a few lines of code.\n\nFor calendar features, **pytimetk** offers `augment_timeseries_signature()` which cuts down on over 30 lines of `pandas` dt extractions. For rolling features, **pytimetk** offers `augment_rolling()`, which is 10X to 3500X faster than `pandas`. It also offers `pad_by_time()` to fill gaps in your time series data, and `anomalize()` to detect and correct anomalies in your time series data.\n\nJoin the revolution in time series analysis. Reduce your code complexity, increase your productivity, and harness the speed that **pytimetk** brings to your workflows.\n\nExplore more at our [pytimetk homepage](https://business-science.github.io/pytimetk/).\n\n# Installation\n\nInstall the latest stable version of `pytimetk` using `pip`:\n\n```bash\npip install pytimetk\n```\n\nAlternatively you can install the development version:\n\n```bash\npip install git+https://github.com/business-science/pytimetk.git\n```\n\n# Quickstart:\n\nThis is a simple code to test the function `summarize_by_time`:\n\n```python\nimport pytimetk as tk\nimport pandas as pd\n\ndf = tk.datasets.load_dataset(\'bike_sales_sample\')\ndf[\'order_date\'] = pd.to_datetime(df[\'order_date\'])\n\ndf \\\n    .groupby("category_2") \\\n    .summarize_by_time(\n        date_column=\'order_date\', \n        value_column= \'total_price\',\n        freq = "MS",\n        agg_func = [\'mean\', \'sum\']\n    )\n```\n\n# Documentation\n\nGet started with the [pytimetk documentation](https://business-science.github.io/pytimetk/)\n\n- [📈 Overview](https://business-science.github.io/pytimetk/)\n- [🏁 Getting Started](https://business-science.github.io/pytimetk/getting-started/02_quick_start.html)\n- [🗺️ Beginner Guides](https://business-science.github.io/pytimetk/guides/01_visualization.html)\n- [📘Applied Data Science Tutorials with PyTimeTK](https://business-science.github.io/pytimetk/tutorials/01_sales_crm.html)\n\n- [📄 API Reference](https://business-science.github.io/pytimetk/reference/)\n\n# Developers (Contributors): Installation\n\nTo install `pytimetk` using [Poetry](https://python-poetry.org/), follow these steps:\n\n### 1. Prerequisites\n\nMake sure you have Python 3.9 or later installed on your system.\n\n### 2. Install Poetry\n\nTo install Poetry, you can use the [official installer](https://python-poetry.org/docs/#installing-with-the-official-installer)  provided by Poetry. Do not use pip.\n\n### 3. Clone the Repository\n\nClone the `pytimetk` repository from GitHub:\n\n```bash\ngit clone https://github.com/business-science/pytimetk\n```\n\n### 4. Install Dependencies\n\nUse Poetry to install the package and its dependencies:\n\n```bash\npoetry install\n```\n\nor you can create a virtualenv with poetry and install the dependencies\n\n```bash\npoetry shell\npoetry install\n```\n\n# 🏆 More Coming Soon...\n\nWe are in the early stages of development. But it\'s obvious the potential for `pytimetk` now in Python. 🐍\n\n- Please [⭐ us on GitHub](https://github.com/business-science/pytimetk) (it takes 2-seconds and means a lot). \n- To make requests, please see our [Project Roadmap GH Issue #2](https://github.com/business-science/pytimetk/issues/2). You can make requests there. \n- Want to contribute? [See our contributing guide here.](/contributing.html) ',
    'author': 'Business Science',
    'author_email': 'info@business-science.io',
    'maintainer': 'Matt Dancho',
    'maintainer_email': 'mdancho@business-science.io',
    'url': 'https://business-science.github.io/pytimetk/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
