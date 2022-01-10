# Model Mime

M2 (Model Mime) is a generator that, given a dataset of models (that conform a meta-model) and a set of addition edit operations, generates models that are similar to the dataset under consideration. 

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

## Organization of the repository 📌

The repository contains the following folders and files:

* Folder [baselines](https://github.com/Antolin1/DMG-Python/tree/main/baselines) - It contains the synthetic models for each dataset and baseline generator (VIATRA, RANDOM and RandomEMF).
* Folder [data](https://github.com/Antolin1/DMG-Python/tree/main/data) - It contains the datasets, meta-models, and data used for testing.
* Folder [dmg](https://github.com/Antolin1/DMG-Python/tree/main/dmg) - All the Python code.
* Folder [java](https://github.com/Antolin1/DMG-Python/tree/main/java) - All the Java code.
* Folder [models](https://github.com/Antolin1/DMG-Python/tree/main/models) - Neural networks used to obtain the results presented in the paper.
* Folder [scripts](https://github.com/Antolin1/DMG-Python/tree/main/scripts) - Some useful scripts.
* Folder [stats](https://github.com/Antolin1/DMG-Python/tree/main/stats) - It contains statistics used to assess the scalability for each dataset and baseline generator (VIATRA, RANDOM and RandomEMF)..
* Folder [tests](https://github.com/Antolin1/DMG-Python/tree/main/tests) - It contains the test cases associated to the Python code.
* Folder [vsconfigs](https://github.com/Antolin1/DMG-Python/tree/main/vsconfigs) - It contains the VIATRA config files. 
* File [requirements.txt](https://github.com/Antolin1/DMG-Python/blob/main/requirements.txt) - Python libraries.

## Procedure 🚀

Steps 1 and 2 are already executed. To obtain the results of the paper, go directly to Step 3. If you want to generate models using the trained generators to see some examples, go to Step 4.

### Step 1: Dataset generation

First of all, we have to preprocess all the datasets and split them into train and test sets. This is done by the following script:

```
$ ./scripts/generateDatasets.sh
```

We consider four datasets:

* *yakindu-github*: Dataset of Yakindu Statecharts crawled from GitHub. It was used in this [paper](http://sanchezcuadrado.es/papers/models21-realistic-model-generators.pdf).
* *yakindu-exercise*: Dataset of Yakindu Statecharts used in this [paper](https://link.springer.com/article/10.1007/s10270-021-00884-z).
* *rds-genmymodel*: Dataset of database models crawled from GenMyModel. It was used in this [paper](http://sanchezcuadrado.es/papers/models21-realistic-model-generators.pdf).
* *ecore-github*: Dataset of ecore models crawled from GithHub. It was used in this [paper](http://sanchezcuadrado.es/papers/models21-realistic-model-generators.pdf).

### Step 2: Fitting and generation process

#### Case M2

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

Once M2 is trained and the generated models of the other generators are in the right folder, we can compare the four generators by executing the following (consistency, diversity and realism):

```
scripts/assessmentScript.sh 
```

To evaluate the scalability just execute the following:

```
scripts/quartileScript.sh
```

### Step 4: Model generation using M2 ⚙️

To generate models using the trained generator, just execute:

```
python scripts/generateModels.py -d rds-genmymodel -hi 64 -ms 300 -ps generatedModels/ -nm 100
python scripts/generateModels.py -d yakindu-github -hi 64 -ms 50 -ps generatedModels/ -nm 100
python scripts/generateModels.py -d yakindu-exercise -hi 64 -ms 150 -ps generatedModels/ -nm 100
python scripts/generateModels.py -d ecore-github -hi 64 -ms 200 -ps generatedModels/ -nm 100
```

where:
* `-d` establishes the dataset.
* `-hi` establishes the hidden dimension of the model (our model uses a hidden dim of 64).
* `-ms` establishes the maximum size of the generated models.
* `-ps` establishes the folder where the models will be saved.
* `-nm` establishes the number of models that will be generated.





