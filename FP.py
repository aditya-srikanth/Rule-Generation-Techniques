import pandas as pd
import numpy as np
import matplotlib as plt
import csv
import operator
from collections import OrderedDict
from pprint import pprint

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
        itemsets.append(list((x[0] for x in sorted_items if x[1]>=min_sup)))
    
    for k, v in list(unique_sets.items()):
        if v < min_sup:
            del unique_sets[k]
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
        for key in self.unique_items_list:
            for node in self.unique_items[key]:
                print('value: ',node.value,'count: ',node.count,'temp_count: ',node.temp_count,'\nchildren')
                for child in node.children.keys():
                    print(child,'count: ',node.children[child].count)
                print()
    def print_supports(self):
        print(self.itemset_counts)
    def reset_nodes(self):
        for key in self.unique_items_list:
            for node in self.unique_items[key]:
                node.temp_count = 0
    
    def generate_conditional_fp_tree(self,prefix_paths):
        cache = {}
        for node in prefix_paths:
            temp_node = node
            while temp_node.value != "None":
                cache[temp_node] = temp_node.temp_count
                temp_node.parent.temp_count = 0
                temp_node = temp_node.parent
                temp_node.visited = False
        for node in prefix_paths:
            temp_node = node
            while temp_node.value != "None":
                temp_node.parent.temp_count += temp_node.temp_count 
                temp_node = temp_node.parent
        return cache
    
    def reset_values(self,cache):
        for key in cache.keys():
            key.temp_count = cache[key]
        
    def get_frequent_itemsets_with_suffix_mk2(self,prefix_tree,itemsets,minsup):
        if len(prefix_tree) == 0 or prefix_tree == None:
            return None
        if len(itemsets) == 0 or itemsets == None:
            return None
        key = list(prefix_tree.keys())[0]

        cache = self.generate_conditional_fp_tree(prefix_tree[key])
        candidate_itemsets = {}
        next_tree = {}

        cache = self.generate_conditional_fp_tree(prefix_tree[key])
        parents = prefix_tree[key]
        parents = [node.parent for node in parents]
        for node in parents:
            temp_node = node
            while temp_node.value != "None":
                if not temp_node.visited:
                    c_key = key + '&' + temp_node.value
                    if c_key not in candidate_itemsets:
                        candidate_itemsets[c_key] = temp_node.temp_count
                        next_tree[c_key] = [temp_node]
                    else:
                        candidate_itemsets[c_key] += temp_node.temp_count
                        next_tree[c_key].append(temp_node)
                    temp_node.visited = True
                temp_node = temp_node.parent
        
        # prune candidates
        next_tree_keys = [key for key in candidate_itemsets.keys() if candidate_itemsets[key] >= minsup]
        candidate_itemsets = { key : candidate_itemsets[key] for key in next_tree_keys}
        next_tree = { key: next_tree[key] for key in next_tree_keys if key in next_tree}
        
        for next_tree_key in next_tree_keys:
            temp = self.get_frequent_itemsets_with_suffix_mk2({next_tree_key:next_tree[next_tree_key]},itemsets[1:],minsup)
            candidate_itemsets.update(temp)
            self.reset_values(cache)
        self.reset_values(cache)
        return candidate_itemsets

    def fp_growth_mk_2(self,minsup):
        counts = {}
        sorted_items = [x[0] for x in sorted(self.items_with_support.items(), key=operator.itemgetter(1), reverse=False)]
        print(sorted_items)
        for item in sorted_items:
            threshold = self.items_with_support[item]
            if threshold < minsup:
                continue
            counts[item] = threshold 
            itemsets = list(sorted_items)
            for node in self.unique_items[item]:
                node.parent.temp_count = node.temp_count = node.count
            _ = self.generate_conditional_fp_tree(self.unique_items[item])
            if len(itemsets) > 0:
                itemsets.pop()
                temp_dict = self.get_frequent_itemsets_with_suffix_mk2({item:[node for node in  self.unique_items[item]]},itemsets,minsup)
                if temp_dict != None:
                    counts.update(temp_dict)
            self.reset_nodes()
        return counts
        
        

if __name__ == "__main__":
    min_sup = int(input('enter min-support\n'))
    data,unique_items = process_dataset('test_data.csv',min_sup)
    # print(unique_items,type(data))
    data = pd.Series.tolist(data)
    pprint(data)
    # unique_items = {}
    # data = [['2','3','1'],['2','3','1'],['2','3','1'],['2','1','5'],['2','3','4'],['3','4','5'],['2','4','6'],['2','4','5']]
    # unique_items['1'] = 4
    # unique_items['2'] = 7
    # unique_items['3'] = 5
    # unique_items['4'] = 4
    # unique_items['5'] = 3
    # unique_items['6'] = 1
    tree = FPTree(unique_items)
    for row in data:
        tree.insert([x for x in row if x is not None])
    # tree.print_nodes()
    res = tree.fp_growth_mk_2(min_sup)
    tree.print_supports()
    for key in sorted(res.keys()):
        print(key,'\t\t\t\t value: ',res[key])
    # print(len(res))