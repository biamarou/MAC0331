from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp.common import point
from geocomp import config
from geocomp.lineintersections import PointBST as PBST
from geocomp.lineintersections import SegmentBST as SBST

import functools as tools

def which_point (point, segment):
    if (point == segment.init):
        return 0
    elif (point == segment.to):
        return 2
    return 1

def cmp_sort_event_point (a, b):
    if (a[0] < b[0]): return -1
    elif (a[0] > b[0]): return 1
    return 0

def insert_point_segment (event_queue, points, segments):
    i = 0
    j = 1
    size = len(points)
    while (i < size):
        w = which_point(points[i][0], segments[points[i][1]])
        points_by_segment = [[w, segments[points[i][1]]]]
        
        while (j < size and points[i][0] == points[j][0]):
            w = which_point(points[j][0], segments[points[j][1]])
            points_by_segment.append([w, segments[points[j][1]]])
            j += 1
        
        points_by_segment.sort(key=tools.cmp_to_key(cmp_sort_event_point))
        event_queue.insert(points[i][0], points_by_segment)
        i = j
        j += 1

def Bentley_ottman (segments_list):
    points_list = filter_points(segments_list) #s is the segments list and p is the points list
    
    intersections = []
    for s in segments_list:
        s.plot()

    event_queue = PBST.PointBST()  
    insert_point_segment(event_queue, points_list, segments_list)
    segment_tree = SBST.SegmentBST()
    
    while(not event_queue.isEmpty()):
        p = event_queue.removeMinKey()
        
        print(p.segment)
        for segment in p.segment:

            # a lista de segmentos de cada ponto eh formada por um par [w , s]
            # onde w eh um numero que indica ponta esquerda ou direita e s eh o segmento
            print(segment)
            if (segment[0] == 0): #p eh ponta esquerda
                p.key.hilight(color = 'blue')
                control.sleep()
                segment_tree.insert(segment[1], p.key)

                pred = segment_tree.get_predecessor(segment[1], p.key)
                succ = segment_tree.get_sucessor(segment[1], p.key)

                if (not pred and not succ):
                    p.key.hilight('red')
                    continue
            
                if (pred): pred.key.hilight(color_line = 'magenta')
                if (succ): succ.key.hilight(color_line = 'magenta')
                control.sleep()

                if (pred and prim.intersect(pred.key.init, pred.key.to, segment[1].init, segment[1].to)):
                    pred.key.hilight(color_line = 'yellow')
                    segment[1].hilight(color_line = 'yellow')
                    control.sleep()
                    segment[1].plot()
                    pred.key.plot()      
                    check_new_event (event_queue, pred.key, segment[1], p.key, intersections)
                    
                if (succ and prim.intersect(succ.key.init, succ.key.to, segment[1].init, segment[1].to)):
                    succ.key.hilight(color_line = 'yellow')
                    segment[1].hilight(color_line = 'yellow')
                    control.sleep()
                    segment[1].plot()
                    succ.key.plot()
                    check_new_event (event_queue, segment[1], succ.key, p.key, intersections)
                    
            
                if (pred): pred.key.plot()
                if (succ): succ.key.plot()
                segment[1].init.hilight('red')

            elif (segment[0] == 2): #p eh ponta direita
                segment[1].to.hilight(color = 'blue')
                control.sleep()
                print("arvore")
                segment_tree.imprime()
                pred = segment_tree.get_predecessor(segment[1], p.key)
                succ = segment_tree.get_sucessor(segment[1], p.key)
            
                #######################################
                print("pred")
                if(pred):
                    print([pred.key.init.x, pred.key.init.y])
                else:
                    print("null")
            
                print("succ")
                if (succ):
                    print([succ.key.init.x, succ.key.init.y])
                else:
                    print("null")
                #######################################

                print("vou remover ponta direita")
                print(segment[1])
                segment_tree.imprime()
                segment_tree.remove(segment[1], p.key)
                print("removi")
                segment_tree.imprime()

                if(not pred or not succ):
                    p.key.hilight('red')
                    continue
                
                pred.key.hilight(color_line = 'magenta')
                succ.key.hilight(color_line = 'magenta')
                control.sleep()
            
                if (prim.intersect(pred.key.init, pred.key.to, succ.key.init, succ.key.to)):
                    succ.key.hilight(color_line = 'yellow')
                    pred.key.hilight(color_line = 'yellow')
                    control.sleep()
                    pred.key.plot()
                    succ.key.plot()
                    check_new_event (event_queue, pred.key, succ.key, p.key, intersections)
            
                pred.key.plot()
                succ.key.plot()
                segment[1].to.hilight('red')

            ############################# falta adaptar
            else: # ponto de intersecao
                p.key.plot()
                p.key.hilight('blue')
                control.sleep()
                print("arvore antes do pred succ inversao")
                segment_tree.imprime()
                print('segment[0]: (' + str(segment[1][0].init.x) + ', ' + str(segment[1][0].init.y) + ')')
                print('segment[1]: (' + str(segment[1][1].init.x) + ', ' + str(segment[1][1].init.y) + ')')
            
                segment_tree.remove(segment[1][0], p.key)
                segment_tree.remove(segment[1][1], p.key)
                print("arvore depois de remover na inversao")
                segment_tree.imprime()

                segment_tree.insert(segment[1][1], p.key)
                segment_tree.insert(segment[1][0], p.key)
                print("arvore depois da insercao na inversao")
                segment_tree.imprime()

                pred = segment_tree.get_predecessor(segment[1][1], p.key)
                print("Pegando o succ:")
                succ = segment_tree.get_sucessor(segment[1][0], p.key)

                if (pred):
                    segment[1][1].hilight(color_line = 'green') 
                    pred.key.hilight(color_line = 'magenta')
                    control.sleep()


                if(pred and prim.intersect(pred.key.init, pred.key.to, segment[1][1].init, segment[1][1].to)):
                    pred.key.hilight(color_line = 'yellow')
                    segment[1][1].hilight(color_line = 'yellow')
                    control.sleep()
                    pred.key.plot()
                    segment[1][1].plot()
                    check_new_event (event_queue, pred.key, segment[1][1], p.key, intersections)

                if (pred): 
                    pred.key.plot()
                    segment[1][1].plot()
            
                if (succ): 
                    succ.key.hilight(color_line = 'magenta')
                    segment[1][0].hilight('green') 
                    control.sleep()

                if(succ and prim.intersect(succ.key.init, succ.key.to, segment[1][0].init, segment[1][0].to)):
                    succ.key.hilight(color_line = 'yellow')
                    segment[1][0].hilight(color_line = 'yellow')
                    control.sleep()
                    segment[1][0].plot()
                    succ.key.plot()
                    check_new_event (event_queue, segment[1][0], succ.key, p.key, intersections)

                if (succ): 
                    succ.key.plot()
                    segment[1][0].plot()

                p.key.hilight('red')
        
