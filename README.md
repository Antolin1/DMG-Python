# Deep Model Generation

This project has two aims:

* To build a generator of models. The input will be a set of edit operations and a dataset. The resultant models will be similar to the models in the dataset.
* To build a recommendation system for models. The idea is that this recommendation will try to anticipate the next operation.

## Before using it

Install requirements:

```
TODO
```


Generate datasets:

```
$ python scripts/datasetGeneration.py data/rdsDataset/raw/ data/rdsDataset/preprocess data/rdsDataset/train data/rdsDataset/test data/rdsDataset/val rds
```

```
$ python scripts/datasetGeneration.py data/yakinduDataset/raw/ data/yakinduDataset/preprocess data/yakinduDataset/train data/yakinduDataset/test data/yakinduDataset/val yakindu
```

```
$ python scripts/datasetGeneration.py data/ecoreDataset/raw/ data/ecoreDataset/preprocess data/ecoreDataset/train data/ecoreDataset/test data/ecoreDataset/val ecore
```

Compile java code with maven:

```
$ cd java/model2graph

$ mvn package
```

Execute tests:

```
$ python -m unittest discover
```

