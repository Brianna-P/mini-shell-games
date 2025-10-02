import curses
import random
import time

SHAPES = [
    [[1, 1, 1, 1]],                        
    [[1, 1], [1, 1]],                            
    [[0, 1, 0], [1, 1, 1]], 
    [[0, 0, 1], [1, 1, 1]],  
    [[1, 0, 0], [1, 1, 1]], 
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]]
]

COLORS = {
    0: 1,  # I - Cyan
    1: 2,  # O - Yellow  
    2: 3,  # T - Purple
    3: 4,  # L - Orange
    4: 5,  # J - Blue
    5: 6,  # S - Green
    6: 7   # Z - Red
}

FIELD_HEIGHT = 20
FIELD_WIDTH = 10

def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)    
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK) 
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)   
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)  
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)  

def create_windows(stdscr):
    h, w = stdscr.getmaxyx()
    
    game_window = curses.newwin(FIELD_HEIGHT + 2, FIELD_WIDTH + 2, 0, 0)
    info_window = curses.newwin(FIELD_HEIGHT + 2, 30, 0, FIELD_WIDTH + 3)
    
    return game_window, info_window

def draw_field(win, field):
    for y in range(FIELD_HEIGHT):
        for x in range(FIELD_WIDTH):
            if field[y][x]:
                try:
                    win.addstr(y+1, x+1, "##", curses.color_pair(0))
                except curses.error:
                    pass
            else:
                try:
                    win.addstr(y+1, x+1, "  ")
                except curses.error:
                    pass

def draw_score(info_window, score, level, lines_cleared, shape_index):
    try:
        info_window.clear()
        info_window.border()
        info_window.addstr(1, 2, "TETRIS")
        info_window.addstr(3, 2, f"Score: {score}")
        info_window.addstr(4, 2, f"Level: {level}")
        info_window.addstr(5, 2, f"Lines: {lines_cleared}")
        
        info_window.addstr(7, 2, "Next Piece:")
        next_shape = SHAPES[shape_index]
        for y, row in enumerate(next_shape):
            for x, cell in enumerate(row):
                if cell:
                    try:
                        info_window.addstr(9 + y, 4 + x * 2, "##", curses.color_pair(COLORS[shape_index]))
                    except curses.error:
                        pass
        
        info_window.addstr(13, 2, "Controls:")
        info_window.addstr(14, 2, "← → : Move")
        info_window.addstr(15, 2, "↑ : Rotate")
        info_window.addstr(16, 2, "↓ : Soft Drop")
        info_window.addstr(17, 2, "Space : Hard Drop")
        info_window.addstr(18, 2, "Q : Quit")
        
        info_window.refresh()
    except curses.error:
        pass

def check_collision(field, shape, offset_y, offset_x):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                fy = y + offset_y
                fx = x + offset_x
                if fy >= FIELD_HEIGHT or fx < 0 or fx >= FIELD_WIDTH:
                    return True
                if fy >= 0 and field[fy][fx]:
                    return True
    return False

def merge_shape(field, shape, offset_y, offset_x, shape_index):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell and 0 <= y+offset_y < FIELD_HEIGHT and 0 <= x+offset_x < FIELD_WIDTH:
                field[y+offset_y][x+offset_x] = shape_index + 2 

def clear_lines(field):
    new_field = []
    cleared = 0
    
    for row in field:
        if all(cell != 0 for cell in row):
            cleared += 1
        else:
            new_field.append(row)
    
    for _ in range(cleared):
        new_field.insert(0, [0] * FIELD_WIDTH)
    
    return new_field, cleared

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]
def get_drop_speed(level):
    return max(0.05, 0.5 - (level * 0.05))

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    init_colors()
    
    game_win, info_window = create_windows(stdscr)
    game_win.keypad(1)
    game_win.nodelay(1)

    field = [[0] * FIELD_WIDTH for _ in range(FIELD_HEIGHT)]
    current_shape_index = random.randint(0, len(SHAPES) - 1)
    current_shape = SHAPES[current_shape_index]
    next_shape_index = random.randint(0, len(SHAPES) - 1)
    shape_y = 0
    shape_x = FIELD_WIDTH // 2 - len(current_shape[0]) // 2
    score = 0
    level = 1
    lines_cleared = 0
    last_drop_time = time.time()
    drop_speed = get_drop_speed(level)

    while True:
        current_time = time.time()
    
        key = game_win.getch()
        if key == ord('q') or key == ord('Q'):
            break
        elif key == curses.KEY_LEFT:
            if not check_collision(field, current_shape, shape_y, shape_x - 1):
                shape_x -= 1
        elif key == curses.KEY_RIGHT:
            if not check_collision(field, current_shape, shape_y, shape_x + 1):
                shape_x += 1
        elif key == curses.KEY_DOWN:
            if not check_collision(field, current_shape, shape_y + 1, shape_x):
                shape_y += 1
        elif key == curses.KEY_UP:
            rotated = rotate(current_shape)
            if not check_collision(field, rotated, shape_y, shape_x):
                current_shape = rotated
        elif key == ord(' '): 
            while not check_collision(field, current_shape, shape_y + 1, shape_x):
                shape_y += 1

        # Automatic drop
        if current_time - last_drop_time > drop_speed:
            if not check_collision(field, current_shape, shape_y + 1, shape_x):
                shape_y += 1
            else:
                merge_shape(field, current_shape, shape_y, shape_x, current_shape_index)
                field, cleared = clear_lines(field)
                
                if cleared > 0:
                    lines_cleared += cleared
                    if cleared == 1:
                        score += 100 * level
                    elif cleared == 2:
                        score += 300 * level
                    elif cleared == 3:
                        score += 500 * level
                    elif cleared == 4:
                        score += 800 * level
                    
                    level = lines_cleared // 10 + 1
                    drop_speed = get_drop_speed(level)
                current_shape_index = next_shape_index
                current_shape = SHAPES[current_shape_index]
                next_shape_index = random.randint(0, len(SHAPES) - 1)
                shape_y = 0
                shape_x = FIELD_WIDTH // 2 - len(current_shape[0]) // 2
                
                if check_collision(field, current_shape, shape_y, shape_x):
                    try:
                        game_win.addstr(FIELD_HEIGHT // 2, FIELD_WIDTH // 2 - 4, "GAME OVER")
                        game_win.refresh()
                        time.sleep(2)
                    except curses.error:
                        pass
                    break
            
            last_drop_time = current_time

        game_win.clear()
        game_win.border()
        draw_field(game_win, field)
        for y, row in enumerate(current_shape):
            for x, cell in enumerate(row):
                if cell and 0 <= shape_y + y < FIELD_HEIGHT:
                    try:
                        game_win.addstr(shape_y + y + 1, shape_x + x + 1, "##", curses.color_pair(COLORS[current_shape_index]))
                    except curses.error:
                        pass

        draw_score(info_window, score, level, lines_cleared, next_shape_index)

        game_win.refresh()
        time.sleep(0.01)

if __name__ == "__main__":
    curses.wrapper(main)