def check_new_event (event_queue, segment1, segment2, sweepline, intersections):
    
    x,y = get_intersection(segment1, segment2)
    new_event = point.Point(x, y)

    if (sweepline.x > new_event.x or new_event == sweepline):
        return
    else:
        intersections.append((segment1, segment2))
        node_point = event_queue.contains(new_event)

        if (node_point):
            node_point.segment.append([1, [segment1, segment2]])
            node_point.segment.sort(key=tools.cmp_to_key(cmp_sort_event_point))
        else:
            event_queue.insert(new_event, [[1, [segment1, segment2]]])


def filter_points (segments):
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
    return points

def cmp_sort_point (a, b):
    if (a[0].x > b[0].x): return 1
    elif (a[0].x < b[0].x): return -1
    elif (a[0].y > b[0].y): return 1
    elif (a[0].y < b[0].y): return -1
    else: return 0

def get_intersection_2(r, s):
    
    if (r.init == s.init or r.init == s.to):
        return (r.init.x, r.init.y)
    elif (r.to == s.to or r.to == s.init):
        return (r.to.x, r.to.y)
    
    # r = (a.x, a.y) (b.x, b.y)
    # s = (c.x, c.y) (d.x, d.y)
    ab = [r.to.x - r.init.x, r.to.y - r.init.y]
    ca = [r.init.x - s.init.x, r.init.y - s.init.y]
    cd = [s.to.x - s.init.x, s.to.y - s.init.y]
    ac = [s.init.x - r.init.x, s.init.y - r.init.y]

    y = prim.cross(ca, ab)[0]/prim.cross(cd, ab)[0]
    x = prim.cross(ac, cd)[0]/prim.cross(ab, cd)[0]

    return (x, y)

def get_intersection(r, s):
    # quando a reta estah na forma 'y = ax + b' o coef a eh delta

    if (r.init == s.init or r.init == s.to):
        return (r.init.x, r.init.y)
    elif (r.to == s.to or r.to == s.init):
        return (r.to.x, r.to.y)
    elif (r.init.x == r.to.x):
        y_intercept = ((s.to.y-s.init.y)/(s.to.x-s.init.x))*(r.init.x - s.init.x) + s.init.y 
        #y = ((y1-y0)/(x1-x0))*(x-x0) + y0
        if (r.init.y <= y_intercept <= r.to.y):
            return (r.to.x, y_intercept)
        else:
            print("EITA CARAI")
    elif (s.init.x == s.to.x):
        y_intercept = ((r.to.y-r.init.y)/(r.to.x-r.init.x))*(s.init.x - r.init.x) + r.init.y 
        if (s.init.y <= y_intercept <= s.to.y):
            return (s.to.x, y_intercept)
        else:
            print("EITA CARAI")

    delta_r = (r.init.y - r.to.y)/(r.init.x - r.to.x)
    delta_s = (s.init.y - s.to.y)/(s.init.x - s.to.x)

    b_r = -(delta_r * r.init.x) + r.init.y
    b_s = -(delta_s * s.init.x) + s.init.y

    x = -(b_r - b_s)/(delta_r - delta_s)
    y = delta_r * (x - r.init.x) + r.init.y

    return (x, y)
