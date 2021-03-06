import numpy as np

iterations = 0

# Read graph from file and return the HashMap of "startnodes counting" and a set of total nodes, and a list of all edges
def readGraph(file):
    graph_file = open(file, 'r')
    
    # map for counting the total contributions of a node to other nodes
    count_map = {}  
    
    # a list of edges [0, 1] means 0 contribute to 1
    edge_list = []
    
    #a set for counting all the nodes
    count_set = set()
    
    line1 = graph_file.readline()
    while line1:
        edge = line1.split()
        start_node = int(edge[0])
        end_node = int(edge[1])
        count_set.add(start_node)
        count_set.add(end_node)
        if start_node in count_map:
            tmp = count_map[start_node]
            count_map[start_node] = tmp +1
        else:
            count_map[start_node] = 1
        edge_list.append([start_node, end_node])
        line1 = graph_file.readline()
    return count_map, count_set, edge_list

# build the transition_matrix based on if the graph contains dangling nodes
def buildMatrix(file):
    read_graph = readGraph(file)
    count_map = read_graph[0]
    count_set = read_graph[1]
    edge_list = read_graph[2]

    #mapping the nodes number (3242, 2, 4, 51, 232, 45, etc) to range 0, 1, 2, 3.....n - 1 by using nodes_map
    nodes_list = list(count_set)
    nodes_list.sort();
    nodes_map = {}
    for i in range(len(nodes_list)):
        nodes_map[nodes_list[i]] = i
    
    # size of the set is the total number of nodes in the original graph 
    size = len(count_set)
    
    matrix = [[0 for i in range(size)] for j in range(size)]
    matrix_original = [[0 for i in range(size)] for j in range(size)]
    for p in edge_list:
        start_node = nodes_map[p[0]]
        end_node = nodes_map[p[1]]
        matrix[end_node][start_node] = matrix[end_node][start_node] + 1.0/count_map[p[0]]
        matrix_original[end_node][start_node]  = matrix_original[end_node][start_node]  + 1.0/count_map[p[0]]

    # check if dangling nodes in the graph, choose the easier way. So set all the column vector 1.0/matrix_length
    '''
    for i in range(size):
        if nodes_list[i] not in count_map:
            for j in range(size):
               matrix[j][i] = 1.0/len(matrix)
    '''
    graph = np.array(matrix)
    return graph, matrix_original 

#return the output transition matrix rank_output_matrixand the Converge rank vector pre_rank
def calculate(pre_rank, M, BETA):
    global iterations
    rank_output_matrix = M
    new_rank = pre_rank
    while True:        
        new_rank = BETA * M.dot(pre_rank) + (1 - BETA) * 1/M[0].size
        if check(pre_rank, new_rank):
            break
        iterations += 1
        pre_rank = new_rank
        rank_output_matrix = np.dot(M, rank_output_matrix)
    return (rank_output_matrix, pre_rank)

# check if iterations are done
def check(first, second):
    for i in range(len(first)):
        if first[i] - second[i] > 1e-6:
            return False
    return True

def main():
    s = input("Please enter the txt file path in your computer: ")
    BETA = float(input('Please enter the damping factor BETA: '))
    
    #build transition matrix and iterate
    res = buildMatrix(s)
    M = res[0]
    matrix_len = M[0].size
    pagerank = np.array([1.0/matrix_len for i in range(matrix_len)])
    result = calculate(np.array(pagerank), M, BETA)
    
    #show the result
    print("The transition matrix is\n", M)
    print("The Original Rank Vector is\n", pagerank)
    print("The Converged Rank Vector is\n", result[1])
    print("The number of iterations is\n", iterations)
    
    
if __name__ == '__main__':
    main()
