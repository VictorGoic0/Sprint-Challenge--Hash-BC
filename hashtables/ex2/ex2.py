#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    ht = HashTable(length)
    route = [None] * length
    for ticket in tickets:
        if ticket.source == "NONE":
            hash_table_insert(ht, "start", ticket.destination)
        else:
            hash_table_insert(ht, ticket.source, ticket.destination)
    route[0] = hash_table_retrieve(ht, "start")
    for i in range(1, length):
        route[i] = hash_table_retrieve(ht, route[i-1])
    return route
