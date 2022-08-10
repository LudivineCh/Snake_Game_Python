# Import the module Curses
import curses
import random

# Setup window:
## Import library
s = curses.initscr()
##  Hide the cursor
curses.curs_set(0)
## Create a new window + specify the number of lines, columns and starting point (y, x)
sh, sw = s.getmaxyx()
print(f'sh={sh},sw={sw}')
w = curses.newwin(sh, sw, 0, 0)

##  To use the key pad
w.keypad(1)

##  refrech the screen every 100 ms
w.timeout(100)

##  Draw a border
w.border(0)

# Food and Snake
## Snake : position at left to center (int car les méthodes n'aiment pas le float si nombre impair)
snk_x = int(sw/4)
snk_y = int(sh/2)
snake = [[snk_y,snk_x],[snk_y,snk_x-1],[snk_y,snk_x-2]]

## Snake : position at the center of the screen (int dans le cas où nombre impair car addch ne supporte pas le float)
food = [int(sh/2), int(sw/2)]
## add that food to the screen, and the name is PI
w.addch(food[0], food[1], curses.ACS_PI)

## tell the snake where is going initially
key = curses.KEY_RIGHT

# Game logic:
score = 0

## infinite loop
while True:
    
    #set the next key 
    next_key = w.getch()
    ## si tu ne touches à rien (-1 = nothing), ça va dans le mm sens, sinon next_key
    key = key if next_key == -1 else next_key

    # check if the person has lost the game (if head position (y) is at the top or at the height of the screen if head position (x) at the right or left of the sceen the is the head snake is inside itself)
    if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
        ## close the window and quit
        curses.endwin()
        quit()

    # determine what the new head of the snake is gonna be
    ## new head = old head as a starting point
    new_head = [snake[0][0], snake[0][1]]

    ## Figure out what key is being clink in, and change the new head accordingly.
    if key == curses.KEY_DOWN:
        new_head[0] +=1
    if key == curses.KEY_UP:
        new_head[0] -=1
    if key == curses.KEY_LEFT:
        new_head[1] -=1
    if key == curses.KEY_RIGHT:
        new_head[1] +=1

    ## insert the new head of the snake
    snake.insert(0, new_head)

    ## ajoute un caractère plein pour le serpent
    w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

    ## determine whether or not the snake has run into the food
    if snake[0] == food:
        food = None
        while food is None:
            ## return random integers between 1 and sh-1 / 1 and sw-1 (on ne veut pas les murs)
            nf = [random.randint(1, sh-1), random.randint(1, sw-1)]
            ## if nf not in snake: food = nf, else food = none
            food = nf if nf not in snake else None
         ## rajoute la nouvelle position de la food avec le caractère PI
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        ## Python list pop() is an inbuilt function in Python that removes and returns the last value from the List or the given index value.
        tail = snake.pop()
        ## ajout un espace là où était la queue
        w.addch(tail[0],tail[1], ' ')

    
# Destroy the window
curses.endwin()
