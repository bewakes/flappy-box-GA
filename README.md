# Travelling Salesman Problem(TSP) using genetic algorithm
This program uses Genetic Algorithm to find an sub-optimal solution to the travelling salesman problem.

## Requirements
Any system with `python>=3.6` and `pip` will do.

## Usage
**NOTE:** These are linux specific instructions. For windows users please find equivalent command. These should work on a Mac. 

1. Bare minimum [Not recommended]
    - This installs the requirements for this project along with system python libraries.
    - Install requirements: `pip install -r requirements.txt`
    - Run program: `python tsp/main.py`
2. Using virtualenv [Recommended]
    - Install virtualenv: `pip install virtualenv`
    - Create a virtual environment: `virtualenv myenv`
    - Activate virtualenv: `source <path-to myenv>/bin/activate`
    - Install requirements: `pip install -r requirements.txt`
    - Run program: `python tsp/main.py`
3. Using pipenv [Recommended, but don't bother if you don't have `pipenv`]
    - Install requirements: `pipenv install`
    - Run program: `pipenv run python tsp/main.py`
