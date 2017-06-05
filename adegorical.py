def help(encoding=None):
    if encoding == 'dummy':
        print('dummy')
    elif encoding == 'binary':
        print('binary')
    elif encoding == 'simple_contrast':
        print('simple_contrast')
    elif encoding == 'simple_regression':
        print('simple_regression')
    elif encoding == 'forward_difference_contrast':
          print('forward_difference_contrast')
    elif encoding == 'backward_difference_contrast':
            print('backward_difference_contrast')
    else:
        encoding_types = ['dummy', 'binary', 'simple_contrast', 'simple_regression', 'backward_difference_contrast', 'forward_difference_contrast', 'simple_helmert']
        print(encoding_types)
        return encoding_types


def _create_remapping_dict(column, reference=None):
    '''
    Remaps categorical variables to integers for indexing purposes
    By doing this we allow the possibility of changing the reference categorical variable
    '''
    # - returns dict for remapping categorical values to integers -- #
    unique_set = list(set(column))
    unique_numbers = [x for x in range(len(unique_set))]
    categorical_int_dict = dict(zip(unique_set, unique_numbers))

    if reference is not None:
        last_value = len(categorical_int_dict) - 1
        last_value_key = next((key for key, value in categorical_int_dict.items() if value == last_value))
        swap_value = categorical_int_dict[last_value_key]
        try:
            reference_value = categorical_int_dict[reference]
        except KeyError:
            raise KeyError('Reference value not found in column')
        categorical_int_dict[reference] = swap_value
        categorical_int_dict[last_value_key] = reference_value
    else:
        print('Reference is default')
    return categorical_int_dict


def _return_pandas(column, row_mappings_dict, remap_dict, number_of_columns, encoding=None, column_name=None):

    print(remap_dict)
    import pandas as pd
     # --create columns-- #
    if column_name is None:
        if encoding is not None:
            column_name = encoding
        else:
            column_name = 'dummy'

    inv_remap_dict = {v: k for k, v in remap_dict.items()}
    columns = []
    for i in range(number_of_columns):
        col_name_i = str(inv_remap_dict[i]) + '_' + column_name
        columns.append(col_name_i)

    # initialize df
    df = []

    for categorical in list(column):
        df.append(row_mappings_dict[remap_dict[categorical]])

    df = pd.DataFrame(df)
    df.columns = columns
    return df


def _return_array(column, row_mappings_dict, remap_dict, number_of_columns):

        import numpy as np

        # --remap dict to array-- #
        copy_column = np.copy(column)
        for k, v in remap_dict.items(): copy_column[column==k] = v
        column = copy_column.astype(int)

        # --create and attach the new rows to a list-- #
        array_list = []

        for i in column:
            array_list.append(row_mappings_dict[i])
        array = np.array(array_list)

        return array


def _return_list(column, row_mappings_dict, remap_dict):
    # --create dict of unique values-- #

    for index, item in enumerate(column):
        column[index] = remap_dict[item]

    # --create and attach the new rows to a list-- #
    mapping_list = []
    for item in column:
        mapping_list.append(row_mappings_dict[item])

    return mapping_list


def _binary(column, unique_remapping_integers):

    row_mappings_dict = {}

    number_of_columns = len(bin(len(unique_remapping_integers))[2:])
    for integer in unique_remapping_integers:
        binary_value = bin(integer)[2:]
        extra_zeros = (number_of_columns - len(binary_value)) * '0'
        binary_value = extra_zeros + str(binary_value)
        binary_list = [int(integer) for integer in binary_value]
        row_mappings_dict[integer] = binary_list

    return row_mappings_dict, number_of_columns


def _dummy(column, unique_remapping_integers):
        # dummy encoding specifications
        unique_values_count = len(unique_remapping_integers)
        less_rows = 1
        number_of_columns = unique_values_count - less_rows

        baserow = [0 for x in range(number_of_columns)]
        lastrow = baserow[:]
        output = 1

        # -- create dictionary of new rows -- #
        row_mappings_dict = {}
        unique_remapping_integers = set(unique_remapping_integers) # take the largest value to avoid index error
        last_value = list(unique_remapping_integers)[-1]

        for index in set(unique_remapping_integers):

            if index != last_value:
                newrow = baserow[:]
                newrow[index] = output
            else:
                newrow = lastrow[:]

            row_mappings_dict[index] = newrow

        return row_mappings_dict, number_of_columns


