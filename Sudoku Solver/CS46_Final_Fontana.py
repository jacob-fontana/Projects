
# coding: utf-8

# This project will create an algorithm that will solve a sudoku puzzle. Sudoku is a popular puzzle game, where players are given a partially filled n by n grid, and asked to fill in the rest of the values. The rules are as follows:
# 
# 1. Each cell in the grid can take on a value between 1 and n
# 2. A number can only occur once in each row
# 3. A number can only occur once in each column
# 4. A number can only occur once in each subgrid of the board
# 
# Sudoku boards can in theory be any size, and have arbitrary subgrid structures. However, in this case, we will focus on games where n is a square number, and each subgrid is also square, evenly spaced throughout the board, with dimensions that are the square root of the size of the board.
# 
# There are numerous algorithmic solutions of sudoku, ranging from brute force searching, to more elaborate stochastic methods. We will examine two algorithms, a greedy algorithm, that updates the board whenever it sees a possible move, and a deep searching algorithm, that updates values until a rule violation occurs, and then backtracks. We find that while the greedy algorithm is able to solve simple 9 by 9 sudokus, it fails on more difficult problems. However, the deep searching algorithm is always able to find a solution (provided one exists). 

# This first set of functions will translate a sudoku puzzle into a graph structure. Sudoku puzzles are specified by a size n, and an initial set of values. The puzzle boards are n by n grids, with each cell in the grid taking on a value between 1 and n. 
# 
# To translate this into a graph structure, we first generate a set of nodes in an array of array. We then make 3 different adjacency lists for each nodes, the nodes in that nodes column, row, and subgrid. These are then combined into a single adjacency list for each node.
# 
# Any number can only occur once in a given row, column, or grid of a sudoku board. By turning the cells of the board into nodes and the other cells in that cell's row, column, and grids into an adjacency list, the constraints of the game are represented in the adjacency list. No value that any node in the adjacency list takes on can be used for the node. This allows us to reconcieve of the problem as a graph coloring problem. We need to find a n-coloring of the board (where n is the size of the board). 

# In[94]:


import math

### generates array of array to represent cells on the grid, with each one being assigned to a node
def get_nodes(size):
    grid_size = math.sqrt(size)
    if grid_size.is_integer() == False:
        return('Not a Valid Grid')
    
    nodes = []
    count = 0
    for i in range(size):
        temp = []
        for j in range(size):
            temp.append(count)
            count = count + 1
        nodes.append(temp)
    return(nodes)
    

### finds the adjacency lists for each node as a result of being in the same column 
def get_col_adj(size):
    nodes = get_nodes(size)
    adj_col = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            temp = []
            for k in range(len(nodes)):
                if k != i:
                    temp.append(nodes[k][j])
            adj_col.append(temp)
    return(adj_col)
            
### finds the adjacency lists for each node as a result of being in the same row 
def get_row_adj(size):
    nodes = get_nodes(size)
    adj_row = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            temp = nodes[i][:]
            del temp[j]
            adj_row.append(temp)
            
            
    return(adj_row)

