#!/bin/bash

conda create -n data-service-api python=3.10 -y
source activate data-service-api
pip install -r requirements.txt