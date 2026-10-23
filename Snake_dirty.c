
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


typedef struct {
    int y;
    int x;
} Change;

static Change changeList[GAME_HEIGHT * GAME_WIDTH]; 
static int    changeCount = 0;
static int    dirtyFlag[GAME_HEIGHT][GAME_WIDTH]; 

static int snakeGrid[GAME_HEIGHT][GAME_WIDTH];

static void markDirty(int y, int x) {
    if (y < 0 || y >= GAME_HEIGHT || x < 0 || x >= GAME_WIDTH) return;
    if (dirtyFlag[y][x]) return;           
    dirtyFlag[y][x] = 1;
    changeList[changeCount].y = y;
    changeList[changeCount].x = x;
    changeCount++;
}

static void markAllDirty(void) {
    for (int y = 0; y < GAME_HEIGHT; y++)
        for (int x = 0; x < GAME_WIDTH; x++)
            markDirty(y, x);
}


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


static void drawCell(int y, int x, Point food, int definition, const char* pixel) {
    int color_code = 8;                       
    if (snakeGrid[y][x]) {
        color_code = 10;                      
    } else if (x == food.x && y == food.y) {
        color_code = 1;                      
    }


    int n = y + 1;
    int m = x * definition + 1;
    printf("\033[%d;%dH", n, m);              
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
    printf("\033[%d;1H", GAME_HEIGHT + 1);
    fflush(stdout);
}

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
            for (int i = snake_len; i > 0; i--) {
                snake[i] = snake[i - 1];
            }
            snake[0] = head;
            snake_len++;

            snakeGrid[head.y][head.x] = 1;
            markDirty(head.y, head.x);          

            markDirty(food.y, food.x);           
            food.x = rand() % GAME_WIDTH;
            food.y = rand() % GAME_HEIGHT;
            markDirty(food.y, food.x);           
        } else {
            Point tail = snake[snake_len - 1];

            for (int i = snake_len - 1; i > 0; i--) {
                snake[i] = snake[i - 1];
            }
            snake[0] = head;

            snakeGrid[tail.y][tail.x] = 0;
            markDirty(tail.y, tail.x);

            snakeGrid[head.y][head.x] = 1;
            markDirty(head.y, head.x);
        }

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
