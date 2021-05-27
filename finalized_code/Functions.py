#!/usr/bin/env python
# coding: utf-8

#To use in notebooks
#from finalized_code.Functions import Cleaning_Functions
#cl = Cleaning_Functions()


# Ana's functions

import numpy as np
import pandas as pd 

class Cleaning_Functions:
    """
     Conatins all cleaning function for this data
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
        
        """
         Input: Full dataset
         Output: Full dataset where object strings have underscores and spaces removed
         EX:'No_School-> NoSchool, no school -> noschool'
        """
        
        for i in df.columns:
            df[i] = df[i].replace(np.nan, 'na')
        return df
    
    # removes underscores and spaces from instances, 
    def remove_underscores_spaces(self, df):
        
        """
         Input: Full dataset
         Output: Full dataset where object strings have underscores and spaces removed
         EX:'No_School-> NoSchool, no school -> noschool'
        """
        
        for i in df.columns:
            if (df[i].dtype == "O"):
                df[i] = df[i].str.replace('_', "")
                df[i] = df[i].str.replace(' ', "")
        return df
    
    
    
    def convert_to_categorical(self, df, variables):
        """
         Input: dataframe, column names of variables to be transformed
         Output: dataframe with dtypes of indicated variables changed
         
         #NOTE: USE this function AFTER preprocessing functions above
        """
    
    # convert these to categories
    #df[v1] = df[v1].astype(‘category’)
    
        for i in variables:
            df[i] = df[i].astype('category')
        return df
    
    
    def impute_data(self, Xtrain, Xtest):
        """
        Input: XTraining set, XTesting Set
        Output: The inputs with NA numerical variabes imputed by column median, and categorical
        NA varaibles converted into a seperate category "Na" 
        """
        
       
   
        num_train = Xtrain.select_dtypes(include=['float64', 'int64'])
        num_test = Xtest.select_dtypes(include=['float64', 'int64'])
        
        cat_train = Xtrain.select_dtypes(include=['object', 'category'])
        cat_test = Xtest.select_dtypes(include=['object', 'category'])
      

    # imputes NA numerics with median
        for i in num_train.columns:
            Xtrain[i] = num_train.fillna(np.nanmedian(Xtrain[i]))
        
        for i in num_test.columns:
            Xtest[i] = num_test.fillna(np.nanmedian(num_test[i]))
        
    # categorical NA to "Na" level
        for i in cat_train.columns:
            Xtrain[i] = cat_train.replace(np.nan, "Na")
        
        for i in cat_test.columns:
            Xtest[i] = cat_test.replace(np.nan, "Na")

   
        return Xtrain, Xtest

    def drop_response_rows_with_NAs(self,df,y_variable):
        """
        Input: dataframe, response variable column 
        Output: dataframe rows with missing response varaibles
        are dropped entirely (we cannot use these to train or test)
        But these dropped rows are saved to be used later
        
        """
    
    ## need to delete PPI_threshold since that is like our y2 which we won’t use
        df = df.drop("PPI_Threshold", axis=1)
        condition = df[y_variable]
        rows_to_delete = df[np.isnan(condition)].index
    
    #save all rows with y=NA. Will use this data to predict the y later.
        prediction_dataset = df.iloc[rows_to_delete,:]
    
    #create new data
        new_data = df.drop(labels=rows_to_delete, axis=0)
    
        return new_data, prediction_dataset

