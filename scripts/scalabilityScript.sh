#!/bin/bash

python scripts/scalability.py -m models/ecore-github-finalModel-cuda.m -d ecore-github -hi 64 -ms 200 -emf java
