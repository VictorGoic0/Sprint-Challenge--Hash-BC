#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)
    for i in range(length):
        hash_table_insert(ht, weights[i], i)
    for i in range(length):
        if hash_table_retrieve(ht, limit-weights[i]):
            index_1 = i
            index_2 = hash_table_retrieve(ht, limit-weights[i])
            if index_1 > index_2:
                return (index_1, index_2)
            return (index_2, index_1)
    return None


def print_answer(answer):
    if answer is None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
