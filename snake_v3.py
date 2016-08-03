# SNAKES GAME
"""""
        PATH PLANNING
        PRIORITY QUEUE
"""""
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN #261,260,259,258
from random import randint
import random
from Queue import PriorityQueue; 

f= open("debug","w")
LEFT = 0; RIGHT=11;BOTTOM=0;TOP=11;
curses.initscr()
win = curses.newwin(TOP+1, RIGHT+1, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)
 
key = KEY_RIGHT                                                    # Initializing values
score = 0
 
snake = [[4,10], [4,9], [4,8]]                                     # Initial snake co-ordinates
snake = [[10,10], [10,9], [10,8]]                                     # Initial snake co-ordinates
food = [TOP/2,RIGHT/2]                                                     # First food co-ordinates
food = [1,1]
win.addch(food[0], food[1], '*')                                   # Prints the food

def PQ(food,snake,key):
    queue = PriorityQueue();
    queue.put((heuristic(snake,food),[snake,[key]]));
    visited = set();
    visited.add(tuple([l for k in snake for l in k]));
    while queue!=[]:
        state = queue.get();
        if (state[1][0][0]==food): 
            return state[1][1][1:];
        moves = getMoves(food,state[1][0]);
        f.write(str(queue.qsize())+"\n");
        for m in moves:
            temp = tuple([l for k in m[0] for l in k]);
            if temp not in visited:
                m[1]=state[1][1]+m[1];
                queue.put((heuristic(m[0],food),m));
                visited.add(temp);
    return [27]
            

def heuristic(snake, food):
    return ((snake[0][0]-food[0])**2 + (snake[0][1]-food[1])**2)+\
    1*((snake[-1][0]-food[0])**2+(snake[-1][1]-food[1])**2)
def valid(p1,snake):
    return p1 not in snake and BOTTOM<p1[0]<TOP and LEFT<p1[1]<RIGHT;
def getMoves(food,snake):
    head = snake[0];
    up = [head[0]-1,head[1]];
    down = [head[0]+1,head[1]];
    left = [head[0],head[1]-1];
    right = [head[0],head[1]+1];
    #up,down,left, right;
    moves = [];
    if valid(up,snake):
        moves.append([[up]+snake[:-1],[KEY_UP]]);
    if valid(down,snake):
        moves.append([[down]+snake[:-1],[KEY_DOWN]]);
    if valid(left,snake):
        moves.append([[left]+snake[:-1],[KEY_LEFT]]);
    if valid(right,snake):
        moves.append([[right]+snake[:-1],[KEY_RIGHT]]);
    return moves; 
random.seed(1021411);
while key != 27:                                                   # While Esc key is not pressed
    win.border(0)
    win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score' and
    win.timeout(10)
#    win.timeout(150 - (len(snake)/5 + len(snake)/10)%120)          # Increases the speed of Snake as its length increases
    
    prevKey = key                                                  # Previous key pressed
    moves= PQ(food,snake,prevKey);
    f.write("Path: "+ str(moves) + "\n");
    for i in moves:
        event  = win.getch();
        event = i;
        key = key if event == -1 else event 
 
 
        if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
            key = -1                                                   # one (Pause/Resume)
            while key != ord(' '):
                key = win.getch()
            key = prevKey
            continue
 
        if key == 27:
            curses.endwin();
 
        # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
        # This is taken care of later at [1].
        snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

        # If snake runs over itself
        if snake[0] in snake[1:] or snake[0][0] == 0 or snake[0][1] == 0 or snake[0][0] == 19 or snake[0][1] ==59: break;
        if snake[0] == food:                                            # When snake eats the food
            food = []
            score += 1
            while food == []:
                food = [randint(BOTTOM+1, TOP-1), randint(LEFT+1, RIGHT-1)]                 # Calculating next food's coordinates
                if food in snake: food = []
            win.addch(food[0], food[1], '*')
        else:    
            last = snake.pop()                                          # [1] If it does not eat the food, length decreases
            win.addch(last[0], last[1], ' ')
        win.addch(snake[0][0], snake[0][1], '#')
    
curses.endwin()
print("\nScore - " + str(score))
f.write("\nScore - " + str(score))



f.close()
