Music Analysis
==============================

Analyse Songs that made it to the Billboard Year-end Hot 100 charts.

Project Organization
------------

    ├── LICENSE
    ├── Makefile
    ├── README.md
    ├── data
    │   ├── processed
    │   └── raw
    │
    ├── docs
    │
    ├── notebooks
    │   ├── 01-analysis-billboard.ipynb
    │   ├── 02-analysis-spotify.ipynb
    │   └── 03-analysis-billboard-spotify.ipynb
    │
    ├── reports
    │   └── figures
    │
    ├── requirements.txt
    │
    ├── setup.py
    ├── src
    │   ├── __init__.py
    │   │
    │   ├── data
    │   │   ├── scrape_spotify.py
    │   │   └── scrape_billboard.py
    │   │
    │   └── preprocessing
    │       ├── preprocess_spotify.py
    │       └── preprocess_billboard.py
    │
    └── tox.ini


--------

## TODO

- [ ] Readme
- [ ] Makefile
- [ ] Docs
- [ ] Build ML models
- [ ] Add lyrics data
- [ ] Write test cases
- [ ] RecSys
- [ ] User Interface

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
