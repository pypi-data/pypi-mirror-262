## neurons_metrics_package * NeuronsMemoryTestPipeline

## Summary
This package contains three subpackages: 
1. qa
2. frt_metrics
    - frt score calculation modules
3. mrt_metrics
    - free memory recall text recognition and score computation modules
    - ad recognition / brand recognition score computation modules

Each section is the alone standing computational package that provides scores for the selected metrics.

## Installation

Install the latest package

```
!pip install git+https://gitlab.com/neurons-inc1/data-analyst/neurons_metrics_package.git#egg=NeuronsMemoryTestPipeline
```

If the above Installation Process is not working, consider to use:

```
python3 -m pip install git+https://gitlab.com/neurons-inc1/data-analyst/neurons_metrics_package.git#egg=NeuronsMemoryTestPipeline


```

## Used Libraries:
fuzzywuzzy==0.18.0
google_cloud_aiplatform==1.42.1
matplotlib==3.8.1
numpy==1.26.4
pandas==2.2.1
pingouin==0.5.4
protobuf==4.25.3
scikit_learn==1.3.2
scipy==1.12.0
seaborn==0.13.2
setuptools==65.5.0
torch==2.2.0
tqdm==4.66.1
transformers==4.38.1
vertexai==0.0.1


## Authors
Irina White (i.white@neuronsinc.com) and Theo Sell (t.sell@neuronsinc.com)


## Project status
Project is under continuous update and monitoring.
