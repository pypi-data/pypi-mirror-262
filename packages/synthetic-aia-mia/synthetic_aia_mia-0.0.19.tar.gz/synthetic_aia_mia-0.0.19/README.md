# Impact of using synthetic data on MIA and AIA

## API documentation
The [documentation](docs/build/html/index.html) is generated using [sphinx](https://www.sphinx-doc.org/).
To view it, clone the repo and use your web browser to open docs/build/html/index.html.
To regenerate the API documentation: 
```bash
sphinx-apidoc -f -F -o docs src;
sphinx-build -M html docs docs/build/
```


## Tests
Unit tests are setup in the test directory.
They use the python unittest packages.
To run all tests:
```bash
python -m unittest discover -v -p "*.py" -s test
```

## Installation
Instal with pip in a venv.
In the directory containing pyproject.toml :
```bash
 pip install --editable .
 ```

## Usage 
```python
#Load data
from synthetic.fetch_data import adult
from synthetic.fetch_data import utk
data_adult = adult.load()
data_utk = utk.load()

#Train a neural network an adult 
form synthetic.predictor.adult import AdultNN
adultNN = AdultNN()
adultNN.fit(data_adult["train"])

#Evalute trained neural network
adultNN.predict(data_adult["test"])
```

## Datasets
### Adult
We are using [folktables adult](https://github.com/socialfoundations/folktables).

### UTKFaces
From Kaggle: jangedoo/utkfaces-new.
For loading and parsing files we use [aia_fairness.dataset_processing](https://pypi.org/project/aia-fairness/)
