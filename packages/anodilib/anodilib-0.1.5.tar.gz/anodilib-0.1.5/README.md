# ANODI

This is the Python library **ANODI** for Time Series Anomaly Detection. It offers easy access to algorithms and benchmark data.

## Short Description

- the core of the ANODI library is the **algorithm** class (```anodilib.algorithm```) that wrapps an algorithm and the data that the algorithm should be fit on. It has - for example - the following attributes:
   - ``` self.X_train_df, self.Y_train_df, self.X_test_df, self.Y_test_df```: Dataframes for train and test data and labels
   - ```train_dls, test_dls```: Dataloaders (fastAI Usage) for train and test data
   - ```learner```: The Learner object for fastAI
   - most of the algorithms have additional attributes for _window_length_, _stride_ and _batch_size_
- the data and some meta arguments are set up as a ```DatasetSpecification``` in the ```data``` module and given as argument to the ```algorithm``` object. 
   - If not overriden by another test-DatasetSpecification in the ```predict``` function, the given data behind des DatasetSpecification is automatically split into the Dataframes and Dataloaders from above using the parameter ```test_fraction```
- ANODI offers the following modules: ```algorithm```, ```data```, ```metrics```, ```model```(containing the underlying pytorch models), ```visualization```

## Example Usage

- **Example Usage of IsolationForest Algorithm on the ECG200_TRAIN Dataset**:

```python 
from anodilib.algorithm.IsolationForest import IsolationForest as IF
from anodilib.data.DatasetSpecification import ECG200_TRAIN

alg = IF(dataset_specification=ECG200_TRAIN, contamination="auto", test_fraction=0.2)
alg.fit()
alg.predict()
anoms = alg.getAnomalies()

print(anoms)
```

- **Example Usage of ModifiedLSTM Algorithm on the ECG200_TRAIN Dataset using c_f1_score Metric**:

```python
from anodilib.algorithm.ModifiedLSTM import ModifiedLSTM
from anodilib.data.DatasetSpecification import ECG200_TRAIN
from metrics.cmetrics import c_f1_score
import numpy as np

alg = ModifiedLSTM(dataset_specification=ECG200_TRAIN, batch_size=28,window_len=4, stride=1)

alg.fit(epoch_num=50, learning_rate="lr_find",learning_rate_iteration=200)
alg.fit(epoch_num=50, learning_rate="lr_find",learning_rate_iteration=200)
alg.fit(epoch_num=50, learning_rate="lr_find",learning_rate_iteration=200)
alg.fit(epoch_num=50, learning_rate="lr_find",learning_rate_iteration=200)

alg.predict()

anoms, _ , _ = alg.getAnomalies()
print(anoms)
print(c_f1_score(anoms, np.array(alg.Y_test_df)))
```

- **Example on how to put your local data into a DatasetSpecification** (here: _WADI_ Dataset)

```python
from anodilib.data.DatasetSpecification import DatasetSpecification

WADI = DatasetSpecification(
    dataset_name="WADI.A2_19_Nov_2019_WADI_attackdataLABLE.csv",
    location=None,
    delimiter=",",
    label_column=130, # column containing the label
    is_data_column=lambda c: c != 130 and c >= 3, # use data of columns
    columns=None,
    skip_header=3,
    skip_footer=3,
    label_realizations=[1, -1],
    decimal=".",
    only_first_n_entries=-1, # if -1, use all entries
    predefined_dataset=None,
)

# use for algorithms ...

```

- for more information, have a look at the ```anodilib/tests/``` or on our [Githlib Repository](https://gitlab.fachschaften.org/timonius/anodi/)

## Dev Installation

This package is built using poetry, run the following code to install an editable version of the package for development
```
pip install poetry
poetry install
```