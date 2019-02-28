import pandas as pd
import numpy as np
import matplotlib as plt
import csv
import operator
from collections import OrderedDict
from pprint import pprint
from itertools import combinations, chain

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
        self.count = 0      # default value
        self.temp_count = 0 # When doing the subtree selection
        self.children = {}  # KEY = item (string), value = reference

class FPTree:
    def __init__(self,unique_items):
        self.root = Node('Null') 
        self.unique_items = {unique_item : [] for unique_item in unique_items.keys()}           # maps item to nodes in tree
        self.itemset_counts = {unique_item : 0 for unique_item in unique_items.keys()}          # maps counts of each item
        self.unique_items_list = unique_items.keys()                                            # list of item values, used in the algorithm
        self.items_with_support = unique_items                                                  
    def insert(self,transaction):
        if len(transaction) > 0:
            # check if the root has the corresponding child or not
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
<<<<<<< HEAD
    def generate_conditional_fp_tree(self,prefix_paths, item_name):
=======

    def generate_conditional_fp_tree(self,prefix_paths):
>>>>>>> 67fe7408161baa44f9287f7426a69338862bb6f8
        cache = {}
        for node in self.unique_items[item_name]:
            temp_node = node
            cache[temp_node] = temp_node.temp_count
<<<<<<< HEAD
            temp_node.temp_count = temp_node.count
            
            while temp_node.value != 'Null':
=======
            while temp_node.value != "None":
>>>>>>> 67fe7408161baa44f9287f7426a69338862bb6f8
                temp_node.parent.temp_count = 0
                temp_node = temp_node.parent
                temp_node.visited = False
        for node in self.unique_items[item_name]:
            temp_node = node
<<<<<<< HEAD
            while temp_node.value != 'Null':
                temp_node.parent.temp_count += temp_node.temp_count 
                if temp_node.count > 5000:
                    print('eureka', temp_node.value, temp_node.count)
                temp_node = temp_node.parent
        return cache
    def reset_values(self,cache):
        for key in cache.keys():
            key.temp_count = cache[key]
    def get_frequent_itemsets_with_suffix(self,prefix_tree,itemsets, item_name,minsup):
=======
            while temp_node.value != "None":
                temp_node.parent.temp_count += temp_node.temp_count
                temp_node = temp_node.parent
        return cache

    def reset_values(self,cache):
        for key in cache.keys():
            key.temp_count = cache[key]

    def get_frequent_itemsets_with_suffix_mk2(self,prefix_tree,itemsets,minsup):
>>>>>>> 67fe7408161baa44f9287f7426a69338862bb6f8
        if len(prefix_tree) == 0 or prefix_tree == None:
            return None
        if len(itemsets) == 0 or itemsets == None:
            return None
        key = list(prefix_tree.keys())[0]
<<<<<<< HEAD
        cache = self.generate_conditional_fp_tree(prefix_tree[key], item_name)
        candidate_itemsets = {}
        next_tree = {}
        child_nodes = prefix_tree[key]
        # parents = [node.parent for node in child_nodes]
        for node in child_nodes:
            temp_node = node.parent
            while temp_node.value != 'Null':
                if not temp_node.visited and temp_node.value != 'Null':
=======
        # cache = self.generate_conditional_fp_tree(prefix_tree[key])
        candidate_itemsets = {}
        next_tree = {}

        cache = self.generate_conditional_fp_tree(prefix_tree[key])
        child_nodes = prefix_tree[key]
        parents = [node.parent for node in child_nodes]
        for node in parents:
            temp_node = node
            while temp_node.value != "None":
                if not temp_node.visited:
>>>>>>> 67fe7408161baa44f9287f7426a69338862bb6f8
                    c_key = key + '&' + temp_node.value
                    if c_key not in candidate_itemsets:
                        candidate_itemsets[c_key] = node.count
                        next_tree[c_key] = [temp_node]
                    else:
                        candidate_itemsets[c_key] += node.count
                        next_tree[c_key].append(temp_node)
                        if candidate_itemsets[c_key] > 5000:
                            print(item_name,temp_node.value, temp_node.temp_count, temp_node.parent.value, temp_node.parent.temp_count, type(temp_node.value), type(temp_node.parent.value))
                    temp_node.visited = True
                temp_node = temp_node.parent

        # prune candidates
        # print('candidates:  ',candidate_itemsets)
        next_tree_keys = [key for key in candidate_itemsets.keys() if candidate_itemsets[key] >= minsup]
        candidate_itemsets = { key : candidate_itemsets[key] for key in next_tree_keys}
        next_tree = { key: next_tree[key] for key in next_tree_keys if key in next_tree}

        for next_tree_key in next_tree_keys:
            temp = self.get_frequent_itemsets_with_suffix({next_tree_key:next_tree[next_tree_key]},itemsets[1:],item_name, minsup)
            candidate_itemsets.update(temp)
            self.reset_values(cache)
        self.reset_values(cache)
        return candidate_itemsets
    def fp_growth(self,minsup):
        counts = {}
