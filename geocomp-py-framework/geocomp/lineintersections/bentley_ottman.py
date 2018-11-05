from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config
from geocomp.lineintersections import PointBST
from geocomp.lineintersections import SegmentBST


def Bentley_ottman (l):
    segments_list, points_list = filter_segments_and_points(l) #s is the segments list and p is the points list
    
    intersections = []
    for s in segments_list:
        s.plot()

    event_queue = PointBST()
    for p in points_list:
        event_queue.insert(p[0], segments_list[p[1]])

    segment_tree = SegmentBST()
    while(not event_queue.isEmpty()):
        p = event_queue.removeMinKey()
        if(p.segment.init == p.key): #p eh ponta esquerda
            segment_tree.insert(p.segment)
            pred = segment_tree.get_predecessor(p.segment, False) #mando False pois nao estou removendo o segmento
            succ = segment_tree.get_sucessor(p.segment, False)
            if(#intersectam)

        else: #p eh ponta direita
            pred = segment_tree.get_predecessor(p.segment, True)
            succ = segment_tree.get_sucessor(p.segment, True)
            segment_tree.remove(p.segment)
            if(#intersectam)
        #ESTAVAMOS AQUI !!!!

def filter_segments_and_points (l):
    segments = []
    points = []
    for i in range (0, len(l) - 1, 2):
        segments.append(segment.Segment(l[i], l[i + 1]))
        points.append((l[i], i))
        points.append((l[i + 1], i))

    return segments, points

