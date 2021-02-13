#--------------------------------------
#tup = ('e','x','e','r','c','i','s','e','s')
#for i in range(9):
#    print(str(tup[i]), end = '')
#str = ''.join(tup)
#print(str)
#--------------------------------------

class Node: #this does not create a node, only defines one
    #single node
    def __init__(self,data=None):
        self.data = data
        self.next = None
class singly_linked_list:
    def __init__(self):
        #create an empty list
        self.head = None
        self.tail = None
        self.count = 0
    def iterate_item(self):
        current_item = self.head
        while current_item:
            val = current_item.data
            current_item = current_item.next
            yield val #return data of current item (simlar to print)
    def append_item(self,data): # append items to the end of the list
        node = Node(data)
        if self.tail: # adds node in the end (when it reaches the current tail)
            self.tail.next = node
            self.tail = node
        else:
            self.head = node # adds a node for the head section of the list
            self.tail = node
        self.count += 1

# implememtation of the classes above
items = singly_linked_list() # dont need to call the class "node" since it was aready called in the "singly linked list" class

#appending items with the append_item function to append items into the empty linked list
items.append_item('PHP')
items.append_item('PYTHON')
items.append_item('C#')
items.append_item('C++')
items.append_item('JAVA')

for val in items.iterate_item():
    print(val)
print("\nhead.data: ",items.head.data)
print("tail.data: ",items.tail.data)
