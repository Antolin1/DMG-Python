#!/bin/bash

python scripts/scalabilityQuartiles.py -m models/yakindu-exercise-finalModel-cuda.m -d yakindu-exercise -hi 64 -ms 150 -emf python -pd data/yakindu-exercise/

python scripts/scalabilityQuartiles.py -m models/ecore-github-finalModel-cuda.m -d ecore-github -hi 64 -ms 200 -emf java -pd data/ecore-github/

python scripts/scalabilityQuartiles.py -m models/rds-genmymodel-finalModel-cuda.m -d rds-genmymodel -hi 64 -ms 300 -emf python -pd data/rds-genmymodel/

python scripts/scalabilityQuartiles.py -m models/yakindu-github-finalModel-cuda.m -d yakindu-github -hi 64 -ms 50 -emf python -pd data/yakindu-github/

