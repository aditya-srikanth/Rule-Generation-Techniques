import pandas as pd
import numpy as np
import matplotlib as plt
import csv
import operator

with open('groceries.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)

unique_items=[]
for row in rows:
    unique_items.extend(row)
    
df=pd.Series(unique_items)
counts=df.value_counts()
unique_sets=counts.to_dict()    

sorted_items = sorted(unique_sets.items(), key=operator.itemgetter(1), reverse=True)
 
itemsets=[]
    
for row in rows:
    l=[]
    for value in row:
        l.append(unique_sets[value])
    d = dict(zip(row, l))
    sorted_items = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    itemsets.append(sorted_items)
    
    

"""I have unique items in the form of a dictionary
"""

class Tree:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None
        


root = Tree()
root.data = "root"
root.left = Tree()
root.left.data = "left"
root.right = Tree()
root.right.data = "right"
