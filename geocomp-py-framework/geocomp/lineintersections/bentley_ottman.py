from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp.common import point
from geocomp import config
from geocomp.lineintersections import PointBST as PBST
from geocomp.lineintersections import SegmentBST as SBST 

sleep_time = 2.0

def Bentley_ottman (l):
    segments_list, points_list = filter_segments_and_points(l) #s is the segments list and p is the points list
    
    intersections = []
    for s in segments_list:
        s.plot()

    event_queue = PBST.PointBST()
    for p in points_list:
        event_queue.insert(p[0], [segments_list[p[1]]])

    segment_tree = SBST.SegmentBST()
    while(not event_queue.isEmpty()):
        p = event_queue.removeMinKey()

        if (p.segment[0].init == p.key): #p eh ponta esquerda
            p.key.hilight(color = 'blue')
            control.sleep(sleep_time)
            segment_tree.insert(p.segment[0], p.key)

            pred = segment_tree.get_predecessor(p.segment[0], p.key)
            succ = segment_tree.get_sucessor(p.segment[0], p.key)

            if (not pred and not succ):
                p.key.hilight('red')
                continue
            
            if (pred): pred.key.hilight(color_line = 'magenta')
            if (succ): succ.key.hilight(color_line = 'magenta')
            control.sleep(sleep_time)

            if (pred and prim.intersect(pred.key.init, pred.key.to, p.segment[0].init, p.segment[0].to)):
                pred.key.hilight(color_line = 'yellow')
                p.segment[0].hilight(color_line = 'yellow')
                control.sleep(sleep_time)
                p.segment[0].plot()
                pred.key.plot()      
                intersections.append((pred.key, p.segment[0]))
                x,y = get_intersection(pred.key, p.segment[0])
                event_queue.insert(point.Point(x, y), [pred.key, p.segment[0]])
               
            if (succ and prim.intersect(succ.key.init, succ.key.to, p.segment[0].init, p.segment[0].to)):
                succ.key.hilight(color_line = 'yellow')
                p.segment[0].hilight(color_line = 'yellow')
                control.sleep(sleep_time)
                p.segment[0].plot()
                succ.key.plot()
                intersections.append((succ.key, p.segment[0]))
                x,y = get_intersection(succ.key, p.segment[0])
                event_queue.insert(point.Point(x, y), [p.segment[0], succ.key])

            if (pred): pred.key.plot()
            if (succ): succ.key.plot()
            p.segment[0].init.hilight('red')

        elif (p.segment[0].to == p.key): #p eh ponta direita
            p.segment[0].to.hilight(color = 'blue')
            control.sleep(sleep_time)
            print("arvore")
            segment_tree.imprime()
            pred = segment_tree.get_predecessor(p.segment[0], p.key)
            succ = segment_tree.get_sucessor(p.segment[0], p.key)
            
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


            print("vou remover ponta direita")
            print(p.segment[0])
            segment_tree.imprime()
            segment_tree.remove(p.segment[0], p.key)
            print("removi")
            segment_tree.imprime()


            if(not pred or not succ): 
                p.key.hilight('red')
                continue
            
            pred.key.hilight(color_line = 'magenta')
            succ.key.hilight(color_line = 'magenta')
            control.sleep(sleep_time)
            
            if (prim.intersect(pred.key.init, pred.key.to, succ.key.init, succ.key.to)):
                succ.key.hilight(color_line = 'yellow')
                pred.key.hilight(color_line = 'yellow')
                control.sleep(sleep_time)
                pred.key.plot()
                succ.key.plot()
                intersections.append((pred.key, succ.key))
                x,y = get_intersection(pred.key, succ.key)
                event_queue.insert(point.Point(x, y), [pred.key, succ.key])
            
            pred.key.plot()
            succ.key.plot()
            p.segment[0].to.hilight('red')
        
        else: # ponto de intersecao
            p.key.plot()
            p.key.hilight('blue')
            control.sleep(sleep_time)
            print("arvore antes do pred succ inversao")
            segment_tree.imprime()
            print('p.segment[0]: (' + str(p.segment[0].init.x) + ', ' + str(p.segment[0].init.y) + ')')
            print('p.segment[1]: (' + str(p.segment[1].init.x) + ', ' + str(p.segment[1].init.y) + ')')
            
            pred = segment_tree.get_predecessor(p.segment[0], p.key)
            succ = segment_tree.get_sucessor(p.segment[1], p.key)

            segment_tree.remove(p.segment[0], p.key)
            segment_tree.remove(p.segment[1], p.key)
            print("arvore depois de remover na inversao")
            segment_tree.imprime()
            
            segment_tree.insert(p.segment[0], p.key)
            segment_tree.insert(p.segment[1], p.key)
            print("arvore depois da insercao na inversao")
            segment_tree.imprime()

            if (pred): pred.key.hilight(color_line = 'magenta')
            if (succ): succ.key.hilight(color_line = 'magenta')
            control.sleep(sleep_time)


            if(pred and prim.intersect(pred.init, pred.to, p.segment[1].init, p.segment[1].to)):
                pred.key.hilight(color_line = 'yellow')
                p.segment[1].hilight(color_line = 'yellow')
                control.sleep(sleep_time)
                pred.key.plot()
                p.segment[1].key.plot()
                intersections.append((pred.key, p.segment[1].key))
                x,y = get_intersection(pred.key, p.segment[1].key)
                event_queue.insert(point.Point(x, y), [pred.key, p.segment[1].key])
            

            if(succ and prim.intersect(succ.init, succ.to, p.segment[0].init, p.segment[0].to)):
                succ.key.hilight(color_line = 'yellow')
                p.segment[0].hilight(color_line = 'yellow')
                control.sleep(sleep_time)
                segment[0].key.plot()
                succ.key.plot()
                intersections.append((pred.key, p.segment[0].key))
                x,y = get_intersection(pred.key, p.segment[0].key)
                event_queue.insert(point.Point(x, y), [p.segment[0].key, succ.key])

            p.key.hilight('red')
            pred.key.plot()
            succ.key.plot()


def filter_segments_and_points (l):
    segments = []
    points = []
    seg_index = 0
    
    for i in range (0, len(l) - 1, 2):
        if (l[i].x > l[i + 1].x):
            init, to = l[i+1], l[i]
        else:
            init, to = l[i], l[i+1]

        segments.append(segment.Segment(init, to))
        points.append([init, seg_index])
        points.append([to, seg_index])
        seg_index += 1
    return segments, points


def get_intersection(r, s):
    # quando a reta estah na forma 'y = ax + b' o coef a eh delta

    delta_r = (r.init.y - r.to.y)/(r.init.x - r.to.x)
    delta_s = (s.init.y - s.to.y)/(s.init.x - s.to.x)

    b_r = -(delta_r * r.init.x) + r.init.y
    b_s = -(delta_s * s.init.x) + s.init.y

    x = -(b_r - b_s)/(delta_r - delta_s)
    y = delta_r * (x - r.init.x) + r.init.y

    return (x, y)


