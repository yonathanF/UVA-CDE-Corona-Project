"""
Graph structure with basic methods built in
"""

from personal_information import (Address, Person, COVID_Status)
from basic_data_structures import (Stack, Queue, PriorityQueue)
import csv
import random
import math

random.seed(42)


class Node:
    """
    A single entity in the graph
    """

    def __init__(self, person, weight):
        self.person = person
        self.neighbors = []
        self.visited = False
        self.weight = weight
        self.path_weight = math.inf
        self.parent = None

    def __eq__(self, other):
        return self.person.person_id == other.person.person_id

    def __hash__(self):
        return self.person.person_id

    def __str__(self):
        return f"Person ID: {self.person.person_id} | Person First Name: {self.person.first_name} | Person edge weight: {self.weight} | Person neighbors IDs: {self.neighbors} | Person path weight: {self.path_weight}"


class Graph:
    """
    A graph representation of the COVID-19 data
    """

    def __init__(self, root=None, count=0, affected=0):
        self.root = root
        # Note: this is useful only for testing. The student code should use
        # the dictionary version
        self.nodes = []
        # self.nodes = {}
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

    def get_affected_percentage(self, node=None, thres=0):
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
            if node.neighbors.count == 0:  # base case
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

        # print(str(node))
        self.nodes.append(node)

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

    def find_shortest_path(self, source, target):
        """An implementation of Dijkstras shortest path algorithm"""

        queue = PriorityQueue()
        source.path_weight = 0
        # for node in self.nodes.keys():
        # Note: this is useful for testing only; student should use the above
        for node in self.nodes:
            queue.enqueue(node)

        queue.resort()

        while not queue.empty():
            current = queue.dequeue()

            current_short_path = current.weight * current.path_weight

            for neighbor in current.neighbors:
                if neighbor.path_weight > current_short_path:
                    neighbor.parent = current
                    neighbor.path_weight = current_short_path

            queue.resort()

    def extract_path(self, source, target):
        "A utility function to extract the path after running shortest path"
        if target == source:
            return [target]

        path = [target]
        parent_path = self.extract_path(source, target.parent)
        for node in parent_path:
            path.append(node)

        return path

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

    def compute_path_probability(self, path):
        return 1 if not path else path.pop().weight/100 * self.compute_path_probability(path)


if __name__ == "__main__":
    graph = Graph()
    root = Node(Person(0, "a", "b", "123"), weight=random.randint(1, 100))
    n1 = Node(Person(1, "a", "b", "123"), weight=random.randint(1, 100))
    n2 = Node(Person(2, "a", "b", "123", COVID_Status.AFFECTED),
              weight=random.randint(1, 100))
    n3 = Node(Person(3, "a", "b", "123"), weight=random.randint(1, 100))
    n4 = Node(Person(4, "a", "b", "123"), weight=random.randint(1, 100))
    n5 = Node(Person(5, "a", "b", "123"), weight=random.randint(1, 100))

    root.neighbors = [n5, n1]
    n1.neighbors = [n3, n2]
    n2.neighbors = [n4]
    n3.neighbors = []
    n4.neighbors = []
    graph.root = root

    # print(graph.get_affected_percentage())
    # graph.print_all_nodes()
    # print(graph.iterative_bfs(root, Node(Person("123", "t", "l", "123"))))
    # for n in graph.iterative_dfs(graph.root, n5):
    # print(str(n.person.person_id), end=" --> ")
    # graph.print_all_nodes()
    # graph.print_all_nodes()
    # path = graph.iterative_dfs(root, n5)
    # for node in path:
    # print(str(node.person.person_id), end=" --> ")
    graph.find_shortest_path(root, n5)
    path = graph.extract_path(root, n5)
    weight = graph.compute_path_probability(path)
    print(weight)