def _simple_contrast(column, unique_remapping_integers):

    unique_values_count = len(unique_remapping_integers)
    less_rows = 1
    number_of_columns = unique_values_count - less_rows

    baserow = [0 for x in range(number_of_columns)]
    lastrow = [-1 for x in range(number_of_columns)]
    output = 1

    # -- create dictionary of new rows -- #
    row_mappings_dict = {}
    unique_remapping_integers = set(unique_remapping_integers) # take the largest value to avoid index error
    last_value = list(unique_remapping_integers)[-1]

    for index in set(unique_remapping_integers):

        if index != last_value:
            newrow = baserow[:]
            newrow[index] = output
        else:
            newrow = lastrow[:]

        row_mappings_dict[index] = newrow

    return row_mappings_dict, number_of_columns


def _simple_regression(column, unique_remapping_integers):
    #-- -1/k else (k-1)/k --#
    unique_values_count = len(unique_remapping_integers)
    less_rows = 1
    number_of_columns = unique_values_count - less_rows

    baserow = [(-1 / unique_values_count) for x in range(number_of_columns)]
    lastrow = baserow[:]
    output = ((unique_values_count - 1) / unique_values_count)

    # -- create dictionary of new rows -- #
    row_mappings_dict = {}
    unique_remapping_integers = set(unique_remapping_integers) # take the largest value to avoid index error
    last_value = list(unique_remapping_integers)[-1]

    for index in set(unique_remapping_integers):

        if index != last_value:
            newrow = baserow[:]
            newrow[index] = output
        else:
            newrow = lastrow[:]

        row_mappings_dict[index] = newrow

    return row_mappings_dict, number_of_columns


def _forward_difference_contrast(column, unique_remapping_integers):

    unique_values_count = len(unique_remapping_integers)
    less_rows = 1
    number_of_columns = unique_values_count - less_rows

    baserow = [0 for x in range(number_of_columns)]
    lastrow = baserow[:]
    lastrow[-1] = -1
    output = 1
    comparison = -1

    # -- create dictionary of new rows -- #
    row_mappings_dict = {}
    unique_remapping_integers = set(unique_remapping_integers) # take the largest value to avoid index error
    last_value = list(unique_remapping_integers)[-1]

    for index in set(unique_remapping_integers):

        if index != last_value:
            newrow = baserow[:]
            newrow[index] = output
        else:
            newrow = lastrow[:]
            if comparison is not None:

                    if index != 0:
                        newrow[index - 1] = comparison

        row_mappings_dict[index] = newrow

    return row_mappings_dict, number_of_columns


def _backward_difference_contrast(column, unique_remapping_integers):

    unique_values_count = len(unique_remapping_integers)
    less_rows = 1
    number_of_columns = unique_values_count - less_rows

    baserow = [0 for x in range(number_of_columns)]
    lastrow = baserow[:]
    lastrow[-1] = -1
    output = 1
    comparison = 1

    # -- create dictionary of new rows -- #
    row_mappings_dict = {}
    unique_remapping_integers = set(unique_remapping_integers) # take the largest value to avoid index error
    last_value = list(unique_remapping_integers)[-1]

    for index in set(unique_remapping_integers):

        if index != last_value:
            newrow = baserow[:]
            newrow[index] = output
        else:
            newrow = lastrow[:]
            if comparison is not None:

                    if index != 0:
                        newrow[index - 1] = comparison

        row_mappings_dict[index] = newrow

    return row_mappings_dict, number_of_columns


