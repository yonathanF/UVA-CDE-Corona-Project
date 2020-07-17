"""
Generate random COVID-19 data

File format:
     ID, First name, Last name, Street, City, State,
     Covid_affected, [children ids]
"""
from personal_information import (Person, Address, COVID_Status)
from random import randrange, shuffle, choice
from queue import Queue
import logging
from uuid import uuid1


log = logging.getLogger("main-logger")
s = logging.StreamHandler()
log.addHandler(s)
logging.basicConfig(level=logging.CRITICAL)


class PersonGenerator(Person):
    """A person with children list to help with generation"""

    def __init__(self, person_id, first_name, last_name, address):
        super().__init__(person_id, first_name, last_name, address)
        self.children = []
        self.visited = False

    def add_child(self, person):
        self.children.append(person)

    def __str__(self):
        children = ""
        for child in self.children:
            children += " "+child.person_id

        return super().__str__()+children


class Generator:
    """Base data generator"""

    def __init__(self, name_file, addresses_file, depth_limit, min_children, max_children, degree_max, graph_edge):
        self.first_names, self.last_names = self.name_parser(name_file)
        self.streets, self.cities, self.states = self.address_parser(
            addresses_file)
        self.min_children = min_children
        self.max_children = max_children
        self.depth_limit = depth_limit
        self.global_num_nodes = 0
        self.degree_max = degree_max
        self.graph_edge = graph_edge

        # index in the information lists above, used in generate_person function
        self.index = 0

    def generate_data(self):
        """
        Generates the tree data under the parameter of the init
        """
        root = self.generate_person()
        self.global_num_nodes += 1

        def generate_single_path(self, parent, current_depth):
            # log.debug("Depth:  {}".format(current_depth))
            if current_depth >= self.depth_limit:
                return None

            num_children = randrange(self.min_children, self.max_children)
            for _ in range(num_children):
                self.global_num_nodes += 1
                new_child = self.generate_person()
                parent.add_child(new_child)
                new_child.add_child(parent)

            # log.debug(f"\t Parent has {len(parent.children)} children")
            for child_index in range(num_children):
                generate_single_path(self,
                                     parent.children[child_index], current_depth+1)
                # log.debug(f"\t Finished child {child_index} path")

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
                if root.visited:
                    continue
                else:
                    root.visited = True
                output.append(root)
                stack.extend(root.children[::-1])

            return output

        output_list = dfs(root)

        # count the number of total children per node
        def count(person):
            num_of_children = 1
            if person.visited:
                return 0
            else:
                person.visited = True

            for child in person.children:
                num_of_children += count(child)
            return num_of_children

        # iterate through our persons list and if the persons total number of
        # children divded by the total number of nodes in the tree is less
        # than the threshold and that number is not 0 (aka a leaf node) then
        # mark that person as affected
        for person in output_list:
            # we subtract one because we don't want to include ourself
            # persons_children = count(person) - 1
            # print("person childern: ", persons_children)
            bias = randrange(1, 100)
            if threshold_to_mark > bias:
                person.covid_affected = COVID_Status.AFFECTED

    def generate_person(self):
        """
        Sample a (somewhat) unique person from the data passed in
        :returns: Person
        """
        # When we have reached the max index for our bank of information,
        # shuffle the lists in random order and use them again
        if self.index >= len(self.first_names):
            shuffle(self.first_names)
            shuffle(self.last_names)
            shuffle(self.streets)
            shuffle(self.cities)
            shuffle(self.states)
            self.index = 0

        address = Address(
            self.streets[self.index],
            self.cities[self.index],
            self.states[self.index]
        )
        person = PersonGenerator(
            str(uuid1()),
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
                if node.visited:
                    continue
                else:
                    node.visited = True

                output_file.write(str(node)+"\n")
                for child in node.children:
                    queue.put(child)

    def produce_graph_viz(self, root):
        queue = Queue()
        queue.put(root)
        red = "[color=\"0.000 1.000 1.000\"]"
        blue = "[color=\"0.603 0.258 1.000\"]"
        while not queue.empty():
            node = queue.get()
            if not node.visited:
                continue
            else:
                node.visited = False

            for child in node.children:
                if child.covid_affected == COVID_Status.AFFECTED:
                    child_color = red
                else:
                    child_color = blue

                if node.covid_affected == COVID_Status.AFFECTED:
                    node_color = red
                else:
                    node_color = blue

                print(
                    f"\"{node.person_id}\" -> \"{child.person_id}\"")
                print(f"\"{node.person_id}\" {node_color};")
                print(f"\"{child.person_id}\" {child_color};")
                queue.put(child)

    def convert_to_graph(self, root):
        def convert_to_list(root):
            queue = Queue()
            queue.put(root)
            node_list = []
            while not queue.empty():
                node = queue.get()

                if not node.visited:
                    continue
                else:
                    node.visited = False

                node_list.append(node)
                for child in node.children:
                    queue.put(child)

            return node_list

        def pick_two():
            node1, node2 = choice(node_list), choice(node_list)
            while node1 == node2:
                node1, node2 = choice(node_list), choice(node_list)
            return node1, node2

        node_list = convert_to_list(root)

        dm = self.degree_max

        def f(item):
            return len(item.children) < dm

        current_conn = 0
        failed_attempts = 0
        while current_conn < self.graph_edge and failed_attempts < 10:
            node1, node2 = pick_two()
            log.debug("Current conn: "+str(current_conn))

            if len(node1.children) < self.degree_max and len(node2.children) < self.degree_max:
                node1.children.append(node2)
                node2.children.append(node1)
                current_conn += 1
                failed_attempts = 0
            else:
                failed_attempts += 1

            node_list = list(filter(f, node_list))


if __name__ == "__main__":

    generator = Generator("data/names_to_sample.txt",
                          "data/addresses_to_sample.txt", depth_limit=6, min_children=3, max_children=6, degree_max=5, graph_edge=12)

    log.debug("Created the generator")

    root = generator.generate_data()
    log.debug("Generated data")

    generator.mark_affected(root, 9)
    log.debug("Marked the affected")

    generator.convert_to_graph(root)
    log.debug("Finished converting to graph")

    generator.produce_csv(root, "data.csv")
    log.debug("Finished producing the csv")

    generator.produce_graph_viz(root)

    # generator.produce_graph_viz(root)

