def binary(column,column_name=None):
    unique = len(column.unique())
    cols = len(bin(unique)[2:])
    print('Number of columns needed:',cols)
    
    #--generate column names--#
    columns = []
    if column_name == None:
        column_name = ''
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
    
    #--set expectations--#
    for i in column:
        binary = bin(i)[2:]
        zeros = cols - len(binary)
        str_zeros = '0' * zeros
        binary = str_zeros+str(binary)
        bin_list = [i for i in binary]
        df = pd.concat([df,pd.Series(bin_list)],axis=1)
    df.index = columns
    df = df.T
    df = df.reset_index().drop('index',axis=1).drop(0).reset_index().drop('index',axis=1)
    return df
