from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config


def filter_segments (l):
    segments = []

    for i in range (0, len(l) - 1, 2):
        segments.append(segment.Segment(l[i], l[i + 1]))
    return segments


def Brute_force (l):
    s = filter_segments(l)
    intersections = []

    for i in range(len(s)):
        s[i].plot()

    for i in range(0, len(s) - 1):
        for j in range(i + 1, len(s)):
            s[i].hilight(color_line = "yellow")
            s[j].hilight(color_line = "yellow")
            if (prim.intersect(s[i].init, s[i].to, s[j].init, s[j].to)):
                # guarda os indices dos segmentos que se intersectam
                s[i].hilight(color_line = "red")
                s[j].hilight(color_line = "red")
                control.sleep(10)                
                intersections.append((i, j))

            s[i].plot()
            s[j].plot()