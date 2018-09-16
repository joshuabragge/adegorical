import unittest

import numpy as np
import pandas as pd
import scipy.stats as ss

import adegorical as ad

base_categories = 10
base_size = 100
multiplier = 10

np.random.seed(seed=1)

data_simple = ['yellow', 'red', 'yellow','red', 'magenta']
# 10 unique / 100 count
data_small = ss.truncnorm.rvs(0, base_categories, size=base_size)
# 50 unique/ 1000 count
data_medium = ss.truncnorm.rvs(0, base_categories*multiplier/2, size=base_size*multiplier)

test_datasets = [data_simple, data_small, data_medium]

encoding_methods = ad.help()

class Help(unittest.TestCase):
	"""
	Ensures the help function has all the encoding methods available
	"""

	encoding_types = ['dummy', 'binary', 'simple_contrast', 'simple_regression', 'backward_difference_contrast', 'forward_difference_contrast', 'simple_helmert']

	def test_help_list(self):
		self.assertEqual(len(self.encoding_types), len(encoding_methods))


class DataType(unittest.TestCase):
	"""
	Checks that methods return the data type given 
	for all encoding methods
	"""

	def test_pandas_series_output(self):
		pandas_series = pd.Series(data_simple)
		for encoding_method in encoding_methods:
			encoded_results_pandas = ad.get_categorical(pandas_series, encoding=encoding_method)
			self.assertTrue(isinstance(encoded_results_pandas, pd.DataFrame))

	def test_numpy_array_output(self):
		numpy_array = np.array(data_simple)
		for encoding_method in encoding_methods:
			encoded_results_numpy = ad.get_categorical(numpy_array, encoding=encoding_method)
			self.assertTrue(isinstance(encoded_results_numpy, np.ndarray))
				

	def test_list_output(self):
		python_list = data_simple
		for encoding_method in encoding_methods:
			encoded_results_list = ad.get_categorical(python_list, encoding=encoding_method)	
			self.assertTrue(isinstance(encoded_results_list, list))


class DummyEncoding(unittest.TestCase):
	"""
	Test cases for dummy variable encoding.
	Checks that the correct number of columns are returned for dummy encoded objects. 
	n-1 columns should be returned where n is the number of unique variables.
	"""
	def test_dummy_list_column_size(self):

		for test_dataset in test_datasets:
			unique_variables = len(set(test_dataset))
			test_dataset_column_count = unique_variables - 1
			encoded_results_column_count = len(ad.get_categorical(test_dataset, encoding='dummy')[0])
			self.assertEqual(test_dataset_column_count, encoded_results_column_count)

	def test_dummy_pandas_column_size(self):

		for test_dataset in test_datasets:
			unique_variables = len(set(test_dataset))
			test_dataset_column_count = unique_variables - 1
			test_dataset_pandas = pd.Series(test_dataset)
			encoded_results_column_count = ad.get_categorical(test_dataset_pandas, encoding='dummy').shape[1]
			self.assertEqual(test_dataset_column_count, encoded_results_column_count)

	def test_dummy_numpy_column_size(self):

		for test_dataset in test_datasets:
			unique_variables = len(set(test_dataset))
			test_dataset_column_count = unique_variables - 1
			test_dataset_numpy = np.array(test_dataset)
			encoded_results_column_count = len(ad.get_categorical(test_dataset_numpy, encoding='dummy')[0])
			self.assertEqual(test_dataset_column_count, encoded_results_column_count)


class InputCheck(unittest.TestCase):
	"""Checks edge cases to make sure proper handling is administrated"""

	def test_list_zero_len_dataset(self):
		zero_dataset = []

		for encoding_method in encoding_methods:
			self.assertRaises(ad.OutOfRangeError, ad.get_categorical, column=zero_dataset, encoding=encoding_method)

	def test_numpy_zero_len_dataset(self):
		zero_dataset = np.array([])

		for encoding_method in encoding_methods:
			self.assertRaises(ad.OutOfRangeError, ad.get_categorical, column=zero_dataset, encoding=encoding_method)
			
	def test_pandas_zero_len_dataset(self):
		zero_dataset = pd.Series([])

		for encoding_method in encoding_methods:
			self.assertRaises(ad.OutOfRangeError, ad.get_categorical, column=zero_dataset, encoding=encoding_method)
	
	def test_list_one_len_dataset(self):
		one_dataset = ['len_of_one']

		for encoding_method in encoding_methods:
			self.assertRaises(ad.OutOfRangeError, ad.get_categorical, column=one_dataset, encoding=encoding_method)

	def test_numpy_one_len_dataset(self):
		one_dataset = np.array(['len_of_one'])

		for encoding_method in encoding_methods:
			self.assertRaises(ad.OutOfRangeError, ad.get_categorical, column=one_dataset, encoding=encoding_method)
			
	def test_pandas_one_len_dataset(self):
		one_dataset = pd.Series(['len_of_one'])

		for encoding_method in encoding_methods:
			self.assertRaises(ad.OutOfRangeError, ad.get_categorical, column=one_dataset, encoding=encoding_method)

	def test_none_input(self):
		for encoding_method in encoding_methods:
			self.assertRaises(ad.InvalidDataTypeError, ad.get_categorical, column=None, encoding=encoding_method)

if __name__ == '__main__':
    unittest.main()