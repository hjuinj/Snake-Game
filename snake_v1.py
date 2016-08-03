# SNAKES GAME
"""""
        REFLEX AGENT
always choose the move that shortens the distance to goal the most
and incorport tail awareness
"""""
# Use ARROW KEYS to play, SPACE BAR for pausing/resuming and Esc Key for exiting
 
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN #261,260,259,258
from random import randint
 
f= open("debug","a")
LEFT = 0; RIGHT=19;BOTTOM=0;TOP=9;
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
food = [TOP/2,RIGHT/2]                                                     # First food co-ordinates
 
win.addch(food[0], food[1], '*')                                   # Prints the food
 
def squareDistance(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2;
def valid(p1,snake):
    return p1 not in snake and BOTTOM<p1[0]<TOP and LEFT<p1[1]<RIGHT;
def getMove(food,snake):
    head = snake[0];
    tail = snake[-1];
    up = [head[0]-1,head[1]];
    down = [head[0]+1,head[1]];
    left = [head[0],head[1]-1];
    right = [head[0],head[1]+1];
    #up,down,left, right;
    moves = [[up,KEY_UP],
            [down,KEY_DOWN],
            [left,KEY_LEFT],
            [right,KEY_RIGHT]]
    cost=2**24;move=KEY_UP; 
    for m in moves:
        if valid(m[0],snake) and (1*(squareDistance(m[0],food)+9*squareDistance(head,tail))) < cost:
            move = m[1];
            cost = (1*squareDistance(m[0],food)+9*squareDistance(head,tail));
    return move; 

while key != 27:                                                   # While Esc key is not pressed
    win.border(0)
    win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score' and
    win.timeout(10)
#    win.timeout(150 - (len(snake)/5 + len(snake)/10)%120)          # Increases the speed of Snake as its length increases
    
    prevKey = key                                                  # Previous key pressed
    event  = win.getch();
    event = getMove(food,snake);
    key = key if event == -1 else event 
    #f.write(str(event)+"\n");
 
 
    if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
        key = -1                                                   # one (Pause/Resume)
        while key != ord(' '):
            key = win.getch()
        key = prevKey
        continue
 
    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
        key = prevKey
 
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
