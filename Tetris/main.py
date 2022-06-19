from typing import List, Tuple
from math import cos, sin, radians
from random import randint

Block = List[Tuple[int, int]]

BLOCK_I, BLOCK_J, BLOCK_L, BLOCK_S, BLOCK_Z, BLOCK_T, BLOCK_O = range(7)
LEFT, RIGHT, ROTATE_CW, ROTATE_CCW, DOWN, DROP, QUIT = range(7)

WALL = "##"
SQUARE = "[]"
EMPTY = "  "

Arena = List[List[int]]

BLOCKS = {
    BLOCK_I: [(0, 0), (0, 1), (0, - 1), (0, 2)],
    BLOCK_J: [(0, 0), (0, 1), (0, - 1), (- 1, 1)],
    BLOCK_L: [(0, 0), (0, 1), (0, - 1), (1, 1)],
    BLOCK_S: [(0, 0), (0, 1), (- 1, 1), (1, 0)],
    BLOCK_Z: [(0, 0), (0, 1), (- 1, 0), (1, 1)],
    BLOCK_T: [(0, 0), (0, 1), (- 1, 0), (1, 0)],
    BLOCK_O: [(0, 0), (0, 1), (1, 0), (1, 1)]
}


def coords(block_type: int) -> Block:
    return BLOCKS[block_type]


def rotate_block(angle: int, coords: Block) -> Block:
    rotated: Block = []
    rads = radians(angle)
    for coord in coords:
        rotated.append((round(coord[0] * cos(rads) - coord[1] * sin(rads)),
                        round(coord[0] * sin(rads) + coord[1] * cos(rads))))

    return rotated


def rotate_cw(coords: Block) -> Block:
    return rotate_block(90, coords)


def rotate_ccw(coords: Block) -> Block:
    return rotate_block(- 90, coords)


def new_arena(cols: int, rows: int) -> Arena:
    return [[0 for i in range(cols)] for j in range(rows)]


def is_occupied(arena: Arena, x: int, y: int) -> bool:
    if 0 <= x < len(arena[0]) and 0 <= y < len(arena):
        return bool(arena[y][x])

    return True


def set_occupied(arena: Arena, x: int, y: int, occupied: bool) -> None:
    if 0 <= x < len(arena[0]) and 0 <= y < len(arena):
        arena[y][x] = int(occupied)

    return None


def draw(arena: Arena, score: int) -> None:
    for row in range(len(arena) + 1):
        for col in range(len(arena[0]) + 2):
            if col == 0 or col == len(arena[0]) + 1 or row == len(arena):
                print(WALL, end="")
            else:
                if arena[row][col - 1] == 1:
                    print(SQUARE, end="")
                else:
                    print(EMPTY, end="")
        print()

    print("  Score:", end="")
    print(str(score).rjust(2 * (len(arena[0]) - 3)))


def next_block() -> Block:
    block = coords(randint(0, 6))
    rotate = randint(0, 3)

    for i in range(rotate):
        block = rotate_block(90, block)

    return block


def try_moving(arena: Arena, x: int, y: int, active_block: Block,
               x_diff: int, y_diff: int) -> int:
    for coord in active_block:
        if is_occupied(arena, coord[0] + x + x_diff, coord[1] + y + y_diff):
            return 0

    return 1


def event_check(arena: Arena, x: int, y: int,
                active_block: Block, event: int, score: int) \
        -> Tuple[Arena, Block, int, int, int, bool]:

    running = True

    if event == LEFT:
        x -= try_moving(arena, x, y, active_block, - 1, 0)

    elif event == RIGHT:
        x += try_moving(arena, x, y, active_block, 1, 0)

    elif event == ROTATE_CW:
        diff = try_moving(arena, x, y, rotate_cw(active_block), 0, 0)
        active_block = active_block if diff == 0 else rotate_cw(active_block)

    elif event == ROTATE_CCW:
        diff = try_moving(arena, x, y, rotate_ccw(active_block), 0, 0)
        active_block = active_block if diff == 0 else rotate_ccw(active_block)

    elif event == DOWN:
        y += try_moving(arena, x, y, active_block, 0, 1)

    elif event == DROP:
        while try_moving(arena, x, y, active_block, 0, 1) == 1:
            y += 1

        update_arena(arena, active_block, x, y, True)
        active_block = next_block()
        y = abs(min(active_block, key=lambda i: i[1])[1])
        x = find_spawn_x(arena, active_block)
        arena, score = score_check(arena, score)

    else:
        running = False

    return arena, active_block, x, y, score, running


def poll_event() -> int:
    return int(input("Event number (0-6): "))


def score_check(arena: Arena, score: int) -> Tuple[Arena, int]:
    updated_arena: Arena = []
    for i in range(len(arena) - 1, - 1, - 1):
        if sum(arena[i]) != len(arena[0]):
            updated_arena.insert(0, arena[i])

    score += (len(arena) - len(updated_arena)) ** 2

    for i in range(len(arena) - len(updated_arena)):
        updated_arena.insert(0, [0 for i in range(len(arena[0]))])

    return updated_arena, score


def update_arena(arena: Arena, active_block: Block,
                 x: int, y: int, occupied: bool) -> None:

    for coord in active_block:
        set_occupied(arena, coord[0] + x, coord[1] + y, occupied)


def find_spawn_x(arena: Arena, active_block: Block) -> int:
    x_list = []
    for coord in active_block:
        x_list.append(coord[0])

    most_left = abs(min(active_block, key=lambda x: x[0])[0])
    spawn_x = (len(arena[0]) - len(set(x_list))) // 2

    return spawn_x + most_left


def play(arena: Arena) -> int:
    active_block = next_block()
    arena_x = find_spawn_x(arena, active_block)
    arena_y = abs(min(active_block, key=lambda x: x[1])[1])
    running = True
    score = 0

    while try_moving(arena, arena_x, arena_y, active_block, 0, 0) == 1 \
            and running:

        update_arena(arena, active_block, arena_x, arena_y, True)
        draw(arena, score)
        update_arena(arena, active_block, arena_x, arena_y, False)
        event = poll_event()

        if try_moving(arena, arena_x, arena_y, active_block, 0, 1) == 0 \
                and event == DOWN:
            event = DROP

        arena, active_block, arena_x, arena_y, score, running = \
            event_check(arena, arena_x, arena_y,
                        active_block, event, score)

    if not running:
        update_arena(arena, active_block, arena_x, arena_y, True)

    draw(arena, score)

    return score


if __name__ == "__main__":
    print("Number 0 -> move left")
    print("Number 1 -> move right")
    print("Number 2 -> rotate right")
    print("Number 3 -> rotate left")
    print("Number 4 -> move down")
    print("Number 5 -> drop")
    print("Number 6 -> quit")
    print()

    play(new_arena(6, 6))
