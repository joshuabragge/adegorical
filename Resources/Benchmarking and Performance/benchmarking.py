import os.path as path
import sys

sys.path.append(path.abspath(path.join(__file__ ,"../../..")))

import timeit
import json
import pandas as pd
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt

import adegorical as ad

performance = []

## Generate random data

np.random.seed(seed=1)

base_categories = 10
base_size = 100
multiplier = 10

data_small = ss.truncnorm.rvs(0, base_categories, size=base_size)
data_medium = ss.truncnorm.rvs(0, base_categories*multiplier, size=base_size*multiplier)
data_large = ss.truncnorm.rvs(0, base_categories*multiplier**2, size=base_size*multiplier**2)
# data_massive = ss.truncnorm.rvs(0, base_categories*multiplier**3, size=base_size*multiplier**3)

data_sets = [data_small, data_medium, 
			 data_large]

data_sets_name = ['data_small', 'data_medium', 
			 	  'data_large']

encoding_methods = ad.help()


for encoding_method in encoding_methods:
	print('==================== Checking ', encoding_method, 'Encoding ====================')

	for index, data_set in enumerate(data_sets):
		print('------ Loading ',data_sets_name[index], '------')

		list_data = list(data_set)
		numpy_data = data_set
		pandas_data = pd.Series(data_set)

		# baseline 
		if encoding_method == 'dummy':
			print('=== Checking Baseline ===')
			baseline_results = timeit.Timer(lambda: pd.get_dummies(pandas_data)).timeit(number=2)
			baseline_row = ['baseline', 'Dummy', data_sets_name[index], baseline_results]
			performance.append(baseline_row)

		# list
		print('=== Checking List ===')
		list_results = timeit.Timer(lambda: ad.get_categorical(list_data, encoding=encoding_method)).timeit(number=2)

		# numpy 
		print('=== Checking Numpy ===')
		numpy_results = timeit.Timer(lambda: ad.get_categorical(numpy_data, encoding=encoding_method)).timeit(number=2)

		# pandas
		print('=== Checking Pandas ===')
		pandas_results = timeit.Timer(lambda: ad.get_categorical(pandas_data, encoding=encoding_method)).timeit(number=2)

		pandas_row = ['Pandas', encoding_method, data_sets_name[index], pandas_results]
		numpy_row = ['Numpy', encoding_method, data_sets_name[index], numpy_results]
		list_row = ['List', encoding_method, data_sets_name[index], list_results]
		performance.append(pandas_row)
		performance.append(numpy_row)
		performance.append(list_row)

df = pd.DataFrame(performance)
df.columns = ['Data Type','Encoding Method', 'Data Size', 'Performance']
file_pathname = os.path.join('Test Results', 'performance.csv')
df.to_csv(file_pathname, index=False)


## Column increase graph
max_range = 30
results = []
unique_categorical_count = [i for i in range(max_range)]
for option in encoding_methods:
    print("Checking encoding results for", option)
    number_of_columns = []
    for i in range(max_range):
        random_data = [str(x) for x in range(i+3)]
        columns_count = ad.get_categorical(pd.Series(random_data), encoding=option).shape[1]
        number_of_columns.append(columns_count)
    results.append(number_of_columns)

for index,encoding_result in enumerate(results):
    plt.plot(unique_categorical_count, encoding_result, label=encoding_methods[index])
plt.legend()
# plt.show()
image_pathname = os.path.join('Test Results','column-growth-per-encoding')
plt.savefig(image_name)