#include "minesweeper.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define UNUSED(A) (void) (A)

/**
 * @brief Counts and checks neighbours depending on the given function
 *
 * @param cell The cell we are counting the neighbours of (pointer)
 * @param row First index of the cell
 * @param col Second index of the cell
 * @param rows Number of rows
 * @param cols Number of cols
 * @param board 2D array that represents the mines board
 * @return if counting mines -> 0 if given number of neighboring mines does not
 * equal counted mines, otherwise 1 if counting unrevealed -> counted unrevealed
 * neighbours
 */
bool count_surrounding_mines(uint16_t *cell, size_t row, size_t col, size_t rows, size_t cols, uint16_t board[rows][cols]);

/**
 * @brief Counts cells depending on what function is given function in argument
 *
 * @param rows Number of rows
 * @param cols Number of cols
 * @param board 2D array that represents the mines board
 * @param f Function deciding what should be counted
 * @return Number of mines or flags
 */
int count_requested(size_t rows, size_t cols, uint16_t board[rows][cols], bool (*f)(uint16_t));

/**
 * @brief Prints the top row of numbers representing columns
 *
 * @param cols Number of cols
 */
void print_col_nums(size_t cols);

/**
 * @brief Prints numbers representing rows
 *
 * @param i First index
 * @param j Second index
 */
void print_row_nums(size_t i, size_t j);

/**
 * @brief Prints body of the cell
 *
 * @param i First index
 * @param j Second index
 * @param rows Number of rows
 * @param cols Number of cols
 * @param board 2D array that represents the mines board
 */
void print_cell_body(size_t i, size_t j, size_t rows, size_t cols, uint16_t board[rows][cols]);

/**
 * Checks whether the cell is not revealed
 *
 * @param cell Single cell representation from the board
 * @return True is cell is not revealed, otherwise false
 */
bool not_revealed(uint16_t cell);

/**
 * Similar to 'set_cell', but takes only 'X' and '0' - '8' values
 *
 * @param cell Single cell representation from the board (pointer)
 * @param val The character representation of the cell
 * @return True if the function ran successfully, otherwise false
 */
bool set_cell_bonus(uint16_t *cell, char val);

/**
 * Similar to 'load_board', but loads only 'X' and '0' - '8' inputs
 *
 * @param rows Number of rows
 * @param cols Number of cols
 * @param board 2D array that represents the mines board
 */
void load_board_bonus(size_t rows, size_t cols, uint16_t board[rows][cols]);

/**
 * Puts an flag on all the unrevealed and unflagged neighbours of the cell
 *
 * @param row First index of the cell
 * @param col Second index of the cell
 * @param rows Number of rows
 * @param cols Number of cols
 * @param board 2D array that represents the mines board
 * @return Number of neighbours that were flagged
 */
int flag_neighbours(size_t row, size_t col, size_t rows, size_t cols, uint16_t board[rows][cols]);

/**
 * Sets all cells to 'X'
 *
 * @param rows Number of rows
 * @param cols Number of cols
 * @param board 2D array that represents the mines board
 */
void hide_all_cells(size_t rows, size_t cols, uint16_t board[rows][cols]);

/**
 * Check whether the cell has wrong flag
 *
 * @param cell Single cell representation from the board
 * @return True if the flag is wrong, otherwise false
 */
bool is_wrong_flag(uint16_t cell);

/**
 * Checks whether the number was given during the cell initialisation
 *
 * @param cell Single cell representation from the board
 * @return True if number was given, otherwise false
 */
bool is_number(uint16_t cell);

/**
 * Counts unrevealed cells around the given cell
 *
 * @param row First index of the cell
 * @param col Second index of the cell
 * @param rows Number of rows
 * @param cols Number of cols
 * @param board 2D array that represents the mines board
 * @return Number of unrevealed neighbours
 */
int count_unrevealed_neighbours(size_t row, size_t col, size_t rows, size_t cols, uint16_t board[rows][cols]);

/* ************************************************************** *
 *                         HELP FUNCTIONS                         *
 * **********************************************-**************** */

bool is_flag(uint16_t cell)
{
    return (0x40 & cell) || (0x80 & cell);
}

bool is_mine(uint16_t cell)
{
    return (0x20 & cell);
}

bool is_revealed(uint16_t cell)
{
    return !(0x10 & cell);
}

int get_number(uint16_t cell)
{
    if (is_mine(cell))
        return 0;

    return cell & 0xf;
}

bool not_revealed(uint16_t cell)
{
    return 0x10 & cell;
}

bool is_wrong_flag(uint16_t cell)
{
    return 0x80 & cell;
}

bool is_number(uint16_t cell)
{
    return 0x200 & cell;
}

/* ************************************************************** *
 *                         INPUT FUNCTIONS                        *
 * ************************************************************** */

