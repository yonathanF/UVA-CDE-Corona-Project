"""
Generate random COVID-19 data

File format:
     ID, First name, Last name, Street, City, State,
     Covid_affected, [children ids]
"""
from person import (Person, Address)


class Generator:
    """Base data generator"""

    def __init__(self, name_file, addresses_file, num_nodes, max_children, min_children):
        self.first_names, self.last_names = self.name_parser(name_file)
        self.streets, self.cities, self.states = self.address_parser(addresses_file)

        #index in the information lists above, used in generate_person function
        self.index = 0 

        """
        while x < num_nodes:
            num_children = random(max, min)
            root = call gen
            while y < num_children: 
                person.append(call generat_person)
                x ++ 

            root.children = person

            ...
            for each child: 
                root = child ... repeat 


            """

    def name_parser(self,filename):
        """
        Input: the name file we are parsing
        Return: list of first and list last names
        Notes: Indecies of the return lists refer to each other (the first name at index n corresponds to the last name at index n)
        """
        file_ = open(filename,"r+")
        first_names = [] #first name list
        last_names = [] #last name list
        for line in file_:
            helper = line.split(" ") #split the string at the space
            first_names.append(helper[0])
            last_names.append(helper[1].rstrip()) #rstrip to get rid of the \n char at the end of the string
        file_.close()
        return first_names, last_names

    def address_parser(self,filename):
        """
        Input: the address file we are parsing
        Return: list of streets, list of cities and list states
        Notes: Indecies of the return lists refer to each other (the street at index n corresponds to the city and state at index n)
        """
        file_ = open(filename,"r+")
        streets = []
        cities = []
        states = []
        for line in file_:
            helper = line.split(",") #split the address at the comma
            streets.append(helper[0])
            cities.append(helper[1]) 
            states.append((helper[2].replace(" ","")).rstrip())#rstrip to get rid of the \n char at the end of the string and strip to get rid of the whitespace surrounding the states
        print(len(states),len(streets),len(cities))
        return streets, cities, states

    def mark_affected(self, threshold_to_mark=10):
        pass

    def generate_person(self):
        """
        Sample a (somewhat) unique person from the data passed in
        :returns: Person
        """
        if self.index < len(self.first_names):
            address = Address(
                            self.streets[self.index],
                            self.last_names[self.index],
                            self.states[self.index]
            )
            person = Person(
                            self.first_names[self.index],
                            self.last_names[self.index],
                            address
            )
            self.index += 1
            return person
        else:
            print("No more people left to sample")
            return None

    def produce_csv(self, file_name):
        """
        loop through all nodes depth/width first
        call str on it
        with file as open(filename, 'w'):
            file.write(str ^^^)
            file.write("\n")
        """
        pass


if __name__ == "__main__":
    """
    create gen object (pass lists of names )  <-- tree is built but not marked
    obj.mark_affected(10)
    obj.produce_csv
    """
