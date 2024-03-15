# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 23:33:14 2024

@author: MOHAMMED
"""
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

class read_data():
    """
    constrctour called with intilization to ask the user about the path of 
    file than determin the file foramt and read the file in dataframe
    """
    def __init__(self):
        try:
            file_name = input("please enter file path")
            if file_name.split(".")[1] == "json":
                self.file = pd.read_json(file_name)
                self.type = "json"
            elif file_name.split(".")[1] == "csv":
                self.file = pd.read_csv(file_name)
                self.type = "csv"
            elif file_name.split(".")[1] == "excel":
                self.file = pd.read_excel(file_name)
                self.type = "excel"
            else:
                print("sorry "+file_name.split(".")[1]+" file not supported")
           
        except:
            print("sorry try again with valid file name format json,excel or csv")
        
            
    def summary(self):
        """
        function that return some info about the dataset shape,columns dtypes
        some statistics
        """
        print("rows: {} columns: {} ".format(str(self.file.shape[0]),str(self.file.shape[1])))
        print("=========================================================")
        print(self.file.info())
        print(self.file.describe())
        print("Most Frequent values\n",self.file.mode().iloc[0])
        
    ##=====================================================
    
    def show(self,num_to_show=5):
        """function that return back the dataframe depending on how many
        columns the user want
        
        Parameter :int num_to_show how many rows you want
        
        return : dataframe
        """
        return self.file.head(num_to_show)
  
    ##==========================================
    def col_names(self):
        """
        function print the columns names for the user 
        
        """
        print("index name")
        for index,name in enumerate(self.file.columns):
            print(" ",index," "+name)
    ##==========================================

    def unique_values(self):
        """
        function print the unique values in each column 
        column name value pair 

        Returns
        -------
        None.

        """
        columns = self.file.columns
        for col in columns:
            print("ColumnName ----------------UniqueValues")
            print(col,"-->",self.file[col].unique())
            print("=========================================")
            
    ##==========================================

    def null_sum(self):
        """
        function show you the sum of null values in each column
        

        Returns
        -------
        None.

        """
        print("ColumnName-------------HowManyNulls")
        print(self.file.isnull().sum())
        
    ##==========================================

    def show_row_wnull(self,column_name):
        """
        this function return back the rows in which this passed column 
        has null value 

        Parameters
        ----------
        column_name :string the column contain the null value

        Returns
        -------
        dataframe of x of rows depending on how many nulls in the 
        column

        """
        return self.file.query('`{0}`.isnull()'.format(column_name))
    ##==========================================

    def drop_col_wnan(self,column_name):
        """
        drops the column passed if it contain nulls

        Parameters
        ----------
        column_name :string column with null

        Returns
        -------
        None.

        """
        try:    
            self.file.dropna(subset=[column_name],inplace=True)
        except KeyError :
            print("please enter vaild column name ")
            
    ##==========================================
    #drop colum without nan
    def drop_col_wname(self,*args):
        """
        drop columns by names passed

        Parameters
        ----------
        *args :string series of vaalues of columns names

        Returns
        -------
        None.

        """
        self.file.drop(list(args),axis=1,inplace=True)
        
    ##=====================================
        
    def fill_col_wmean(self,column_name):
        """
        fill missing values in passed colum by mean of columns values 

        Parameters
        ----------
        column_name string column with null values

        Returns
        -------
        None.

        """
        mean_A = self.file[column_name].mean()
        self.file[column_name] = self.file[column_name].fillna(mean_A)
        
    ##==========================================

    def fill_col_wmode(self,column_name):
        """
        fill missing values in passed column by mode of columns values 

        Parameters
        ----------
        column_name :string  column with null values

        Returns
        -------
        None.

        """
        mean_A = self.file[column_name].mode()[0]
        self.file[column_name] = self.file[column_name].fillna(mean_A)
        
    ##==========================================
    def dis_duplic_row(self):
        """
        show the dublicates rows depending on all columns in 
        the data note:it retrn the seconed duplicat ask you also 
        if you want to drop duplicats

        Returns
        -------
        None.

        """
        print(self.file.loc[self.file.duplicated()])
        if self.file.duplicated().sum():    
            answer = input("Do you want to drop duplicts? y/n")
            if answer=="y":
                self.file = self.file.drop_duplicates()
    ##==========================================
    def dublic_basedOn_col(self,*args):
        """
        show duplicate rows depending on selectd columns by user 

        Parameters
        ----------
        *args :string columns names given by the user 

        Returns
        -------
        None.

        """
        print(self.file.loc[self.file.duplicated(args)])
        if self.file.duplicated(args).sum():    
            answer = input("Do you want to drop duplicts? y/n")
            if answer=="y":
                self.file = self.file.drop_duplicates(args)
    ##==========================================
    def catg_ecoding_col(self,*args):
        """
        genrate enocding columns for the user input columns 

        Parameters
        ----------
        *args :string user input columna names

        Returns
        -------
        None.

        """
        self.file = pd.get_dummies(self.file,columns=list(args))
        print(self.file.head())
        
    ##==========================================
    def fill_missing_numbers(self,user_prf="m"):
        """
        this function handel missing values in numeric columns the 
        default is filling with mean or you can chose ch to chose differ
        method of filling for each column

        Parameters
        ----------
        user_prf : string, optional
            user prefered method to fill the values. The default is "m".

        Returns
        -------
        None.

        """
        columns_with_null = self.file.select_dtypes(include=['number']).columns[self.file.select_dtypes(include=['number']).isnull().any()].tolist()
        if len(columns_with_null)>0:  
            print("this columns",columns_with_null,"contain nulls")
            if user_prf == "m":
                for col in columns_with_null:
                    mean_A = self.file[col].mean()
                    self.file[col] = self.file[col].fillna(mean_A)
                print("by defult filled with mean")
            elif user_prf =="ch":
                for col in columns_with_null:
                    fill_way = input("how you would like to fill {0} with  median , mode , mean or a number ".format(col))
                    if fill_way == "median":
                        median_A = self.file[col].median()
                        self.file[col] = self.file[col].fillna(median_A)
                    elif fill_way== "mean":
                        mean_A = self.file[col].mean()
                        self.file[col] = self.file[col].fillna(mean_A)
                    elif fill_way == "mode":
                        mean_A = self.file[col].mode()[0]
                        self.file[col] = self.file[col].fillna(mean_A)
                    elif fill_way == "number":
                        self.file[col] = self.file[col].fillna(int(fill_way))
        else:
            print("no missing values in numeric coulmns")
    ##==========================================
    def fill_missing_catg(self,user_prf="m"):
        """
        this function handel missing values in categorical columns the 
        default is filling with mode or you can chose n to chose differ
        method of filling for each column

        Parameters
        ----------
        user_prf : string, optional
            user prefered method to fill the values. The default is "m".

        Returns
        -------
        None.

        """
        columns_with_null = self.file.select_dtypes(include=['object']).columns[self.file.select_dtypes(include=['object']).isnull().any()].tolist()
        if len(columns_with_null)>0: 
            for col in columns_with_null:
                if self.file.nunique()[col]>10:
                    columns_with_null.remove(col)
            print("this columns",columns_with_null,"contain nulls")
            if user_prf=="m":
                for col in columns_with_null:
                    mean_A = self.file[col].mode()[0]
                    self.file[col] = self.file[col].fillna(mean_A)
                print("by default you fill them with mode")
            elif user_prf=="n":
                for col in columns_with_null:
                    fill_way = input("how you would like to fill {0} with \n backfill(bf) , forwardfill(ff) , constant(c) , interpolation(ip) or don't touch (not) ".format(col))
                    if fill_way == "bf":
                        self.file[col].fillna(method="bfill",inplace=True)
                        if self.file.isnull().sum()[col]>0:
                            print("this way dosen't match the null position please use another for this col",col)
                    elif fill_way == "ff":
                        self.file[col].fillna(method="ffill",inplace=True)
                    elif fill_way == "c":
                        const = input("please enter constant")
                        self.file.fillna(const,inplace=True)
                    elif fill_way == "ip":
                        self.fillna(method="linear",inplace=True)
                    elif fill_way == "not":
                        continue
                    else:
                        print("this option is not supported please try again using bf,ff,c,ip")
            else:
                print("this option is not supported try again using m,n")
        else:
            print("No missing values in categorical columns")
    
    ##==========================================
    def rename_col(self,old_name,new_name):
        """
        change the name of column by getting the old_name and the new_name

        Parameters
        ----------
        old_name : string
            old column name 
        new_name : string
            new column name 

        Returns
        -------
        None.

        """
        self.file=self.file.rename(columns={old_name:new_name})
    ##==========================================
    def fill_col_wmedian(self,column_name):
        """
        fill missing values in passed colum by median of columns values 

        Parameters
        ----------
        column_name : string column with null values

        Returns
        -------
        None.

        """
        median_A = self.file[column_name].median()
        self.file[column_name] = self.file[column_name].fillna(median_A)
    def drop_by_index(self,*indcies):
        """
         drop rows by index 

        Parameters
        ----------
        *indcies : int
            series of indcies want to drop .

        Returns
        -------
        None.

        """
        self.file=self.file.drop(indcies)
    def drop_bcol_value(self,column_name,value):
        """
        alter the dataframe to return just the filtered data based on value 
        condition 

        Parameters
        ----------
        column_name : string
            the column you want to filter based on it.
        value : int,string,float depedns on the column
            the value you want to filter based on it .

        Returns
        -------
        None.

        """
        self.file = self.file[self.file[column_name]!=value]
    def plot_two_col(self,col1,col2):
        plt.plot(self.file[col1],color="red",label=col1)
        plt.plot(self.file[col2],label=col2)
        plt.legend()
        plt.show()
    def get_dataframe(self):
        return self.file