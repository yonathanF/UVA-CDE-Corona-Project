from graph import (Graph, Node)
from personal_information import (Person, Address, COVID_Status)
import csv
import random
# import os

# print(os.listdir())

if __name__ == "__main__":
    # Lists Holding People and neighbors information
    people = []
    neighbors = []

    # Reading CSV file and adding each person to lists
    with open('project/data.csv') as file: # was breaking on my machine if I didn't write out the full path from root
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
            # Parse neighbors info and add to children list
            contacts = row[7].split()
            neighbors.append(contacts)

    """
    Setting root node for the tree. To be used as the starting point for
    the print_all_nodes and get_affected_percentage method calls
    """

    nodes = {}
    for person in people:
        nodes[person.person_id] = Node(person=person, weight=random.randint(0,10))

    graph = Graph()

    for person, child in zip(people, neighbors):
        pid = person.person_id
        for c in child:
            curr_child = nodes[c]
            nodes[pid].neighbors.append(curr_child)
        if not graph.root:
            graph.root = nodes[pid]
        else:
            graph.insert(pid, nodes[pid])

    # print(len(graph.root.neighbors))
    # print(graph.print_all_nodes())
    # print(graph.get_affected_percentage())
    # print(graph.number_of_people(graph.root))

    # graph2 = graph()
    # root = Node(Person(0, "a", "b", "123"), weight=random.randint(0,10))
    # n1 = Node(Person(1, "a", "b", "123"), weight=random.randint(0,10))
    # n2 = Node(Person(2, "a", "b", "123"), weight=random.randint(0,10))
    # n3 = Node(Person(3, "a", "b", "123"), weight=random.randint(0,10))
    # n4 = Node(Person(4, "a", "b", "123"), weight=random.randint(0,10))
    # n5 = Node(Person(5, "a", "b", "123"), weight=random.randint(0,10))
# root.neighbors = [n1] n1.children = [n2, n3, n4, n5]
    # # n2.neighbors = [n3]
    # # n3.neighbors = [n4]
    # # n4.neighbors = [n5]
    # graph2.root = root

    target = random.choice(list(nodes.values()))
    print(graph.get_affected_percentage())
    # print(graph.number_of_people(graph.root))
    # for n in graph.iterative_dfs(graph.root, target):
    # print(str(n.person.first_name), end=" --> ")
    # print(graph.iterative_bfs(graph.root, target))
    # print(graph.iterative_dfs(graph.root, Node(Person("123", "t", "l", "123"))))
    # print(graph.iterative_bfs(graph.root, Node(Person("123", "t", "l", "123"))))
