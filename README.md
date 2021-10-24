# Deep Model Generation

DMG (Deep Model Generation) is a generator that, given a dataset of models (that conform a meta-model) and a set of addition edit operations, generates models that are similar to the dataset under consideration. It could have the following applications:

* To generate realistic models. For example, in the context of autonomous cars. There, unrealistic test cases are considered false positives.
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
```

```
$ mvn package
```

Execute tests:

```
$ python -m unittest discover
```

## Procedure 🚀

### Step 1: dataset generation

First of all, we have to preprocess all the datasets and split tehm into train and test sets. This is done by the following script:

```
$ ./scripts/generateDatasets.sh
```

### Step 2: fitting and generation process

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

#### Case EMF Random Instantiator


