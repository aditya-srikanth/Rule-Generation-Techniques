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
    
    def get_frequent_itemsets_with_suffix(self,value,minsup_count):
        if value == "None":
            return None
        intermediate_itemsets = {}
        intermediate_itemsets[(value,)] = 0
        for item in self.unique_items[value]:
            key = (item.value,)
            node = item
            node.temp_count = node.count
            intermediate_itemsets[key] += node.count
            while node.parent.value != "None":
                key += (node.parent.value,)
                if key not in intermediate_itemsets.keys():
                    intermediate_itemsets[key] = node.temp_count
                    node.parent.temp_count = node.temp_count
                else:
                    # print('entered elif')
                    intermediate_itemsets[key] += node.temp_count
                    node.parent.temp_count += node.temp_count
                node = node.parent
        to_return_itemsets = {key: value for (key,value) in intermediate_itemsets.items() if value >= minsup_count}
        return to_return_itemsets
    
    def get_frequent_itemsets_with_suffix_mk2(self,prefix_tree,itemsets,minsup):
        if len(prefix_tree) == 0 or prefix_tree == None:
            return None
        if len(itemsets) == 0 or itemsets == None:
            return None
        key = list(prefix_tree.keys())[0]

        # cache = self.generate_conditional_fp_tree(prefix_tree[key])
        # candidate_itemsets = {}
        # next_tree = {}
        # changelog = {}
        # print(prefix_tree)
        # for node in prefix_tree[key]:
        #     p_node = node
        #     # print('v: ',p_node.value,p_node.temp_count,p_node.count,p_node.parent.value)
        #     while p_node.value != "None":
        #         c_key = key + ' & '+p_node.value
                
        #         if c_key in candidate_itemsets and not p_node.visited:
        #             p_node.visited = True
        #             candidate_itemsets[c_key] += p_node.temp_count
        #             if p_node.parent.value != "None":
        #                 next_tree[c_key].append(p_node.parent)
        #                 changelog[c_key].append((p_node.parent,p_node.parent.temp_count,p_node))
                
        #         elif c_key not in candidate_itemsets and not p_node.visited:
        #             p_node.visited = True
        #             candidate_itemsets[c_key] = p_node.temp_count
        #             if p_node.parent.value != "None":
        #                 changelog[c_key] = [(p_node.parent,p_node.parent.temp_count,p_node)]
        #                 next_tree[c_key] = [p_node.parent]
        
        #         p_node = p_node.parent
        
        # keys = [key for key in candidate_itemsets.keys() if candidate_itemsets[key] >= minsup]
        # next_tree = { key: next_tree[key] for key in keys if key in next_tree}
        # candidate_itemsets = { key: candidate_itemsets[key] for key in keys }
        
        
        # for key in next_tree.keys():
        #     for change in changelog[key]:
        #         (p_node.parent,temp_count,p_node) = change
        #         p_node.parent.temp_count = p_node.temp_count
        #     temp = {key:next_tree[key]}    
        #     if len(itemsets) > 0:
        #         itemsets.pop()
        #         candidates = self.get_frequent_itemsets_with_suffix_mk2(temp,itemsets,minsup)
        #         self.reset_values(cache)
        #         if candidates != None:
        #             candidate_itemsets.update(candidates)
        #     for change in changelog[key]:
        #         (p_node.parent,temp_count,p_node) = change
        #         p_node.parent.temp_count = temp_count
        
        # return candidate_itemsets

        cache = self.generate_conditional_fp_tree(prefix_tree[key])
        self.print_nodes()

        return {}

    def fp_growth(self,minsup_count):
        # algorithm begins with the lowest support value and gradually goes up
        counts = {}
        sorted_items = [x[0] for x in sorted(self.items_with_support.items(), key=operator.itemgetter(1), reverse=True)]
        for item in reversed(sorted_items):
            self.reset_nodes()
            temp_dict = self.get_frequent_itemsets_with_suffix(item,minsup_count)
            counts.update(temp_dict)
        return counts
    def fp_growth_mk_2(self,minsup):
        counts = {}
        sorted_items = [x[0] for x in sorted(self.items_with_support.items(), key=operator.itemgetter(1), reverse=False)]
        print(sorted_items)
        for item in sorted_items:
            counts[item] = self.items_with_support[item]
            itemsets = list(sorted_items)
            # for node in self.unique_items[item]:
            #     node.parent.temp_count = node.temp_count = node.count
            # _ = self.generate_conditional_fp_tree(self.unique_items[item])
            if len(itemsets) > 0:
                itemsets.pop()
                # temp_dict = self.get_frequent_itemsets_with_suffix_mk2({item:[node.parent for node in  self.unique_items[item]]},itemsets,minsup)
                temp_dict = self.get_frequent_itemsets_with_suffix_mk2({item:[node for node in  self.unique_items[item]]},itemsets,minsup)
                if temp_dict != None:
                    counts.update(temp_dict)
            self.reset_nodes()
            # print('counts: ',counts)
            
        return counts
        
        

if __name__ == "__main__":
    min_sup = int(input('enter min-support\n'))
    # data,unique_items = process_dataset('groceries.csv',min_sup)
    # print(unique_items,type(data))
    # data = pd.Series.tolist(data)
    # pprint(data)
    unique_items = {}
    data = [['2','3','1'],['2','3','1'],['2','3','1'],['2','1','5'],['2','3','4'],['3','4','5'],['2','4','6'],['2','4','5']]
    unique_items['1'] = 4
    unique_items['2'] = 7
    unique_items['3'] = 5
    unique_items['4'] = 4
    unique_items['5'] = 3
    unique_items['6'] = 1
    tree = FPTree(unique_items)
    for row in data:
        tree.insert([x for x in row if x is not None])
    # tree.print_nodes()
    res = tree.fp_growth_mk_2(min_sup)
    # tree.print_supports()
    # for key in sorted(res.keys()):
    #     print(key,'\t value: ',res[key])
    # print(len(res))