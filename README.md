# EyeOnWater YOLO: Deep Learning for Water Quality Assessment

[![Build Status](https://jenkins.services.ai4os.eu/buildStatus/icon?job=AI4OS-hub/eyeonwater-yolo/main)](https://jenkins.services.ai4os.eu/job/AI4OS-hub/job/eyeonwater-yolo/job/main/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A deep learning application for automated water quality assessment using YOLO (You Only Look Once) object detection and classification algorithms, integrated with the [DEEPaaS API](https://github.com/ai4os/DEEPaaS) framework for scientific applications.

## Scientific Background

Water color is one of the most apparent optical characteristics observable to the human eye and serves as a primary indicator of water quality. This helps researchers classify rivers, lakes, coastal waters, seas, and oceans by colour. It can be used for both fresh and saline natural waters.
This automated classification system utilizes computer vision and deep neural networks to analyze water quality parameters from optical imagery, providing quantitative assessments for environmental monitoring and water management applications.

**System Capabilities:**

- Real-time water quality classification using convolutional neural networks
- RESTful API integration via DEEPaaS framework for scientific workflows
- Support for multi-spectral image-based water analysis
- Docker containerization for reproducible deployments
- Comprehensive validation and testing framework

## Installation and Deployment

### Local Installation

1. **Clone the repository:**

```bash
git clone https://github.com/ai4os-hub/eyeonwater-yolo
cd eyeonwater-yolo
```

2. **Install dependencies:**

```bash
pip install -e .
```

3. **Launch the API service:**

```bash
deepaas-run --listen-ip 0.0.0.0
```

The API will be available at `http://localhost:5000`

### Docker Deployment

```bash
docker build -t eyeonwater-yolo .
docker run -p 5000:5000 eyeonwater-yolo
```

## API Interface and Usage

### Available Endpoints

Once the service is running, you can access:

- **Swagger UI:** `http://localhost:5000/ui/` - Interactive API documentation
- **Prediction endpoint:** `POST /v2/models/eyeonwater-yolo/predict`
- **Metadata endpoint:** `GET /v2/models/eyeonwater-yolo/`

### Example Implementation

```python
import requests

# Upload an image for water quality analysis
files = {'data': open('water_sample.jpg', 'rb')}
response = requests.post('http://localhost:5000/v2/models/eyeonwater-yolo/predict', files=files)
result = response.json()
print(result)
```

## Technical Specifications

- **Framework:** TensorFlow/Ultralytics YOLOv8
- **Task:** Classification
- **Data Type:** Images
- **Dataset:** [Zenodo Dataset](https://zenodo.org/records/14017143)
- **Pre-trained Models:** YOLOv8 variants included

## Repository Structure

```text
eyeonwater-yolo/
│
├── Dockerfile                   <- Container configuration for deployment
├── Jenkinsfile                 <- CI/CD pipeline configuration
├── LICENSE                     <- MIT license
├── README.md                   <- Project documentation
├── VERSION                     <- Version information
├── pyproject.toml              <- Python package configuration
├── requirements.txt            <- Production dependencies
├── requirements-test.txt       <- Testing dependencies
├── tox.ini                     <- Testing automation config
├── ai4-metadata.yml            <- AI4OS Hub metadata
├── metadata.json               <- Legacy metadata
│
├── data/                       <- Data storage directory
├── models/                     <- Pre-trained model files
│   ├── best.pt                 <- Custom trained model
│   ├── yolov8n-cls.pt         <- YOLOv8 nano classification
│   └── yolov8n.pt             <- YOLOv8 nano detection
│
├── eyeonwater_yolo/            <- Main package source code
│   ├── __init__.py             <- Package initialization
│   ├── api.py                  <- DEEPaaS API integration
│   ├── config.py               <- Configuration management
│   ├── misc.py                 <- Utility functions
│   └── schema.py               <- Data validation schemas
│
└── tests/                      <- Test suite
    ├── __init__.py             <- Test package init
    └── test_api.py             <- API endpoint tests
```

## Development Environment

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git
- Docker (optional)

### Setting up Development Environment

1. **Clone and navigate:**

```bash
git clone https://github.com/ai4os-hub/eyeonwater-yolo
cd eyeonwater-yolo
```

2. **Create virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  
# On Windows:
python -m venv venv
venv\Scripts\activate
```

3. **Install in development mode:**

```bash
pip install -e .
pip install -r requirements-test.txt
```

### Testing Framework

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=eyeonwater_yolo

# Run tox for multiple Python versions
tox
```

### Quality Assurance

The project implements several tools for code quality maintenance:

- **pytest** for unit and integration testing
- **tox** for multi-version Python compatibility testing
- **Jenkins** for continuous integration and deployment

## API Documentation

### Prediction Endpoint

**POST** `/v2/models/eyeonwater-yolo/predict`

**Parameters:**

- `data` (file): Image file for water quality analysis
- `accept` (string): Response format (application/json)

**Response:**

```json
{
  "predictions": [
    {
      "file_name": "image0.jpg",
      "class_name": "water_good",
      "confidence": 0.9981828331947327
    }
  ],
  "timestamp": "2025-07-03T14:42:07.463860",
  "model_used": "best.pt"
}
```

### Model Information Endpoint

**GET** `/v2/models/eyeonwater-yolo/`

Returns model metadata and configuration information.

## Related Resources

- **Dataset:** [EyeOnWater Dataset on Zenodo](https://zenodo.org/records/14017143)
- **AI4OS Hub:** [Project Page](https://dashboard.cloud.ai4os.eu/)
- **DEEPaaS API:** [Documentation](https://docs.ai4os.eu/en/latest/user/overview/api.html)
- **Docker Image:** `ai4oshub/eyeonwater-yolo`

## Model Performance

The model is based on YOLOv8 architecture and has been specifically trained for water quality classification tasks. Performance metrics and validation results can be found in the training documentation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- **Thomas Warbout** - [thomas@maris.nl](mailto:tjerk@maris.nl)
- **Tjerk Krijger** - [tjerk@maris.nl](mailto:thomas@maris.nl)

## Acknowledgments

- AI4OS project for the DEEPaaS framework
- Ultralytics for the YOLO implementation
- The water quality research community
- Contributors and maintainers

Developed for water quality monitoring and environmental research applications
