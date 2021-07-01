import copy
from queue import PriorityQueue
import sys
sys.setrecursionlimit(10**6)

## This function generate a legal next move while the information of the state is entered
## This function takes four agruments: the initial board state, size of the board, who is the mover, and the depth need to be search
## This function returns a optimized next step based on the states that have been searched
def hexapawn(input,size,target,depth):
    start = arr_conv(input)
    rc = check_if_one_wins(start,target,size)
    if rc != False:
        return start
    layer = 1
    next_moves = generate_new(start,size,target,"MAX")
    if next_moves == []:
        return start
    values = []
    for x in next_moves:
        val = find_desire_state(x,size,target,depth,layer)
        values.append(val)
    insertion_sort_both(values,next_moves)
    result = next_moves[-1]
    str_result = []
    for i in range(size):
        temp = ""
        for j in range(size):
            temp += result[i][j]
        str_result.append(temp)
    return str_result

## MINIMAX Search contains function find_desire_state,  minimax, find_value

##The first layer of states that we need to assign values to is the "next-move" layer
##So hexpawn function will generates all states for next-moves and call find_desire_state to assign value to each of them

##This function generate a value for the given state
##This function takes five parameters: the state, size of the board, who is the mover, the depth need to be search, and the number indicates current layer
##This function returns a value for the state
def find_desire_state(start,size,target,depth,layer):
    rc = check_if_one_wins(start,target,size)
    if rc != False:
        return rc
    result_val = 0
    if layer % 2 == 1:
        mode = "MIN"
    else:
        mode = "MAX"
    new_states = generate_new(start,size,target,mode)
    if layer >= (depth-1):
        if new_states == []:
            if mode == "MIN":
                return size
            else:
                return -size
        return find_value(new_states,target,mode,size)
    else:
        values = []
        for x in new_states:
            rc = find_desire_state(x,size,target,depth,layer+1)
            values.append(rc)
        if new_states == []:
            if mode == "MIN":
                return size
            else:
                return -size
        result_val = minimax(values,mode)
        return result_val

## This function sort the values of giving layer and return the minimum value or the maximum value based on MINIMAX level
## This function takes two agruments: a list of value, and the Minimax level
def minimax(values,mode):
    insertion_sort(values)
    if mode == "MIN":
        return values[-1]
    else:
        return values[0]

## This function is uses at the bottom layer to evaluate each states ,and return the minimum value or the maximum value based on MINIMAX level
## This function is takes four agrument: board states in the bottom layer, color of program's pawns, its parents' minimax level, size of board
def find_value(states,target,modeofparent,size):
    values = []
    if target == 'w':
        for x in states:
            value = evaluate_w(x,size)
            values.append(value)
    if target == 'b':
        for x in states:
            value = evaluate_b(x,size)
            values.append(value)
    insertion_sort(values)
    if modeofparent == "MIN":
        return values[0]
    else:
        return values[-1]   

##Broad Evaluator contains functions: check_if_one_wins,evaluate_w, evaluate_b,check_empty_route

## This function checks is a state is already a winning state
## It returns False when the state have no winner, or returns the winning value if a player wins 
## This function takes three parameters: the state, color of program's pawns, size of board
def check_if_one_wins(start,target,size):
    for i in start[0]:
        if i == 'b':
            if target == 'b':
                return size
            else:
                return -size
    length = len(start)
    for i in start[length-1]:
        if i == 'w':
            if target == 'w':
                return size
            else:
                return -size
    return False


## The following two function are evaluation functions
## One of them get called based on the color of program's pawns
## Both of them takes two parameters: the state, size of board
## Both of them return a integer for the value of a board state
def evaluate_w(start,size):
    for i in start[0]:
        if i == 'b':
            return -size
    length = len(start)
    for i in start[length-1]:
        if i == 'w':
            return size
    num_white = 0
    num_black = 0 
    for i in range(size):
        for j in range(size):
            if start[i][j] == 'w':
                num_white += 1
            elif start[i][j] == 'b':
                num_black += 1
    result = num_white - num_black
    result += check_empty_route(start,size,'w')    
    return result
                
def evaluate_b(start,size):
    for i in start[0]:
        if i == 'b':
            return size
    length = len(start)
    for i in start[length-1]:
        if i == 'w':
            return -size
    num_white = 0
    num_black = 0 
    for i in range(size):
        for j in range(size):
            if start[i][j] == 'w':
                num_white += 1
            elif start[i][j] == 'b':
                num_black += 1
    result = num_black - num_white
    result += check_empty_route(start,size,'b')
    return result

