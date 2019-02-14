import pandas as pd
import numpy as np
import matplotlib as plt
import csv
import operator
from collections import OrderedDict

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
row=rows[3]   
for row in rows:
    l=[]
    for value in row:
        l.append(unique_sets[value])
    d = dict(zip(row, l))
    sorted_items = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    itemsets.append(list((x[0] for x in sorted_items)))
    
ItemFrame=pd.DataFrame(itemsets)

   
    
    
 """   
    
class Node:
    def __init__(self, dataval=None):
        self.dataval = dataval
        self.nextval = None
        
class SLinkedList:
    def __init__(self):
        self.headval = None

    def listprint(self):
        printval = self.headval
        while printval is not None:
            print (printval.dataval)
            printval = printval.nextval

list = SLinkedList()
list.headval = Node([0])
e2 = Node("Tue")
e3 = Node("Wed")

row=itemsets[0]
len(row["ready soups"])
# Link first Node to second node
list.headval.nextval = e2

# Link second Node to third node
e2.nextval = e3

list.listprint()





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
"""