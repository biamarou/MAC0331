#!/usr/bin/env python
"""Modulo para leitura de um arquivo de dados"""

from geocomp.common.point   import Point
from geocomp.common.polygon import Polygon
from geocomp.common.segment import Segment

""" 

* Função que le pontos, vértices e segmentos de um arquivo, ignorando
  linhas que começam por #

Essa funão lê os seguintes objetos

 * Ponto: duas coordenadas separadas por espaço em uma linha

 * Segmento: 4 coordenadas separadas por espaço em uma linha

 * uma série de linhas, delimitadas por uma linha com '[' no começo e
   uma com ']' no final, e os pontos do polígono em ordem
   anti-horário, sendo cada linha as duas coordenadas separadas por
   espaços.

Note que espera-se que os objetos retornados tenham a função 'plot'


"""
def read(filename):
    with open(filename) as file:
        i = 0
        vertices = []
        data = []
        expecting_polygon = False
        for line in file:
            i += 1
            line = line.split()
            if len(line) == 0 or line[0] == "#":
                continue
            if line[0] == "[":
                expecting_polygon = True
            elif line[0] == "]":
                expecting_polygon = False
                data.append(Polygon(vertices))
                vertices = []
            elif len(line) == 4:
                data.append(
                    Segment(
                        Point(float(line[0]), float(line[1])),
                        Point(float(line[2]), float(line[3]))
                    )
                )
            elif len(line) == 2:
                if expecting_polygon:
                    vertices.append(Point(float(line[0]), float(line[1])))
                else:
                    data.append(Point(float(line[0]), float(line[1])))
            else:
                raise ValueError(
                    "Invalid input from file: {}: line: {}: {}".format(filename, i, line))
        return data

# if __name__ == '__main__':
#     import sys
#
#     for i in sys.argv[1:]:
#         print((i,':'))
#         lista = read_points (i)
#         print(('  ',repr(len(lista)), 'pontos:'))
#         for p in lista:
#             print(p)
