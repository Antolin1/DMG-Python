#!/bin/bash

python scripts/scalability.py -m models/ecore-github-finalModel-cuda.m -d ecore-github -hi 64 -ms 200 -emf java

python scripts/scalability.py -m models/yakindu-github-finalModel-cuda.m -d yakindu-github -hi 64 -ms 50 -emf python

python scripts/scalability.py -m models/yakindu-exercise-finalModel-cuda.m -d yakindu-exercise -hi 64 -ms 150 -emf python

python scripts/scalability.py -m models/rds-genmymodel-finalModel-cuda.m -d rds-genmymodel -hi 64 -ms 300 -emf python
