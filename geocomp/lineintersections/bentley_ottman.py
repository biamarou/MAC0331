from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp.common import point
from geocomp import config
from geocomp.lineintersections import PointBST as PBST
from geocomp.lineintersections import SegmentBST as SBST

import functools as tools

def which_point (point, segment):
    "Retorna 0 se point é ponta esquerda de segment,\
     2 se for ponta direita e 1 caso contrário"
    if (point == segment.init):
        return 0
    elif (point == segment.to):
        return 2
    return 1

def cmp_sort_insertion_segments (a, b):
    if(prim.left(b.init, b.to, a.to)):
        return 1
    else:
        return -1

def cmp_sort_remove_segments (a, b):
    if(prim.left(b.init, b.to, a.init)):
        return 1
    else:
        return -1

def cmp_sort_intersection_segments (a, b):
    if(prim.left(b.init, b.to, a.to)):
        return 1
    else:
        return -1

def insert_point_segment (event_queue, points, segments):
    "event_queue é uma PointBST, segments é uma lista de Segment e\
    points é uma lista de pares [p, i], onde p é um Point e i é\
    um índice de segments indicando que p é ponto extremo de segments[i].\
    Elementos com mesmo p são adjacentes na lista.\
    Filtra pontos repetidos e os insere na event_queue."
    i = 0
    j = 1
    size = len(points)
    while (i < size):
        insertion = []
        remove = []
        w = which_point(points[i][0], segments[points[i][1]])
        if (w == 0):
            insertion.append(segments[points[i][1]])
        elif (w == 2):
            remove.append(segments[points[i][1]])

        while (j < size and points[i][0] == points[j][0]):
            w = which_point(points[j][0], segments[points[j][1]])
            if (w == 0):
                insertion.append(segments[points[j][1]])
            elif (w == 2):
                remove.append(segments[points[j][1]])
            j += 1
        
        insertion.sort(key=tools.cmp_to_key(cmp_sort_insertion_segments))
        remove.sort(key=tools.cmp_to_key(cmp_sort_remove_segments))

        event_queue.insert(points[i][0], [insertion, [], remove])
        i = j
        j += 1

def Bentley_ottman (segments_list):
    points_list = filter_points(segments_list)
    intersection_points = []
    event_queue = PBST.PointBST()  
    segment_tree = SBST.SegmentBST()
    sweepline_id = None
    
    for s in segments_list:
        s.plot()

    insert_point_segment(event_queue, points_list, segments_list)

    while(not event_queue.isEmpty()):
        event_node = event_queue.removeMinKey()
        control.plot_delete(sweepline_id)
        sweepline_id = control.plot_vert_line(event_node.key.x, color='blue')
        print("~~~O ponto evento é: (" + str(event_node.key.x) + ", " +  str(event_node.key.y) + ")")
        print("Sua lista de inserções é: ")
        print(event_node.segment[0])
        print("Sua lista de interseções é: ")
        print(event_node.segment[1])
        print("Sua lista de remoções é: ")
        print(event_node.segment[2])

        if (len(event_node.segment[0]) + len(event_node.segment[1]) + len(event_node.segment[2]) > 1):
            print("Entrei no primeiro if")
            print("Vou imprimir a SegmentBST: ")
            segment_tree.imprime()

            intersection_points.append(event_node.key)
            for segment in event_node.segment[0]:
                segment.hilight(color_line="yellow")
            for segment in event_node.segment[1]:
                segment.hilight(color_line="yellow")
            for segment in event_node.segment[2]:
                segment.hilight(color_line="yellow") 
            for segment in event_node.segment[1]:
                segment_tree.remove(segment, event_node.key)
            for segment in event_node.segment[2]:
                segment_tree.remove(segment, event_node.key)
            for segment in event_node.segment[0]:
                segment_tree.insert(segment, event_node.key)
            for segment in event_node.segment[1]:
                segment_tree.insert(segment, event_node.key)
            
            print("Vou imprimir a SegmentBST: ")
            segment_tree.imprime()

            control.sleep()
            for segment in event_node.segment[0]:
                segment.plot()
            for segment in event_node.segment[1]:
                segment.plot()
            for segment in event_node.segment[2]:
                segment.plot() 

        if (len(event_node.segment[0]) + len(event_node.segment[1]) == 0):
            print("Entrei no segundo if")
            lower = event_node.segment[2][0]
            upper = event_node.segment[2][len(event_node.segment[2]) - 1]
            if(lower):
                print("O lower é: ")
                print(lower)
                print("O upper é: ")
                print(upper)
                lower.hilight(color_line="green")
                upper.hilight(color_line="green")
                control.sleep()
                print("Vou imprimir a SegmentBST: ")
                segment_tree.imprime()
                pred = segment_tree.get_predecessor(lower, event_node.key)
                succ = segment_tree.get_sucessor(upper, event_node.key)
                if (pred and succ):
                    pred.key.hilight(color_line="magenta")
                    succ.key.hilight(color_line="magenta")
                    find_new_event(pred.key, succ.key, event_node.key, event_queue)

                control.sleep()
                if(succ): succ.key.plot()
                if(pred): pred.key.plot()
                lower.plot()
                upper.plot()
            for segment in event_node.segment[2]:
                segment_tree.remove(segment, event_node.key)
        else:
            print("Entrei no else")
            if (len(event_node.segment[0]) == 1 and len(event_node.segment[0]) + len(event_node.segment[1]) + len(event_node.segment[2]) <= 1):
                print("Tenho um segmento para inserir")
                segment_tree.insert(event_node.segment[0][0], event_node.key)
            print("Vou imprimir a SegmentBST: ")
            segment_tree.imprime()

            lower = get_lower_segment(event_node.segment[0], event_node.segment[1])
            print("O lower é: ")
            print(lower)
            lower.hilight(color_line="green")
            pred = segment_tree.get_predecessor(lower, event_node.key)
            if (pred):
                pred.key.hilight(color_line="magenta")
                find_new_event(pred.key, lower, event_node.key, event_queue)
            
            control.sleep()
            if(pred): pred.key.plot() 
            lower.plot()

            upper = get_upper_segment(event_node.segment[0], event_node.segment[1])
            print("O upper é: ")
            print(upper)
            upper.hilight(color_line="green")
            succ = segment_tree.get_sucessor(upper, event_node.key)
            if (succ):
                succ.key.hilight(color_line="magenta")
                find_new_event(upper, succ.key, event_node.key, event_queue)
            
            control.sleep()
            if(succ): succ.key.plot()
            upper.plot()
            
            for segment in event_node.segment[2]:
                segment_tree.remove(segment, event_node.key)

    for point in intersection_points:
        point.plot("yellow")

