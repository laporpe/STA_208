#!/usr/bin/env python
# coding: utf-8

#To use in notebooks
#from Functions import Cleaning_Functions
#cl = Cleaning_Functions()


# Ana's functions

import numpy as np
import pandas as pd 

class Cleaning_Functions:
    """
     Conatins all our function we want to use 
    """


#     def __init__(self,df):

    def getNAs(self, df):
        colNames = []
        percentNA = []
        for i in df.columns:
            colNames.append(i)
            numNA = df[i].isna().sum()
            percent = (numNA/len(df))*100
            percentNA.append(percent)

        colNames = pd.DataFrame(colNames)
        colNames = colNames.rename(columns={0: "label"})
        percentNA = pd.DataFrame(percentNA)
        percentNA = percentNA.rename(columns={0: "numNA"})
        self.data = pd.concat([colNames,percentNA], axis = 1).sort_values(by=['numNA'], ascending = False)

        return self.data
        
    def drop_columns(self, df, threshold_percent):
        '''drop columns by a threshold (percentage of na)'''
        global data ### double check...
        data = self.getNAs(df)
        column_names = data[data.numNA >= threshold_percent].label
        self.clean_data = df.drop(column_names, axis = 1)

        return self.clean_data
    
    def entry_to_lowercase(self, df):
        for i in df.columns:
            if (df[i].dtype == "O"):
                df[i] = df[i].str.lower()
        return df
    
    def id_data_types(self, df):
        names = pd.DataFrame()
        category = pd.DataFrame()
        data_type = pd.DataFrame()
        numUni = pd.DataFrame()

        for i in df.columns:

            names = names.append({"variable": i},ignore_index = True)
            category = category.append({"category": list(df[i].unique())}, ignore_index = True)
            numUni = numUni.append({"numUnique": len(df[i].unique())}, ignore_index = True)
            data_type = data_type.append({"data_type": df[i].dtype}, ignore_index = True)

        view_data = pd.concat([names, category, numUni,data_type],axis =1)

        return (view_data)
    
    def replace_na_with_NaN(self, df):
        for i in df.columns:
            df[i] = df[i].replace('na', np.NaN)
        return df
    
    # removes underscores and spaces from instances, examples: 'No_School-> NoSchool, no school -> noschool'
    def remove_underscores_spaces(self, df):
        for i in df.columns:
            if (df[i].dtype == "O"):
                df[i] = df[i].str.replace('_', "")
                df[i] = df[i].str.replace(' ', "")
        return df

