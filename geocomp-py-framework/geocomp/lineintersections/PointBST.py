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
        self.root = None

    def isEmpty(self):
        return self.root == None
    
    def size (self):
        return size_aux(self.root)
    
    def size_aux(self, n):
        if (n == None): 
            return 0
        return n.size

    def height (self):
        return height_aux(self.root)
    
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
    

    def insert (self, point, segment):
        #We pass the segments of which the point is a vertice
        if (self.root == None):
            self.root = self.Node(point, 0, 1, None, None, segment)    
        else:
            self.root = self.insert_aux(self.root, point, segment)
    
    def compare_to (self, p1, p2):
        if (p1.x > p2.x):
            return 1
        elif (p1.x < p2.x):
            return -1
        return 0

    # Assuming there aren't two equal points
    # se tiver ponto igual os ponta esquerda sao menores
    def insert_aux (self, node, point, segment):
        if (node == None):
            return self.Node(point, 0, 1, None, None, segment)
        cmp = self.compare_to(node.key, point)
        if (cmp > 0):
            node.left = self.insert_aux(node.left, point, segment)
        elif (cmp < 0):
            node.right = self.insert_aux(node.right, point, segment)
        else:
            if (node.key.y > point.y):
               node.left = self.insert_aux(node.left, point, segment)
            else:
                node.right = self.insert_aux(node.right, point, segment)
                
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

    def contains(self, point):
        if (point == None): return False
        return self.contains_aux(self.root, point)

    def contains_aux(self, node, point):
        if (node == None):
            return False
        cmp = self.compare_to(node.key, point)
        if (cmp > 0):
            return self.contains_aux(node.left, point)
        elif (cmp < 0):
            return self.contains_aux(node.right, point)
        else:
            if (node.key.y > point.y):
                return self.contains_aux(node.left, point)
            elif (node.key.y < point.y):
                return self.contains_aux(node.right, point)
            else:
                return True


    def remove(self, point):
        if (self.contains(point)):
            self.root = self.remove_aux(self.root, point)

    #Assuming there aren`t two equal points  
    def remove_aux(self, node, point):
        cmp = self.compare_to(node.key, point)
        if (cmp > 0): node.left = self.remove_aux(node.left, point)
        elif (cmp < 0): node.right = self.remove_aux(node.right, point)
        else:
                if (node.key.y > point.y):
                    node.left = self.remove_aux(node.left, point)
                elif (node.key.y < point.y):
                    node.right = self.remove_aux(node.right, point)
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