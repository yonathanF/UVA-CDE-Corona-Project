"""
Tree structure with basic methods built in
"""

from person import (Address, Person, COVID_Status)
from basic_dts import (Stack, Queue)
import csv
import random


class Node:
    """
    A single entity in the tree
    """

    def __init__(self, person):
        self.person = person
        self.children = []

    def __eq__(self, other):
        return self.person.person_id == other.person.person_id

    def __str__(self):
        return f"Person ID: {self.person.person_id} | Person First Name: {self.person.first_name} | Person Children IDs: {self.children}"


class Tree:
    """
    A tree representation of the COVID-19 data
    """

    def __init__(self, root=None, count=0, affected=0):
        self.root = root
        self.nodes = {}
        self.count = count
        self.affected = affected

    def insert(self, id, node):
        """
        Inserts the node somewhere in the tree
        """
        if id not in self.nodes:
            self.nodes[id] = node

    def search(self, node):
        """
        Find the node in the tree. Return empty node
        if not found
        """
        pass

    def get_affected_percentage(self, node=None):
        """
        Return the percentage of affected nodes in the whole tree.
        """
        self.count += 1

        if not node:
            node = self.root

        if node.person.is_person_affected():
            self.affected += 1

        if len(node.children) == 0:  # base case
            return
        for each in node.children:
            self.get_affected_percentage(tree.nodes[each])
        return str((self.affected / self.count) * 100) + "%"

    def print_all_nodes(self, node=None):
        """
        Print all nodes recusively; depth-first traversal.
        """
        if not node:
            node = self.root

        print(str(node))

        if len(node.children) == 0:  # base case
            return
        for each in node.children:
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
            elif not current_node.children:
                path.pop()

            for child in current_node.children:
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
            for child in current_node.children:
                queue.enqueue(child)

        return found_target

    def number_of_people(self, node):
        """Counts the number of people in the data set"""
        count = 1
        for child in node.children:
            count += self.number_of_people(child)

        return count


if __name__ == "__main__":
    # Lists Holding People and Children information
    people = []
    children = []

    # Reading CSV file and adding each person to lists
    with open('data/test_with_affected_marked.csv') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            street, city, state = row[3], row[4], row[5]
            address = Address(street=street, city=city, state=state)

            person_id, first_name, last_name, covid_affected = row[0], row[1], row[2], row[6]
            covid_affected = covid_affected.strip()
            if(covid_affected == "UNKNOWN"):
                covid_affected = COVID_Status.UNKNOWN
            elif(covid_affected == "AFFECTED"):
                covid_affected = COVID_Status.AFFECTED
            else:
                covid_affected = COVID_Status.NOT_AFFECTED
            person = Person(person_id=person_id, first_name=first_name, last_name=last_name,
                            covid_affected=covid_affected, address=address)

            # Add newly created person object to people list
            people.append(person)
            # Parse children info and add to children list
            contacts = row[7].split()
            children.append(contacts)

    """
    Setting root node for the tree. To be used as the starting point for
    the print_all_nodes and get_affected_percentage method calls
    """

    nodes = {}
    for person in people:
        nodes[person.person_id] = Node(person=person)

    tree = Tree()

    for person, child in zip(people, children):
        pid = person.person_id
        for c in child:
            curr_child = nodes[c]
            nodes[pid].children.append(curr_child)
        if not tree.root:
            tree.root = nodes[pid]
        else:
            tree.insert(pid, nodes[pid])

    # print(len(tree.root.children))
    # print(tree.print_all_nodes())
    # print(tree.get_affected_percentage())
    # print(tree.number_of_people(tree.root))

    # tree2 = Tree()
    # root = Node(Person(0, "a", "b", "123"))
    # n1 = Node(Person(1, "a", "b", "123"))
    # n2 = Node(Person(2, "a", "b", "123"))
    # n3 = Node(Person(3, "a", "b", "123"))
    # n4 = Node(Person(4, "a", "b", "123"))
    # n5 = Node(Person(5, "a", "b", "123"))
# root.children = [n1] n1.children = [n2, n3, n4, n5]
    # # n2.children = [n3]
    # # n3.children = [n4]
    # # n4.children = [n5]
    # tree2.root = root

    # # print(tree2.number_of_people(tree2.root))
    target = random.choice(list(nodes.values()))
    for n in tree.iterative_dfs(tree.root, target):
        print(str(n.person.first_name), end=" --> ")
    # print(tree.iterative_bfs(tree.root, target))
    # print(tree.iterative_dfs(tree.root, Node(Person("123", "t", "l", "123"))))
    # print(tree.iterative_bfs(tree.root, Node(Person("123", "t", "l", "123"))))