def get_lower_segment(list1, list2):
    if(list1):
        lower = list1[0]
        for segment in list2:
            if (prim.left(segment.init, segment.to, lower.to)):
                lower = segment
        return lower
    return list2[0]

def get_upper_segment(list1, list2):
    if(list1):
        upper = list1[len(list1) - 1]
        for segment in list2:
            if (prim.left(upper.init, upper.to, segment.to)):
                upper = segment
        return upper
    return list2[len(list2) - 1]

def find_new_event(segment1, segment2, sweepline, event_queue):
    print("find_new_event: Recebi os seguintes argumentos: ")
    print(segment1)
    print(segment2)
    print(sweepline)

    if(not prim.intersect(segment1.init, segment1.to, segment2.init, segment2.to)):
        print("find_new_event: segment1 e segment2 não se intersectam")
        return

    print("find_new_event: segment1 e segment2 se intersectam")
    x,y = get_intersection(segment1, segment2)
    new_event = point.Point(x, y)

    if (new_event.x > sweepline.x or (new_event.x == sweepline.x and new_event.y > sweepline.y)):
        print("find_new_event: não vou ignorar a interseção")
        node_point = event_queue.contains(new_event)
        if (node_point):
            print("find_new_event: o ponto de interseção já existia na PointBST")
            node_point.segment[1].append(segment1)
            node_point.segment[1].append(segment2)
            node_point.segment[1].sort(key=tools.cmp_to_key(cmp_sort_intersection_segments))
        else:
            print("find_new_event: o ponto de interseção não existia na PointBST")
            if(prim.left(segment1.init, segment1.to, segment2.to)):
                new_segment_list = [segment1, segment2]
            else:
                new_segment_list = [segment2, segment1]
            event_queue.insert(new_event, [[], new_segment_list, []])
    else: print("find_new_event: Decidi ignorar a interseção")

def filter_points (segments):
    "Separa os pontos extremos dos segmentos e os ordena na lista points."
    points = []
    for i in range (len(segments)):
        
        if (segments[i].init.x > segments[i].to.x):
            segments[i].init, segments[i].to = segments[i].to, segments[i].init
        elif (segments[i].init.x == segments[i].to.x):
            if (segments[i].init.y > segments[i].to.y):
                segments[i].init, segments[i].to = segments[i].to, segments[i].init

        points.append([segments[i].init, i])
        points.append([segments[i].to, i])
    points.sort(key=tools.cmp_to_key(cmp_sort_point))
    print("Points: ")
    print(points)
    return points

