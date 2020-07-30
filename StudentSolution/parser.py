from graph import (Graph, Node)
from personal_information import (Person, Address, COVID_Status)
import csv
import random

random.seed(52)

if __name__ == "__main__":
    # Lists Holding People and neighbors information
    people = []
    neighbors = []

    # Reading CSV file and adding each person to lists
    # was breaking on my machine if I didn't write out the full path from root
    with open('data.csv') as file:
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
    random.seed(30)
    nodes = {}
    for person in people:
        nodes[person.person_id] = Node(
            person=person, weight=random.randint(1, 100))

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

    # use these to play with the different graph methods
    # that need a target and source
    target = random.choice(list(nodes.values()))
    source = random.choice(list(nodes.values()))

    # try uncommenting one at a time and printing the variable

    # affected_percentage = graph.get_affected_percentage(target)
    # source_target_bfs = graph.iterative_bfs(source, target)
    # source_target_dfs = graph.iterative_dfs(source, target)

    # uncomment the following lines together
    graph.find_shortest_path(source, target)
    shortest_path = graph.extract_path(source, target)

    for node in shortest_path:
        print(node.person.first_name, end=" -> ")

    path_probability = graph.compute_path_probability(shortest_path)
    print("\n\nPath probability: ", path_probability)
