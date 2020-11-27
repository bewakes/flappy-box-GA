# Genetic Algorithm that plays flappy Bird(Box)
This is a part of assignment of Knowledge Engineering course 2020. This program uses Genetic Algorithm to play flappy bird. The bird is replaced with a box. It's no fancy, just serves the purpose.

## Requirements
Any system with `python>=3.6` and `pip` will do.

## Usage
**NOTE:** These are linux specific instructions. For windows users please find equivalent command. These should work on a Mac.

1. Bare minimum [Not recommended]
    - This installs the requirements for this project along with system python libraries.
    - Install requirements: `pip install -r requirements.txt`
    - Run program: `python tsp/flappy.py`
2. Using virtualenv [Recommended]
    - Install virtualenv: `pip install virtualenv`
    - Create a virtual environment: `virtualenv myenv`
    - Activate virtualenv: `source <path-to myenv>/bin/activate`
    - Install requirements: `pip install -r requirements.txt`
    - Run program: `python tsp/flappy.py`
3. Using pipenv [Recommended, but don't bother if you don't have `pipenv`]
    - Install requirements: `pipenv install`
    - Run program: `pipenv run python tsp/flappy.py`


## Or if you want to play
Inside `main()` function of `flappy.py` module, initialize `Game` with `play=True`
