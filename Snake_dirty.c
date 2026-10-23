/*
 * Snake_dirty.c
 * ---------------------------------------------------------------------------
 * Same game as Snake.c (same controls, speed, collision rules, colors), but
 * with a "change list" renderer:
 *
 *   - A snakeGrid[][] occupancy array mirrors the game state.
 *   - Every time a cell changes (head drawn, tail erased, food moved) the
 *     coordinate is pushed onto changeList[] via markDirty(y, x). A dirtyFlag
 *     grid prevents the same cell being listed twice in one frame.
 *   - printFrame() walks ONLY changeList[], converts each game (y, x) into a
 *     terminal (row n, col m) using  n = y + 1,  m = x * definition + 1,
 *     jumps there with CSI n;m H  ("\033[%d;%dH") and prints just that cell.
 *
 * Nothing else about gameplay was altered.
 * ---------------------------------------------------------------------------
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <sys/select.h>
#include <termios.h>

#define GAME_HEIGHT 10
#define GAME_WIDTH 20
#define MAX_SNAKE_LEN (GAME_HEIGHT * GAME_WIDTH)

typedef struct {
    int x;
    int y;
} Point;

/* ------------------------------------------------------------------ */
/* Change-list (dirty cell) tracking                                   */
/* ------------------------------------------------------------------ */
typedef struct {
    int y;
    int x;
} Change;

static Change changeList[GAME_HEIGHT * GAME_WIDTH]; /* coords needing redraw */
static int    changeCount = 0;
static int    dirtyFlag[GAME_HEIGHT][GAME_WIDTH];  /* de-dupe per frame      */

/* Occupancy mirror of the board: 1 where a snake segment sits, else 0. */
static int snakeGrid[GAME_HEIGHT][GAME_WIDTH];

/* Record that game cell (y, x) must be redrawn on the next frame. */
static void markDirty(int y, int x) {
    if (y < 0 || y >= GAME_HEIGHT || x < 0 || x >= GAME_WIDTH) return;
    if (dirtyFlag[y][x]) return;           /* already listed this frame */
    dirtyFlag[y][x] = 1;
    changeList[changeCount].y = y;
    changeList[changeCount].x = x;
    changeCount++;
}

/* Used once at start-up so the first frame paints the whole board. */
static void markAllDirty(void) {
    for (int y = 0; y < GAME_HEIGHT; y++)
        for (int x = 0; x < GAME_WIDTH; x++)
            markDirty(y, x);
}

/* ------------------------------------------------------------------ */
/* Terminal helpers (unchanged)                                        */
/* ------------------------------------------------------------------ */
struct termios old_settings;

void init_terminal() {
    struct termios new_settings;
    tcgetattr(STDIN_FILENO, &old_settings);
    new_settings = old_settings;
    new_settings.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &new_settings);
}

void reset_terminal() {
    tcsetattr(STDIN_FILENO, TCSANOW, &old_settings);
}

int kbhit() {
    struct timeval tv = {0L, 0L};
    fd_set fds;
    FD_ZERO(&fds);
    FD_SET(STDIN_FILENO, &fds);
    return select(STDIN_FILENO + 1, &fds, NULL, NULL, &tv);
}

/* ------------------------------------------------------------------ */
/* Rendering: only the listed changes are written to the terminal      */
/* ------------------------------------------------------------------ */
/* Draw one game cell at its terminal position.                        */
static void drawCell(int y, int x, Point food, int definition, const char* pixel) {
    int color_code = 8;                       /* background */
    if (snakeGrid[y][x]) {
        color_code = 10;                      /* snake      */
    } else if (x == food.x && y == food.y) {
        color_code = 1;                       /* food       */
    }

    /* game (y, x)  ->  terminal (n, m): rows/cols are 1-based,
       and each game cell is `definition` characters wide.               */
    int n = y + 1;
    int m = x * definition + 1;
    printf("\033[%d;%dH", n, m);              /* CSI n ; m H */
    for (int d = 0; d < definition; d++) {
        printf(pixel, color_code);
    }
}

