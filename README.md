# eyeonwater-yolo
[![Build Status](https://jenkins.services.ai4os.eu/buildStatus/icon?job=AI4OS-hub/eyeonwater-yolo/main)](https://jenkins.services.ai4os.eu/job/AI4OS-hub/job/eyeonwater-yolo/job/main/)

eyeonwater_yolo  is an application using the DEEPaaS API.

One of the most apparent characteristics of water to the human eye is water colour. Water colour indicates the algae and organic content of the water that feeds organisms. Your observations are therefore valuable to scientists and water authorities.

To launch it, first install the package then run [deepaas](https://github.com/ai4os/DEEPaaS):
```bash
git clone https://github.com/ai4os-hub/eyeonwater-yolo
cd eyeonwater-yolo
pip install -e .
deepaas-run --listen-ip 0.0.0.0
```

## Project structure
```
│
├── Dockerfile             <- Describes main steps on integration of DEEPaaS API and
│                             eyeonwater_yolo application in one Docker image
│
├── Jenkinsfile            <- Describes basic Jenkins CI/CD pipeline (see .sqa/)
│
├── LICENSE                <- License file
│
├── README.md              <- The top-level README for developers using this project.
│
├── VERSION                <- eyeonwater_yolo version file
│
├── .sqa/                  <- CI/CD configuration files
│
├── eyeonwater_yolo    <- Source code for use in this project.
│   │
│   ├── __init__.py        <- Makes eyeonwater_yolo a Python module
│   │
│   ├── api.py             <- Main script for the integration with DEEPaaS API
│   |
│   ├── config.py          <- Configuration file to define Constants used across eyeonwater_yolo
│   │
│   └── misc.py            <- Misc functions that were helpful accross projects
│
├── data/                  <- Folder to store the data
│
├── models/                <- Folder to store models
│   
├── tests/                 <- Scripts to perfrom code testing
|
├── metadata.json          <- Metadata information propagated to the AI4OS Hub
│
├── pyproject.toml         <- a configuration file used by packaging tools, so eyeonwater_yolo
│                             can be imported or installed with  `pip install -e .`                             
│
├── requirements.txt       <- The requirements file for reproducing the analysis environment, i.e.
│                             contains a list of packages needed to make eyeonwater_yolo work
│
├── requirements-test.txt  <- The requirements file for running code tests (see tests/ directory)
│
└── tox.ini                <- Configuration file for the tox tool used for testing (see .sqa/)
```
