# GEE-Visualise
Visualise Remote Sensing Data from GEE using Python

```
GEE-Visualise/
│
├── data/                                   <- Raw input data
│   ├── Maha_NTL_NDVI_2014_20.csv
│   └── Maha_BuiltUp_2015_2020.csv
│
├── notebooks/                              <- Jupyter notebooks for cleaning, processing, and visualisation
│   └── analysis.ipynb
│
├── src/                                    <- Source code for the project
│   ├── gee/                                
│   │   └── extract_satellite_data.txt      <- Google Earth Engine script for satellite data extraction
│   │
│   ├── setup.py                            <- Load raw data and initialize paths
│   ├── clean_data.py                       <- Clean and preprocess raw datasets
│   └── visualize_data.py                   <- Generate maps, trends, and visualisations
│
└── requirements.txt                        <- Project dependencies

```
