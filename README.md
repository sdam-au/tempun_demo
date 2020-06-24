# Modelling Temporal Uncertainty in Historical Datasets
* ANALYSIS

![Project_status](https://img.shields.io/badge/status-in__progress-brightgreen "Project status logo")
---

## Purpose
This repo collects all scripts and models useful for dealing with temporal uncertainty in historical & archaeological datasets.
It contains models for the uniform, normal, and trapezoidal distribution of temporal datasets, and their combinations.

---
## Authors
* Vojtěch Kaše [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)]([0000-0002-6601-1605](https://www.google.com/url?q=http://orcid.org/0000-0002-6601-1605&sa=D&ust=1588773325679000)), SDAM project, vojtech.kase@gmail.com
* Petra Heřmánková [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-6349-0540), SDAM project, petra@ancientsocialcomplexity.org

## License
CC-BY-SA 4.0, see attached License.md

## DOI
[Here will be DOI or some other identifier once we have it]

### References
[Here will go related articles or other sources we will publish/create]

---
# How to use this repository

## Sources and prerequisites
### Data
The scripts in this repository should work with all historical data with dates expressed as numerical intervals. For instance, it might be a table with two columns: `not_before` and `not_after`.

 

### Software
1. Python3
1. Jupyter Notebooks or Google Colab

### Registered account
1. Google Colab

---
## Installation
[Describe the steps necessary to install the tool/package; example: https://gist.github.com/PurpleBooth/109311bb0361f32d87a2]

---
## Instructions 
A minimal usage is just to execute the main script in your python environment, being it either local or cloud based.

```python
# (1) import requests & scipy (or: first install them with pip)
>>> import requests
>>> import scipy
# (2) path to the script
>>> url = "https://raw.githubusercontent.com/sdam-au/modelling_temporal_uncertainty/master/scripts/modelling_distributions.py"
# (3) make a request to this path
>>> resp = requests.get(url)
# (4) execute the script
>>> exec(resp.content)
```

Now you have access to the main function, `model_date()`. This function requires at least to parameters:

* `start`
* `stop`

If both `start` and `stop` are numbers, model_date(start, stop) returns a random number within the range starting with `start` and ending with `stop`.

If `stop` is not a valid number or contains an empty value, `start` is interpreted as defining a NOT BEFORE date (the so called ante quem*)

If `start` is not a valid number or contains an empty value, `stop` is interpreted as defining a NOT AFTER date (the so called *post quem*)

If `start` and `stop` are identical, the function returns the same number as well.

There are three optional parameters:

* `size=1`: how many random numbers you want to get; by default, size=1, i.e. only one number is returned
* `b`: bending point *b* defining shape of the trapezoidal distribution; by default, *b*=0.1; set to 0 to get uniform distribution
* `scale`:  scale of the half-uniform distribution used to model ante quem and post quem; by default scale=25

The function returns an individual number (if size=1; i.e. by default) or a list of numbers of length equal to size

```python
# example 1: only start and stop
>>> model_date(-340, -330)
-337
# example 2: size specified (returns a list of numbers of given size
>>> model_date(-340, -330, 10)
[-334, -333, -332, -336, -332, -338, -333, -336, -333, -331]
# example 3: model post quem (with default scale)
>>> model_date(114, "", 10)
[123, 143, 123, 149, 123, 155, 125, 115, 128, 132]
```



To use the rest of the repo:

1. First, clone this repository to your local machine.
1. Second, go to the folder `scripts/Python` and open the selected script (in Jupyter Notebooks or in Google Colab)
1. You are now set to go!


## Screenshots
![Example of the Trapezoidal distribution](https://github.com/sdam-au/modelling_temporal_uncertainty/blob/master/screenshots/Trapezoidal_distribution.png)
Example of the Trapezoidal distribution




