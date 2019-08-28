import csv
import sys
import os
import time
from threading import Thread
import datetime
from copy import deepcopy
from diccionario import priorityDictionary

xmluser_name = "dia151378@alumchat.xyz"

start = 0
end = 0
def Dijkstra(G,start,end=None):
	D = {}	#distancia final
	P = {}	# predecedores
   
	Q = priorityDictionary()   
	Q[start] = 0
	for v in Q:
		D[v] = Q[v]
		if v == end: break
		for w in G[v]:
			vwLength = D[v] + G[v][w]
			if w in D:
				if vwLength < D[w]:
					pass
			elif w not in Q or vwLength < Q[w]:
				Q[w] = vwLength
				P[w] = v
	return (D,P)
def shortestPath(G,start,end):
	D,P = Dijkstra(G,start,end)
	Path = []
	while 1:
		Path.append(end)
		if end == start: break
		end = P[end]
	Path.reverse()
	return Path
#linkstaterouting
def call_linkstaterouting():
    graph = {}
    data = []
    path = []
  
    while True:
        try:
            localgraph = deepcopy(graph)
            G = {}
            for x in graph:
                G[x] = {}
                for y in localgraph[x]["data"]:
                    G[x][y[0]] = float(y[1])
                    for x in graph:
                        if x != xmluser_name:
                            path = shortestPath(G, xmluser_name, x)
                            cost = 0
                            for x in range(0, len(path)-1):
                                cost += G[path[x]][path[x+1]]
                                print(path[x], end="")
                                print(path[len(path)-1],end="")
                                print("%.1f" % cost)
        except Exception as e:
            print(e)
            pass
            time.sleep(2)