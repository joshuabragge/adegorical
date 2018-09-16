import timeit
import json
import pandas as pd
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt

import adegorical as ad

performance = {}

setup_code = '''import pandas as pd
import numpy as np
import adegorical as ad'''

## Generate random data

np.random.seed(seed=1)

base_categories = 10
base_size = 100
multiplier = 10

data_small = ss.truncnorm.rvs(0, base_categories, size=base_size)
data_medium = ss.truncnorm.rvs(0, base_categories*multiplier, size=base_size*multiplier)
data_large = ss.truncnorm.rvs(0, base_categories*multiplier**2, size=base_size*multiplier**2)
data_massive = ss.truncnorm.rvs(0, base_categories*multiplier**3, size=base_size*multiplier**3)

data_sets = [data_small, data_medium, 
			 data_large, data_massive]

data_sets_name = ['data_small', 'data_medium', 
			 	  'data_large', 'data_massive']

encoding_methods = ad.help()

for encoding_method in encoding_methods:

	for index, data_set in enumerate(data_sets):

		list_data = list(data_set)
		numpy_data = data_set
		pandas_data = pd.Series(data_set)

		# baseline 

		baseline_results = timeit.Timer(lambda: pd.get_dummies(pandas_data)).timeit(number=2)

		# list
		list_results = timeit.Timer(lambda: ad.get_categorical(list_data, encoding=encoding_method)).timeit(number=2)

		# numpy 
		numpy_results = timeit.Timer(lambda: ad.get_categorical(numpy_data, encoding=encoding_method)).timeit(number=2)

		# pandas
		pandas_results = timeit.Timer(lambda: ad.get_categorical(pandas_data, encoding=encoding_method)).timeit(number=2)

		performance['pandas'] = {encoding_method: {data_sets_name[index]: pandas_results}}
		performance['baseline'] = {encoding_method: {data_sets_name[index]: baseline_results}}
		performance['numpy'] = {encoding_method: {data_sets_name[index]: numpy_results}}
		performance['list'] = {encoding_method: {data_sets_name[index]: list_results}}

with open('performance.json', 'w') as outfile:
    json.dump(performance, outfile)

## Column increase graph
max_range = 30
results = []
unique_categorical_count = [i for i in range(max_range)]
for option in encoding_methods:
    print("Checking encoding results for", option)
    number_of_columns = []
    for i in range(max_range):
        random_data = [str(x) for x in range(i+3)]
        columns_count = ad.get_categorical(pd.Series(random_data),encoding=option).shape[1]
        number_of_columns.append(columns_count)
    results.append(number_of_columns)

for index,encoding_result in enumerate(results):
    plt.plot(unique_categorical_count, encoding_result, label=encoding_methods[index])
plt.legend()
plt.show()
plt.savefig('fig')