class Stack:
    """A simple stack wrapper class around a Python list"""

    def __init__(self, init_items=None):
        self.items = init_items if init_items else []

    def empty(self):
        """Returns true if the stack is empty"""
        return False if self.items else True

    def push(self, new_item):
        """Adds a new item to the top of the stack"""
        self.items.append(new_item)

    def pop(self):
        """Returns and removes the item at the top of the stack"""
        return self.items.pop()


class Queue:
    """A not-so-efficient implementation of a queue"""

    def __init__(self, init_items=None):
        self.items = init_items if init_items else []

    def empty(self):
        """Returns true if the stack is empty"""
        return False if self.items else True

    def enqueue(self, item):
        """Adds a new item to the queue"""
        self.items.insert(0, item)

    def dequeue(self):
        """Removes the oldest item from the queue"""
        return self.items.pop()


class PriorityQueue:
    """A not-so-efficient implementation of a priority queue"""

    def __init__(self, init_items=None):
        self.items = init_items if init_items else []

    def empty(self):
        """Returns true if the stack is empty"""
        return False if self.items else True

    def enqueue(self, node):
        """Adds a new item to the queue"""
        self.items.append(node)
        self.items.sort(key=lambda node: node.path_weight)

    def dequeue(self):
        """Removes the oldest item from the queue"""
        return self.items.pop()

