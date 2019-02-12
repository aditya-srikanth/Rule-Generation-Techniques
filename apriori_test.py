import os
import pandas as pd
from pprint import pprint
import pickle
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
import itertools
'''
def support_hash_tree_gen(data_list, max_len):
    support_hash_tree = {}

    single_itemset = {}

    single_itemset_keys = single_itemset.keys()

    print("Generating order 1...")
    for d_list in data_list:
        for data in d_list:
            if data != '':
                if data in single_itemset_keys:
                    single_itemset[data] = single_itemset[data] + 1
                else:
                    single_itemset[data] = 1

    support_hash_tree['1'] = single_itemset

    for i in range(2, max_len + 1):
        print("Generating order " + str(i) + "...")
        prev_itemset = support_hash_tree[str(i - 1)]
        new_itemset = support_calculation(prev_itemset, data_list, i)
        support_hash_tree[str(i)] = new_itemset

    return support_hash_tree

def support_calculation(prev_itemset, data_list, set_len):
    new_itemset = {}

    for item in prev_itemset:
        for sec_item in prev_itemset:
            if item != sec_item:
                if set_len == 2:
                    new_tuple = tuple(set([item]).union(set([sec_item])))
                    if len(new_tuple) == set_len and sorted(new_tuple) not in sorted(tuple(new_itemset.keys())):
                        #print(new_tuple)   # remove later
                        new_itemset[new_tuple] = 0
                else:
                    new_tuple = tuple(set(list(item)).union(set(list(sec_item))))
                    if len(new_tuple) == set_len and sorted(new_tuple) not in sorted(tuple(new_itemset.keys())):
                        #print(new_tuple)   # remove later
                        new_itemset[new_tuple] = 0

    for d_list in data_list:
        for new_key in new_itemset.keys():
            if set(d_list).intersection(set(new_key)) == set(new_key):
                new_itemset[new_key] = new_itemset[new_key] + 1

    return new_itemset

def freq_itemset_gen(support_hash_tree, min_support):
    freq_itemsets = {}

    hash_keys = support_hash_tree.keys()

    for hash_key in hash_keys:
        for itemset in support_hash_tree[hash_key]:
            if support_hash_tree[hash_key][itemset] >= min_support:
                if hash_key not in freq_itemsets.keys():
                    freq_itemsets[hash_key] = {}
                freq_itemsets[hash_key][itemset] = support_hash_tree[hash_key][itemset]

    return freq_itemsets

def maximal_freq_itemset_gen(freq_itemsets, support_hash_tree, max_len):
    max_freq_len = int(max(list(freq_itemsets.keys())))
    maximal_freq_itemsets = {}

    if max_len > max_freq_len:
        for itemset in freq_itemsets[str(max_freq_len)]:
            flag = 0
            for sec_itemset in support_hash_tree[str(max_freq_len + 1)]:
                if set(list(itemset)).issubset(set(list(sec_itemset))):
                    if sec_itemset in freq_itemsets:
                        flag = 1
            if flag == 0:
                maximal_freq_itemsets[str(itemset)] = freq_itemsets[str(max_freq_len)][itemset]
            max_len = max_len - 1

    return maximal_freq_itemsets

def max_length(some_list):
    max_len = 0
    for single_list in some_list:
        if max_len < len(single_list):
            max_len = len(single_list)

    return max_len

if __name__ == "__main__":
    groceries_data = pd.read_csv('test_data.csv', sep='delimiter', header=None, engine='python')

    temp_list = groceries_data[0].tolist()
    groceries_list = []

    for g_list in temp_list:
        groceries_list.append(g_list.split(','))

    transactions = len(groceries_list)
    max_len = max_length(groceries_list)

    pool = ThreadPool(processes=cpu_count())

    print("Generating support hash tree...")
    #support_hash_tree = support_hash_tree_gen(groceries_list, max_len)
    #support_hash_tree = (pool.apply_async(support_hash_tree_gen, (groceries_list, max_len))).get()

    #pkl_file = open('hash_tree.obj', 'wb+')
    #pickle.dump(support_hash_tree, pkl_file)
    #pkl_file.close()
    pkl_file= open('hash_tree.obj', 'rb')
    support_hash_tree = pickle.load(pkl_file)
    pkl_file.close()

    #min_support_vals = [0.1, 0.2, 0.3, 0.4]
    #min_support = int(min_support_vals[2] * max(support_hash_tree['1'].values()))
    min_support = 3
    print("\nMinimum support: " + str(min_support))

    print("\nGenerating frequent itemsets...")
    #freq_itemsets = freq_itemset_gen(support_hash_tree, min_support)
    freq_itemsets = (pool.apply_async(freq_itemset_gen, (support_hash_tree, min_support))).get()
    pprint(freq_itemsets)

    print("\nGenerating maximal frequent itemsets...")
    maximal_itemsets = (pool.apply_async(maximal_freq_itemset_gen, (freq_itemsets, support_hash_tree, max_len))).get()
    pprint(maximal_itemsets)

itemset = ['bread', 'butter', 'beer']
set_len = len(itemset)

for consequent_len in range(1, set_len):
    itemset_subsets = set(itertools.combinations(set(list(itemset)), (set_len - consequent_len)))
    consequents = set(itertools.combinations(set(list(itemset)), consequent_len))
    for itemset_subset in itemset_subsets:
        for consequent in consequents:
            set_union = set(list(itemset_subset)).union(set(list(consequent)))
            if set_union == set(list(itemset)) and len(set_union) == len(itemset):
                print(itemset_subset, consequent)'''

def preprocess(data_file, write_flag=True):
    data = pd.read_csv(data_file, sep='delimiter', header=None, engine='python')
    unique = []
    processed_data = []

    for i in data[0]:
        transaction = (i.lower()).split(',')
        processed_data.append(transaction)
        for item in transaction:
            if item not in unique:
                unique.append(item)

    if write_flag:
        processed_df = pd.DataFrame(processed_data)
        processed_df.to_csv('prcessed_groceries.csv', header=None, index=False)
    unique.sort()
    #print(unique)
    return unique
