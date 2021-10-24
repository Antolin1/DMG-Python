#!/bin/bash

python scripts/datasetGeneration.py -d ecore-github -pd data/ecore-github/ -emf java
python scripts/datasetGeneration.py -d yakindu-github -pd data/yakindu-github/ -emf python
python scripts/datasetGeneration.py -d yakindu-exercise -pd data/yakindu-exercise/ -emf python
python scripts/datasetGeneration.py -d rds-genmymodel -pd data/rds-genmymodel/ -emf python
