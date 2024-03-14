# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 20:28:46 2024

@author: Marcel Tino
"""

import pandas as pd
from string import punctuation
import warnings
warnings.filterwarnings("ignore")
from pkg_resources import resource_filename
filepath = resource_filename('retail_dictionary', 'rd.xlsx')
#Read the csv file

data=pd.read_excel(filepath)

def get_meaning(text):
    text=text.lower()
    print(text)
    variable_list=[]
    type_list=[]
    
    variable_list=data["Entity Name"].tolist()
    #convert each item to lowercase
    for i in range(len(variable_list)):
        variable_list[i] =variable_list[i].lower()
        
    type_list=data["type"].tolist()
    for i in range(len(type_list)):
        type_list[i] = type_list[i].lower()
        
    index_pos=variable_list.index(text)
    meaning=type_list[index_pos]
    return meaning
