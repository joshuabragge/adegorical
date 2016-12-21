def get_contrast(column, encoding=None, column_name=None):

    #--returns dict for remapping categorical values to integers--#
    def get_remapping_dict(column):
        unique_set = list(set(column))
        unique_numbers = [x for x in range(len(unique_set))] 
        remap_dict = dict(zip(unique_set, unique_numbers)) 
        return remap_dict
    
    remap_dict = get_remapping_dict(column)
    
    #create contrast mapping
    unique = list(remap_dict.values())
    
    #--create dictionary for new rows--#
    def get_row_mappings_dict(int_unique,encoding=None):
        row_mappings_dict = {}
        unique = set(int_unique)
        last = list(unique)[-1]

        if encoding == 'scontrast': # simple contrast coding
            #-- one categorical item has all -1 --#
            equalizer = 1
            baserow = [0 for x in range(len(unique)-equalizer)]
            lastrow = [-1 for x in range(len(unique)-equalizer)]
            output = 1
            comparison = None

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

        return row_mappings_dict, equalizer
    
    row_map, equalizer = get_row_mappings_dict(unique,encoding=encoding)
    
    series = list(column)
    
    #if pandas == True
    if str(type(column)) == "<class 'pandas.core.series.Series'>":
        import pandas as pd
        
         #--create columns--#
        if column_name == None:
            column_name = 'contrast'
        columns = []
        for i in range(len(unique)-equalizer):
            col_name_i = column_name + '_' + str(i)
            columns.append(col_name_i)          
        
        #initialize df
        tdf = pd.DataFrame()
        
        for i in series:
            tdf = pd.concat([tdf,pd.Series(row_map[remap_dict[i]])],axis=1)
        
        tdf = tdf.T.reset_index().drop('index',axis=1).drop(0).reset_index().drop('index',axis=1)
        tdf.columns = columns
        return tdf