def cmp_sort_point (a, b):
    "Comparação para pontos evento"
    if (a[0].x > b[0].x): return 1
    elif (a[0].x < b[0].x): return -1
    elif (a[0].y > b[0].y): return 1
    elif (a[0].y < b[0].y): return -1
    else: return 0

def get_intersection(r, s):
    "Encontra o ponto de interseção entre as retas r e s"

    if (r.init == s.init or r.init == s.to): #interseção não-própria
        return (r.init.x, r.init.y)
    elif (r.to == s.to or r.to == s.init): #interseção não-própria
        return (r.to.x, r.to.y)

    elif (r.init.x == r.to.x): #r é vertical
        #y = ((y1-y0)/(x1-x0))*(x-x0) + y0
        y_intercept = ((s.to.y-s.init.y)/(s.to.x-s.init.x))*(r.init.x - s.init.x) + s.init.y 
        if (r.init.y <= y_intercept <= r.to.y):
            return (r.to.x, y_intercept)
    elif (s.init.x == s.to.x): #s é vertical
        y_intercept = ((r.to.y-r.init.y)/(r.to.x-r.init.x))*(s.init.x - r.init.x) + r.init.y 
        if (s.init.y <= y_intercept <= s.to.y):
            return (s.to.x, y_intercept)

    #interseção própria não-degenerada
    delta_r = (r.init.y - r.to.y)/(r.init.x - r.to.x)
    delta_s = (s.init.y - s.to.y)/(s.init.x - s.to.x)

    b_r = -(delta_r * r.init.x) + r.init.y
    b_s = -(delta_s * s.init.x) + s.init.y

    x = -(b_r - b_s)/(delta_r - delta_s)
    y = delta_r * (x - r.init.x) + r.init.y

    return (x, y)

def insertion_event(event_point, segment, segment_tree, event_queue):
    print("O ponto evento é ponta esquerda")
    event_point.hilight(color = 'blue')
    control.sleep()
    print("Vou imprimir a SegmentBST: ")
    segment_tree.imprime()
    print("Vou inserir o ponto evento na SegmentBST")
    segment_tree.insert(segment, event_point)
    print("Vou imprimir a SegmentBST após a inserção: ")
    segment_tree.imprime()
    print("Vou procurar o pred do ponto evento")
    pred = segment_tree.get_predecessor(segment, event_point)

    print("Vou procurar o succ do ponto evento")
    succ = segment_tree.get_sucessor(segment, event_point)

    if (not pred and not succ):
        print("Não encontrei pred nem succ")
        event_point.hilight('red')
        return
            
    if (pred):
        print("O pred é: [("+str(pred.key.init.x)+","+str(pred.key.init.y)+"), ("+str(pred.key.to.x)+","+ str(pred.key.to.y)+")]")
        print("Vou pintar o pred")
        pred.key.hilight(color_line = 'magenta')
    else:
        print("Não encontrei pred")

    if (succ): 
        print("O succ é: [("+str(succ.key.init.x)+","+str(succ.key.init.y)+"), ("+str(succ.key.to.x)+","+ str(succ.key.to.y)+")]")
        print("Vou pintar o succ")
        succ.key.hilight(color_line = 'magenta')
    else: 
        print("Não encontrei succ")
        control.sleep()

    if (pred and prim.intersect(pred.key.init, pred.key.to, segment.init, segment.to)):
        print("Encontrei interseção com o pred")
        add_intersection(pred.key, segment)
                    
    if (succ and prim.intersect(succ.key.init, succ.key.to, segment.init, segment.to)):
        print("Encontrei interseção com o succ")
        add_intersection(succ.key, segment)
                   
    segment.plot() 
    if (pred): pred.key.plot()
    if (succ): succ.key.plot()
    segment.init.hilight('red')


