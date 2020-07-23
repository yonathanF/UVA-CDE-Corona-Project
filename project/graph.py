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

    def __init__(self, person,weight):
        self.person = person
        self.neighbors = []
        self.visited = False
        self.weight = weight

    def __eq__(self, other):
        return self.person.person_id == other.person.person_id

    def __hash__(self):
        return self.person.person_id

    def __str__(self):
        return f"Person ID: {self.person.person_id} | Person First Name: {self.person.first_name} | Person weight: {self.weight} | Person neighbors IDs: {self.neighbors}"


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

    def get_affected_percentage(self, node=None, thres=50):
        """
        Return the percentage of affected nodes in the whole graph.
        """

        node = node if node else self.root

        if node.visited:
            return
        else:
            node.visited = True

        self.count += 1

        if node.person.is_person_affected() and node.weight >= thres:
            self.affected += 1
            if node.neighbors.count == 0: # base case
                return
            else:
                for each in node.neighbors:
                    each.person.covid_affected = COVID_Status.AFFECTED

        for each in node.neighbors:
            self.get_affected_percentage(each)

        return (self.affected / self.count) * 100

    def print_all_nodes(self, node=None):
        """
        Print all nodes recusively; depth-first traversal.
        """
        if not node:
            node = self.root

        if node.visited:
            return
        else:
            node.visited = True

        print(str(node))

        if node.neighbors.count == 0:  # base case
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
            if current_node.visited:
                continue
            else:
                current_node.visited = True

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
            if current_node.visited:
                continue
            else:
                current_node.visited = True

            if current_node == target_node:
                found_target = True
            for child in current_node.neighbors:
                queue.enqueue(child)

        return found_target

    def number_of_people(self, node):
        """Counts the number of people in the data set"""
        count = 1
        for child in node.neighbors:
            if child.visited:
                continue
            else:
                child.visited = True
            count += self.number_of_people(child)

        return count


if __name__ == "__main__":
    graph = Graph()
    root = Node(Person(0, "a", "b", "123"), weight=random.randint(1,100))
    n1 = Node(Person(1, "a", "b", "123"), weight=random.randint(1,100))
    n2 = Node(Person(2, "a", "b", "123", COVID_Status.AFFECTED), weight=random.randint(1,100))
    n3 = Node(Person(3, "a", "b", "123"), weight=random.randint(1,100))
    n4 = Node(Person(4, "a", "b", "123"), weight=random.randint(1,100))
    n5 = Node(Person(5, "a", "b", "123"), weight=random.randint(1,100))

    root.neighbors = [n1]
    n1.neighbors = [n2, n3, n4, n5]
    n2.neighbors = [n3]
    n3.neighbors = [n4]
    n4.neighbors = [n5]
    graph.root = root

    # print(graph.get_affected_percentage())
    # graph.print_all_nodes()
    # print(graph.iterative_bfs(root, Node(Person("123", "t", "l", "123"))))
    # for n in graph.iterative_dfs(graph.root, n5):
    # print(str(n.person.person_id), end=" --> ")
    graph.print_all_nodes()
