#!/bin/bash

echo "Starting evaluation for ecore-github"
echo ""
python scripts/eval.py -m models/ecore-github-finalModel-cuda.m -d ecore-github -pd data/ecore-github/ -nm 500 -ms 200 -emf java -hi 64

echo "Starting evaluation for yakindu-exercise"
echo ""
python scripts/eval.py -m models/yakindu-exercise-finalModel-cuda.m -d yakindu-exercise -pd data/yakindu-exercise/ -nm 500 -ms 150 -emf python -hi 64

echo "Starting evaluation for yakindu-github"
echo ""
python scripts/eval.py -m models/yakindu-github-finalModel-cuda.m -d yakindu-github -pd data/yakindu-github/ -nm 500 -ms 50 -emf python -hi 64

echo "Starting evaluation for rds-genmymodel"
echo ""
python scripts/eval.py -m models/rds-genmymodel-finalModel-cuda.m -d rds-genmymodel -pd data/rds-genmymodel/ -nm 500 -ms 300 -emf python -hi 64


