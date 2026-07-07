"""
用 OrderedDict 实现 LRU 是最简洁的写法,因为 OrderedDict 自带两个正好为 LRU量身定做的方法:
    move_to_end() (把元素移到末尾=标记为最近使用)和
    popitem(last=False) (弹出头部=最久未使用)。
"""



from collections import OrderedDict
from typing import Any

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key: Any) -> Any:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: Any, value: Any) -> Any:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last = False)

if __name__ == '__main__':
    lru = LRUCache(2)
    lru.put(1, 1)             # cache = {1=1}
    lru.put(2, 2)             # cache = {1=1, 2=2}
    print(lru.get(1))         # 1  (访问1,1移到末尾)→ {2=2, 1=1}
    lru.put(3, 3)             # 超容,淘汰头部2 → {1=1, 3=3}
    print(lru.get(2))         # -1 (2已被淘汰)
    lru.put(4, 4)             # 超容,淘汰头部1 → {3=3, 4=4}
    print(lru.get(1))         # -1
    print(lru.get(3))         # 3
    print(lru.get(4)) 