import numpy as np
BETA = 0.85
iterations = 0

# Read graph from file and return the HashMap of "startnodes counting" and a set of total nodes, and a list of all edges
def readGraph(file):
    graph_file = open(file, 'r')
    count_map = {}
    line1 = graph_file.readline()
    res = []
    count_set = set()
    while line1:
        edge = line1.split(" ")
        count_set.add(int(edge[0]))
        count_set.add(int(edge[1]))
        if int(edge[0]) in count_map:
            tmp = count_map[int(edge[0])]
            count_map[int(edge[0])] = tmp +1
        else:
            count_map[int(edge[0])] = 1
        res.append([int(edge[0]), int(edge[1])])
        line1 = graph_file.readline()
    return [count_map, count_set, res]

# build the M based on if the graph contains dangling nodes
def buildMatrix(file):
    read_graph = readGraph(file)
    count_map = read_graph[0]
    count_set = read_graph[1]
    res = read_graph[2]

    # size of the set is the total number of nodes in the original graph 
    size = len(count_set)
    matrix = [[0 for i in range(size)] for j in range(size)]
    
    for p in res:
        matrix[p[1]][p[0]] = matrix[p[1]][p[0]] + 1.0/count_map[p[0]]

    # check if dangling nodes in the graph, we choose the easier way. So we set all the column vector 1.0/matrix_length
    for i in range(len(matrix)):
        if i not in count_map:
            for j in range(len(matrix)):
               matrix[j][i] = 1.0/len(matrix)
               
    '''
    if flag:
        for i in range(size):
            for j in range(size):
                matrix[i][j] = (1 - BETA)*matrix[i][j]
                matrix[i][j] += (BETA)*1.0/size
    '''
    
    graph = np.array(matrix)
    return graph

#recursively solve the iterations
def calculate(second_graph, M):
    global iterations
    third_graph = (1 - BETA)*(M.dot(second_graph)) + BETA*second_graph
    iterations += 1
    if check(second_graph, third_graph):
        return third_graph
    print(third_graph)
    return calculate(third_graph, M)

# check if iterations is done
def check(first, second):
    for i in range(len(first)):
        if abs(first[i] - second[i]) > 1e-6:
            return False
    return True

def main():
    s = input("Please enter the txt file path in your computer such as: /Users/xxx.txt ")
    M = buildMatrix(s)
    len = M[0].size
    ori = [1.0/len for i in range(len)]
    res = calculate(np.array(ori), M)
    
    #Get the result
    print("The M is", M)
    print("The number of iteration is", iterations)
    print("The original Rank Vector is", ori)
    print("The Converged Rank Vector is", res)
    
    
if __name__ == '__main__':
    main()
