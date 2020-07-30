class Stack:
    """A simple stack wrapper class around a Python list"""

    def __init__():
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def empty(self):
        return len(self.items) == 0


class Queue:
    """A simple implementation of a queue using a Python list"""
    def __init__():
        self.items = []

    def push(self, item):
        #self.items.insert(0, item)
        self.items.append(item)

    def pop(self):
        # return self.items.pop()
        return self.items.pop(0)

    def empty(self):
        return len(self.items) == 0


q = Queue()
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
q.enqueue(4)

while not q.empty():
    print(q.dequeue())

# run as
# python basic_data_structures.py
# Expected output:
# 1
# 2
# 3
# 4

