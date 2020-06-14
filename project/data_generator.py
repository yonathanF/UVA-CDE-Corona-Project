"""
Generate random COVID-19 data

File format:
     ID, First name, Last name, Street, City, State,
     Covid_affected, [children ids]
"""
from person import (Person, Address, COVID_Status)
from random import randrange
from queue import Queue
import logging


log = logging.getLogger("main-logger")
s = logging.StreamHandler()
log.addHandler(s)
logging.basicConfig(level=logging.CRITICAL)


class PersonGenerator(Person):
    """A person with children list to help with generation"""

    def __init__(self, first_name, last_name, address):
        super().__init__(first_name, last_name, address)
        self.children = []

    def add_child(self, person):
        self.children.append(person)

    def __str__(self):
        children = ""
        for child in self.children:
            children += ","+child.person_id

        return super().__str__()+children


class Generator:
    """Base data generator"""

    def __init__(self, name_file, addresses_file, depth_limit, min_children, max_children):
        self.first_names, self.last_names = self.name_parser(name_file)
        self.streets, self.cities, self.states = self.address_parser(
            addresses_file)
        self.min_children = min_children
        self.max_children = max_children
        self.depth_limit = depth_limit
        self.global_num_nodes = 0

        # index in the information lists above, used in generate_person function
        self.index = 0

    def generate_data(self):
        """
        Generates the tree data under the parameter of the init
        """
        root = self.generate_person()
        self.global_num_nodes += 1

        def generate_single_path(self, parent, current_depth):
            log.debug("Depth:  {}".format(current_depth))
            if current_depth >= self.depth_limit:
                return None

            num_children = randrange(self.min_children, self.max_children)
            for _ in range(num_children):
                self.global_num_nodes += 1
                parent.add_child(self.generate_person())

            log.debug(f"\t Parent has {len(parent.children)} children")
            for child_index in range(num_children):
                generate_single_path(self,
                                     parent.children[child_index], current_depth+1)
                log.debug(f"\t Finished child {child_index} path")

        generate_single_path(self, root, 0)
        return root

    def name_parser(self, filename):
        """
        Input: the name file we are parsing
        Return: list of first and list last names
        Notes: Indcies of the return lists refer to each other
              (the first name at index n corresponds to the last name at index n)
        """
        file_ = open(filename, "r+")
        first_names = []  # first name list
        last_names = []  # last name list
        for line in file_:
            helper = line.split(" ")  # split the string at the space
            first_names.append(helper[0])
            # rstrip to get rid of the \n char at the end of the string
            last_names.append(helper[1].rstrip())
        file_.close()
        return first_names, last_names

    def address_parser(self, filename):
        """
        Input: the address file we are parsing
        Return: list of streets, list of cities and list states
        Notes: Indecies of the return lists refer to each other 
               (the street at index n corresponds to the city and state at index n)
        """
        file_ = open(filename, "r+")
        streets = []
        cities = []
        states = []
        for line in file_:
            helper = line.split(",")  # split the address at the comma
            streets.append(helper[0])
            cities.append(helper[1])
            # rstrip to get rid of the \n char at the end of the string and strip to get
            # rid of the whitespace surrounding the states
            states.append((helper[2].replace(" ", "")).rstrip())
        return streets, cities, states

    def mark_affected(self, root, threshold_to_mark=10):
        """
        Marks the nodes as affected depending on the threshold_to_mark
        Input: the root and the threshold we wish to mark
        Return: N/A
        """
        
        # dfs traversal of the tree and pushing people onto a list
        # so that we can iterate through it easier
        def dfs(root):
            if root is None:
                return []
        
            stack, output = [root, ], []            
            while stack:
                root = stack.pop()
                output.append(root)
                stack.extend(root.children[::-1])
                    
            return output
        
        output_list = dfs(root)

        # count the number of total children per node
        def count(person):
            num_of_children = 1
            for child in person.children:
                num_of_children += count(child)
            return num_of_children

        # iterate through our persons list and if the persons total number of 
        # children divded by the total number of nodes in the tree is less
        # than the threshold and that number is not 0 (aka a leaf node) then
        # mark that person as affected
        for person in output_list:
            persons_children = count(person) - 1 # we subtract one because we don't want to include ourself
            if (((persons_children / self.global_num_nodes) * 100) < threshold_to_mark) and persons_children != 0:
                person.covid_affected = COVID_Status.AFFECTED

    def generate_person(self):
        """
        Sample a (somewhat) unique person from the data passed in
        :returns: Person
        """
        if self.index > len(self.first_names):
            raise ValueError("No more people left to sample")

        address = Address(
            self.streets[self.index],
            self.last_names[self.index],
            self.states[self.index]
        )
        person = PersonGenerator(
            self.first_names[self.index],
            self.last_names[self.index],
            address
        )
        self.index += 1
        return person

    def produce_csv(self, root, file_name):
        """
        Produce a csv file of the data
        """

        queue = Queue()
        queue.put(root)
        with open(file_name, 'w') as output_file:
            while not queue.empty():
                node = queue.get()
                output_file.write(str(node)+"\n")
                for child in node.children:
                    queue.put(child)


if __name__ == "__main__":

    generator = Generator("data/names_to_sample.txt",
                          "data/addresses_to_sample.txt", 3, 3, 5)
    root = generator.generate_data()
    generator.mark_affected(root)
    generator.produce_csv(root, "test_with_affected_marked.csv")

    queue = Queue()
    queue.put(root)
    while not queue.empty():
        node = queue.get()
        for child in node.children:
            print(f"\"{node.person_id, node.covid_affected}\" -> \"{child.person_id, node.covid_affected}\"")
            queue.put(child)
