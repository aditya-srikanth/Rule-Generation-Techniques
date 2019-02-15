import pandas as pd
import numpy as np
import matplotlib as plt
import csv
import operator
from collections import OrderedDict

def process_dataset(path,store=False):
    with open(path) as csv_file:
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
    if store:
        ItemFrame.to_csv('sorted_processed_groceries.csv', header=None, index=False)
    return ItemFrame,unique_sets

print(len(process_dataset('groceries.csv')[1]))

class Node:
    def __init__(self,value,parent=None):
        assert isinstance(value,str)
        if parent != None:
            assert isinstance(parent,Node)
        self.value = value
        self.parent = parent
        self.count = 0
        self.temp_count = 0 # When doing the subtree selection
        self.children = {}  # KEY = string, value = pointer



class FPTree:
    def __init__(self,unique_items):
        self.root = Node('None') 
        self.unique_items = {unique_item : [] for unique_item in unique_items}
        self.unique_items_list = unique_items

    def insert(self,transaction):
        # check if the root has the corresponding child or not,
        if transaction[0] in self.root.children:
            self.insert_recurse(self.root.children[transaction[0]],transaction[1:])
        else:
        # if not, create the child and recurse
            newNode = Node(transaction[0],self.root)
            self.root.children[transaction[0]] = newNode
            self.unique_items[transaction[0]].append(newNode)
            self.insert_recurse(self.root.children[transaction[0]],transaction[1:])
        
    def insert_recurse(self,node,transaction):
        node.count += 1
        # does the depth traversal of the tree and inserts the node
        # invariant: the transaction contains the NEXT item to be traversed 
        # if the item does not exit, then return
        if len(transaction) <= 0:
            return
        if transaction[0] in node.children:
            # if the current node has that child, recurse
            self.insert_recurse(node.children[transaction[0]],transaction[1:])
        else:
            # if not then create that child and then recurse
            newNode = Node(transaction[0],node)
            node.children[transaction[0]] = newNode 
            self.unique_items[transaction[0]].append(newNode)
            self.insert_recurse(node.children[transaction[0]],transaction[1:])
    def print_nodes(self):
        # FOR NOW....
        # prints the values of the nodes within the tree
        # later version, it will print the entire tree in inorder.
        for key in self.unique_items_list:
            for node in self.unique_items[key]:
                print(node.value,node.count,node.parent)
        
        

if __name__ == "__main__":
    # dummy code
    lol = Node("1",None)
    tree = FPTree(["1","2","3","4","5"]) # No. of unique items is the parameter
    tree.insert(["1","2","3"])
    tree.insert(["1","4","5"])
    tree.insert(["2","4","5"])
    tree.insert(["2","4","1"])
    tree.print_nodes()