from geocomp.common import point
from geocomp.common import prim

class IntersectionBST:
    
    class Node:
        def __init__(self, k, h, s, r, l):
            self.key = k #key is a point
            self.height = h
            self.size = s
            self.right = r
            self.left = l

    def __init__(self):
        self.root = None

    def isEmpty(self):
        return self.root == None
    
    def size (self):
        return self.size_aux(self.root)
    
    def size_aux(self, n):
        if (n == None): 
            return 0
        return n.size

    def height (self):
        return self.height_aux(self.root)
    
    def height_aux(self, n):
        if (n == None): 
            return -1
        return n.height

    def removeMinKey(self):
        node = self.root
        while (node.left != None):   
            node = node.left
        self.remove(node.key)
        return node

    def compare_to (self, a, b):
        if(prim.left(b.init, b.to, a.to)):
            return 1
        elif (prim.left_on(b.init, b.to, a.to)):
            return 0
        return -1
    
    def insert (self, segment):
        if (self.root == None):
            self.root = self.Node(segment, 0, 1, None, None)    
        else:
            self.root = self.insert_aux(self.root, segment)
    
    def insert_aux (self, node, segment):
        if (node == None):
            return self.Node(segment, 0, 1, None, None)
        cmp = self.compare_to(node.key, segment)
        if (cmp > 0):
            node.left = self.insert_aux(node.left, segment)
        elif (cmp < 0):
            node.right = self.insert_aux(node.right, segment)
                        
        node.size = 1 + self.size_aux(node.left) + self.size_aux(node.right)
        node.height = 1 + max(self.height_aux(node.left), self.height_aux(node.right))
        return self.balance(node)

    def balance_factor(self, node):
        return self.height_aux(node.left) - self.height_aux(node.right)

    def balance (self, node):
        if (self.balance_factor(node) < -1):
            if (self.balance_factor(node.right) > 0):
                node.right = self.rotate_right(node.right)
            node = self.rotate_left(node)

        elif (self.balance_factor(node) > 1):
            if (self.balance_factor(node.left) < 0):
                node.left = self.rotate_left(node.left)
            node = self.rotate_right(node)

        return node        

    def rotate_right(self, node):
        node2 = node.left
        node.left = node2.right
        node2.right = node
        node2.size = node.size
        node.size = 1 + self.size_aux(node.left) + self.size_aux(node.right)
        node.height = 1 + max(self.height_aux(node.left), self.height_aux(node.right))
        node2.height = 1 + max(self.height_aux(node2.left), self.height_aux(node2.right))
        return node2

    def rotate_left(self, node):
        node2 = node.right
        node.right = node2.left
        node2.left = node
        node2.size = node.size
        node.size = 1 + self.size_aux(node.left) + self.size_aux(node.right)
        node.height = 1 + max(self.height_aux(node.left), self.height_aux(node.right))
        node2.height = 1 + max(self.height_aux(node2.left), self.height_aux(node2.right))
        return node2

    def contains(self, segment):
        if (segment == None): return False
        return self.contains_aux(self.root, segment)

    def contains_aux(self, node, segment):
        if (node == None):
            return node
        
        cmp = self.compare_to(node.key, segment)
        
        if (cmp > 0):
            return self.contains_aux(node.left, segment)
        elif (cmp < 0):
            return self.contains_aux(node.right, segment)
        
        return node

    def remove(self, segment):
        if (self.contains(segment)):
            self.root = self.remove_aux(self.root, segment)

    def remove_aux(self, node, segment):
        cmp = self.compare_to(node.key, segment)
        if (cmp > 0): node.left = self.remove_aux(node.left, point)
        elif (cmp < 0): node.right = self.remove_aux(node.right, point)
        else:
            if (node.left == None):
                return node.right
            elif(node.right == None):
                return node.left
            else:
                node_y = self.Node(node.key, node.height, node.size, node.right, node.left, node.segment)
                node = self.min_aux(node_y.right)
                node.right = self.remove_min_aux(node_y.right)
                node.left = node_y.left  
        
        node.size = 1 + self.size_aux(node.left) + self.size_aux(node.right)
        node.height = 1 + max(self.height_aux(node.left), self.height_aux(node.right))
        return self.balance(node)

    def remove_min(self):
        if(not self.isEmpty()):
            self.root = self.remove_min_aux(self.root)

    def remove_min_aux(self, node):
        if (node.left == None): return node.right
        node.left = self.remove_min_aux(node.left)
        node.size = 1 + self.size_aux(node.left) + self.size_aux(node.right)
        node.height = 1 + max(self.height_aux(node.left), self.height_aux(node.right))
        return self.balance(node)

    def min(self):
        if (not self.isEmpty()):
            return self.min_aux(self.root)

    def min_aux(self, node):
        if(node.left == None):
            return node
        return self.min_aux(node.left)

    def max(self):
        if (not self.isEmpty()):
            return self.max_aux(self.root)

    def max_aux(self, node):
        if(node.right == None):
            return node
        return self.max_aux(node.right)

    def imprime(self):
        if (self.root == None): return
        print_root = 'init: ' + str(self.root.key.init) + ', to: ' + str(self.root.key.to) 
        print("A raíz é: " + print_root)
        self.imprime_aux(self.root)
        
    def imprime_aux(self, node):
        if (node == None):
            return
        self.imprime_aux(node.left)
        print('init: ' + str(node.key.init) + ', to: ' + str(node.key.to))
        self.imprime_aux(node.right)
        
    
    def plot_segments(self, color):
        self.plot_segments_aux(color, self.root)
    
    
    def plot_segments_aux(self, color, node):
        if (node == None): return
        
        self.plot_segments_aux(color, node.left)
        node.key.hilight(color)
        self.plot_segments_aux(color, node.right)
    
    def remove_from_sweepline(self, segment_tree, event_key):
        self.remove_from_sweepline_aux(segment_tree, event_key, self.root)
    
    def remove_from_sweepline_aux(self, segment_tree, event_key, node):
        if (node == None): return

        self.remove_from_sweepline_aux(segment_tree, event_key, node.left)
        segment_tree.remove(node.key, event_key)
        self.remove_from_sweepline_aux(segment_tree, event_key, node.right)

    def insert_in_sweepline(self, segment_tree, event_key):
        self.insert_in_sweepline_aux(segment_tree, event_key, self.root)

    def insert_in_sweepline_aux(self, segment_tree, event_key, node):
        if (node == None): return

        self.insert_in_sweepline_aux(segment_tree, event_key, node.left)
        segment_tree.insert(node.key, event_key)
        self.insert_in_sweepline_aux(segment_tree, event_key, node.right)
