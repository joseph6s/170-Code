import copy
from queue import PriorityQueue
import sys
sys.setrecursionlimit(10**6)
totalstates = 0

## This function turn the list of input string into a list of list
## It takes one agrument: the list of input string
## It returns a list of list 
def arr_conv(start):
    arr = []
    for i in range(len(start)):
        arr.append(list(start[i]))
    return arr

## This function checks whether a state is goal state
## It takes one agrument : the current state
## It returns True if the state is gaol state, False otherwise.
def isgoal(start):
    if (start[2][4] == 'X' and start[2][5]== 'X'):
        return True
    return False

##This is the main function for rushhour, it takes the input values and call the state_search function, and print the result
##It takes two agrument : mode ,  input list of string(represent initial state)
##It does not return a value
def rushhour(mode,start):
    global totalstates
    totalstates = 0
    start_arr = arr_conv(start)
    pq = PriorityQueue()
    pq.put((0,start_arr))
    result = state_search(pq,[],0,mode,[start_arr])
    moves = len(result) -1
    print(result)
    print("Total moves: "+ str(moves))
    print("Total states explored:" +str(totalstates))

## This is the function using A* search to find the goal state
## THis function takes four agrument : the priority queue, path of states, g(n) value, mode, a list containing all the states that have been generated
## It returns the path(a list of states on the path from initial state to goal state)
#### How I implement my A* search : I use a prioirty queue to store all state in this format (fn value, state)
#### so each element in prioirty queue has fn value on their index 0 and the correspond state on index 1
#### then I will check if the first state is goal state
#### if not I will expand the first state( which has the least fn value), and put all the generated states back to the priority queue
#### then repeat until the goal state is reached
def state_search(pq,path,g,mode,allstate):
    if pq == []:
        return []
    pq_head = pq.get()
    start = pq_head[1]
    if isgoal(start): #check if it is goal state
        return [start]
    else:
        temp = generate_new(start,g,allstate)
        for i in range(len(temp)): # this for loop put the newly generated states into priority queue
            global totalstates
            totalstates += 1 # count states explored
            if mode == 0:
                pq.put((blocking_heu(temp[i],g),temp[i]))
            else:
                pq.put((my_heu(temp[i],g),temp[i]))
            allstate.append(temp[i])
        path.append(start)
        result = state_search(pq,path,g+1,mode,allstate)
        dif = check_dif(result,start) # check difference between two states to find the previous state on the path
        if dif == 2:
            result.insert(0,start)
        return result


## This function calculate the difference betweem two states
## It takes two arguments : a list of paths that have already collected, a state that is currently been explored
## It return a int value of the number of elements out of position
def check_dif(result,start):
    dif = 0
    for a in range(6):
        for b in range(6):
            if start[a][b] != result[0][a][b]:
                dif += 1 
    return dif

## This function calculate the f(n) value of a state
## It takes two arguements : the state and current g(n) value
## The output is a int value of f(n)
def blocking_heu(start,g):
    if isgoal(start) == True:
        return 0
    tail = 0
    count = 1
    for i in range(len(start[2])):
        if start[2][i] == 'X' and start[2][i+1] != 'X':#find the index of tail of car X
            tail = i
            break
    for j in range(tail+1,6): # then count how many cars are between the tail and the end of wall
        if start[2][j] != '-':
            count += 1
    return count+g

## This function is my heuristic
## Instead of blocking heuristic which simply count the number of cars blocking the way, my heurisitic gives h(n) value based on whether the blocking car is blocked
## if the blocking car is blocked , I add 2 to f(n), otherwise I add 1 to f(n)
## f(n) start at 1
## this way will save more states explored while there are more cars blocking the way, save less states explored while there are fewer cars blocking the way
def my_heu(start,g):
    if isgoal(start) == True:
        return 0
    tail = 0
    for i in range(len(start[2])):
        if start[2][i] == 'X' and start[2][i+1] != 'X':
            tail = i
            break
    v_cars = all_v_car(start)
    count = 0
    for j in range(tail+1,6):
        if start[2][j] != '-':
            if start[0][j] == start[2][j]:
                if start[3][j] != '-':
                    count += 2
                else:
                    count += 1
            if start[4][j] == start[2][j]:
                if start[5][j] != '-':
                    count +=2
                else:
                    count += 0
            if start[1][j] == start[2][j]:
                if start[0][j] != '-' and start[3][j] != '-':
                    count += 2
                else:
                    count += 1
            if start[3][j] == start[2][j]:
                if start[1][j] != '-' and start[4][j] != '-':
                    count += 2
                else:
                    count += 1
            if start[1][j] == start[2][j] and start[3][j] == start[2][j]:
                if start[0][j] != '-' and start[4][j] != '-':
                    count += 2
                else:
                    count += 1
    return count+g

