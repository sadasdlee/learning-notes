class Node:
    def __init__(self, key = 0, value = 0):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = {}
        self.capacity = capacity
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        # add_to_head
        # remove_node
        # move_to_head
        # pop_tail
        # get
        # put
    def _add_to_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        return node

    def _move_to_head(self, node):
        self._remove_node(node)
        self._add_to_head(node)
        

    def _pop_tail(self):
        if self.head.next == self.tail:
            print("no node to pop for tail")
            return None
        else:
            node = self._remove_node(self.tail.prev)
            return node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)
        return node.value
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                tail_node = self._pop_tail()
                del self.cache[tail_node.key]
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)

lru = LRUCache(2)
lru.put(1, 1)
lru.put(2, 2)
print(lru.get(1))
lru.put(3, 3)
print(lru.get(2))