def remove_event(event_point, segment, segment_tree, event_queue):
    print("O ponto evento é ponta direita")
    segment.to.hilight(color = 'blue')
    control.sleep()
    print("Vou imprimir a SegmentBST: ")
    segment_tree.imprime()

    print("Vou procurar o pred")
    pred = segment_tree.get_predecessor(segment, p.key)
    print("Vou procurar o succ")
    succ = segment_tree.get_sucessor(segment, p.key)
            
    if(pred):
        print("O pred é: [("+str(pred.key.init.x)+","+str(pred.key.init.y)+"), ("+str(pred.key.to.x)+","+ str(pred.key.to.y)+")]")
    else:
        print("Não encontrei pred")
            
    if (succ):
        print("O succ é: [("+str(succ.key.init.x)+","+str(succ.key.init.y)+"), ("+str(succ.key.to.x)+","+ str(succ.key.to.y)+")]")
    else:
        print("Não encontrei succ")
                
        print("Vou imprimir a SegmentBST: ")
        segment_tree.imprime()
        print("Vou remover o segmento do qual sou ponta direita")
        print("O segmento é: [("+str(segment.init.x)+","+str(segment.init.y)+"), ("+str(segment.to.x)+","+ str(segment.to.y)+")]")

        segment_tree.remove(segment, event_point)
        print("Removi o segmento. Vou imprimir a SegmentBST: ")
        segment_tree.imprime()

        if(not pred or not succ):
            event_point.hilight('red')
            return
                
        print("Vou pintar o pred")
        pred.key.hilight(color_line = 'magenta')
        print("Vou pintar o succ")
        succ.key.hilight(color_line = 'magenta')
        control.sleep()
            
        if (prim.intersect(pred.key.init, pred.key.to, succ.key.init, succ.key.to)):
            check_new_event(pred.key, succ.key)
            
        pred.key.plot()
        succ.key.plot()
        segment.to.hilight('red')

def intersection_event():
    print("O ponto evento é ponto de interseção dos seguintes segmentos: ")
    print("O segment[0] é: [("+str(segment[1][0].init.x)+","+str(segment[1][0].init.y)+"),("+str(segment[1][0].to.x)+","+ str(segment[1][0].to.y)+")]")
    print("O segment[1] é: [("+str(segment[1][1].init.x)+","+str(segment[1][1].init.y)+"),("+str(segment[1][1].to.x)+","+str(segment[1][1].to.y)+")]")
    p.key.plot()
    p.key.hilight('blue')
    control.sleep()
    print("Vou imprimir a SegmentBST: ")
    segment_tree.imprime()

    print("Vou remover o segment[0]")
    segment_tree.remove(segment[1][0], p.key)
    print("Vou remover o segment[1]")
    segment_tree.remove(segment[1][1], p.key)
    print("Vou imprimir a SegmentBST após a remoção do segment[0] e segment[1]: ")
    segment_tree.imprime()

    print("Vou inserir o segment[1]")
    segment_tree.insert(segment[1][1], p.key)
    print("Vou inserir o segment[0]")
    segment_tree.insert(segment[1][0], p.key)
    print("Vou imprimir a SegmentBST após a inserção do segment[1] e segment[0]: ")
    segment_tree.imprime()

    print("Vou procurar o pred")
    pred = segment_tree.get_predecessor(segment[1][1], p.key)
    print("Vou procurar o succ")
    succ = segment_tree.get_sucessor(segment[1][0], p.key)

    if (pred):
        print("O pred é: [("+str(pred.key.init.x)+","+str(pred.key.init.y)+"),("+str(pred.key.to.x)+","+ str(pred.key.to.y)+")]")
        print("Vou pintar o segment[1] de verde e o pred de magenta")
        segment[1][1].hilight(color_line = 'green') 
        pred.key.hilight(color_line = 'magenta')
        control.sleep()
    else:
        print("Não encontrei pred")

    if(pred and prim.intersect(pred.key.init, pred.key.to, segment[1][1].init, segment[1][1].to)):
        print("Encontrei interseção entre pred e segment[1]")
        check_new_event (event_queue, pred.key, segment[1][1], p.key, intersections)

    if (pred): 
        pred.key.plot()
        segment[1][1].plot()
            
    if (succ): 
        print("O succ é: [("+str(succ.key.init.x)+","+str(succ.key.init.y)+"),("+str(succ.key.to.x)+","+ str(succ.key.to.y)+")]")
        print("Vou pintar o segment[0] de verde e o succ de magenta")
        segment[1][0].hilight('green') 
        succ.key.hilight(color_line = 'magenta')
        control.sleep()
    else:
        print("Não encontrei succ")

    if(succ and prim.intersect(succ.key.init, succ.key.to, segment[1][0].init, segment[1][0].to)):
        print("Encontrei interseção entre succ e segment[0]")
        check_new_event(event_queue, segment[1][0], succ.key, p.key, intersections)

    if (succ): 
        succ.key.plot()
        segment[1][0].plot()

    p.key.hilight('red')
