"""
Person related classes
"""

from enum import Enum


class COVID_Status(Enum):
    AFFECTED = 1
    NOT_AFFECTED = 2
    UNKNOWN = 3


class Address:
    def __init__(self, street, city, state):
        self.street = street
        self.city = city
        self.state = state

    def __str__(self):
        return "{}, {}, {}".format(self.street, self.city, self.state)


class Person:
    """A representation of a single person in the COVID-19 data"""

    def __init__(self, person_id,first_name, last_name, address, covid_affected=COVID_Status.UNKNOWN):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.covid_affected = covid_affected

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.person_id, self.first_name, self.last_name, str(self.address), self.covid_affected.name)

