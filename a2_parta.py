#    Main Author(s): Arad Fadaei
#    Main Reviewer(s): Jagbir Singh

from typing import Any, Iterator, Optional

class HashTableLinkedList:
    """
    LinkedList used for HashTable
    """
    class Node:
        """
        A nested class that represents a node in the doubly linked list.
        """
        def __init__(self, 
                    key: Optional[str] = None,
                    data: Optional[Any] = None, 
                    next: Optional['HashTableLinkedList.Node'] = None, 
                    prev: Optional['HashTableLinkedList.Node'] = None) -> None:
            """
            Initializes a new node.
            
            Parameters:
                key (Optional[str]): Hashed key for retrieval.
                data (Optional[Any]): The data to be stored in the node.
                next (Optional['HashTableLinkedList.Node']): The next node in the list.
                prev (Optional['HashTableLinkedList.Node']): The previous node in the list.
            """
            self._key: Optional[str] = key
            self._data: Optional[Any] = data
            self._next: Optional['HashTableLinkedList.Node'] = next
            self._prev: Optional['HashTableLinkedList.Node'] = prev


        def get_key(self) -> Optional[str]:
            """
            Get the key of the node.
            
            Returns:
                Optional[str]: The key of the node if it exists, else None.
            """
            return self._key if self._key is not None else None
        
        
        def get_data(self) -> Optional[Any]:
            """
            Get the data stored in the node.
            
            Returns:
                Optional[Any]: The data of the node if it exists, else None.
            """
            return self._data


        def set_data(self, data: Any) -> None:
            """
            Set the data of the node.
            
            Parameters:
                data (Any): The new data to be set.
            
            Returns:
                None
            """
            self._data = data


        def get_next(self) -> Optional['HashTableLinkedList.Node']:
            """
            Get the next node in the list.
            
            Returns:
                Optional['HashTableLinkedList.Node']: The next node if it exists, else None.
            """
            return self._next


        def get_previous(self) -> Optional['HashTableLinkedList.Node']:
            """
            Get the previous node in the list.
            
            Returns:
                Optional['HashTableLinkedList.Node']: The previous node if it exists, else None.
            """
            return self._prev


        def set_next(self, next: 'HashTableLinkedList.Node') -> None:
            """
            Set the next node in the list.
            
            Parameters:
                next (HashTableLinkedList.Node): The new next node.
            
            Returns:
                None
            """
            self._next = next


        def set_previous(self, prev: 'HashTableLinkedList.Node') -> None:
            """
            Set the previous node in the list.
            
            Parameters:
                prev (HashTableLinkedList.Node): The new previous node.
            
            Returns:
                None
            """
            self._prev = prev


    def __init__(self):
        """
        Initializes an empty linked list with sentinel head and tail nodes.
        """
        self.head: 'HashTableLinkedList.Node' = self.Node()
        self.tail: 'HashTableLinkedList.Node' = self.Node()

        # link sentinels
        self.head.set_next(self.tail)
        self.tail.set_previous(self.head)

        # for len operation
        self.len: int = 0


    def __iter__(self) -> Iterator['HashTableLinkedList.Node']:
        """
        Iterates through the nodes in the linked list.

        Returns:
            Iterator['HashTableLinkedList.Node']: An iterator over the nodes in the list.
        """
        curr: Optional['HashTableLinkedList.Node'] = self.get_front()
        while curr != self.tail:
            if curr is None:
                break
            yield curr
            curr = curr.get_next()


    def get_front(self) -> Optional['HashTableLinkedList.Node']:
        """
        Get the front node (the first actual node after the head) of the linked list.

        Returns:
            Optional['HashTableLinkedList.Node']: The front node if it exists, else None.
        """
        if self.len:
            return self.head.get_next()
            

    def get_back(self) -> Optional['HashTableLinkedList.Node']:
        """
        Get the back node (the last actual node before the tail) of the linked list.

        Returns:
            Optional['HashTableLinkedList.Node']: The back node if it exists, else None.
        """
        if self.len:
            return self.tail.get_previous()


    def is_empty(self) -> bool:
        """
        Check if the linked list is empty.

        Returns:
            bool: True if the linked list is empty, else False.
        """
        return self.len == 0


    def __len__(self) -> int:
        """
        Get the number of nodes in the linked list.

        Returns:
            int: The number of nodes in the linked list.
        """
        return self.len        


    def insert(self, key: str, data: Any) -> 'HashTableLinkedList.Node':
        """
        Inserts a new element into the linked list.

        Parameters:
            data (Any): The data to be inserted.
            
        Returns:
            'HashTableLinkedList.Node': The newly created node
        """
        new_node: 'HashTableLinkedList.Node' = self.Node(key, data)
        if self.len == 0:
            self.tail.set_previous(new_node)
            self.head.set_next(new_node)

            new_node.set_next(self.tail)
            new_node.set_previous(self.head)
        else:
            back: 'HashTableLinkedList.Node' = self.get_back() # type: ignore
            back.set_next(new_node)
            self.tail.set_previous(new_node)
            new_node.set_previous(back)
            new_node.set_next(self.tail)
            
        self.len += 1
        return new_node
    
    
    def erase(self, node: 'HashTableLinkedList.Node') -> None:
        """
        Removes a node from the list.

        Parameters:
            node ('HashTableLinkedList.Node'): The node to be removed
        """
        if self.len == 0:
            return

        curr: 'HashTableLinkedList.Node' = self.get_front() # type: ignore
        
        while curr != self.tail:
            if curr is node:
                curr.get_previous().set_next(curr.get_next()) # type: ignore
                curr.get_next().set_previous(curr.get_previous()) # type: ignore
                self.len -= 1
                return
            curr = curr.get_next() # type: ignore
        
        
    def search(self, key: str) -> Optional['HashTableLinkedList.Node']:
        """
        Searches for a node with the specified key.

        Parameters:
            key (str): The key to search for.

        Returns:
            Optional['HashTableLinkedList.Node']: The node with the key, or None if not found
        """
        if self.len == 0:
            return

        curr: 'HashTableLinkedList.Node' = self.get_front() # type: ignore
        
        while curr != self.tail:
            if curr.get_key() == key:
                return curr
            curr = curr.get_next() # type: ignore

            
