"""
Graph structure with basic methods built in
"""

from personal_information import (Address, Person, COVID_Status)
from basic_data_structures import (Stack, Queue)
import csv
import random


class Node:
    """
    A single entity in the graph
    """
    pass


class Graph:
    """
    A graph representation of the COVID-19 data
    """

    def iterative_dfs(self, source_id, target_id):
        # source_id -> source objce
        source = self.nodes.get(source_id)
        target = self.nodes.get(target_id)
        stack = Stack()
        path = []

        while not stack.empty():
            # check if visited
            # if not mark as visited
            node = stack.pop()
            if node.visited == True:
                continue

            node.visited = True
            if node == target:
                return path

            path.append(node)

            # node.neighbors --> list of neighbors of node
            for neighbor_id in node.neighbors:
                neigbhor = self.nodes.get(neighbor_id)

        return False

    def shortest_path(self, source_id, target_id):
        """
        loop to iterate over all the nodes --> 
            use the id of the source
            use that until you find the target

        how to  use dict : similar idea 
            id --> node  <<--- 
            python dict: dict.value() --> a list of all the right side of the map

        some of bruteforce algo

        """

        source = self.nodes.get(source_id)
        source.path_weight = 0

        target = self.nodes.get(target_id)

        queue = PriorityQueue()
        queue.enqueue(source)

        for node in self.nodes.values():
            queue.enqueue(node)
        while not queue.empty():
            node = queue.dequeue()
            for neigbhor_id in node.neighbors:
                alt_path_weight = node.path_weight + node.weight
                if alt_path_weight <= neighbor.path_weight:
                    neighbor.path_weight = alt_path_weight
                    neighbor.parent = node
            queue.resort()

    def extract_path(self, source, target):
        # base case
        if target == source:
            return [target]

        path = [target]

        parent_path = self.extract_path(source, target.parent)

        # [1,2,3,4] 5 ---> [1,2,3,4,5]
        for node in parent_path:
            path.append(node)

        return path

    def compute_path_probability(self, path):
        """
        [node_id1, node_id2,node_id3,node_id4]
        1. convert from id to node --> look up in the dict
        2. node1.weight * compute_path_probability(path - the first one)
        pop from list: list.pop()
            - this removes the first (last?) items and returns to you 

        # product([1,2,3,4])  ==> 1 times product([2,3,4])
                                          ==> 2 * product([3,4])
                                                 ==> 3 * product([4])
                                                         ==> 4 * product([])
                                                                 ==> 1 --> base
        """
        # vvv the weight of the first time

        if len(path) == 0:
            return 1

        node = self.nodes.get(path.pop())
        weight = node.weight
        return weight * self.compute_path_probability(path)

