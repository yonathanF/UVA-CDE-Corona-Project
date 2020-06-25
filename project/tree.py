"""
Tree structure with basic methods built in
"""
from person import (Address, Person, COVID_Status)
import csv


class Node:
    """
    A single entity in the tree
    """

    def __init__(self, person, children):
        self.person = person
        self.children = children

    def __str__(self):
        return f"Person ID: {self.person.person_id} | Person First Name: {self.person.first_name} | Person Children IDs: {self.children}"


class Tree:
    """
    A tree representation of the COVID-19 data
    """

    def __init__(self, root, count=0, affected=0):
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
            self.print_all_nodes(self.nodes[each])
        return


if __name__ == "__main__":
    # Lists Holding People and Children information
    people = []
    children = []

    # Reading CSV file and adding each person to lists
    with open('test_with_affected_marked.csv') as file:
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
    root = Node(people[0], children[0])
    tree = Tree(root=root)

    # For each person/child in our data add it to our tree
    for person, children in zip(people, children):
        curr = Node(person=person, children=children)
        tree.insert(person.person_id, curr)

    print(tree.get_affected_percentage())

    """
    examples that might be useful for print method and affected method:
    tree.root gives you the node for the tree.
    tree.root.children gives you list of IDs for root nodes children
    tree.nodes['2'] gives you the node with ID 2
    """
