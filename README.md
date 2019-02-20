# Rule Generation Techniques

The current repository consists of two frequent itemset and association rule mining algorithms: **Apriori Algorithm** and **FP Tree Algorithm**.

### Apriori algorithm

The apriori algorithm has been implemented in Python3 and is contained in the **apriori.py** file. This file houses functions related to the apriori algorithm. The main functions are:
1. ***freq_itemset_gen()***: Generates frequent itemsets for a given transaction database for some given minimum support.
2. ***maximal_itemset_gen()***: Generates maximal frequent itemsets from the given frequent itemsets.
3. ***closed_freq_itemset_gen()***: Generates closed frequent itemsets  from the given frequent itemsets.
4. ***rule_generation***: Generates the association rules for the frequent itemsets for some given minimum confidence.

The current implementation might ocassionally crash while generating association rules. This is due to the fact that an example itemset *(i, j)* is not similar to *(j, i)* and while performing comparision operations during rule generation, this will throw an exception.

The current implementation makes use of thread pools to try and decrease computation costs.

The current average performance metrics of the apriori algorithm are as follows:

**Dataset**: groceries.csv
<br>**Minimum support**: 200
<br>**Minimum confidence**: 50%

Generated data | Avg time taken
--- | ---
Frequent itemsets | 17.46
Maximal frequent itemsets | 0.000337
Closed frequent itemsets | 0.000339
Association rules | 0.000769


### FP Tree

1. ***insert()***: Inserts values into the tree, is a wrapper which calls insert_recurse 
2. ***insert_recurse()***: Recursively descends the tree and inserts the transaction into the tree
3. ***print_nodes()***: Utility for printing the supports, the parent, and the children of each node in the tree
4. ***print_supports()***: Utility for printing the support counts for each item
5. ***reset_nodes()***: Used by get_frequent_itemsets_with_suffix to extract the candidate itemsets
6. ***generate_conditional_fp_tree()***: Used to traverse the tree and generate the tree
7. ***reset_values()***: Resets the temp_val of each node 
8. ***get_frequent_itemsets_with_suffix()***: This returns the frequent itemsets recursively
9. ***fp_growth()***: Wrapper that is used to extact the frequent itemsets
10. ***process_dataset()***: Used to preprocess the dataset, sort according to the supports and remove None values
11. ******

### Built With
 The project uses:
 1. Python3
 2. Pandas
 3. OS
 4. Itertools
 5. Argparse
 6. Pprint
 7. Multiprocessing


 ### Authors

 Naren Surampudi [https://github.com/nsurampu]<br>
 Aditya Srikanth
 Prateek Dasgupta