def _simple_helmert(column, unique_remapping_integers):

    unique_values_count = len(unique_remapping_integers)
    less_rows = 1
    number_of_columns = unique_values_count - less_rows

    baserow = [0 for x in range(number_of_columns)]
    lastrow = baserow[:]
    lastrow[-1] = -1
    lastrow[-2] = 1
    output = 1

    row_mappings_dict = {}
    unique_remapping_integers = set(unique_remapping_integers)
    last_value = list(unique_remapping_integers)[-1]

    for index in set(unique_remapping_integers):
        print(index)
        if index == last_value:
            newrow = lastrow
        else:
            newrow = baserow[:]
            length = number_of_columns - index - 1
            try:
                variable = -1 / length
            except:
                variable = -1

            for indx, value in enumerate(newrow[index:]):
                newrow[indx + index] = variable
            print(newrow)
            newrow[index] = output

        print(newrow)
        row_mappings_dict[index] = newrow

    return row_mappings_dict, number_of_columns


def get_categorical(column, encoding=None, column_name=None, reference=None):

    remap_dict = _create_remapping_dict(column=column, reference=reference)
    unique_remapping_integers = list(remap_dict.values())

    if encoding == 'dummy':
        row_mappings_dict, number_of_columns = _dummy(column, unique_remapping_integers)

    elif encoding == 'binary': # binary!
        row_mappings_dict, number_of_columns = _binary(column, unique_remapping_integers)

    elif encoding == 'simple_contrast': # simple contrast coding // SC
        row_mappings_dict, number_of_columns = _simple_contrast(column, unique_remapping_integers)

    elif encoding == 'simple_regression': # simple regression coding  // SR
        row_mappings_dict, number_of_columns = _simple_regression(column, unique_remapping_integers)

    elif encoding == 'forward_difference_contrast':
        row_mappings_dict, number_of_columns = _forward_difference_contrast(column, unique_remapping_integers)

    elif encoding == 'backward_difference_contrast':
        row_mappings_dict, number_of_columns = _backward_difference_contrast(column, unique_remapping_integers)

    elif encoding == 'simple_helmert':
        row_mappings_dict, number_of_columns = _simple_helmert(column, unique_remapping_integers)

    else:  # dummy
        row_mappings_dict, number_of_columns = _dummy(column, unique_remapping_integers)

    # to cleanup
    #  row_map, equalizer, number_of_columns = get_row_mappings_dict(unique, encoding=encoding)

    series = list(column)
    unique = list(remap_dict.values())

    # if pandas == True
    if str(type(column)) == "<class 'pandas.core.series.Series'>":
        pandas_dataframe = _return_pandas(column, row_mappings_dict, remap_dict, number_of_columns, encoding=encoding, column_name=column_name)
        return pandas_dataframe

    elif str(type(column)) == "<class 'numpy.ndarray'>":
        numpy_array = _return_array(column, row_mappings_dict, remap_dict)
        return numpy_array

    elif str(type(column)) == "<class 'list'>":
        liste = _return_list(column, row_mappings_dict, remap_dict)
        return liste

    else:
        print('Not a Pandas.Series, Numpy.array or Python.list')
        return None


'''
      to cleanup
      elif encoding == 'forward difference regression': # forward difference regression // FDR - roosevelt
          print('nothing')

      elif encoding == 'backward difference regression':
          print('nothing')


      elif encoding == 'simple helmert regression':
          print('nothing')

      elif encoding == 'reverse helmert':
          print('nothing')

      elif encoding == 'reverse helmert regression':
          print('nothing')

      elif encoding == 'polynomial':
          print('nothing')

      elif encoding == 'regression polynomial': # same as simple contrast
          print('nothing')

      elif encoding == 'deviation':
          equalizer = 1
          length = len(unique)
          baserow = [(-1/length) for x in range(len(unique)-equalizer)]
          lastrow = baserow[:]
          output = ((length-1)/length)
          comparison = None

      elif encoding == 'deviation regression': #same as simple contrast
          equalizer = 1
          baserow = [0 for x in range(len(unique)-equalizer)]
          lastrow = [-1 for x in range(len(unique)-equalizer)]
          output = 1
          comparison = None

      else:
          # dummy encoding
          equalizer = 1
          baserow = [0 for x in range(len(unique)-equalizer)]
          lastrow = baserow
          output = 1
          comparison = None
          pass
  '''
