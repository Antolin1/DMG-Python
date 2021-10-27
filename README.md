# Deep Model Generation

DMG (Deep Model Generation) is a generator that, given a dataset of models (that conform a meta-model) and a set of addition edit operations, generates models that are similar to the dataset under consideration. It could have the following applications:

* To generate realistic models. For example, in the context of autonomous cars, unrealistic test cases are considered false positives.
* Benchmarking and stress testing.
* Data augmentation of datasets of models.

## Before using it 🛠️

Install requirements:

```
$ pip install -r requirements.txt
```

Compile maven:

```
$ cd java/model2graph
$ mvn package
```

Download EMF Random Instantiator:

```
TODO
```


Execute tests:

```
$ python -m unittest discover
```

## Procedure 🚀

### Step 1: Dataset generation

First of all, we have to preprocess all the datasets and split them into train and test sets. This is done by the following script:

```
$ ./scripts/generateDatasets.sh
```

In this repository, we consider four:

* *yakindu-github*: Dataset of Yakindu Statecharts crawled from GitHub. It was used in this [paper](http://sanchezcuadrado.es/papers/models21-realistic-model-generators.pdf).
* *yakindu-exercise*: Dataset of Yakindu Statecharts used in this [paper](https://link.springer.com/article/10.1007/s10270-021-00884-z).
* *rds-genmymodel*: Dataset of database models crawled from GenMyModel. It was used in this [paper](http://sanchezcuadrado.es/papers/models21-realistic-model-generators.pdf).
* *ecore-github*: Dataset of ecore models crawled from GithHub. It was used in this [paper](http://sanchezcuadrado.es/papers/models21-realistic-model-generators.pdf).

### Step 2: Fitting and generation process

#### Case DMG

To train the neural networks for each one of the datasets execute the following script:

```
$ ./scripts/trainModels.sh 
```

#### Case VIATRA generator

To generate the vscondigs for VIATRA, execute:

```
$ ./scripts/fitViatra.sh 
```

These config files will be the input of the VIATRA generator.

#### Case RandomEMF

The estimation of the parameters are in the notebooks of this [folder](https://github.com/Antolin1/DMG-Python/tree/main/notebooks/randomEMF).

#### Case EMF Random Instantiator

To generate models from EMF Random Instantiator, just execute:

```
scripts/fitRandomInstantiator.sh
```

### Step 3: Assessment 📋

#### Evaluating DMG

#### Comparing DMG with the other generators


### Step 4: Model generation using DMG ⚙️




