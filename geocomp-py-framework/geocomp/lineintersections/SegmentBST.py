from geocomp.common import segment

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
    
    def insert (self, segment):
        if (self.root == NULL):
            self.root = Node(segment, 0, 1, NULL, NULL)    
        else:
            self.root = self.insert(self.root, segment)
    
    def get_y_coord (self, l, r, x):
        return ((r.y - l.y)/(r.x - l.x)) * (x - (l.x)) + l.y

    def compare_to (self, s, p):
        y = get_y_coord(s.init, s.to, p.x)
        if (y > p.y):
            return 1
        elif (y <= p.y):
            return -1
        return 0

    # Assuming there aren't two equal segments
    def insert (self, node, segment):
        if (node == NULL):
            return Node(segment, 0, 1, NULL, NULL)
        cmp = self.compare_to(segment, node.key.init)
        if (cmp < 0):
            node.left = self.insert(node.left, segment)
        elif (cmp > 0):
            node.right = self.insert(node.right, segment)

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

    def contains(self, segment):
        if (segment == NULL) return False
        return self.contains(self.root, segment)

    def contains(self, node, segment):
        if (node == NULL):
            return False
        cmp = self.compare_to(segment, node.key)
        if (cmp < 0):
            node.left = self.contains(node.left, segment)
        elif (cmp > 0):
            node.right = self.contains(node.right, segment)
        else:
             return True

    def get_predecessor(self, key, remove): 
    #    se o noh tem subarvore direita :min(subarvore direita)
    #                       cc se sou filho esquerdo, meu pai eh antecessor
    #                       cc nao tenho antecessor
        node_dad = self.root
        p = key.init
            
        if (remove):
            p = node.key.to

        if (node_dad == NULL): return False

        while (node_dad != NULL):
            if(self.compare_to(node_dad.key, p) > 0):
                if (node_dad.left.key == key):
                    break
                node_dad = node_dad.left
            else:
                if (node_dad.right.key == key):
                    break
                node_dad = node_dad.right

        if (node_dad == NULL): return False

        #vale que node_dad eh o pai e node_dad.left ou right eh o node
        if(node_dad.left.key == key)
            node = node_dad.left
        else:
            node = node_dad.right

        if (node.right != NULL):
            node_min = node.right
            while (node_min.left != NULL):
                node_min = node.left
            return node_min

        else:
            if(node_dad.left == node):
                return node_dad
        return False

    def get_sucessor(self, node, remove): 
    #    se o noh tem subarvore esquerda :max(subarvore esquerda)
    #                       cc se sou filho direito, meu pai eh sucessor
    #                       cc nao tenho sucessor
        node_dad = self.root
        p = key.init
            
        if (remove):
            p = node.key.to

        if (node_dad == NULL): return False

        while (node_dad != NULL):
            if(self.compare_to(node_dad.key, p) > 0):
                if (node_dad.left.key == key):
                    break
                node_dad = node_dad.left
            else:
                if (node_dad.right.key == key):
                    break
                node_dad = node_dad.right

        if (node_dad == NULL): return False

        #vale que node_dad eh o pai e node_dad.left ou right eh o node
        if(node_dad.left.key == key)
            node = node_dad.left
        else:
            node = node_dad.right

        if (node.left != NULL):
            node_max = node.left
            while (node_max.right != NULL):
                node_max = node.right
            return node_max

        else:
            if(node_dad.right == node):
                return node_dad
        return False


    def remove(self, segment):
        if (self.contains(segment)):
            self.root = self.remove(self.root, segment)

    #Assuming there aren`t two equal segments  
    def remove(self, node, segment):
        cmp = self.compare_to(segment, node.key.init)
        if (cmp < 0) node.left = self.remove(node.left, segment)
        elif (cmp > 0) node.right = self.remove(node.right, segment)
        
        node.size = 1 + self.size(node.left) + self.size(node.right)
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        return balance(node)