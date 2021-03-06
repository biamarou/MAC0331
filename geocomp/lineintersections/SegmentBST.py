from geocomp.common import segment
from geocomp.common import prim

class SegmentBST:
    
    class Node:
        def __init__(self, k, h, s, r, l):
            self.key = k #key is a segment
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

    def compare_to (self, p, s):
        #devolve 1 se p está à esquerda de s.
        left_test = prim.float_left(s.init, s.to, p)
        left_on_test = prim.float_left_on(s.init, s.to, p)

        if (left_on_test): return 0
        elif (left_test): return 1
        else: return -1

    def insert (self, segment, sweepline_point):
        if (self.root == None):
            self.root = self.Node(segment, 0, 1, None, None)    
        else:
            self.root = self.insert_aux(self.root, segment, sweepline_point)

    def insert_aux (self, node, segment, sweepline_point):
        if (node == None):
            return self.Node(segment, 0, 1, None, None)
        cmp = self.compare_to(sweepline_point, node.key)
        if (cmp < 0):
            node.left = self.insert_aux(node.left, segment, sweepline_point)
        elif (cmp > 0):
            node.right = self.insert_aux(node.right, segment, sweepline_point)

        else:
            if (node.key.init == segment.to):
                    cmp = -self.compare_to(segment.init, node.key)
            elif(node.key.to == segment.to):
                cmp = self.compare_to(segment.init, node.key)
            else:
                cmp = self.compare_to(segment.to, node.key)

            if (cmp < 0):
                node.left = self.insert_aux(node.left, segment, sweepline_point)
            else: 
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

    def search_node(self, node_dad, node, key, sweepline_point, last_turn_left, last_turn_right, remove = False):
        
        if(node == None): return None
        
        cmp = self.compare_to(sweepline_point, node.key)
        print('search_node: cmp = ' + str(cmp))
        if (cmp < 0):
            return self.search_node(node, node.left, key, sweepline_point, node, last_turn_right, remove)
        elif (cmp > 0):
            return self.search_node(node, node.right, key, sweepline_point, last_turn_left, node, remove)
        else:
            if (node.key == key): 
                print('search_node: encontrei o nó')
                return (node_dad, node, last_turn_left, last_turn_right)
            else:
                print('search_node: cmp deu igual, mas node.key!=key. Vou calcular um novo cmp.')
                if (node.key.init == key.to):
                    cmp = -self.compare_to(key.init, node.key)
                elif(node.key.to == key.to):
                    cmp = self.compare_to(key.init, node.key)
                else:
                    cmp = self.compare_to(key.to, node.key)
                    if(remove and node.key.init != key.init and node.key.init.x != node.key.to.x and key.init.x !=
                            key.to.x):
                        cmp = -cmp
                print('search_node: meu novo cmp é: ' + str(cmp))
                
                if (cmp < 0):
                    return self.search_node(node, node.left, key, sweepline_point, node, last_turn_right, remove)
                else: 
                    return self.search_node(node, node.right, key, sweepline_point, last_turn_left, node, remove)



    def get_predecessor(self, key, sweepline_point): 
        "se o nó tem subarvore esquerda: max(subarvore esquerda)\
         cc se sou filho direito, meu pai é  antecessor\
         cc não tenho antecessor"
        print('Estou na get_predecessor')

        search_list = self.search_node(None, self.root, key, sweepline_point, None, None)
        if(search_list == None):
            print("Não encontrei o segmento no get_predecessor")
            return False
        node = search_list[1]
        last_turn_right = search_list[3]

        if (node.left != None): 
            print("Chamei max_aux no get_predecessor")
            return self.max_aux(node.left)
        
        elif(last_turn_right != None):
            print("Devolvi last_turn_right no get_predecessor")
            return last_turn_right
        return False

    def get_sucessor(self, key, sweepline_point): 
        "se o nó tem subarvore direita: min(subarvore direita)\
        cc se sou filho esquerdo, meu pai é sucessor\
        cc não tenho sucessor"
        print('Estou na get_sucessor')
        
        search_list = self.search_node(None, self.root, key, sweepline_point, None, None)
        if(search_list == None):
            print("Não encontrei o segmento no get_sucessor")
            return False

        node = search_list[1]
        last_turn_left = search_list[2]

        if (node.right != None):
            print("Chamei min_aux no get_sucessor")
            return self.min_aux(node.right)
    
        elif (last_turn_left != None):
            print("Devolvi o last_turn_left no get_sucessor")
            return last_turn_left
        return False

    def remove(self, segment, sweepline_point):
        if (self.search_node(None, self.root, segment, sweepline_point, None, None, True)):
            self.root = self.remove_aux(self.root, segment, sweepline_point)
        else:
            print("Não encontrei o segmento no search node")
            print(segment)
            print(self.search_node(None, self.root, segment, sweepline_point, None, None, True))
 
    def remove_aux(self, node, segment, sweepline_point):
        
        cmp = self.compare_to(sweepline_point, node.key)
        
        if (cmp < 0): node.left = self.remove_aux(node.left, segment, sweepline_point)
        elif (cmp > 0): node.right = self.remove_aux(node.right, segment, sweepline_point)
        elif(node.key != segment):
            if (node.key.init == segment.to):
                cmp = -self.compare_to(segment.init, node.key)
            elif(node.key.to == segment.to):
                cmp = self.compare_to(segment.init, node.key)
            else:
                cmp = self.compare_to(segment.to, node.key)
                if (node.key.init != segment.init and node.key.init.x != node.key.to.x and segment.init.x != segment.to.x):
                    cmp = -cmp

            if (cmp < 0):
                node.left = self.remove_aux(node.left, segment, sweepline_point)
            elif(cmp > 0): 
                node.right = self.remove_aux(node.right, segment, sweepline_point)
            else:
                print ("cmp deu igual no remove, mas node.key!=segment")
        else:
            print("Encontrei o segmento no remove")
            print(node.key)
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
        if (self.root == None): return
        print_root = 'init: ' + str([self.root.key.init.x, self.root.key.init.y]) + ', to: ' + str([self.root.key.to.x,
            self.root.key.to.y]) 
        print("A raíz é: " + print_root )
        self.imprime_aux(self.root)
        
    def imprime_aux(self, node):
        if (node == None):
            return
        self.imprime_aux(node.left)
        self.imprime_seg(node.key)
        self.imprime_aux(node.right)

    def imprime_seg(self, s):
        segment = 'init: ' + str([s.init.x, s.init.y]) + ', to: ' + str([s.to.x, s.to.y]) 
        print(segment)
