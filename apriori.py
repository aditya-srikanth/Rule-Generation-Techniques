import os
import pandas as pd
from pprint import pprint

def freq_item_set_gen(freq_prev_set, groceries_list, set_len):
    new_itemset = {}

    for item in freq_prev_set:
        for sec_item in freq_prev_set:
            if item != sec_item:
                if set_len  == 2:
                    new_tuple = tuple(set([item]).union(set([sec_item])))
                    if sorted(new_tuple) not in sorted(tuple(new_itemset.keys())) and len(new_tuple) == set_len:
                        new_itemset[new_tuple] = 0
                else:
                    new_tuple = tuple(set(list(item)).union(set(list(sec_item))))
                    if sorted(new_tuple) not in sorted(tuple(new_itemset.keys())) and len(new_tuple) == set_len:
                        new_itemset[new_tuple] = 0

    for g_list in groceries_list:
        for new_key in new_itemset.keys():
            if set(g_list).intersection(set(new_key)) == set(new_key):
                new_itemset[new_key] = new_itemset[new_key] + 1

    freq_new_set = {}

    for new_key in new_itemset.keys():
        if new_itemset[new_key] >= min_support:
            freq_new_set[new_key] = new_itemset[new_key]

    return freq_new_set

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

    single_itemset = {}

    single_itemset_keys = single_itemset.keys()

    for g_list in groceries_list:
        for grocery in g_list:
            if grocery != '':
                if grocery in single_itemset_keys:
                    single_itemset[grocery] = single_itemset[grocery] + 1
                else:
                    single_itemset[grocery] = 1

    min_support_vals = [0.1, 0.2, 0.3, 0.4]

    #min_support = min_support_vals[0] * max(single_itemset.values())
    min_support = 2

    freq_single_set = {}

    for single_key in single_itemset.keys():
        if single_itemset[single_key] >= min_support:
            freq_single_set[single_key] = single_itemset[single_key]

    freq_item_sets = {}

    freq_item_sets['1'] = freq_single_set

    for i in range(2, max_len + 1):
        prev_freq_set = freq_item_sets[str(i - 1)]
        temp_set = freq_item_set_gen(prev_freq_set, groceries_list, i)
        if temp_set == {}:
            break
        else:
            freq_item_sets[str(i)] = temp_set

    pprint(freq_item_sets)
