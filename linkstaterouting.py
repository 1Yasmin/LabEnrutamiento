import csv
import sys
import os
import time
from threading import Thread
import datetime
from copy import deepcopy
from diccionario import priorityDictionary

re_check_off_time = 1
off_time = 3
re_check_send_time = 1
broadcast_delay = 1
off_time_broadcast = 3
data = []
xmluser_name = "dia151378@alumchat.xyz"
seq_number = 0
seq_number_i = 0
no_of_neighbours = 0
graph = {}
graph_time_update = {}
broad_cast_msg = ""
check_last_time = {}


def connection_state_changed():
	global seq_number, broad_cast_msg
	temp = {}
	temp['data'] = [value for value in data if value[3] == True]
	temp['seq'] = seq_number
	temp['time'] = datetime.datetime.now()
	broad_cast_msg = "2?"+ xmluser_name + "?"+str(temp)
	seq_number = seq_number +1
	graph[xmluser_name] = temp

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
send_matrix = []
matrix_set = 0
nodes = []
distances = {}
unvisited = {}
previous = {}
visited = {}
interface = {}
path = []
start = 0
end = 0

def set_distances(send_matrix):
    global distances
    global nodes
    distances = {}
    nodes = []
    num_nodes = len(send_matrix)
    for i in xrange(num_nodes):
        tempdict = {}
        for j in xrange(num_nodes):
            if i!=j and send_matrix[i][j]!=-1:
                tempdict[j+1] = send_matrix[i][j]
        distances[i+1] = tempdict
        nodes.append(i+1)
def dijkstra2(start):

    global distances
    global nodes
    global unvisited
    global previous
    global visited
    global interface

    # set the values to none for initialization.
    
    unvisited = {node: None for node in nodes}
    previous = {node: None for node in nodes}
    interface = {node: None for node in nodes}
    visited = {node: None for node in nodes}

    current = int(start)
    currentDist = 0
    unvisited[current] = currentDist

    while True:
        for next, distance in distances[current].items():

            if next not in unvisited: continue
            
            newDist = currentDist + distance

            if not unvisited[next] or unvisited[next] > newDist:
                unvisited[next] = newDist
                previous[next] = current

                if not interface[current]:
                    interface[next] = next
                else:
                    interface[next] = interface[current]
                    
        visited[current] = currentDist
        del unvisited[current]
        
        done = 1
        for x in unvisited:
            if unvisited[x]:
                done = 0
                break
        if not unvisited or done:
            break

        elements = [node for node in unvisited.items() if node[1]]

        current, currentDist = sorted(elements, key = lambda x: x[1])[0]

def shortest_path(start, end):
    
    global path

    path = []
    dest = int(end)
    src = int(start)
    path.append(dest)

    while dest != src:
        path.append(previous[dest])
        dest = previous[dest]

    path.reverse()

def call_linkstaterouting():
    sendmessagetoss = input("Escribe la persona a la que deseas enviar un mensaje: ")
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