## The functions generates all possibles states from the current states
## It takes three arguments : current state, g(n) value, a list containing all the states that have been generated(for circle checking)
## It returns a list containing all the states generated from current states
def generate_new(start,g,myqueue):
    result = []
    h_cars = all_h_car(start)
    v_cars = all_v_car(start)
    for a in range(len(h_cars)):
        head = h_cars[a][0]
        tail = h_cars[a][1]
        if head[1]>0 and start[head[0]][head[1]-1] == '-':
            temp = h_left(start,head,tail)
            if check_circle(myqueue,temp):
                result.append(temp)
        if tail[1]<5 and start[tail[0]][tail[1]+1] == '-':
            temp = h_right(start,head,tail)
            if check_circle(myqueue,temp):
                result.append(temp)
    for b in range(len(v_cars)):
        head = v_cars[b][0]
        tail = v_cars[b][1]
        if head[0]>0 and start[head[0]-1][head[1]] == '-':
            temp = v_up(start,head,tail)
            if check_circle(myqueue,temp):
                result.append(temp)
        if tail[0]<5 and start[tail[0]+1][tail[1]] == '-':
            temp = v_down(start,head,tail)
            if check_circle(myqueue,temp):
                result.append(temp)
    return result

## The functions checks whether newly generate state is explored or currently waiting for explortion to prevent the program go into a circle
## It take two agruments : a list containing all the states that have been generatetd, the newly generate state
## It returns False if the newly generated state existed before, returns True otherwise   
def check_circle(myqueue,start):
    if start in myqueue:
        return False
    else:
        return True

## This functions takes a state as argument and generate all the horizontal cars' indexs
## Its ouput will be a list containing all the horizontal cars' indexs of head and tail
## Ex: [[1,0],[1,1]],[[2,0],[2,2]]  shows two horizontal car exists, 
## one start at (1,0), end at (1,1). Another one start at (2,0),(2,2)
def all_h_car(start):
    car_indexs =[]
    for i in range(6):
        j = 0
        while j < 5:
            if start[i][j]!='-' and start[i][j+1] == start[i][j]:
                head = [i,j]
                if j+2<=5:
                    if start[i][j+2] == start[i][j]:
                        tail = [i,j+2]
                        j+=3
                    else:
                        tail = [i,j+1]
                        j+=2
                else:
                    tail = [i,j+1]
                    j+=2
                car_indexs.append([head,tail])
            else:
                j+=1
    return car_indexs

## This functions takes a state as argument and generate all the vertical cars' indexs
## Its ouput will be a list containing all the vertical cars' indexs of head and tail
## Ex: [[1,0],[2,0]],[[2,1],[3,1]]  shows two vertical car exists, 
## one start at (1,0), end at (2,0). Another one start at (2,1),(3,1)
def all_v_car(start):
    car_indexs = []
    for j in range(6):
        i = 0
        while i < 5:
            if start[i][j]!='-' and start[i+1][j] == start[i][j]:
                head = [i,j]
                if i+2<= 5:
                    if start[i+2][j] == start[i][j]:
                        tail = [i+2,j]
                        i+=3
                    else:
                        tail = [i+1,j]
                        i+=2
                else:
                    tail = [i+1,j]
                    i+=2
                car_indexs.append([head,tail])
            else:
                i+=1
    return car_indexs        


        
## This function generate a new state with one vertical car moves 1 unit up
## This function takes three arguments : current state, head indexs of the car, tail indexs of the car
## This function returns a new state with one vertical car moves up
def v_up(start,head,tail):
    char = start[head[0]][head[1]]
    newState = copy.deepcopy(start)
    newState[head[0]-1][head[1]] = char
    newState[tail[0]][tail[1]]= '-'
    return newState

## This function generate a new state with one vertical car moves 1 unitdown
## This function takes three arguments : current state, head indexs of the car, tail indexs of the car
## This function returns a new state with one vertical car moves down
def v_down(start,head,tail):
    char = start[head[0]][head[1]]
    newState = copy.deepcopy(start)
    newState[tail[0]+1][tail[1]]= char
    newState[head[0]][head[1]]= '-'
    return newState

## This function generate a new state with one horizontal car moves 1 unit left 
## This function takes three arguments : current state, head indexs of the car, tail indexs of the car
## This function returns a new state with one horizontal car moves left
def h_left(start,head,tail):
    char = start[head[0]][head[1]]
    newState = copy.deepcopy(start)
    newState[head[0]][head[1]-1] = char
    newState[tail[0]][tail[1]]= '-'
    return newState

## This function generate a new state with one horizontal car moves 1 unit right
## This function takes three arguments : current state, head indexs of the car, tail indexs of the car
## This function returns a new state with one horizontal car moves right
def h_right(start,head,tail):
    char = start[head[0]][head[1]]
    newState = copy.deepcopy(start)
    newState[tail[0]][tail[1]+1]= char
    newState[head[0]][head[1]]= '-'
    return newState