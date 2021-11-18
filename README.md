# Deep Model Generation

DMG (Deep Model Generation) is a generator that, given a dataset of models (that conform a meta-model) and a set of addition edit operations, generates models that are similar to the dataset under consideration. It could have the following applications:

* To generate realistic models. For example, in the context of autonomous cars, unrealistic test cases are considered false positives.
* Benchmarking and stress testing.
* Data augmentation of datasets of models.

## Before using it 🛠️

Prerequisites:

* Java 11
* Python 3.X
* Graphviz
* Maven

Install requirements.txt:

```
$ pip install -r requirements.txt
```

Compile maven:

```
$ cd java/model2graph
$ mvn package
```

Download EMF Random Instantiator: 
* Download this [jar](https://drive.google.com/file/d/1rTuxpTZOcrDLxWjXw0Gln4dcdgdqJ2Hq/view?usp=sharing).
* Put it in this [folder](https://github.com/Antolin1/DMG-Python/tree/main/java/randomInstantiator).

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

Once DMG is trained we can evaluate its performance in terms of realism and time of generation:

```
./scripts/evaluationScript.sh
```

#### Comparing DMG with the other generators

Once DMG is trained and the generated models of the other generators are in the right folder, we can compare the four generators by executing the following (consistency, diversity and realism):

```
scripts/assessmentScript.sh 
```

To evaluate the scalability just execute the following:

```
scripts/scalabilityScript.sh
```

### Step 4: Model generation using DMG ⚙️

To generate models using the trained generator, just execute:

```
python scripts/generateModels.py -d rds-genmymodel -hi 64 -ms 300 -ps generatedModels/
python scripts/generateModels.py -d yakindu-github -hi 64 -ms 50 -ps generatedModels/
python scripts/generateModels.py -d yakindu-exercise -hi 64 -ms 150 -ps generatedModels/
python scripts/generateModels.py -d ecore-github -hi 64 -ms 200 -ps generatedModels/
```

where:
* `-d` establishes the dataset.
* `-hi` establishes the hidden dimension of the model (our model uses a hidden dim of 64).
* `-ms` establishes the maximum size of the generated models.
* `-ps` establishes the folder where the models will be saved.





