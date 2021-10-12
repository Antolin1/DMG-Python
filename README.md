# Deep Model Generation

This project has two aims:

* To build a generator of models. The input will be a set of edit operations and a dataset. The resultant models will be similar to the models in the dataset.
* To build a recommendation system for models. The idea is that this recommendation will try to anticipate the next operation.

## Before using it

Install requirements:

```
$ pip install -r requirements.txt
```

Compile java code with maven:

```
$ cd java/model2graph
```

```
$ mvn package
```

Execute tests:

```
$ python -m unittest discover
```

## Dataset generation, training phase and evaluation phase

Generate datasets:

```
$ python scripts/datasetGeneration.py -d ecore-github -pd data/ecore-github/ -emf java

```

```
$ python scripts/datasetGeneration.py -d yakindu-github -pd data/yakindu-github/ -emf python
```

```
$ python scripts/datasetGeneration.py -d yakindu-exercise -pd data/yakindu-exercise/ -emf python
```

```
$ python scripts/datasetGeneration.py -d rds-genmymodel -pd data/rds-genmymodel/ -emf python
```

Example of running the training phase:

```
$ python scripts/train.py -d ecore-github -pd data/ecore-github/ -s models/ecore-github-not-shuffle-tl.m -td models/ecore-github-not-shuffle.details -e 200 -es trainloss -sh False -emf java
```

Example of evaluating the model:

```
$ python scripts/eval.py -m models/ecore-github-not-shuffle-tl.m -d ecore-github -pd data/ecore-github/ -nm 500 -ms 200 -emf java
```

## KDE for baselines and evaluation phase of the baselines (other generators)

```
$ python scripts/kde.py -d yakindu-github -pd data/yakindu-github -emf python -g viatra -ps vsconfigs/yakindu-github/viatra
```

```
$ python ./scripts/evalBaseline.py -d yakindu-github -pd data/yakindu-github/ -emf python -g viatra -ps baselines/yakindu-github/viatra
```



