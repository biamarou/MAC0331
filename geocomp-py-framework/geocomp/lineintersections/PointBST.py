from geocomp.common import point

class PointBST:
    
    class Node:
        def __init__(self, k, h, s, r, l, sg):
            # key is a point
            self.key = k
            self.height = h
            self.size = s
            self.right = r
            self.left = l
            self.segment = sg

    def __init__(self):
        self.root = NULL

    def isEmpty(self):
        return self.root == NULL
    
    def size (self):
        return size(self.root)
    
    def size(self, n):
        if (n == NULL): 
            return 0
        return n.size

    def height (self):
        return height(self.root)
    
    def height(self, n):
        if (n == NULL): 
            return -1
        return n.height

    def removeMinKey(self):
        node = self.root
        while (node.left != NULL):
            node = node.left
        self.remove(node.key)
        return node.key
    
    def insert (self, point, segment):
        #We pass the segments of which the point is a vertice
        if (self.root == NULL):
            self.root = Node(point, 0, 1, NULL, NULL, segment)    
        else:
            self.root = self.insert(self.root, point)
    
    def compare_to (self, p1, p2):
        if (p1.x > p2.x):
            return 1
        elif (p1.x < p2.x):
            return -1
        return 0

    # Assuming there aren't two equal points
    def insert (self, node, point):
        if (node == NULL):
            return Node(point, 0, 1, NULL, NULL)
        cmp = self.compare_to(point, node.key)
        if (cmp < 0):
            node.left = self.insert(node.left, point)
        elif (cmp > 0):
            node.right = self.insert(node.right, point)

        node.size = 1 + self.size(node.left) + self.size(node.right)
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        return balance(node)

    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right)

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
        node.size = 1 + self.size(node.left) + self.size(node.right)
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        node2.height = 1 + max(self.height(node2.left), self.height(node2.right))
        return node2

    def rotate_left(self, node):
        node2 = node.right
        node.right = node2.left
        node2.left = node
        node2.size = node.size
        node.size = 1 + self.size(node.left) + self.size(node.right)
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        node2.height = 1 + max(self.height(node2.left), self.height(node2.right))
        return node2

    def contains(self, point):
        if (point == NULL) return False
        return self.contains(self.root, point)

    def contains(self, node, point):
        if (node == NULL):
            return False
        cmp = self.compare_to(point, node.key)
        if (cmp < 0):
            node.left = self.contains(node.left, point)
        elif (cmp > 0):
            node.right = self.contains(node.right, point)
        else:
             return True


    def remove(self, point):
        if (self.contains(point)):
            self.root = self.remove(self.root, point)

    #Assuming there aren`t two equal points  
    def remove(self, node, point):
        cmp = self.compare_to(point, node.key)
        if (cmp < 0) node.left = self.remove(node.left, point)
        elif (cmp > 0) node.right = self.remove(node.right, point)
        
        node.size = 1 + self.size(node.left) + self.size(node.right)
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        return balance(node)