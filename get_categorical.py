def get_categorical(column, encoding=None, column_name=None):

    #--returns dict for remapping categorical values to integers--#
    unique_set = list(set(column))
    unique_numbers = [x for x in range(len(unique_set))] 
    remap_dict = dict(zip(unique_set, unique_numbers)) 
    
    #create list of all unique variables in dict
    unique = list(remap_dict.values())
    
    #--create dictionary for new rows--#
    
    row_mappings_dict = {}
    unique = set(unique)
    last = list(unique)[-1]

    if encoding == 'scontrast': # simple contrast coding
        #-- one categorical item has all -1 --#
        equalizer = 1
        baserow = [0 for x in range(len(unique)-equalizer)]
        lastrow = [-1 for x in range(len(unique)-equalizer)]
        output = 1
        comparison = None

    elif encoding == 'binary': #binary!
        equalizer = 0

    elif encoding == 'sregression': #simple regression coding 
        #-- -1/k else (k-1)/k --#
        equalizer = 1
        length = len(unique)
        baserow = [(-1/length) for x in range(len(unique)-equalizer)]
        lastrow = baserow
        output = ((length-1)/length)
        comparison = None

    elif encoding == 'fdiff': #forward difference contrast coding
        equalizer = 1
        baserow = [0 for x in range(len(unique)-equalizer)]
        lastrow = baserow[:]
        lastrow[-1] = -1
        output = 1
        comparison = -1

    else:
        #dummy encoding
        equalizer = 1
        baserow = [0 for x in range(len(unique)-equalizer)]
        lastrow = baserow
        output = 1
        comparison = None

    if encoding == 'binary': 
        number_of_columns = len(bin(len(unique))[2:])
        for i in unique:
            integer = i
            binary_value = bin(integer)[2:]
            extra_zeros = (number_of_columns - len(binary_value)) * '0'
            binary_value = extra_zeros + str(binary_value)
            binary_list = [int(i) for i in binary_value]
            row_mappings_dict[i] = binary_list   

    else:
        for i in unique:
            if i == last:
                newrow = lastrow
            else:
                newrow = baserow[:]
                newrow[i] = output
                if comparison != None:
                    try:
                        newrow[i-1] = comparison
                    except:
                        pass
            row_mappings_dict[i] = newrow

        number_of_columns = len(unique)-equalizer         
    
    #row_map, equalizer, number_of_columns = get_row_mappings_dict(unique,encoding=encoding)
    
    row_map = row_mappings_dict
    
    series = list(column)
    unique = list(remap_dict.values())
    
    #if pandas == True
    if str(type(column)) == "<class 'pandas.core.series.Series'>":
        import pandas as pd
        
         #--create columns--#
        if column_name == None:
            if encoding != None:
                column_name = encoding
            else:
                column_name = 'dummy'
        columns = []
        for i in range(number_of_columns):
            col_name_i = column_name + '_' + str(i)
            columns.append(col_name_i)          
        
        #initialize df
        df = pd.DataFrame()
        
        for i in series:
            df = pd.concat([df,pd.Series(row_map[remap_dict[i]])],axis=1)
        
        df = df.T.reset_index().drop('index',axis=1).drop(0).reset_index().drop('index',axis=1)
        df.columns = columns
        return df
    
    elif str(type(column)) == "<class 'numpy.ndarray'>":
        
        import numpy as np
        
        #--create dict of unique values--#
        #remap_dict = get_remapping_dict(column)
        
        #--remap dict to array--#
        copy_column = np.copy(column)
        for k, v in remap_dict.items(): copy_column[column==k] = v
        column = copy_column.astype(int)
        
        #--create and attach the new rows to a list--#
        array_list = []
        for i in column:
            array_list.append(row_map[i])
        array = np.array(array_list)
        
        return array
    
    elif str(type(column)) == "<class 'list'>":
        
        #--create dict of unique values--#
        #remap = get_remapping_dict(column)
        
        for index, item in enumerate(column):
            column[index] = remap_dict[item] 
        
        #--create and attach the new rows to a list--#
        mapping_list = []
        for i in column:
            mapping_list.append(row_map[i])
    
        return mapping_list
    
    else:
        print('Not a pd.Series, np.array or list')
        return None
