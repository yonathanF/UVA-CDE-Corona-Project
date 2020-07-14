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

    def __init__(self, person):
        self.person = person
        self.neighbors = []
        self.visited = False

    def __eq__(self, other):
        return self.person.person_id == other.person.person_id

    def __str__(self):
        return f"Person ID: {self.person.person_id} | Person First Name: {self.person.first_name} | Person neighbors IDs: {self.neighbors}"


class Graph:
    """
    A graph representation of the COVID-19 data
    """

    def __init__(self, root=None, count=0, affected=0):
        self.root = root
        self.nodes = {}
        self.count = count
        self.affected = affected

    def insert(self, id, node):
        """
        Inserts the node somewhere in the graph
        """
        if id not in self.nodes:
            self.nodes[id] = node

    def search(self, node):
        """
        Find the node in the graph. Return empty node
        if not found
        """
        pass

    def get_affected_percentage(self, node=None):
        """
        Return the percentage of affected nodes in the whole graph.
        """
        self.count += 1

        if not node:
            node = self.root

        if node.person.is_person_affected():
            self.affected += 1

        if len(node.neighbors) == 0:  # base case
            return
        for each in node.neighbors:
            self.get_affected_percentage(graph.nodes[each])
        return str((self.affected / self.count) * 100) + "%"

    def print_all_nodes(self, node=None):
        """
        Print all nodes recusively; depth-first traversal.
        """
        if not node:
            node = self.root

        print(str(node))

        if len(node.neighbors) == 0:  # base case
            return
        for each in node.neighbors:
            self.print_all_nodes(each)
        return

    def iterative_dfs(self, start_node, target_node):
        """Iterative implementation of DFS"""

        stack = Stack()
        stack.push(start_node)
        path = []

        while not stack.empty():
            current_node = stack.pop()
            path.append(current_node)

            if current_node == target_node:
                return path
            elif not current_node.neighbors:
                path.pop()

            for child in current_node.neighbors:
                stack.push(child)

        return []

    def iterative_bfs(self, start_node, target_node):
        """Iterative implementation of BFS"""

        queue = Queue()
        queue.enqueue(start_node)
        found_target = False

        while not queue.empty():
            current_node = queue.dequeue()
            if current_node == target_node:
                found_target = True
            for child in current_node.neighbors:
                queue.enqueue(child)

        return found_target

    def number_of_people(self, node):
        """Counts the number of people in the data set"""
        count = 1
        for child in node.neighbors:
            count += self.number_of_people(child)

        return count


if __name__ == "__main__":
    graph = Graph()
    root = Node(Person(0, "a", "b", "123"))
    n1 = Node(Person(1, "a", "b", "123"))
    n2 = Node(Person(2, "a", "b", "123"))
    n3 = Node(Person(3, "a", "b", "123"))
    n4 = Node(Person(4, "a", "b", "123"))
    n5 = Node(Person(5, "a", "b", "123"))

    root.neighbors = [n1]
    n1.neighbors = [n2, n3, n4, n5]
    n2.neighbors = [n3]
    n3.neighbors = [n4]
    n4.neighbors = [n5]
    graph.root = root

    for n in graph.iterative_dfs(graph.root, n5):
        print(str(n.person.person_id), end=" --> ")
