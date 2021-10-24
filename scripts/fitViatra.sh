#!/bin/bash

python scripts/kde.py -d yakindu-github -pd data/yakindu-github -emf python -g viatra -ps vsconfigs/yakindu-github/viatra -p False
python scripts/kde.py -d yakindu-exercise -pd data/yakindu-exercise -emf python -g viatra -ps vsconfigs/yakindu-exercise/viatra -p False
python scripts/kde.py -d ecore-github -pd data/ecore-github -emf java -g viatra -ps vsconfigs/ecore-github/viatra -p False
python scripts/kde.py -d rds-genmymodel -pd data/rds-genmymodel -emf python -g viatra -ps vsconfigs/rds-genmymodel/viatra -p False
