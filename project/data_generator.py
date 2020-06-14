"""
Generate random COVID-19 data

File format:
     ID, First name, Last name, Street, City, State,
     Covid_affected, [children ids]
"""
from person import (Person, Address)
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
        self.num_nodes = 0

        # index in the information lists above, used in generate_person function
        self.index = 0

    def generate_data(self):
        """
        Generates the tree data under the parameter of the init
        """
        root = self.generate_person()
        self.num_nodes += 1

        def generate_single_path(self, parent, current_depth):
            log.debug("Depth:  {}".format(current_depth))
            if current_depth >= self.depth_limit:
                return None

            num_children = randrange(self.min_children, self.max_children)
            for _ in range(num_children):
                self.num_nodes += 1
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

    def mark_affected(self, threshold_to_mark=10):
        pass

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
    generator.produce_csv(root, "test.csv")

    # queue = Queue()
    # queue.put(root)
    # while not queue.empty():
        # node = queue.get()
        # for child in node.children:
            # print(f"\"{node.person_id}\" -> \"{child.person_id}\"")
            # queue.put(child)