bool set_cell(uint16_t *cell, char val)
{
    if (cell == NULL) {
        return false;
    }

    val = toupper(val);
    if (val == 'X') {
        *cell = 0x10;
    } else if (val == 'M') {
        *cell = 0x30;
    } else if (val == 'F') {
        *cell = 0x70;
    } else if (val == 'W') {
        *cell = 0x90;
    } else if (val == '.') {
        *cell = 0x100;
    } else if (0 <= (val - '0') && (val - '0') <= 8) {
        *cell = 0x200 + (val - '0');
    } else {
        return false;
    }
    return true;
}

int load_board(size_t rows, size_t cols, uint16_t board[rows][cols])
{
    if (rows > MAX_SIZE || cols > MAX_SIZE || rows < MIN_SIZE ||
            cols < MIN_SIZE) {
        return -1;
    }

    size_t read = 0;
    int ch;
    while (read < rows * cols && (ch = getchar()) != EOF) {
        if (set_cell(&board[0][read], (char) ch)) {
            read++;
        }
    }

    if (read < rows * cols) {
        return -1;
    }

    return postprocess(rows, cols, board);
}

int postprocess(size_t rows, size_t cols, uint16_t board[rows][cols])
{
    int counter = 0;
    if (rows > MAX_SIZE || cols > MAX_SIZE || rows < MIN_SIZE ||
            cols < MIN_SIZE) {
        return -1;
    }
    if (is_mine(board[0][0]) || is_mine(board[0][cols - 1]) ||
            is_mine(board[rows - 1][cols - 1]) || is_mine(board[rows - 1][0])) {
        return -1;
    }

    for (size_t i = 0; i < rows; i++) {
        for (size_t j = 0; j < cols; j++) {
            if (is_mine(board[i][j])) {
                counter++;
            } else if (!count_surrounding_mines(&board[i][j], i, j, rows, cols, board)) {
                return -1;
            }
        }
    }
    if (counter <= 0) {
        return -1;
    }

    return counter;
}

bool count_surrounding_mines(uint16_t *cell, size_t row, size_t col, size_t rows, size_t cols, uint16_t board[rows][cols])
{
    int x = (int) row, y = (int) col, counter = 0;

    for (int i = -1; i < 2; i++) {
        for (int j = -1; j < 2; j++) {
            if (x + i >= 0 && x + i < (int) rows && y + j >= 0 && y + j < (int) cols &&
                    is_mine(board[x + i][y + j])) {
                counter++;
            }
        }
    }

    if (is_number(*cell) && counter != get_number(*cell)) {
        return false;
    }

    if (!is_number(*cell)) {
        *cell |= counter;
    }

    return true;
}

/* ************************************************************** *
 *                        OUTPUT FUNCTIONS                        *
 * ************************************************************** */

int print_board(size_t rows, size_t cols, uint16_t board[rows][cols])
{
    print_col_nums(cols);
    for (size_t i = 0; i < rows * 2 + 1; i++) {
        for (size_t j = 0; j < cols; j++) {
            if (i % 2 == 0) {
                if (j == 0)
                    printf("   ");
                printf("+---");
            } else {
                print_row_nums(i, j);
                print_cell_body(i, j, rows, cols, board);
            }
        }
        if (i % 2 == 0) {
            printf("+\n");
        } else {
            printf("|\n");
        }
    }
    return 0;
}

void print_col_nums(size_t cols)
{
    printf("   ");
    for (size_t i = 0; i < cols; i++) {
        if (i > 9) {
            printf(" %lu ", i);
        } else {
            printf("  %lu ", i);
        }
    }
    printf("\n");
}

void print_row_nums(size_t i, size_t j)
{
    if (j == 0) {
        if (i / 2 < 10) {
            printf(" %lu ", i / 2);
        } else {
            printf("%lu ", i / 2);
        }
    }
}

void print_cell_body(size_t i, size_t j, size_t rows, size_t cols, uint16_t board[rows][cols])
{
    char to_print = show_cell(board[i / 2][j]);
    switch (to_print) {
    case 'X':
        printf("|XXX");
        break;
    case 'F':
        printf("|_F_");
        break;
    default:
        printf("| %c ", to_print);
        break;
    }
}

char show_cell(uint16_t cell)
{
    if (is_flag(cell)) {
        return 'F';
    }
    if (!is_revealed(cell)) {
        return 'X';
    }
    if (is_mine(cell)) {
        return 'M';
    }
    if (get_number(cell) == 0) {
        return ' ';
    }
    return ('0' + get_number(cell));
}

/* ************************************************************** *
 *                    GAME MECHANIC FUNCTIONS                     *
 * ************************************************************** */

int reveal_cell(size_t rows, size_t cols, uint16_t board[rows][cols], size_t row, size_t col)
{
    int single_output;
    uint16_t *cell = &board[row][col];

    if (row >= rows || col >= cols)
        return -1;

    single_output = reveal_single(cell);
    if (single_output == 0 && get_number(*cell) == 0)
        reveal_floodfill(rows, cols, board, row, col);

    return single_output;
}

