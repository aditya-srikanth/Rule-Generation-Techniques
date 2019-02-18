import pandas as pd
import numpy as np
import matplotlib as plt
import csv
import operator
from collections import OrderedDict

def process_dataset(path,min_sup,store=False):
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
        itemsets.append(list((x[0] for x in sorted_items if x[1]>min_sup)))
    
    for k, v in list(unique_sets.items()):
        if v < min_sup:
            del unique_sets[k]
    if 'detergent' in itemsets:
        print('True')
    if 'chewing gum' in itemsets:
        print('cg hai')   

    ItemFrame=pd.DataFrame(itemsets)
    if store:
        ItemFrame.to_csv('sorted_processed_groceries.csv', header=None, index=False)
    return ItemFrame,unique_sets


class Node:
    def __init__(self,value,parent=None):
        assert isinstance(value,str)
        if parent != None:
            assert isinstance(parent,Node)
        self.value = value
        self.parent = parent
        self.next_node = None
        self.visited = False
        self.count = 0
        self.temp_count = 0 # When doing the subtree selection
        self.children = {}  # KEY = string, value = pointer



class FPTree:
    def __init__(self,unique_items):
        self.root = Node('None') 
        self.unique_items = {unique_item : [] for unique_item in unique_items.keys()}
        self.itemset_counts = {unique_item : 0 for unique_item in unique_items.keys()}
        self.unique_items_list = unique_items.keys()
        self.items_with_support = unique_items

    def insert(self,transaction):
        # check if the root has the corresponding child or not
        if len(transaction) <= 0:
            return []
        if transaction[0] in self.root.children:
            self.insert_recurse(self.root.children[transaction[0]],transaction[1:])
        else:
        # if not, create the child and recurse
            newNode = Node(transaction[0],self.root)
            self.root.children[transaction[0]] = newNode
            previous_occurrences = self.unique_items[transaction[0]]
            if len(previous_occurrences) > 0:
                previous_occurrences[-1].next_node = newNode
            self.unique_items[transaction[0]].append(newNode)
            self.insert_recurse(self.root.children[transaction[0]],transaction[1:])       
    def insert_recurse(self,node,transaction):
        node.count += 1
        self.itemset_counts[node.value] += 1
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
            previous_occurrences = self.unique_items[transaction[0]]
            # print('lite ',previous_occurrences)
            if len(previous_occurrences) > 0:
                previous_occurrences[-1].next_node = newNode
            self.unique_items[transaction[0]].append(newNode)
            self.insert_recurse(node.children[transaction[0]],transaction[1:])
    def print_nodes(self):
        # FOR NOW....
        # prints the values of the nodes within the tree
        # later version, it will print the entire tree in inorder.
        for key in self.unique_items_list:
            for node in self.unique_items[key]:
                print(node.value,node.count,node.parent,node.next_node)
    def print_supports(self):
        print(self.itemset_counts)
    def get_frequent_itemsets_with_suffix(self,value,minsup_count):
        if value == "None":
            return []
        visited_sets = []                                           # contains the frequent itemsets
        intermediate_itemsets = {}                                  # contains the intermediate itemsets i.e 
                                                                    # the current frequent itemsets that will be checked with other itemsets
        intermediate_counts = {}
        intermediate_itemsets[value] = []
        intermediate_counts[value] = 0
        # add the base item's locations in the list
        for item in self.unique_items[value]:
            intermediate_itemsets[value].append(item)
            intermediate_counts[value] += item.count
        while len(intermediate_itemsets) > 0:
            keys = list(intermediate_itemsets.keys())
            for key in keys:
                for node in intermediate_itemsets[key]:
                    if (node.parent.value != "None") and key + ' & '+node.parent.value not in intermediate_itemsets:
                        intermediate_counts[key + ' & '+node.parent.value] = node.count
                        intermediate_itemsets[key + ' & '+node.parent.value] = [node.parent]
                    elif (node.parent.value != "None") and key + ' & '+node.parent.value in intermediate_itemsets:
                        # print('entered elif')
                        intermediate_itemsets[key + ' & '+node.parent.value].append(node.parent)
                        # print(intermediate_counts[key + ' & '+node.parent.value],node.count)
                        intermediate_counts[key + ' & '+node.parent.value] += node.count
                        # print(intermediate_counts[key + ' & '+node.parent.value])

                intermediate_itemsets.pop(key,None)
                visited_sets.append(key)
            # print('intermediate counts: ',intermediate_counts)
            temp = {temp_key : count for (temp_key,count) in intermediate_counts.items() if intermediate_counts[temp_key] >= minsup_count}
            intermediate_counts = temp
            intermediate_itemsets = {temp_key : intermediate_itemsets[temp_key] for temp_key in intermediate_counts.keys() if temp_key in intermediate_itemsets}
            # print('temp: ',temp)
            # break
        return visited_sets,intermediate_counts
    def fp_growth(self,minsup_count):
        # algorithm begins with the lowest support value and gradually goes up
        frequent_itemsets = []
        counts = {}
        sorted_items = [x[0] for x in sorted(self.items_with_support.items(), key=operator.itemgetter(1), reverse=True)]
        for item in reversed(sorted_items):
            temp_list,temp_dict = self.get_frequent_itemsets_with_suffix(item,minsup_count)
            frequent_itemsets += temp_list
            # print(frequent_itemsets)
            counts.update(temp_dict)
        return frequent_itemsets,counts
        
        

if __name__ == "__main__":
    min_sup = int(input('enter min-support\n'))
    data,unique_items = process_dataset('groceries.csv',min_sup)
    # print(unique_items,type(data))
    # unique_items = {}
    # data = [['2','3','1'],['2','1','5'],['2','3','4'],['3','4','5']]
    # unique_items['1'] = 2
    # unique_items['2'] = 3
    # unique_items['3'] = 3
    # unique_items['4'] = 2
    # unique_items['5'] = 2
    tree = FPTree(unique_items)
    data = pd.Series.tolist(data)
    # print(data)
    for row in data:
        tree.insert([x for x in row if x is not None])
    # tree.print_supports()
    # tree.print_nodes()
    res = tree.fp_growth(min_sup)[1]
    print(len(res))
    for key in res.keys():
        print(key,'\t',res[key])