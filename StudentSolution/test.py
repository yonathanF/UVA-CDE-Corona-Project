from basic_data_structures import PriorityQueue
from graph import Node


q = PriorityQueue()
n1 = Node(None, 1)
n1.path_weight = 1
n2 = Node(None, 2)
n2.path_weight = 2
n3 = Node(None, 3)
n3.path_weight = 3
n4 = Node(None, 4)
n4.path_weight = 4


q.enqueue(n4)
q.enqueue(n3)
q.enqueue(n2)
q.enqueue(n1)

q.resort()

while not q.empty():
    print(q.dequeue().path_weight)
