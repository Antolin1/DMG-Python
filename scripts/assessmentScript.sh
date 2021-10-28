#!/bin/bash

echo "Starting assessment for ecore-github"
echo ""
python ./scripts/assessment.py -d ecore-github -pd data/ecore-github/ -ms 200 -emf java -hi 64
echo "Starting assessment for yakindu-exercise"
echo ""
python ./scripts/assessment.py -d yakindu-exercise -pd data/yakindu-exercise/ -ms 150 -emf python -hi 64
echo "Starting assessment for yakindu-github"
echo ""
python ./scripts/assessment.py -d yakindu-github -pd data/yakindu-github/ -ms 50 -emf python -hi 64
echo "Starting assessment for rds-genmymodel"
echo ""
python ./scripts/assessment.py -d rds-genmymodel -pd data/rds-genmymodel/ -ms 300 -emf python -hi 64