## This is the function that add more component to the evalution progress
## The idea is that a pawn is more likely to win if it has a clear pass to the other side
## Therefore, we will check all pawns in a state to see if they have clear paths to the other side
## Then minus the program's number of clear-path-pawn by the opponent's number of clear-path-pawn
## THis function takes three parameters: the state, the size of board, and the color of program's pawns
## This return a integer value
def check_empty_route(start,size,mode):
    w_extra_points = 0
    b_extra_points = 0
    result = []
    num_white = 0
    indexs_white = []
    for i in range(size):
        for j in range(size):
            if start[i][j] == "w":
                num_white += 1
                indexs_white.append([i,j])
    for k in indexs_white:
        i = k[0]
        j = k[1]
        index_w = 0
        for x in range(i+1,size):
            if start[x][j] == 'b':
                index_w = 1
            else:
                continue
        if index_w == 0:
            w_extra_points += 1
    num_black = 0
    indexs_black = []
    for i in range(size):
        for j in range(size):
            if start[i][j] == "b":
                num_black += 1
                indexs_black.append([i,j])
    for k in indexs_black:
        i = k[0]
        j = k[1]
        index_b = 0
        for x in range(0,i):
            if start[x][j] == 'w':
                index_b = 1
            else:
                continue
        if index_b == 0:
            b_extra_points += 1
    if mode == 'w':
        result = w_extra_points - b_extra_points
    else:
        result = b_extra_points - w_extra_points
    return result


## Move generator contains functions: generate_new,check_empty_route, white_moves, and black_moves

## This function will calls correspond moves generator functions base on the color of program's pawns and minimax level
## This functuin takes four parameter: the state, size of board, color of program's pawns, and the current minimax level
## This function returns a list of states
def generate_new(start,size,target,mode):
    if target == 'w':
        if mode == "MAX":
            return white_moves(start,size)
        else:
            return black_moves(start,size)
    else:
        if mode == "MAX":
            return black_moves(start,size)
        else:
            return white_moves(start,size)

## The following two functions (white_moves,black_moves) are functions to generate new states
## One of them get called based on the color of program's pawns
## Both of them takes two parameters: the state, size of board
## Both of them return returns a list of states
def white_moves(start,size):
    result = []
    num_white = 0
    indexs_white = []
    for i in range(size):
        for j in range(size):
            if start[i][j] == "w":
                num_white += 1
                indexs_white.append([i,j])
    for k in indexs_white:
        i = k[0]
        j = k[1]
        if j >= 1 and i < size-1:
            if start[i+1][j-1] == 'b':
                result.append(move_left_down(start,[i,j]))
        if j < size-1 and i < size-1:
            if start[i+1][j+1] == 'b':
                result.append(move_right_down(start,[i,j]))
        if i < size-1:
            if start[i+1][j] == '-':
                result.append(move_down(start,[i,j]))
    return result

def black_moves(start,size):
    result = []
    num_black = 0
    indexs_black = []
    for i in range(size):
        for j in range(size):
            if start[i][j] == "b":
                num_black += 1
                indexs_black.append([i,j])
    for k in indexs_black:
        i = k[0]
        j = k[1]
        if j >= 1 and i > 0:
            if start[i-1][j-1] == 'w':
                result.append(move_left_up(start,[i,j]))
        if j < size-1 and i > 0:
            if start[i-1][j+1] == 'w':
                result.append(move_right_up(start,[i,j]))
        if i > 0:
            if start[i-1][j] == '-':
                result.append(move_up(start,[i,j]))
    return result

## All the following move_"something" functions are help functions for move generators
## They all take two agruments: the state, and the index for the pawn need to be move
## They all return one state 
def move_down(start,index):
    i = index [0]
    j = index [1]
    state = copy.deepcopy(start)
    state[i][j] = '-'
    state[i+1][j] = 'w'
    return state

def move_left_down(start,index):
    i = index [0]
    j = index [1]
    state = copy.deepcopy(start)
    state[i][j] = '-'
    state[i+1][j-1] = 'w'
    return state

def move_right_down(start,index):
    i = index [0]
    j = index [1]
    state = copy.deepcopy(start)
    state[i][j] = '-'
    state[i+1][j+1] = 'w'
    return state

def move_up(start,index):
    i = index [0]
    j = index [1]
    state = copy.deepcopy(start)
    state[i][j] = '-'
    state[i-1][j] = 'b'
    return state

def move_left_up(start,index):
    i = index [0]
    j = index [1]
    state = copy.deepcopy(start)
    state[i][j] = '-'
    state[i-1][j-1] = 'b'
    return state

def move_right_up(start,index):
    i = index [0]
    j = index [1]
    state = copy.deepcopy(start)
    state[i][j] = '-'
    state[i-1][j+1] = 'b'
    return state

## This function is a helpful that convert the input list of string to a list of lists
## This function takes one parameter: the state
def arr_conv(start):
    arr = []
    for i in range(len(start)):
        arr.append(list(start[i]))
    return arr

## This function is a helpful for minimax search to sort the values from lowest to highest
## This function takes one parameter: the list of values
def insertion_sort(values):
    i = 1
    while i < len(values):
        key = values[i]
        j = i-1
        while j>=0 and values[j]>key:
            values[j+1] = values[j]
            j -= 1
        values[j+1] = key
        i += 1
    return 

## This function is a helpful for minimax search to sort the values from lowest to highest and their correspond states
## This function takes one parameter: the list of values, the list of states
def insertion_sort_both(values,states):
    i = 1
    while i < len(values):
        key = values[i]
        key2 = states[i]
        j = i-1
        while j>=0 and values[j]>key:
            values[j+1] = values[j]
            states[j+1] = states[j]
            j -= 1
        values[j+1] = key
        states[j+1] = key2
        i += 1
    return