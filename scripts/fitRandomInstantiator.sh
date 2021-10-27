#!/bin/bash

python scripts/kdeRandomInstantiator.py -d yakindu-github -pd data/yakindu-github -emf python -ps baselines/yakindu-github/randomInstantiator/ -p False
python scripts/kdeRandomInstantiator.py -d yakindu-exercise -pd data/yakindu-exercise -emf python -ps baselines/yakindu-exercise/randomInstantiator/ -p False
python scripts/kdeRandomInstantiator.py -d ecore-github -pd data/ecore-github -emf java -ps baselines/ecore-github/randomInstantiator/ -p False
python scripts/kdeRandomInstantiator.py -d rds-genmymodel -pd data/rds-genmymodel -emf python -ps baselines/rds-genmymodel/randomInstantiator/ -p False
