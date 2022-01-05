#!/bin/bash

python scripts/train.py -k 10 -d yakindu-github -pd data/yakindu-github/ -s models/yakindu-github-finalModel-cuda.m -td models/yakindu-github-finalModel-cuda.details -e 50 -es trainloss -emf python -hi 64 -b 128 -dev cuda

python scripts/train.py -k 10 -d ecore-github -pd data/ecore-github/ -s models/ecore-github-finalModel-cuda.m -td models/ecore-github-finalModel-cuda.details -e 75 -es trainloss -emf java -hi 64 -b 128 -dev cuda

python scripts/train.py -k 10 -d yakindu-exercise -pd data/yakindu-exercise/ -s models/yakindu-exercise-finalModel-cuda.m -td models/yakindu-exercise-finalModel-cuda.details -e 25 -es trainloss -emf python -hi 64 -b 128 -dev cuda

python scripts/train.py -k 10 -d rds-genmymodel -pd data/rds-genmymodel/ -s models/rds-genmymodel-finalModel-cuda.m -td models/rds-genmymodel-finalModel-cuda.details -e 75 -es trainloss -emf python -hi 64 -b 128 -dev cuda
