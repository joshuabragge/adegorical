def binary(column,column_name=None):
    unique = len(set(column))
    cols = len(bin(unique)[2:])
    print('Number of unique values:', unique)
    print('Number of columns needed:',cols)
    
    #if pandas == True
    if str(type(column)) == "<class 'pandas.core.series.Series'>":
        print('Pandas Series found!')
        import pandas as pd
        #--generate column names--#
        columns = []
        if column_name == None:
            column_name = 'binary'
        for i in range(cols):
            col_name_i = column_name + '_' + str(i)
            columns.append(col_name_i)
        #--create df--#
        df = pd.DataFrame(columns)
    
        #--create numberical remapping--#
        
        seen = set()
        #unique_set = [x for x in df.color if x not in seen and not seen.add(x)]
        unique_set = list(set(column))
        unique_numbers = [x for x in range(len(unique_set))] 
        remap = dict(zip(unique_set, unique_numbers))
        print(remap)
        column = list(column.replace(remap))
    
        #--set number of numbers expectations and add to DF--#

        for i in column:
            binary = bin(i)[2:]
            zeros = cols - len(binary)
            str_zeros = '0' * zeros
            binary = str_zeros + str(binary)
            bin_list = [int(i) for i in binary]
            df = pd.concat([df,pd.Series(bin_list)],axis=1)
        
        #--add column names and return transposed DF--#
        
        df.index = columns
        df = df.T
        df = df.reset_index().drop('index',axis=1).drop(0).reset_index().drop('index',axis=1)
        return df
    
    elif str(type(column)) == "<class 'numpy.ndarray'>":
        print('Numpy Array found!')
        import numpy as np
        
        #--create dict of unique values--#
        seen = set()
        unique_set = list(set(column))
        unique_numbers = [x for x in range(len(unique_set))] 
        remap = dict(zip(unique_set, unique_numbers))
        print(remap)
        
        #--remap dict to array--#
        copy_column = np.copy(column)
        for k, v in remap.items(): copy_column[column==k] = v
        column = copy_column.astype(int)
        
        #--create and attach the binary numbers to a list--#
        bins = []
        for i in column:
            binary = bin(i)[2:]
            zeros = 3 - len(binary)
            str_zeros = '0' * zeros
            binary = str_zeros + str(binary)
            bin_list = [int(i) for i in binary]
            bins.append(bin_list)
        bins = np.array(bins)
        
        return bins
    elif str(type([])) == "<class 'list'>":
        print('List found!')
        
        #--create dict of unique values--#
        seen = set()
        unique_set = list(set(column))
        unique_numbers = [x for x in range(len(unique_set))] 
        remap = dict(zip(unique_set, unique_numbers))
        print(remap)
        for index, item in enumerate(column):
            column[index] = remap[item] 
        
        #--create and attach the binary numbers to a list--#
        bins = []
        for i in column:
            binary = bin(i)[2:]
            zeros = 3 - len(binary)
            str_zeros = '0' * zeros
            binary = str_zeros + str(binary)
            bin_list = [int(i) for i in binary]
            bins.append(bin_list)
        
        return bins
    else:
        print('Not a valid format!')
        return None
