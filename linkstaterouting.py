import csv
import sys
import os

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
def dijkstra(start):

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