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

def cmp_sort_event_point (a, b):
    "Usado para comparar os códigos dos eventos, que\
     pertencem a {0, 1, 2}, onde 0 significa inserção,\
     1 significa interseção e 2 significa remoção.\
     Queremos tratá-los em ordem crescente de código."
    if (a[0] < b[0]): return -1
    elif (a[0] > b[0]): return 1
    return 0

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
    points_list = filter_points(segments_list)
    intersections = []
    event_queue = PBST.PointBST()  
    segment_tree = SBST.SegmentBST()
    sweepline_id = None
    
    
    for s in segments_list:
        s.plot()

    insert_point_segment(event_queue, points_list, segments_list)

    while(not event_queue.isEmpty()):
        p = event_queue.removeMinKey()
        control.plot_delete(sweepline_id)
        sweepline_id = control.plot_vert_line(p.key.x, color='blue')
        print('Removi mínimo da PointBST. A lista p.segment é:')
        print(p.segment)
        for segment in p.segment:
            # Um elemento de p.segment é da forma [e, l] onde e é
            # o código do evento e l é uma lista contendo um ou dois segmentos
            print("Tratarei o ponto evento a seguir: ")
            print(segment)
            if (segment[0] == 0): #Evento de inserção
                print("O ponto evento é ponta esquerda")
                p.key.hilight(color = 'blue')
                control.sleep()
                print("Vou imprimir a SegmentBST: ")
                segment_tree.imprime()
                print("Vou inserir o ponto evento na SegmentBST")
                segment_tree.insert(segment[1], p.key)
                print("Vou imprimir a SegmentBST após a inserção: ")
                segment_tree.imprime()
                print("Vou procurar o pred do ponto evento")
                pred = segment_tree.get_predecessor(segment[1], p.key)

                print("Vou procurar o succ do ponto evento")
                succ = segment_tree.get_sucessor(segment[1], p.key)

                if (not pred and not succ):
                    print("Não encontrei pred nem succ")
                    p.key.hilight('red')
                    continue
            
                if (pred):
                    print("O pred é: [("+pred.key.init.x+","+pred.key.init.y+"), ("+pred.key.to.x+","+
                            pred.key.to.y+")]")
                    print("Vou pintar o pred")
                    pred.key.hilight(color_line = 'magenta')
                else:
                    print("Não encontrei pred")

                if (succ): 
                    print("O succ é: [("+succ.key.init.x+","+succ.key.init.y+"), ("+succ.key.to.x+","+
                            succ.key.to.y+")]")
                    print("Vou pintar o succ")
                    succ.key.hilight(color_line = 'magenta')
                else: 
                    print("Não encontrei succ")
                control.sleep()

                if (pred and prim.intersect(pred.key.init, pred.key.to, segment[1].init, segment[1].to)):
                    print("Encontrei interseção com o pred")
                    pred.key.hilight(color_line = 'yellow')
                    segment[1].hilight(color_line = 'yellow')
                    control.sleep()
                    segment[1].plot()
                    pred.key.plot()      
                    check_new_event (event_queue, pred.key, segment[1], p.key, intersections)
                    
                if (succ and prim.intersect(succ.key.init, succ.key.to, segment[1].init, segment[1].to)):
                    print("Encontrei interseção com o succ")
                    succ.key.hilight(color_line = 'yellow')
                    segment[1].hilight(color_line = 'yellow')
                    control.sleep()
                    segment[1].plot()
                    succ.key.plot()
                    check_new_event (event_queue, segment[1], succ.key, p.key, intersections)
                    
            
                if (pred): pred.key.plot()
                if (succ): succ.key.plot()
                segment[1].init.hilight('red')

            elif (segment[0] == 2): #Evento de remoção
                print("O ponto evento é ponta direita")
                segment[1].to.hilight(color = 'blue')
                control.sleep()
                print("Vou imprimir a SegmentBST: ")
                segment_tree.imprime()

                print("Vou procurar o pred")
                pred = segment_tree.get_predecessor(segment[1], p.key)
                print("Vou procurar o succ")
                succ = segment_tree.get_sucessor(segment[1], p.key)
            
                if(pred):
                    print("O pred é: [("+pred.key.init.x+","+pred.key.init.y+"), ("+pred.key.to.x+","+
                            pred.key.to.y+")]")
                else:
                    print("Não encontrei pred")
            
                if (succ):
                    print("O succ é: [("+succ.key.init.x+","+succ.key.init.y+"), ("+succ.key.to.x+","+
                            succ.key.to.y+")]")
                else:
                    print("Não encontrei succ")
                
                print("Vou imprimir a SegmentBST: ")
                segment_tree.imprime()
                print("Vou remover o segmento do qual sou ponta direita")
                print("O segmento é: [("+segment[1].init.x+","+segment[1].init.y+"), ("+segment[1].to.x+","+
                            segment[1].to.y+")]")

                segment_tree.remove(segment[1], p.key)
                print("Removi o segmento. Vou imprimir a SegmentBST: ")
                segment_tree.imprime()

                if(not pred or not succ):
                    p.key.hilight('red')
                    continue
                
                print("Vou pintar o pred")
                pred.key.hilight(color_line = 'magenta')
                print("Vou pintar o succ")
                succ.key.hilight(color_line = 'magenta')
                control.sleep()
            
                if (prim.intersect(pred.key.init, pred.key.to, succ.key.init, succ.key.to)):
                    print("Encontrei interseção entre pred e succ")
                    succ.key.hilight(color_line = 'yellow')
                    pred.key.hilight(color_line = 'yellow')
                    control.sleep()
                    pred.key.plot()
                    succ.key.plot()
                    check_new_event (event_queue, pred.key, succ.key, p.key, intersections)
            
                pred.key.plot()
                succ.key.plot()
                segment[1].to.hilight('red')

            else: #Evento de interseção
                print("O ponto evento é ponto de interseção dos seguintes segmentos: ")
                print("O segment[0] é: [("+segment[1][0].init.x+","+segment[1][0].init.y+"), ("+segment[1][0].to.x+","+
                            segment[1][0].to.y+")]")
                print("O segment[1] é: [("+segment[1][1].init.x+","+segment[1][1].init.y+"), ("+segment[1][1].to.x+","+
                            segment[1][1].to.y+")]")
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
                    print("O pred é: [("+pred.key.init.x+","+pred.key.init.y+"),("+pred.key.to.x+","+ pred.key.to.y+")]")
                    print("Vou pintar o segment[1] de verde e o pred de magenta")
                    segment[1][1].hilight(color_line = 'green') 
                    pred.key.hilight(color_line = 'magenta')
                    control.sleep()
                else:
                    print("Não encontrei pred")

                if(pred and prim.intersect(pred.key.init, pred.key.to, segment[1][1].init, segment[1][1].to)):
                    print("Encontrei interseção entre pred e segment[1]")
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
                    print("O succ é: [("+succ.key.init.x+","+succ.key.init.y+"),("+succ.key.to.x+","+ succ.key.to.y+")]")
                    print("Vou pintar o segment[0] de verde e o succ de magenta")
                    segment[1][0].hilight('green') 
                    succ.key.hilight(color_line = 'magenta')
                    control.sleep()
                else:
                    print("Não encontrei succ")

                if(succ and prim.intersect(succ.key.init, succ.key.to, segment[1][0].init, segment[1][0].to)):
                    print("Encontrei interseção entre succ e segment[0]")
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
    "segment1 e segment2 se intersectam. Verifica se o ponto de interseção\
     já existe na PointBST. Se não existir, insere o ponto. Caso já exista,\
     atualiza o ponto com um evento de interseção."    
    x,y = get_intersection(segment1, segment2)
    new_event = point.Point(x, y)
    print("----------Chamada da check_new_event-------------")
    print("O ponto de interseção é: (" + x + "," + y + ")")
    if (sweepline.x > new_event.x or new_event == sweepline):
        print("Vou ignorar a interseção")
        return
    else:
        intersections.append((segment1, segment2))
        print("Vou checar se o ponto de interseção já está na PointBST")
        node_point = event_queue.contains(new_event)

        if (node_point):
            print("O ponto já existe na PointBST")
            node_point.segment.append([1, [segment1, segment2]])
            node_point.segment.sort(key=tools.cmp_to_key(cmp_sort_event_point))
        else:
            print("O ponto não existe na PointBST. Vou adicioná-lo")
            event_queue.insert(new_event, [[1, [segment1, segment2]]])
    print("-------------------------------------------------")

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
