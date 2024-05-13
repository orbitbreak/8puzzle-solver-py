# 8-puzzle solver.
#
# Super fun stuff.

import copy
import sys

goal = [['1', '2', '3'],
		['4', '5', '6'],
		['7', '8', ' ']]

def main():

    input = choose_puzzle()
    alg = algorithm()
    run_puzzle(input, alg)

def choose_puzzle():

    default = [['1', '2', '3'], ['4', ' ', '6'], ['7', '5', '8']]
    puzzle = []
    print "\n \nWelcome, brave 8-puzzler."

    while 1:
        
        game_choice = raw_input("Enter 1 for built-in puzzle:\n" +
			str(default).translate(None, ' \' [ ] , ') + "\n..Or 2 to enter it yourself,  \
					\n ..or 3 to quit.   \n \n>  ")

        if (game_choice == "1"):
            print "\nYou have chosen the built-in puzzle. Nice choice, man! \n"
            puzzle = default
            return puzzle

        elif (game_choice == "2"):
            print "Use a zero to represent the blanks when typing it in.\n"
            firstrow = raw_input("Enter the first row, use a space between numbers \n> ")
            firstrow = firstrow.split(' ')
            if (firstrow.count('0') == 1):
                firstrow[firstrow.index('0')] = ' '
            
            secondrow = raw_input("Enter the second row, keep using those spaces. Unless you're feeling lucky. \n> ")
            secondrow = secondrow.split(' ')
            if (secondrow.count('0') == 1):
                secondrow[secondrow.index('0')] = ' '

            thirdrow = raw_input("Enter the third row \n> ")
            thirdrow = thirdrow.split(' ')
            if (thirdrow.count('0') == 1):
                thirdrow[thirdrow.index('0')] = ' '

            puzzle.append(firstrow)
            puzzle.append(secondrow)
            puzzle.append(thirdrow)
            print "\n"

            return puzzle
           
        elif (game_choice == "3"):
            sys.exit(0)


def algorithm():
    
    print "> Choose an algorithm."
    print "> 1. Uniform cost"
    print "> 2. A* (misplaced tile)"
    print "> 3. A* (manhattan distance) \n \n"

    while 1:
        algo_choice = raw_input("> ")
        if(algo_choice == '1'):
            return "uniform_cost"
        elif(algo_choice == '2'):
            return "mispl_tile"
        elif(algo_choice == '3'):
            return "manhattan"

    return algo_choice

def expand(puzzle):

    expandList = []
	
    left = copy.deepcopy(puzzle)
    for x in left:
        if (x.count(' ') == 1):
            if (x.index(' ') != 0):
                i = x.index(' ')
                x[i] = x[i - 1]
                x[i - 1] = ' '

                expandList.append(left)

    up = copy.deepcopy(puzzle)
    for x in puzzle:
        if (x.count(' ') == 1):
            if (x != up[0]):
                i = x.index(' ')
                if(x == puzzle[1]):
                    up[1][i] = up[0][i]
                    up[0][i] = ' '
                    expandList.append(up)
                else:
                    up[2][i] = up[1][i]
                    up[1][i] = ' '
                    expandList.append(up)

    down = copy.deepcopy(puzzle)
    for x in puzzle:
        if (x.count(' ') == 1):
            if (x != puzzle[2]):
                i = x.index(' ')
                if(x == puzzle[0]):
                    down[0][i] = down[1][i]
                    down[1][i] = ' '
                    expandList.append(down)
                else:
                    down[1][i] = down[2][i]
                    down[2][i] = ' '
                    expandList.append(down)
				
    right = copy.deepcopy(puzzle)
    for x in right:
        if (x.count(' ') == 1):
            if (x.index(' ') != 2):
                i = x.index(' ')
                x[i] = x[i + 1]
                x[i + 1] = ' '

                expandList.append(right)

    return expandList

	
	
def checkGoal(puzzle):
    return goal == puzzle


def misplacedTiles(puzzle):
    
    mispy = 0
    for x in range(3):
        for y in range(3):
            if (puzzle[x][y] != ' '):
                if (puzzle[x][y] != goal[x][y]):
                    mispy += 1

    return mispy	
	
class node:

    def __init__(self):
        self.heuristic = 0
        self.depth = 0

    def setPuzzle(self, puzzle):
        self.puzzleState = puzzle		
        
    def printPuzzle(self):
        print ''
        print self.puzzleState[0][0], self.puzzleState[0][1], self.puzzleState[0][2]
        print self.puzzleState[1][0], self.puzzleState[1][1], self.puzzleState[1][2]
        print self.puzzleState[2][0], self.puzzleState[2][1], self.puzzleState[2][2]

def manhattan(puzzle):

    the_grid = ['1', '2', '3', '4', '5', '6', '7', '8']
    distance = 0
	
    for x in the_grid:
        for i in range(3):
            for j in range(3):
                if (x == goal[i][j]):
                    goalRow = i
                    goalCol = j
                if (x == puzzle[i][j]):
                    puzzleRow = i
                    puzzleCol = j
        distance += ( abs(goalRow - puzzleRow) + abs(goalCol - puzzleCol) )

    return distance

def bubblesort(queue):

    for passesLeft in xrange(len(queue)-1, 0, -1):
        for index in xrange(passesLeft):
            if (queue[index].heuristic + queue[index].depth) > \
                   (queue[index + 1].heuristic + queue[index + 1].depth):
                queue[index], queue[index + 1] = queue[index + 1], queue[index]

    return queue

def run_puzzle(puzzle, algorithm):

    expanded = 0
    queue = []
    max_q = 0

    puz_node = node()
    puz_node.setPuzzle(puzzle)
    puz_node.depth = 0

    if (algorithm == "uniform_cost"):
        puz_node.heuristic = 1
    if (algorithm == "mispl_tile"):
        puz_node.heuristic = misplacedTiles(puz_node.puzzleState)
    if (algorithm == "manhattan"):
        puz_node.heuristic = manhattan(puz_node.puzzleState)

    queue.append(puz_node)

    while 1:

        if (len(queue) == 0):
            print "Search exhausted. Adios! \n"
            sys.exit(0)

        checkNode = node()
        checkNode.puzzleState = queue[0].puzzleState
        checkNode.heuristic = queue[0].heuristic
        checkNode.depth = queue[0].depth

        print ''
        print "Best node for expansion when g(n) =", checkNode.depth, \
              "& h(n) =", checkNode.heuristic, " "
        checkNode.printPuzzle()
        print "\nExpanding node..."
        
        queue.pop(0)

        if (checkGoal(checkNode.puzzleState)):
            print "\nGot it!"
            checkNode.printPuzzle()
            print "\nIn the search, ", expanded, "nodes were expanded."
            print "The max count of nodes in the queue was ", max_q
            print "Goal depth was ", checkNode.depth
            return

        exp_puzzles = expand(checkNode.puzzleState)

        for x in exp_puzzles:
            throw_node = node()
            throw_node.setPuzzle(x)
            if (algorithm == "uniform_cost"):
                throw_node.heuristic = 1
            if (algorithm == "mispl_tile"):
                throw_node.heuristic = misplacedTiles(throw_node.puzzleState)
            if (algorithm == "manhattan"):
                throw_node.heuristic = manhattan(throw_node.puzzleState)
            throw_node.depth = checkNode.depth + 1
            queue.append(throw_node)
            expanded += 1

            if(len(queue) > max_q):
                max_q = len(queue)

        queue = bubblesort(queue)

# RUNTIME
if __name__ == "__main__":
    main()

