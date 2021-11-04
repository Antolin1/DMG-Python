#!/bin/bash

python scripts/train.py -k 10 -d yakindu-github -pd data/yakindu-github/ -s models/yakindu-github-finalModel.m -td models/yakindu-github-finalModel.details -e 50 -es trainloss -emf python -hi 64 -b 128

python scripts/train.py -k 10 -d ecore-github -pd data/ecore-github/ -s models/ecore-github-finalModel.m -td models/ecore-github-finalModel.details -e 50 -es trainloss -emf java -hi 64 -b 128

python scripts/train.py -k 10 -d yakindu-exercise -pd data/yakindu-exercise/ -s models/yakindu-exercise-finalModel.m -td models/yakindu-exercise-finalModel.details -e 25 -es trainloss -emf python -hi 64 -b 128

python scripts/train.py -k 10 -d rds-genmymodel -pd data/rds-genmymodel/ -s models/rds-genmymodel-finalModel.m -td models/rds-genmymodel-finalModel.details -e 50 -es trainloss -emf python -hi 64 -b 128
