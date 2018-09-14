import unittest

import pandas as pd
import numpy as np
from adegorical import adegorical as ad


class Help(unittest.TestCase):

	encoding_types = ['dummy', 'binary', 'simple_contrast', 'simple_regression', 'backward_difference_contrast', 'forward_difference_contrast', 'simple_helmert']

	def test_help_list(self):
		adegorical_help_types = ad.help()
		self.assertEqual(len(self.encoding_types), len(adegorical_help_types))


class DataType(unittest.TestCase):
	categorical_data = ['yellow', 'red', 'yellow','red', 'magenta']
	encoding_methods = ad.help()

	def test_pandas_series_output(self):
		'''checks that pandas series is outputed'''
		pandas_series = pd.Series(self.categorical_data)
		for encoding_method in self.encoding_methods:
			encoded_results_pandas = ad.get_categorical(pandas_series, encoding=encoding_method)
			self.assertTrue(isinstance(encoded_results_pandas, pd.DataFrame))

	def test_numpy_array_output(self):
		'''checks that numpy ndarray is outputed'''
		numpy_array = np.array(self.categorical_data)
		for encoding_method in self.encoding_methods:
			encoded_results_numpy = ad.get_categorical(numpy_array, encoding=encoding_method)
			self.assertTrue(isinstance(encoded_results_numpy, np.ndarray))
				

	def test_list_output(self):
		'''checks that list is outputed'''
		python_list = self.categorical_data
		for encoding_method in self.encoding_methods:
			encoded_results_list = ad.get_categorical(python_list, encoding=encoding_method)	
			self.assertTrue(isinstance(encoded_results_list, list))


if __name__ == '__main__':
    unittest.main()