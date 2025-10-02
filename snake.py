import curses
from random import randint

def main(stdscr):
    curses.start_color()      
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) 
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  
    
    curses.curs_set(0)
    
    GAME_HEIGHT = 20
    GAME_WIDTH = 40
    
    screen_h, screen_w = stdscr.getmaxyx()
    start_y = (screen_h - GAME_HEIGHT) // 2
    start_x = (screen_w - GAME_WIDTH) // 2
    
    win = curses.newwin(GAME_HEIGHT, GAME_WIDTH, start_y, start_x)
    win.keypad(1)
    win.timeout(100)
    snake_x = GAME_WIDTH // 4
    snake_y = GAME_HEIGHT // 2
    snake = [[snake_y, snake_x], [snake_y, snake_x-1], [snake_y, snake_x-2]]
    
    apple = [GAME_HEIGHT // 2, GAME_WIDTH // 2]
    win.addch(apple[0], apple[1], curses.ACS_DIAMOND, curses.color_pair(2))
    win.border()
    
    key = curses.KEY_RIGHT

    while True:
        next_key = win.getch()
        if next_key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            key = next_key

        head = snake[0].copy()
        if key == curses.KEY_DOWN:
            head[0] += 1
        elif key == curses.KEY_UP:
            head[0] -= 1
        elif key == curses.KEY_LEFT:
            head[1] -= 1
        elif key == curses.KEY_RIGHT:
            head[1] += 1

        snake.insert(0, head)

        if snake[0] == apple:
            apple = None
            while apple is None:
                nf = [randint(1, GAME_HEIGHT-2), randint(1, GAME_WIDTH-2)]
                apple = nf if nf not in snake else None
            win.addch(apple[0], apple[1], curses.ACS_DIAMOND, curses.color_pair(2))
        else:
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')

        if (snake[0][0] in [0, GAME_HEIGHT-1] or
            snake[0][1] in [0, GAME_WIDTH-1] or  
            snake[0] in snake[1:]):
            break

        win.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD, curses.color_pair(1))
        win.refresh()

    # Game over
    win.clear()
    win.addstr(GAME_HEIGHT//2, GAME_WIDTH//2 - 4, "GAME OVER")
    win.refresh()
    win.getch()

if __name__ == "__main__":
    curses.wrapper(main)