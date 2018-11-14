from geocomp.common import segment
from geocomp.common import prim

class SegmentBST:
    
    class Node:
        def __init__(self, k, h, s, r, l):
            # key is a segment
            self.key = k
            self.height = h
            self.size = s
            self.right = r
            self.left = l

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
    
    def get_y_coord (self, l, r, x):
        return ((r.y - l.y)/(r.x - l.x)) * (x - (l.x)) + l.y

    def compare_to (self, p, s): #devolve 1 se p estah ah esquerda de s.
        left_test = prim.left(s.init, s.to, p)
        left_on_test = prim.left_on(s.init, s.to, p)

        if (left_test): return 1
        elif (left_on_test): return 0
        else: return -1

    def insert (self, segment, sweepline_point): #sweepline_point eh a x-coordenada da sweepline
        if (self.root == None):
            self.root = self.Node(segment, 0, 1, None, None)    
        else:
            self.root = self.insert_aux(self.root, segment, sweepline_point)

    # Assuming there aren't two equal segments
    def insert_aux (self, node, segment, sweepline_point):
        if (node == None):
            return self.Node(segment, 0, 1, None, None)
        cmp = self.compare_to(sweepline_point, node.key)
        if (cmp <= 0):
            node.left = self.insert_aux(node.left, segment, sweepline_point)
        elif (cmp > 0):
            node.right = self.insert_aux(node.right, segment, sweepline_point)

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

    def contains(self, segment, sweepline_point):
        if (segment == None): return False
        return self.contains_aux(self.root, segment, sweepline_point)

    def contains_aux(self, node, segment, sweepline_point):
        #print("to procurando")
        if (node == None):
            return False
        cmp = self.compare_to(sweepline_point, node.key)
        #print(cmp)
        if (cmp < 0 or (cmp == 0 and segment != node.key)):
            #print("achei primeiro seg")
            self.contains_aux(node.left, segment, sweepline_point)
        elif (cmp > 0):
            self.contains_aux(node.right, segment, sweepline_point)
        else:
             return True

    def get_predecessor(self, key, sweepline_point): 
    #    se o noh tem subarvore esquerda :min(subarvore esquerda)
    #                       cc se sou filho direito, meu pai eh antecessor
    #                       cc nao tenho antecessor
        node = self.root
        node_dad = None
        
        while (node != None):

            cmp = self.compare_to(sweepline_point, node.key)

            if(cmp > 0):
                node_dad = node
                node = node.right
            elif(cmp < 0 or (cmp == 0 and key != node.key)):
                node_dad = node
                node = node.left
            else:
                break

        if (node.left != None): 
            return self.max_aux(node.left)
        else:
            if (node_dad != None):
                if(node_dad.right != None and node_dad.right.key == key):
                    return node_dad
        return False

    def get_sucessor(self, key, sweepline_point): 
    #    se o noh tem subarvore direita :max(subarvore direita)
    #                       cc se sou filho esquerdo, meu pai eh sucessor
    #                       cc nao tenho sucessor
        node = self.root
        node_dad = None

        while (node != None):

            cmp = self.compare_to(sweepline_point, node.key)
            if(cmp > 0):
                node_dad = node
                node = node.right
            elif(cmp < 0 or (cmp == 0 and key != node.key)):
                node_dad = node
                node = node.left
            else:
                break

        if (node.right != None):
            return self.min_aux(node.right)
        else:
            if (node_dad != None):
                if(node_dad.left != None and node_dad.left.key == key):
                    return node_dad
        return False


    def remove(self, segment, sweepline_point):
        if (self.contains(segment, sweepline_point)):
            #print("There is a point, we should remove it!")
            self.root = self.remove_aux(self.root, segment, sweepline_point)

    #Assuming there aren`t two equal segments  
    def remove_aux(self, node, segment, sweepline_point):
        
        cmp = self.compare_to(sweepline_point, node.key)
        
        if (cmp < 0 or (cmp == 0 and segment != node.key)): 
            node.left = self.remove_aux(node.left, segment, sweepline_point)
        elif (cmp > 0): node.right = self.remove_aux(node.right, segment, sweepline_point)
        else:
            if (node.left == None):
                return node.right
    
            elif (node.right == None):
                return node.left
    
            else:
                p = self.Node(node.key, node.height, node.size, node.right, node.left)
                node = self.min_aux(p.right)
                node.right = self.remove_min_aux(p.right)
                node.left = p.left  
        
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
    
    def max_aux(self, node):
        if(node.right == None):
            return node
        return self.max_aux(node.right)

    def imprime(self):
        self.imprime_aux(self.root)
    
    def imprime_aux(self, node):
        if (node == None):
            return
        self.imprime_aux(node.left)
        self.imprime_seg(node.key)
        self.imprime_aux(node.right)

    def imprime_seg(self, s):
        segment = 'init ' + str([s.init.x, s.init.y]) + ' to ' + str([s.to.x, s.to.y]) 
        print(segment)
