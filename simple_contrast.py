def contrast(column,column_name=None):
    
    #--TODO: can this be remove??--#
    #--returns dict for remapping categorical values to integers--#
    def get_remapping_dict(column):
        unique_set = list(set(column))
        unique_numbers = [x for x in range(len(unique_set))] 
        remap_dict = dict(zip(unique_set, unique_numbers)) 
        return remap_dict
    
    remap_dict = get_remapping_dict(column)
    
    #create contrast mapping
    unique = list(set(remap_dict.values()))
    last = unique[-1]
    first = unique[-2]
    baserow = [0 for x in range(len(unique)-2)]
    
    #create dictionary
    row_map = {}
    for i in unique:
        if i == last:
            new_row = [-1 for x in range(len(unique)-2)]
        elif i == first:
            new_row = [0 for x in range(len(unique)-2)]
        else:
            new_row = baserow[:]
            new_row[i] = 1
        row_map[i] = new_row
    
    series = list(column)
    
    #if pandas == True
    if str(type(column)) == "<class 'pandas.core.series.Series'>":
        import pandas as pd
        
         #--create columns--#
        if column_name == None:
            column_name = 'contrast'
        columns = []
        for i in range(len(unique)-2):
            col_name_i = column_name + '_' + str(i)
            columns.append(col_name_i)          
        
        #initialize df
        tdf = pd.DataFrame()
        
        for i in series:
            tdf = pd.concat([tdf,pd.Series(row_map[remap_dict[i]])],axis=1)
        
        tdf = tdf.T.reset_index().drop('index',axis=1).drop(0).reset_index().drop('index',axis=1)
        tdf.columns = columns
        return tdf
