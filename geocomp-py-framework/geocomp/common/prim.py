#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Primitivas geometricas usadas nos algoritmos

Use o modulo geocomp.common.guiprim para que essas primitivas sejam
desenhadas na tela  medida que elas so usadas. Tambm  possvel
desenh-las de um jeito especfico para um determinado algoritmo.
Veja geocomp.convexhull.quickhull para um exemplo.
"""

# Numero de vezes que a funcao area2 foi chamada
num_area2 = 0
# Numero de vezes que a funcao dist2 foi chamada
num_dist = 0
# epsilon do erro
ERR = 1.0e-5
# Numero de vezes que a funcao intersecta foi chamada
num_intersect = 0

def cmpFloat(a, b):
	if (abs(a-b) < ERR):
		return 0
	elif (a + ERR > b):
		return 1
	return -1

def area2 (a, b, c):
	"Retorna duas vezes a rea do tringulo determinado por a, b, c"
	global num_area2
	num_area2 = num_area2 + 1
	area = (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)
	# Descobrir como aproximar pra zero no ponto de intersec
	return area

def left (a, b, c):
	"Verdadeiro se c est  esquerda do segmento orientado ab"
	if(cmpFloat(area2 (a, b, c), 0) == 1):
		return True
	return False

def left_on (a, b, c):
	"Verdadeiro se c est  esquerda ou sobre o segmento orientado ab"
	if(cmpFloat(area2 (a, b, c), 0) == 0):
		return True
	return False

def collinear (a, b, c):
	"Verdadeiro se a, b, c sao colineares"
	return area2 (a, b, c) == 0

def right (a, b, c):
	"Verdadeiro se c est  direita do segmento orientado ab"
	return not (left_on (a, b, c))

def right_on (a, b, c):
	"Verdadeiro se c est  direita ou sobre o segmento orientado ab"
	return not (left (a, b, c))

def dist2 (a, b):
	"Retorna o quadrado da distancia entre os pontos a e b"
	global num_dist
	num_dist = num_dist + 1
	dy = b.y - a.y
	dx = b.x - a.x

	return dy*dy + dx*dx

def get_count ():
	"Retorna o numero total de operacoes primitivas realizadas"
	return num_area2 + num_dist

def get_count_intersections ():
	"Retorna o numero total de chamadas do intersecta"
	return num_intersect

def reset_count ():
	"Zera os contadores de operacoes primitivas"
	global num_area2, num_dist
	num_area2 = 0
	num_dist = 0

def proper_intersection (a, b, c, d):
	"Verifica se ha intersecao entre os segmentos ab e cd em um ponto interno a ambos"
	if (collinear(a, b, c) or collinear(a, b, d) or collinear(c, d, a) or collinear(c, d, b)):
		return False
	return (bool(left(a, b, c)) ^ bool(left(a, b, d))) and (bool(left(c, d, a)) ^ bool(left(c, d, b)))

def between (a, b, c):
	"Verifica se o ponto c estah no segmento ab"
	if (not collinear(a, b, c)): return False
	if (a.x != b.x): 
		return a.x <= c.x <= b.x or b.x <= c.x <= a.x
	else:
		return a.y <= c.y <= b.y or b.y <= c.y <= a.y

def intersect (a, b, c, d):
	global num_intersect
	num_intersect = num_intersect + 1

	if (proper_intersection(a, b, c, d)): return True
	return between(a, b, c) or between(a, b, d) or between(c, d, a) or between(c, d, b)