### finds the adjacency lists for each node as a result of being in the same miniture grid
def get_grid_adj(size):
    nodes = get_nodes(size)
    adj_grid = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            pos_i_low = int(i//(math.sqrt(size)))
            pos_j_low = int(j//(math.sqrt(size)))
            pos_i_upper = int(i//(math.sqrt(size)))+1
            pos_j_upper = int(j//(math.sqrt(size)))+1
            temp = []
            for k in range(pos_i_low*int(math.sqrt(size)),pos_i_upper*int(math.sqrt(size))):
                for l in range(pos_j_low*int(math.sqrt(size)),pos_j_upper*int(math.sqrt(size))):
                    if k != i or l != j:
                        temp.append(nodes[k][l])
            adj_grid.append(temp)
        
    return(adj_grid)
        

    
### combines the prior adjacency lists to generate a unique adjacency list for each node
def merge_adj(size):
    adj_row = get_row_adj(size)
    adj_col = get_col_adj(size)
    adj_grid = get_grid_adj(size)
    adj_list = []
    for i in range(len(adj_row)):
        temp_set = set(adj_row[i])
        temp_set.update(adj_col[i])
        temp_set.update(adj_grid[i])
        adj_list.append(list(temp_set))
    return(adj_list)
   
### helper function to flatten n dim arrays
def flatten(l):
    new = []
    for i in range(len(l)):
        new = new + l[i]
    return(new)

### generates the adjacency list and initializes entry already given 
# values is a list of ints, pos is a list of tuples specifying row and column
def setup_board(size,values,pos):
    board_values = []
    for i in range(size):
        board_values.append([None]*size)
    
    for i in range(len(values)):
        board_values[int(pos[i][0])][int(pos[i][1])] = values[i]
    
    board_values = flatten(board_values)
    
    adj_list = merge_adj(size)
    
    
    return(board_values,adj_list)

        
        
        
### Test Case
pos1 = [(0,0),(0,1),(0,4),(1,0),(1,3),(1,4),(1,5), (2,1),(2,2),(2,7),(3,0),(3,4),(3,8),(4,0),(4,3),(4,5),(4,8),(5,0),(5,4),(5,8), (6,1),(6,6),(6,7),(7,3),(7,4),(7,5),(7,8),(8,4),(8,7),(8,8)]
values1 = [5,3,7,6,1,9,5,9,8,6,8,6,3,4,8,3,1,7,2,6,6,2,8,4,1,9,5,8,7,9]


board1,adj1 = setup_board(9,values1,pos1)
print(board1)

values2 = [8,3,6,7,9,2,5,7,4,5,7,1,3,1,6,8,8,5,1,9,4]
pos2 = [(0,0),(1,2),(1,3),(2,1),(2,4),(2,6),(3,1),(3,5),(4,4),(4,5),(4,6),(5,3),(5,7),(6,2),(6,7),(6,8),(7,2),(7,3),(7,7),(8,1),(8,6)]
    
board2,adj2 = setup_board(9,values2,pos2)
print(board2)


# The first method we will use to solve sudoku is a greedy algorithm. This algorithm will look at the adjacency list for each node on the graph, which corresponds to the cells constraining a given cell on the board. The algorithm will then generate, from the adjacency list, all the possible colors (numbers) that a given node (cell) can take on. If this list of possible colors (values) is of length one, then we set the node (cell) to this color (value). We then preceded through every node on the graph, updating the colors as such. The updated graph will now impose further color constraints on the uncolored nodes, so we will repeat this procedure until the board is either solved, or the graph no longer updates. This happens if the algorithm gets stuck, where it reaches a point where the current color constraints are insufficent to update some of the remaining nodes, in which case we will need to use a different algorithm. 

# In[120]:


## Done is a list, with an element corresponding to each node, with a zero being uncolored, and a 1 being colored
## This function updates that list given a new board state
def update_done(board_values,done):
    for i in range(len(board_values)):
        if board_values[i] != None:
            done[i] = 1
    return(done)



### This function finds all the possible colors for a specified uncolored node, such that they don't violate the constraints
def possible_colors(board_values,node,adj_list):
    colors = [] ### creates list of all possible colors
    for i in range(1,int(math.sqrt(len(board_values)))+1):
        colors.append(i)
        
    for i in range(len(adj_list[node])): 
        ### eliminates any colors that an adjacent node has
        if board_values[adj_list[node][i]] in colors:
            colors.remove(board_values[adj_list[node][i]])
            
    return(colors)



### Function that updates any empty node in the board that has only one possible color
def find_colors(board_values,adj_list,done):
    for i in range(len(board_values)):
        if done[i] == 0:
            colors = possible_colors(board_values,i,adj_list)
            if len(colors) == 1:
                board_values[i] = colors[0]
         
    return(board_values)


    

### reshifts the board from a list of length n^2 to a list of n lists of n
def compile_board(board_values):
    new_board = []
    for i in range(int(math.sqrt(len(board_values)))):
        new_board.append([None]*int(math.sqrt(len(board_values))))
    
    for i in range(len(board_values)):
        row = i // int(math.sqrt(len(board_values)))
        col = i% int(math.sqrt(len(board_values)))
        new_board[row][col] = board_values[i]
        
    return(new_board)  



### Executes the greedy algorithm 
def greedy_alg(board_values,adj_list):
    done = update_done(board_values,[0]*len(board_values)) ### generates list of whether each node has been colored
    
    ### Repeatedly updates node colors until no new nodes are colored after a run of the algorithm 
    go = 1
    while go == 1:
        
        count = sum(done)
        board_values = find_colors(board_values,adj_list,done)
        done = update_done(board_values,done)

        if sum(done) == count:
            go = 0

    board_values = compile_board(board_values)
    return(board_values)

        

    



    
        
        
        

    


# Let's test this algorithm on two sudoku boards. The first one is rather easy, and the second is the so claimed  'world's hardest sudoku problem'. We see that the greedy algorithm can effectively solve the first puzzle, but cannot even update a single node on the second. Clearly, we need a different technique to solve a puzzle such as this. 

# In[121]:


### Test Case
pos1 = [(0,0),(0,1),(0,4),(1,0),(1,3),(1,4),(1,5), (2,1),(2,2),(2,7),(3,0),(3,4),(3,8),(4,0),(4,3),(4,5),(4,8),(5,0),(5,4),(5,8), (6,1),(6,6),(6,7),(7,3),(7,4),(7,5),(7,8),(8,4),(8,7),(8,8)]
values1 = [5,3,7,6,1,9,5,9,8,6,8,6,3,4,8,3,1,7,2,6,6,2,8,4,1,9,5,8,7,9]
board1,adj1 = setup_board(9,values1,pos1)


values2 = [8,3,6,7,9,2,5,7,4,5,7,1,3,1,6,8,8,5,1,9,4]
pos2 = [(0,0),(1,2),(1,3),(2,1),(2,4),(2,6),(3,1),(3,5),(4,4),(4,5),(4,6),(5,3),(5,7),(6,2),(6,7),(6,8),(7,2),(7,3),(7,7),(8,1),(8,6)]
board2,adj2 = setup_board(9,values2,pos2)

print('First Puzzle (Easy)')
print(compile_board(board1))
board1_try = greedy_alg(board1,adj1)
print(board1_try)

print('Second Puzzle (Hard)')
print(compile_board(board2))
board2_try = greedy_alg(board2,adj2)
print(board2_try)


# It is clear that the greedy algorithm cannot solve more difficult sudoku puzzles. Instead, we will use a depth first search to color the nodes. We will start by generating a list of nodes that are yet to be colored. Then we will generate all the possible colors those nodes can take on, based on the given constraints of the problem. Then we iterate through the possible colors for each node, accepting the first one that doesn't violate the constraints. Then we precede to the next node. We continue until we get stuck, when no possible color can satisfy the constraints. Then, we uncolor the previous node and try and color it again. We repeat this procedure, which is a depth first search of the graph, testing possible colorings and backtracking. We see that this procedure is able to effectively solve the puzzle. 

# In[115]:


### Function that tells us if a given coloring of a node would violate the coloring constraints imposed on it
### returns true if there is a violation
def violations(board_values,node,new_value,adj_list):
    for i in range(len(adj_list[node])):
        if new_value == board_values[adj_list[node][i]]:
            return(True)
    return(False)
  
### Function that returns a list of nodes yet to be colored, and the possible colors they can take on based on constraints

def initialize_deep(board_values,adj_list):
    done = update_done(board_values,[0]*len(board_values))

    to_search = []
    colors = []
    for i in range(len(done)):
        if done[i] == 0:
            to_search.append(i)
            colors.append(possible_colors(board_values,i,adj_list))
    return(to_search,colors)


### Function that performs a depth first search of the graph to find a viable coloring

def DFS(board_values,adj_list,colors,to_search):
    # the index of possible colors for each node that the search will start from
    # initially start with the first value in the list of colors

    starts = [0]*len(to_search)
    
    # copies the board to a temporary board
    new_board = board_values 

    i = 0 # starts with first uncolored node
    while i < len(to_search):
        added = 0 # tracks if a new color was added
        
        # looks through the possible colors for the node, starting from the start value
        # this functions similarly to a queue or stack, where a coloring is removed from the search if the algorithm backtracks
        # It's a little different, in that new values aren't added, also more space efficient than storing n^2 stacks/queues
        
        for j in range(starts[i],len(colors[i])):
            
            # if there is a violation, move onto next possible color
            if violations(new_board,to_search[i],colors[i][j],adj_list):
                continue
            
            # if no violation, keep track of where in the list of colors this occured and exits the loop
            if not violations(new_board,to_search[i],colors[i][j],adj_list):
                starts[i] = j
                added = 1
                break
        
        # if no color could be found
        if added == 0:
            new_board[to_search[i-1]] = None # decolors previous node
            starts[i] = 0 # resets the starting point for the color search on the current node 
            starts[i-1] = starts[i-1]+1 # shifts the starting point of the color search for the previous node
            i = i - 1 # moves the loop back to the previous node
            
        # if a viable color is found
        else:
            new_board[to_search[i]] = colors[i][starts[i]] # updates board
            i = i + 1 # moves to next node
        
        
    return(new_board)
             
### Function that executes the search and formats the solutions
def deep_search(board_values,adj_list):
    
    # generates possible colors and nodes to  search
    to_search, colors = initialize_deep(board_values,adj_list) 
           
    # DFS
    board_values = DFS(board_values,adj_list,colors,to_search)
    
    # formats board
    board_values = compile_board(board_values)
    
    return(board_values)
 


# Now let's test the new searching algorithm. We can see that it solves the first puzzle, just as the greedy algorithm can. However, it is also able to solve the second puzzle. We check these solutions and find that they are indeed correct. 

# In[125]:


### Test Case
pos1 = [(0,0),(0,1),(0,4),(1,0),(1,3),(1,4),(1,5), (2,1),(2,2),(2,7),(3,0),(3,4),(3,8),(4,0),(4,3),(4,5),(4,8),(5,0),(5,4),(5,8), (6,1),(6,6),(6,7),(7,3),(7,4),(7,5),(7,8),(8,4),(8,7),(8,8)]
values1 = [5,3,7,6,1,9,5,9,8,6,8,6,3,4,8,3,1,7,2,6,6,2,8,4,1,9,5,8,7,9]
board1,adj1 = setup_board(9,values1,pos1)


values2 = [8,3,6,7,9,2,5,7,4,5,7,1,3,1,6,8,8,5,1,9,4]
pos2 = [(0,0),(1,2),(1,3),(2,1),(2,4),(2,6),(3,1),(3,5),(4,4),(4,5),(4,6),(5,3),(5,7),(6,2),(6,7),(6,8),(7,2),(7,3),(7,7),(8,1),(8,6)]
board2,adj2 = setup_board(9,values2,pos2)


def check_solutions(board,adj):
    board = flatten(board)
    for i in range(len(board)):
        for j in range(len(adj[i])):
            if board[i] == board[adj[i][j]]:
                return('Incorrect!')
    return('Solved!')


print('First Puzzle (Easy)')
print(compile_board(board1))
board1_try = deep_search(board1,adj1)
print(board1_try)
print(check_solutions(board1_try,adj1))

print('Second Puzzle (Hard)')
print(compile_board(board2))
board2_try = deep_search(board2,adj2)
print(board2_try)
   
print(check_solutions(board2_try,adj2))