int reveal_single(uint16_t *cell)
{
    if (cell == NULL)
        return -1;

    if (is_revealed(*cell) || (is_flag(*cell)))
        return -1;

    *cell &= 0xffef;

    if (is_mine(*cell))
        return 1;

    return 0;
}

void reveal_floodfill(size_t rows, size_t cols, uint16_t board[rows][cols], size_t row, size_t col)
{
    int x = (int) row, y = (int) col;

    for (int i = -1; i < 2; i++) {
        for (int j = -1; j < 2; j++) {
            if (x + i >= 0 && x + i < (int) rows && y + j >= 0 && y + j < (int) cols &&
                    !is_revealed(board[x + i][y + j])) {
                if (is_wrong_flag(board[x + i][y + j])) {
                    board[x + i][y + j] &= 0xff7f;
                }
                reveal_cell(rows, cols, board, x + i, y + j);
            }
        }
    }
}

int flag_cell(size_t rows, size_t cols, uint16_t board[rows][cols], size_t row, size_t col)
{
    if (is_revealed(board[row][col]))
        return INT16_MIN;
    if (is_mine(board[row][col])) {
        board[row][col] ^= 0x40;
    } else {
        board[row][col] ^= 0x80;
    }

    return count_requested(rows, cols, board, is_mine) -
            count_requested(rows, cols, board, is_flag);
}

bool is_solved(size_t rows, size_t cols, uint16_t board[rows][cols])
{
    return count_requested(rows, cols, board, is_mine) ==
            count_requested(rows, cols, board, not_revealed);
}

int count_requested(size_t rows, size_t cols, uint16_t board[rows][cols], bool (*f)(uint16_t))
{
    int counter = 0;
    for (size_t i = 0; i < rows * cols; i++) {
        if (f(*(board[0] + i)))
            counter++;
    }
    return counter;
}

/* ************************************************************** *
 *                         BONUS FUNCTIONS                        *
 * ************************************************************** */

int generate_random_board(size_t rows, size_t cols, uint16_t board[rows][cols], size_t mines)
{
    if (mines > (rows * cols) - 4) {
        return -1;
    }
    if (mines == 0) {
        return -1;
    }
    hide_all_cells(rows, cols, board);

    while (mines > 0) {
        size_t row = (rand() % (rows));
        size_t col = (rand() % (cols));
        uint16_t *cell = &board[row][col];

        if (cell != &board[0][0] && cell != &board[rows - 1][0] &&
                cell != &board[0][cols - 1] && cell != &board[rows - 1][cols - 1] &&
                !is_mine(*cell)) {
            set_cell(cell, 'M');
            mines--;
        }
    }
    return postprocess(rows, cols, board);
}

void hide_all_cells(size_t rows, size_t cols, uint16_t board[rows][cols])
{
    for (size_t i = 0; i < rows * cols; i++) {
        set_cell(board[0] + i, 'X');
    }
}

int count_unrevealed_neighbours(size_t row, size_t col, size_t rows, size_t cols, uint16_t board[rows][cols])
{
    int x = (int) row, y = (int) col, counter = 0;
    for (int i = -1; i < 2; i++) {
        for (int j = -1; j < 2; j++) {
            if (x + i >= 0 && x + i < (int) rows && y + j >= 0 && y + j < (int) cols &&
                    not_revealed(board[x + i][y + j])) {
                counter++;
            }
        }
    }
    return counter;
}

int find_mines(size_t rows, size_t cols, uint16_t board[rows][cols])
{
    int counter = 0;
    uint16_t cell;
    load_board_bonus(rows, cols, board);

    for (size_t r = 0; r < rows; r++) {
        for (size_t c = 0; c < cols; c++) {
            cell = board[r][c];
            if (is_revealed(cell) &&
                    get_number(cell) ==
                            count_unrevealed_neighbours(r, c, rows, cols, board)) {
                counter += flag_neighbours(r, c, rows, cols, board);
            }
        }
    }
    return counter;
}

bool set_cell_bonus(uint16_t *cell, char val)
{
    val = toupper(val);
    if (val == 'X') {
        *cell = 0x10;
    } else if (0 <= (val - '0') && (val - '0') <= 8) {
        *cell = (val - '0');
    } else {
        return false;
    }
    return true;
}

void load_board_bonus(size_t rows, size_t cols, uint16_t board[rows][cols])
{
    int ch, i = 0;
    while ((ch = getchar()) != EOF) {
        if (set_cell_bonus(&board[0][i], (char) ch)) {
            i++;
        }
    }
}

int flag_neighbours(size_t row, size_t col, size_t rows, size_t cols, uint16_t board[rows][cols])
{
    int x = (int) row, y = (int) col, counter = 0;
    for (int i = -1; i < 2; i++) {
        for (int j = -1; j < 2; j++) {
            if (x + i >= 0 && x + i < (int) rows && y + j >= 0 && y + j < (int) cols &&
                    !is_flag(board[x + i][y + j]) && !is_revealed(board[x + i][y + j])) {
                set_cell(&board[x + i][y + j], 'F');
                counter++;
            }
        }
    }
    return counter;
}
