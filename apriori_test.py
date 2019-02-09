import os
import pandas as pd
import numpy as np
from pprint import pprint

groceries_data = pd.read_csv('test_data.csv', sep='delimiter', header=None, engine='python')

'''groceries_list = []

for g_list in temp_list:
    groceries_list.append(g_list.split(','))

transactions = len(groceries_list)

single_itemset = {}

single_itemset_keys = single_itemset.keys()

for g_list in groceries_list:
    for grocery in g_list:
        if grocery in single_itemset_keys:
            single_itemset[grocery] = single_itemset[grocery] + 1
        else:
            single_itemset[grocery] = 1

min_support_vals = [0.1, 0.2, 0.3, 0.4]

min_support = min_support_vals[1] * max(single_itemset.values())

freq_single_set = {}

for single_key in single_itemset.keys():
    if single_itemset[single_key] >= min_support:
        freq_single_set[single_key] = single_itemset[single_key]

print(min_support)
#pprint(freq_single_set)

double_itemset = {}

for item in freq_single_set:
    for sec_item in freq_single_set:
        if item != sec_item:
            double_tuple = tuple(set([item]).union(set([sec_item])))
            if double_tuple not in tuple(double_itemset.keys()):
                double_itemset[double_tuple] = 0

for g_list in groceries_list:
    for double_key in double_itemset.keys():
        if set(g_list).intersection(set(double_key)) == set(double_key):
            double_itemset[double_key] = double_itemset[double_key] + 1

freq_double_set = {}

for double_key in double_itemset.keys():
    if double_itemset[double_key] >= min_support:
        freq_double_set[double_key] = double_itemset[double_key]'''

item = ('bread', 'beer')
sec_item = ('beer', 'diapers')
new_tuple = tuple(set(list(item)).union(set(list(sec_item))))
print(new_tuple)
