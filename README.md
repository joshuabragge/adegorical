# Adegorical
Advanced transformations for categorical data. T
This function can handle:
* Pandas series by returning a pandas dataframe
* Numpy column by returning an numpy array
* Python list by returning a list of lists

## Adegorical Encoding Methods:
1. Binary
2. Dummy
3. Simple Contrast
4. Simple Regression
5. Forward Difference Contrast
6. Backward Difference Contrast
7. Simple Helmert

[UCLA Advance Categorical Variable Encoding](http://www.ats.ucla.edu/stat/sas/webbooks/reg/chapter5/sasreg5.htm)


[Harris Holly Presentation](http://slideplayer.com/slide/6307838/)

## Getting Started
```python
import adegorical as ad
import pandas as pd
import numpy as np

encoding_types = ad.help()
print(encoding_types)

['dummy', 'binary', 'simple_contrast', 'simple_regression',
'backward_difference_contrast', 'forward_difference_contrast', 'simple_helmert']

colors = ['yellow', 'red', 'green', 'orange', 'red', 'yellow']
pandas_frame = pd.DataFrame({'colors':colors})

binary_pandas_frame = ad.get_categorical(pandas_frame['colors'],
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


#### Todo
1. Forward Difference Regression
2. Backward Difference Regression
3. Simple Helmert Regression
4. Reverse Helmert
5. Polynomial
6. Regression Polynomial
7. Deviation
8. Deviation Regression
