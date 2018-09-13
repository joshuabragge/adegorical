# Adegorical
Adegorical is a python package for performing advanced transformations on [categorical data](https://en.wikipedia.org/wiki/Categorical_variable). This can be particularily useful in [regression analysis](https://en.wikipedia.org/wiki/Regression_analysis) but can be applied to other machine learning techniques (at your own peril).

## Table of Contents
* [Encoding Methods](#encoding-methods)
	- [Dummy](#dummy)
	- [Binary](#binary)
	- [Simple Contrast](#simple-contrast)
	- [Simple Regression](#simple-regression)
	- [Forward Difference Contrast](#forward-diff-contrast)
	- [Backward Difference Contrast](#backward-diff-contrast)
	- [Simple Helmert](#simple-helmert)
* [Getting Started](#getting-started)
* [Todo](#todo)

## Encoding Methods
1. [Dummy](#dummy)
2. [Binary](#binary)
3. [Simple Contrast](#simple-contrast)
4. [Simple Regression](#simple-regression)
5. [Forward Difference Contrast](#forward-diff-contrast)
6. [Backward Difference Contrast](#backward-diff-contrast)
7. [Simple Helmert](#simple-helmert)

The encoding methods in this package were built off of the work found on [UCLA's Advance Categorical Variable Encoding](http://www.ats.ucla.edu/stat/sas/webbooks/reg/chapter5/sasreg5.htm) and a [Presentation by Harris Holly](http://slideplayer.com/slide/6307838/). Unfortunately, UCLA removed the webpage from their website. [An archived version of the website can be found in this repository.](https://github.com/joshuabragge/adegorical/tree/master/Resources/UCLA%20Advance%20Categorical%20Variable%20Encoding%20Website)

## Getting Started
This function returns the data structure it is given:
* Pandas series input returns a pandas dataframe
* Numpy column input returns a numpy array
* Python list input returns a list of lists
```python
import adegorical as ad
import pandas as pd

colors = ['yellow', 'red', 'green', 'orange', 'red', 'yellow']
df = pd.DataFrame({'colors':colors})

binary_pandas_frame = ad.get_categorical(df['colors'],
                                          encoding='binary',
                                          reference='red',
                                          column_name='binary')
```

| yellow_binary | orange_binary | green_binary |
| ------------- |:-------------:| ------------:|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 0 | 1 | 0 |
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 0 | 0 | 0 |

### Dummy
Dummy is the standard when it comes to categorical variable encoding. N-1 columns is expected where N is the number of unique categorical variables.

```python
import adegorical as ad
import pandas as pd

colors = ['yellow', 'red', 'green', 'wenge', 'orange', 'red', 'yellow', 'blue', 'magenta', 'wenge']
df = pd.DataFrame({'colors':colors})

categorial_frame = ad.get_categorical(df['colors'],
                                          encoding='dummy',
                                          column_name=None)
```

| yellow_dummy | wenge_dummy | red_dummy | green_dummy | magenta_dummy | magenta_dummy |
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:------------:|
|1|0|0|0|0|0|
|0|0|1|0|0|0|
|0|0|0|1|0|0|
|0|1|0|0|0|0|
|0|0|0|0|0|0|
|0|0|1|0|0|0|
|1|0|0|0|0|0|
|0|0|0|0|0|1|
|0|0|0|0|1|0|
|0|1|0|0|0|0|

### Binary




## Todo
1. Forward Difference Regression
2. Backward Difference Regression
3. Simple Helmert Regression
4. Reverse Helmert
5. Polynomial
6. Regression Polynomial
7. Deviation
8. Deviation Regression