static void printFrame(Point food, int definition, const char* pixel) {
    for (int i = 0; i < changeCount; i++) {
        int y = changeList[i].y;
        int x = changeList[i].x;
        drawCell(y, x, food, definition, pixel);
        dirtyFlag[y][x] = 0;
    }
    changeCount = 0;
    /* Park the cursor under the board so stray output never lands on it. */
    printf("\033[%d;1H", GAME_HEIGHT + 1);
    fflush(stdout);
}

/* ------------------------------------------------------------------ */
int main() {
    srand(time(NULL));
    init_terminal();

    int dx = 1, dy = 0;
    Point food = {2, 2};

    Point snake[MAX_SNAKE_LEN];
    int snake_len = 1;
    snake[0].x = 9;
    snake[0].y = 9;

    int definition = 2;
    char pixel[] = "\033[48;5;%dm \033[0m";

    /* Initial board state + full first paint */
    snakeGrid[snake[0].y][snake[0].x] = 1;
    printf("\033[2J\033[?25l");
    fflush(stdout);
    markAllDirty();
    printFrame(food, definition, pixel);

    while (1) {
        if (kbhit()) {
            char ch = getchar();
            int nx = 0, ny = 0, valid_key = 0;

            if (ch == 'w') { nx = 0;  ny = -1; valid_key = 1; }
            else if (ch == 's') { nx = 0;  ny = 1;  valid_key = 1; }
            else if (ch == 'a') { nx = -1; ny = 0;  valid_key = 1; }
            else if (ch == 'd') { nx = 1;  ny = 0;  valid_key = 1; }
            else if (ch == 'q') { break; }
            if (valid_key && (dx != -nx || dy != -ny)) {
                dx = nx;
                dy = ny;
            }
        }

        Point head = {snake[0].x + dx, snake[0].y + dy};

        if (head.x < 0 || head.x >= GAME_WIDTH || head.y < 0 || head.y >= GAME_HEIGHT) {
            break;
        }

        int self_collision = 0;
        for (int i = 0; i < snake_len; i++) {
            if (head.x == snake[i].x && head.y == snake[i].y) {
                self_collision = 1;
                break;
            }
        }
        if (self_collision) break;

        if (head.x == food.x && head.y == food.y) {
            /* Grow: shift every segment back, insert new head */
            for (int i = snake_len; i > 0; i--) {
                snake[i] = snake[i - 1];
            }
            snake[0] = head;
            snake_len++;

            /* --- change list: FUTURE coordinate of the head --- */
            snakeGrid[head.y][head.x] = 1;
            markDirty(head.y, head.x);           /* (was the food cell) */

            /* --- change list: PAST + FUTURE coordinates of the food --- */
            markDirty(food.y, food.x);           /* old food spot (same as head here) */
            food.x = rand() % GAME_WIDTH;
            food.y = rand() % GAME_HEIGHT;
            markDirty(food.y, food.x);           /* new food spot */
        } else {
            /* Move: remember the tail BEFORE shifting so we can erase it */
            Point tail = snake[snake_len - 1];

            for (int i = snake_len - 1; i > 0; i--) {
                snake[i] = snake[i - 1];
            }
            snake[0] = head;

            /* --- change list: PAST coordinate (tail leaves) --- */
            snakeGrid[tail.y][tail.x] = 0;
            markDirty(tail.y, tail.x);

            /* --- change list: FUTURE coordinate (head arrives) --- */
            snakeGrid[head.y][head.x] = 1;
            markDirty(head.y, head.x);
        }

        /* Only the cells in changeList[] get written to the terminal */
        printFrame(food, definition, pixel);

        if (dy != 0) {
            usleep(110000);
        } else {
            usleep(80000);
        }
    }

    reset_terminal();
    printf("\033[2J\033[H\033[?25hGame Over!\n");
    return 0;
}