<<<<<<< HEAD
        sorted_items = [x[0] for x in sorted(self.itemset_counts.items(), key=operator.itemgetter(1), reverse=False) if x[0] != '']
        #print(sorted_items)
=======
        sorted_items = [x[0] for x in sorted(self.items_with_support.items(), key=operator.itemgetter(1), reverse=False)]
        # print(sorted_items)
>>>>>>> 67fe7408161baa44f9287f7426a69338862bb6f8
        for item in sorted_items:
            threshold = self.items_with_support[item]
            if threshold < minsup:
                print('skipped ',item)
                continue

            counts[item] = threshold
            itemsets = list(sorted_items)
            #print('item: ',item)
            # for node in self.unique_items[item]:
            #     node.parent.temp_count = node.temp_count = node.count
            # _ = self.generate_conditional_fp_tree(self.unique_items[item])
            if len(itemsets) > 0:
<<<<<<< HEAD
                temp_dict = self.get_frequent_itemsets_with_suffix({item:[node for node in  self.unique_items[item]]},itemsets,item,minsup)
=======
                temp_dict = self.get_frequent_itemsets_with_suffix_mk2({item:[node for node in  self.unique_items[item]]},itemsets,minsup)
                itemsets.pop()
>>>>>>> 67fe7408161baa44f9287f7426a69338862bb6f8
                if temp_dict != None:
                    counts.update(temp_dict)
                itemsets.pop()
            self.reset_nodes()
        data = {}
        for key in counts.keys():
            temp = tuple(str(key).split('&'))
            data[temp] = counts[key]
<<<<<<< HEAD
=======

>>>>>>> 67fe7408161baa44f9287f7426a69338862bb6f8
        return data



if __name__ == "__main__":
<<<<<<< HEAD
    min_sup = int(input('enter min-support\n'))
    data,unique_items = process_dataset('test_data.csv',min_sup,store=True)
    # data,unique_items = process_dataset('groceries.csv',min_sup,store=True)
    #print(unique_items,type(data))
=======
    # min_sup = int(input('enter min-support\n'))
    min_sup = 300
    data,unique_items = process_dataset('groceries.csv',min_sup,store=True)
    # print(unique_items,type(data))
    # data = pd.Series.tolist(data[:30])
>>>>>>> 67fe7408161baa44f9287f7426a69338862bb6f8
    data = pd.Series.tolist(data)
    # print(data)
    # pprint(data)
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
        # print('key: ',[x for x in row if x is not None])
        tree.insert([x for x in row if x is not None])
<<<<<<< HEAD
    #tree.print_nodes()
    res = tree.fp_growth(min_sup)
    tree.print_supports()
=======
    # tree.print_nodes()
    # tree.print_nodes()
    res = tree.fp_growth_mk_2(min_sup)
>>>>>>> 67fe7408161baa44f9287f7426a69338862bb6f8
    for key in sorted(res.keys()):
        print(key,'value: ',res[key],sep='    ')
    print(len(res))
<<<<<<< HEAD
    
import re
import ast
rows=rows[1:]
ast.literal_eval(strTup)
new_rows=[row[0] for row in rows]  
yo=list(ast.literal_eval(new_rows[100]))
lol=[]

for row in new_rows[59:]:
    lol.append(list(ast.literal_eval(row)))
for row in new_rows[:59]:
    lol.append([row])
rows=[list(ast.literal_eval(new_rows[i])) for i in range(len(new_rows))
lol.append(list(ast.literal_eval(new_rows[10])))


    

def Support(Frequent_Itemsets, itemset):
    itemset_count=0
    Frequent_Itemsets=lol
    for Item_row in Frequent_Itemsets:
        for val in Item_row:
            result =  all(elem in val  for elem in itemset)
#            print(result, itemset)
            if result:
                itemset_count+=1
#    print(itemset_count)
    return itemset_count

def Conf(itemset1, itemset2):
    Frequent_Itemsets=lol
    if Support(lol, itemset1)!=0:
        conf=Support(lol, itemset2+itemset1)/Support(lol, itemset1)
        return conf
    return 0
#minconf=0
Rules=[]
def Rule_Generation(Frequent_Itemsets, minsup, minconf):
#    Frequent_Itemsets=lol
    for val in Frequent_Itemsets:
       for i in range(1,len(val)):
            subsets = [v for v in combinations(val, i)]
            for subset in subsets:
                itemset1=list(subset)
                itemset2=[item for item in list(val) if not item in itemset1]
                if Conf(itemset1, itemset2)>minconf:
                    print(itemset1,"----->", itemset2)
                        
=======
>>>>>>> e0c186360821c1bd48c6e49cc07dda68f20752da
