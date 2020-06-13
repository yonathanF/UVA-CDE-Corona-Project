"""
Generate random COVID-19 data

File format:
     ID, First name, Last name, Street, City, State,
     Covid_affected, [children]
"""
from person import (Person, Address)

class Generator:
    """Data generator"""

    def __init__(self, num_nodes, max_children, min_children, first_names, last_names, cities, states):
        """
        while x < num_nodes:
            num_children = random(max, min)
            root = call gen
            while y < num_children: 
                person.append(call generat_person)

            root.children = person

            ...
            for each child: 
                root = child ... repeat 


            """


    def mark_affected(self, threshold_to_mark=10):
        pass

    def generate_person(self):
        """
        Sample a (somewhat) unique person from the data passed in
        """
        pass

    def produce_csv(self, file_name):
        """
        loop through all nodes depth/width first
        call str on it
        with file as open(filename, 'w'):
            file.write(str ^^^)
            file.write("\n")
        """
        pass
