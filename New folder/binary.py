def get_binary(column,column_name=None):
    unique = len(set(column))
    number_of_columns = len(bin(unique)[2:])
    
    #--returns dict for remapping categorical values to integers--#
    def get_remapping_dict(column):
        unique_set = list(set(column))
        unique_numbers = [x for x in range(len(unique_set))] 
        remap_dict = dict(zip(unique_set, unique_numbers)) 
        return remap_dict
    
    #--ensures enough 0s are added to binary number if lt than max--#
    def create_binary_number(integer,number_of_columns):
        binary_value = bin(integer)[2:]
        extra_zeros = (number_of_columns - len(binary_value)) * '0'
        binary_value = extra_zeros + str(binary_value)
        binary_list = [int(i) for i in binary_value]
        return binary_list
    
    #if pandas == True
    if str(type(column)) == "<class 'pandas.core.series.Series'>":
        import pandas as pd
        
        #--create columns--#
        if column_name == None:
            column_name = 'binary'
        columns = []
        for i in range(number_of_columns):
            col_name_i = column_name + '_' + str(i)
            columns.append(col_name_i)
    
        #--create a dict of unique values and replace--#
        remap = get_remapping_dict(column)
        column = list(column.replace(remap))
    
        #--intialize df--#
        binary_df = pd.DataFrame(columns)
        
        #--set number of numbers expectations and add to DF--#
        for i in column:
            binary_value = create_binary_number(i,number_of_columns)
            binary_df = pd.concat([binary_df,pd.Series(binary_value)],axis=1)
        
        #--add column names and return transposed DF--#
        binary_df.index = columns
        binary_df = binary_df.T.reset_index().drop('index',axis=1).drop(0).reset_index().drop('index',axis=1)
        
        return binary_df
    
    elif str(type(column)) == "<class 'numpy.ndarray'>":
        
        import numpy as np
        
        #--create dict of unique values--#
        remap = get_remapping_dict(column)
        
        #--remap dict to array--#
        copy_column = np.copy(column)
        for k, v in remap.items(): copy_column[column==k] = v
        column = copy_column.astype(int)
        
        #--create and attach the binary numbers to a list--#
        binary_list = []
        for i in column:
            binary_value = create_binary_number(i,number_of_columns)
            binary_list.append(binary_value)
        binary_array = np.array(binary_list)
        
        return binary_array
    
    elif str(type(column)) == "<class 'list'>":
        
        #--create dict of unique values--#
        remap = get_remapping_dict(column)
        for index, item in enumerate(column):
            column[index] = remap[item] 
        
        #--create and attach the binary numbers to a list--#
        binary_list = []
        for i in column:
            binary_value = create_binary_number(i,number_of_columns)
            binary_list.append(binary_value)
        
        return binary_list
    
    else:
        print('Not a pd.Series, np.array or list')
        return None
