<!-- -*- mode: markdown; fill-column: 8192 -*- -->

Adegorical
======================
Adegorical is a python package for performing advanced transformations on [categorical data](https://en.wikipedia.org/wiki/Categorical_variable). This can be particularily useful in [regression analysis](https://en.wikipedia.org/wiki/Regression_analysis) but can be applied to other machine learning techniques (at your own peril).

## Table of Contents
* [Overview](#adegorical)
* [Getting Started](#getting-started)
* [Encoding Methods](#encoding-methods)
	- [Dummy](#dummy)
	- [Binary](#binary)
	- [Simple Contrast](#simple-contrast)
	- [Simple Regression](#simple-regression)
	- [Forward Difference Contrast](#forward-diff-contrast)
	- [Backward Difference Contrast](#backward-diff-contrast)
	- [Simple Helmert](#simple-helmert)
* [Todo](#todo)

## Getting Started
This function returns the data structure it is given:
* Pandas series input returns a pandas dataframe
* Numpy column input returns a numpy array
* Python list input returns a list of lists

```python
import adegorical as ad

encoding_types = ad.help()	
print(encoding_types)	
 ['dummy', 'binary', 'simple_contrast', 'simple_regression','backward_difference_contrast', 'forward_difference_contrast', 'simple_helmert']
```

## Encoding Methods
1. [Dummy](#dummy)
2. [Binary](#binary)
3. [Simple Contrast](#simple-contrast)
4. [Simple Regression](#simple-regression)
5. [Forward Difference Contrast](#forward-diff-contrast)
6. [Backward Difference Contrast](#backward-diff-contrast)
7. [Simple Helmert](#simple-helmert)

The encoding methods in this package were built off of the work found on [UCLA's Advance Categorical Variable Encoding](http://www.ats.ucla.edu/stat/sas/webbooks/reg/chapter5/sasreg5.htm) and a [Presentation by Harris Holly](http://slideplayer.com/slide/6307838/). Unfortunately, UCLA removed the webpage from their website. [An archived version of the website can be found in this repository.](https://github.com/joshuabragge/adegorical/tree/master/Resources/UCLA%20Advance%20Categorical%20Variable%20Encoding%20Website)

### Dummy
[Dummy is the standard](https://en.wikipedia.org/wiki/Dummy_variable_(statistics)) when it comes to categorical variable encoding. N-1 columns is expected where N is the number of unique categorical variables.

```python
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
All the columns in sequential combination compose a binary representation of the categorical variable. The length of the string of the binary representation of the unique number of categorical variables is expected.

```python
colors = ['yellow', 'red', 'green', 'wenge', 'orange', 'red', 'yellow', 'blue', 'magenta', 'wenge']
df = pd.DataFrame({'colors':colors})

categorial_frame = ad.get_categorical(df['colors'],
                                          encoding='binary',
                                          reference='red',
                                          column_name='binary')
```

| binary_1 | binary_2 | binary_3 |
|:-------------:|:-------------:|:------------:|
|0|0|0|
|1|1|0|
|0|1|1|
|0|0|1|
|0|1|0|
|1|1|0|
|0|0|0|
|1|0|1|
|1|0|0|
|0|0|1|

### Simple Contrast
Instead of all zeros on our reference value as with dummy variables, the row becomes negative one. N-1 columns is expected

```python
colors = ['yellow', 'red', 'green', 'wenge', 'orange', 'red', 'yellow', 'blue', 'magenta', 'wenge']
df = pd.DataFrame({'colors':colors})

categorial_frame = ad.get_categorical(df['colors'],
                                          encoding='simple_contrast',
                                          reference='red',
                                          column_name='simple_contrast')
```

|yellow_simple_contrast|wenge_simple_contrast|orange_simple_contrast|green_simple_contrast|magenta_simple_contrast|blue_simple_contrast|
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:------------:|
|1|0|0|0|0|0|
|-1|-1|-1|-1|-1|-1|
|0|0|0|1|0|0|
|0|1|0|0|0|0|
|0|0|1|0|0|0|
|-1|-1|-1|-1|-1|-1|
|1|0|0|0|0|0|
|0|0|0|0|0|1|
|0|0|0|0|1|0|
|0|1|0|0|0|0|



## Todo
### Enhancements
#### Encoding Methods
1. Forward Difference Regression
2. Backward Difference Regression
3. Simple Helmert Regression
4. Reverse Helmert
5. Polynomial
6. Regression Polynomial
7. Deviation
8. Deviation Regression
#### Performance
1. Manipulate data in native format rather than converting to lists and back to native format (i.e. pandas data input, transforming via optimized pandas methods) 
#### Miscellaneous
1. Redo column naming convension on binary. Results are a combination of columns so having a "blue" column doesn't make much sense
### Readme
1. Simple Regression
2. Backward Difference Contrast
3. Forward Difference Contrast
4. Simple Helmert
5. Remaining encoding methods found in todo encoding methods