class HashTable:
    """
    Hash table implementation using chaining for conflict resolution. 
    Uses the HashTableLinkedList as the buckets
    """
    def __init__(self, cap: int = 32) -> None:
        """
        Initializes a new HashTable
        
        Parameters:
            cap (int = 32): Initial capacity of the Hash table
        """
        self._buckets: list = [None] * cap
        self._cap: int = cap
        self._size: int = 0

        for i in range(self.capacity()):
            self._buckets[i] = HashTableLinkedList()
        

    def insert(self, key: Any, value: Any) -> bool:
        """
        Insert a new key-value pair into the hash table.

        Parameters:
            key (Any): The key to be hashed.
            value (Any): The data to be stored.

        Returns:
            bool: Returns True if the key-value pair was successfully inserted, else False.
        """
        index: int = hash(key) % self.capacity()
        
        if self.search(key) is None:
            bucket: 'HashTableLinkedList' = self._buckets[index]
            bucket.insert(key, value)
            self._size += 1 
            
            if self.load_factor() > .7:
                self.resize()
                
            return True
        
        return False
        
        
    def modify(self, key, value) -> bool:
        """
        Modify the value associated with a key in the hash table.

        Parameters:
            key (Any): The key whose value is to be modified.
            value (Any): The new value to be associated with the key.

        Returns:
            bool: Returns True if the value was successfully modified, else False.
        """
        index: int = hash(key) % self.capacity()
        
        if self.search(key) is not None:
            bucket: HashTableLinkedList = self._buckets[index]
            node: Optional['HashTableLinkedList.Node'] = bucket.search(key)
            if node is not None:
                node.set_data(value)
                return True

        return False


    def remove(self, key) -> bool:
        """
        Remove a key-value pair from the hash table.

        Parameters:
            key (Any): The key to be removed.

        Returns:
            bool: Returns True if the key-value pair was successfully removed, else False.
        """
        index: int = hash(key) % self.capacity()
        
        if self.search(key) is not None:
            bucket: HashTableLinkedList = self._buckets[index]
            node: Optional['HashTableLinkedList.Node'] = bucket.search(key)
            if node is not None:
                bucket.erase(node)
                self._size -= 1
                return True

        return False


    def search(self, key) -> Optional[Any]:
        """
        Search for a value associated with a key in the hash table.

        Parameters:
            key (Any): The key to be searched.

        Returns:
            Optional[Any]: Returns the value associated with the key if found, else None.
        """
        index: int = hash(key) % self.capacity()
        cell: HashTableLinkedList = self._buckets[index]
        
        searched: Optional['HashTableLinkedList.Node'] = cell.search(key)
        
        if searched is None:
            return None
        else:
            return searched.get_data()
            
            
    def resize(self) -> None:
        """
        Resize the hash table by doubling its capacity and rehashing all existing key-value pairs.

        Returns:
            None
        """
        new_capacity = self.capacity() * 2
        new_buckets: list = [None] * new_capacity

        for i in range(new_capacity):
            new_buckets[i] = HashTableLinkedList()

        for bucket in self._buckets:
            for node in bucket:
                index: int = hash(node.get_key()) % new_capacity
                new_buckets[index].insert(node.get_key(), node.get_data())

        self._buckets = new_buckets
        self._cap = new_capacity
            
            
    def load_factor(self) -> float:
        """
        Calculate the current load factor of the hash table.

        Returns:
            float: The load factor of the hash table.
        """
        return self._size / self.capacity()


    def capacity(self) -> int:
        """
        Get the current capacity of the hash table.

        Returns:
            int: The capacity of the hash table.
        """
        return self._cap


    def __len__(self) -> int:
        """
        Get the number of key-value pairs in the hash table.

        Returns:
            int: The number of key-value pairs in the hash table.
        """
        return self._size