# Deep Model Generation

This project has two aims:

* To build a generator of models. The input will be a set of edit operations and a dataset. The resultant models will be similar to the models in the dataset.
* To build a recommendation system for models. The idea is that this recommendation will try to anticipate the next operation.

## Before using it

Install requirements:

```
$ pip install -r requirements.txt
```


Generate datasets:

```
$ python scripts/datasetGeneration.py data/yakindu-github/ yakindu-github python

```

```
$ python scripts/datasetGeneration.py data/rds-genmymodel/ rds-genmymodel python
```

```
$ python scripts/datasetGeneration.py data/ecore-github/ ecore-github java
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

Example of running the training phase:

```
$ python scripts/train.py -s models/yakindu-github-clean-shuffle.m -d yakindu-github -pd data/yakindu-github/ -e 100 -emf python -mp 10 -td models/yakindu-github-clean-shuffle.deta
```

Example of evaluating the model:

```
$ python scripts/eval.py data/yakindu-github/ yakindu-github models/yakindu-github-clean-shuffle.m 500 python 50 128
```


