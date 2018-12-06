from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config

def Brute_force (l):
    s = filter_segments(l)
    intersections = []

    for i in range(len(s)):
        s[i].plot()

    for i in range(0, len(s) - 1):
        s[i].hilight(color_line = "blue")
        control.sleep()
        for j in range(i + 1, len(s)):
            s[j].hilight()
            control.sleep()
            if (prim.intersect(s[i].init, s[i].to, s[j].init, s[j].to)):
                # guarda os indices dos segmentos que se intersectam
                s[i].hilight(color_line = "yellow")
                s[j].hilight(color_line = "yellow")
                control.sleep()                
                intersections.append((i, j))
                s[i].hilight(color_line = "blue")
            s[j].plot()
        s[i].plot()

def filter_segments (l):
    segments = []

    for i in range (0, len(l) - 1, 2):
        segments.append(segment.Segment(l[i], l[i + 1]))
    return segments
