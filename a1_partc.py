# Copy over your a1_partc.py file here
#    Main Author(s): Dragomira Veleva
#    Main Reviewer(s): Arad Fadaei



class Stack:

    def __init__(self, cap=10):
        self.stack = []
        self.cap = cap

    def capacity(self):
        return self.cap

    def push(self, data):
        self.stack.append(data)
        if len(self.stack) > self.cap:
            self.cap *= 2

    def pop(self):
        if len(self.stack) != 0:
            returner = self.stack[-1]
            del self.stack[-1]
            return returner
        raise IndexError('pop() used on empty stack')	


    def get_top(self):
        if len(self.stack) != 0:
            return self.stack[-1]
        return None	

    def is_empty(self):
        return len(self.stack) == 0

    def __len__(self):
        return len(self.stack)


class Queue:


    def __init__(self, cap=10):
        self.queue = [None]*cap # start with an array of size [cap]
        self.front = 0
        self.back = -1
        self.cap = cap
        self.size = 0


    def capacity(self):
        return self.cap

    def resize(self):
        new_cap = self.cap*2
        nwe_queue = [None] * new_cap
        for i in range(self.size):
            nwe_queue[i] = self.queue[(self.front + i) % self.cap]
        self.queue = nwe_queue
        
        self.front = 0
        self.back = self.size -1
        self.cap = new_cap

    def enqueue(self, data):
        if self.size == self.cap:
            self.resize()
        self.back = (self.back + 1) % self.cap
        self.queue[self.back] = data
        self.size = self.size + 1

    def dequeue(self):
        if not self.is_empty():
            item = self.queue[self.front]
            self.front = (self.front + 1) % self.cap
            self.size = self.size - 1
            return item
        raise IndexError("dequeue() used on empty queue")
            

    def get_front(self):
        if not self.is_empty():
            return self.queue[self.front]
        return None

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size




class Deque:

    def __init__(self, cap=10):
        self.queue = [None]*cap
        self.front = 0
        self.back = -1
        self.cap = cap
        self.size = 0

    def capacity(self):
        return self.cap

    def push_front(self, data):
        self.check_for_resize()
        self.front = (self.front - 1) % self.cap
        self.queue[self.front] = data
        self.size = self.size + 1
    
    def resize(self):
        new_cap = self.cap*2
        nwe_queue = [None] * new_cap
        for i in range(self.size):
            nwe_queue[i] = self.queue[(self.front + i) % self.cap]
        self.queue = nwe_queue
        
        self.front = 0
        self.back = self.size -1
        self.cap = new_cap

    def check_for_resize(self):
        if self.size == self.cap:
            self.resize()

    def push_back(self, data):
        self.check_for_resize()
        self.back = (self.back + 1) % self.cap
        self.queue[self.back] = data
        self.size += 1

    def pop_front(self):
        if not self.is_empty():
            item = self.queue[self.front]
            self.front = (self.front + 1) %self.cap
            self.size = self.size - 1
            return item
        raise IndexError("pop_front() used on empty deque")

    def pop_back(self):
        if not self.is_empty():
            item = self.queue[self.back]
            self.back = (self.back - 1) % self.cap
            self.size = self.size - 1
            return item
        raise IndexError("pop_back() used on empty deque")

    # assignemnt does not say return None, but seems correct
    def get_front(self):
        if self.is_empty():
            return None
        return self.queue[self.front]

    def get_back(self):
        if self.is_empty():
            return None
        return self.queue[self.back]

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def __getitem__(self, k):
        if k < 0 or k >= self.size:
            raise IndexError('Index out of range')
        return self.queue[(self.front + k) % self.cap]