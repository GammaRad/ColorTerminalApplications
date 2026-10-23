
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/select.h>
#include <termios.h>

#define H 24
#define W 30
#define BUFFER_SIZE 64
#define VISIBLE_W (W - 3
#define CELL_COLS 2            

typedef struct {
    int val;                  
    char bg[BUFFER_SIZE];    
    int is_bg;                
} Cell;

Cell gameArray[H][W];
int gameRun = 1;
char birdEye = '^';
char prevBirdEye = '^';
int birdY = 12;
int birdMoveState = 0;

int colorList[4][3] = {
    {62, 191, 11},   // 0
    {48, 145, 10},   // 1
    {33, 117, 55},   // 2
    {255, 208, 1}    // 3: Bird
};

typedef struct {
    int y;
    int x;
} Change;

static Change changeList[H * W];
static int    changeCount = 0;
static int    dirtyFlag[H][W];

static void markDirty(int y, int x) {
    if (y < 0 || y >= H || x < 0 || x >= VISIBLE_W) return;  
    if (dirtyFlag[y][x]) return;
    dirtyFlag[y][x] = 1;
    changeList[changeCount].y = y;
    changeList[changeCount].x = x;
    changeCount++;
}

static void markAllDirty(void) {
    for (int y = 0; y < H; y++)
        for (int x = 0; x < VISIBLE_W; x++)
            markDirty(y, x);
}


static int cellsLookSame(const Cell* a, const Cell* b) {
    return a->is_bg == b->is_bg && a->val == b->val;
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

void getBGpixel(int y, int x, Cell* cell) {
    cell->is_bg = 1;
    cell->val = -1;
    if (y <= 21 && x <= 27) {
        strcpy(cell->bg, "\033[48;5;14m \033[0m");
    } else if (y == 22) {
        if (x % 2 == 0) strcpy(cell->bg, "\x1b[48;5;10m \x1b[0m");
        else strcpy(cell->bg, "\x1b[48;5;2m \x1b[0m");
    } else if (y == 23) {
        strcpy(cell->bg, "\x1b[48;2;230;211;151m \x1b[0m");
    }
}

static void setBackground(int y, int x) {
    getBGpixel(y, x, &gameArray[y][x]);
    markDirty(y, x);
}

static void setValue(int y, int x, int val) {
    gameArray[y][x].val = val;
    gameArray[y][x].is_bg = 0;
    markDirty(y, x);
}

void createPipePair(int height) {
    for (int i = 0; i < height; i++) {
        for (int k = 1; k < 4; k++) {
            int targetX = W - k;
            setValue(H - 1 - i, targetX, abs(k - 2) * -1 + 1);
        }
        if (i == height - 1) {
            for (int a = 1; a < 3; a++) {
                for (int j = 3; j > 0; j--) {
                    int targetX = W - j;
                    setValue(H - (a + 1) - i, targetX, a);
                }
            }
        }
    }
    for (int i = 0; i < (H - height - 8); i++) {
        for (int k = 1; k < 4; k++) {
            int targetX = W - k;
            setValue(i, targetX, abs(k - 2) * -1 + 1);
        }
        if (i == (H - height - 9)) {
            for (int a = 1; a < 3; a++) {
                for (int j = 3; j > 0; j--) {
                    int targetX = W - j;
                    setValue(i + a, targetX, a);
                }
            }
        }
    }
}

int shiftPipes() {
    for (int y = 0; y < H; y++) {
        for (int x = 0; x < W; x++) {
            if (!gameArray[y][x].is_bg && (gameArray[y][x].val == 0 || gameArray[y][x].val == 1 || gameArray[y][x].val == 2)) {
                if (x == 0) {
                    setBackground(y, x);                       
                } else {
                    if (!gameArray[y][x - 1].is_bg && gameArray[y][x - 1].val == 3) {
                        printf("Player hit pipe\n");
                        return 0; 
                    }
                    if (!cellsLookSame(&gameArray[y][x - 1], &gameArray[y][x])) {
                        gameArray[y][x - 1] = gameArray[y][x];
                        markDirty(y, x - 1);
                    } else {
                        gameArray[y][x - 1] = gameArray[y][x];
                    }
                    if (x + 1 >= W || gameArray[y][x + 1].is_bg) {
                        setBackground(y, x);
                    }
                }
            }
        }
    }
    return 1;
}


static void drawCell(int y, int x) {
    int n = y + 1;                 
    int m = x * CELL_COLS + 1;     
    printf("\033[%d;%dH", n, m);   

    if (gameArray[y][x].is_bg) {
        printf("%s%s", gameArray[y][x].bg, gameArray[y][x].bg);
    } else {
        int val = gameArray[y][x].val;
        if (val != 3) {
            printf("\033[48;2;%d;%d;%dm  \033[0m", colorList[val][0], colorList[val][1], colorList[val][2]);
        } else {
            printf("\033[48;2;%d;%d;%dm\033[38;5;0m«%c\033[0m", colorList[val][0], colorList[val][1], colorList[val][2], birdEye);
        }
    }
}

void printGame() {
    printf("\033[?25l");

    if (birdEye != prevBirdEye) {
        markDirty(birdY, 8);
        prevBirdEye = birdEye;
    }

    for (int i = 0; i < changeCount; i++) {
        int y = changeList[i].y;
        int x = changeList[i].x;
        drawCell(y, x);
        dirtyFlag[y][x] = 0;
    }
    changeCount = 0;
}

int moveBird() {
    int offset = 0;
    if (birdMoveState == 4 || birdMoveState == 3) offset = -1;
    else if (birdMoveState == 2) offset = 0;
    else if (birdMoveState == 1 || birdMoveState == 0) offset = 1;

    if (offset != 0) {
        int newY = birdY + offset;
        if (newY < 0 || newY > 21) {
            if (newY > 21) printf("Player hit bottom\n");
            else printf("Player hit top\n");
            return 0;
        } else if (!gameArray[newY][8].is_bg) {
            printf("Player hit pipe\n");
            return 0;
        } else {
            setBackground(birdY, 8);     
            birdY = newY;
            setValue(birdY, 8, 3);       
        }
    }
    return 1;
}

int main() {
    srand(time(NULL));
    init_terminal();

    while (gameRun) {
        birdMoveState = 0;
        printf("\033[2J\033[H\033[?25l");
        fflush(stdout);


        changeCount = 0;
        memset(dirtyFlag, 0, sizeof(dirtyFlag));
        for (int y = 0; y < H; y++) {
            for (int x = 0; x < W; x++) {
                getBGpixel(y, x, &gameArray[y][x]);
            }
        }
        markAllDirty();

        birdY = 12;
        setValue(birdY, 8, 3);
        birdEye = '^';
        prevBirdEye = '^';

        int a = 0;
        double gameDifficulty = 0.0;
        int pipeIter = -1;
        int score = 0;

        while (1) {
            if (kbhit()) {
                char key = getchar();
                if (key == 'w') {
                    birdMoveState = 4;
                } else if (key == 'q') {
                    gameRun = 0;
                    break;
                }
            } else {
                birdMoveState = (birdMoveState != 0) ? (birdMoveState - 1) : birdMoveState;
            }

            if (!moveBird()) break;
            birdEye = (birdMoveState > 0) ? '^' : 'v';

            if (pipeIter % 20 == 0) {
                createPipePair((rand() % 15) + 1);
                pipeIter = 0;
                a += 1;
                if (a % 7 == 0) gameDifficulty += 0.01;
            }

            if (!shiftPipes()) break;
            printGame();

            printf("\033[%d;1H\033[2K", H + 1);
            printf("Score=%d GameDifficulty=%.2f\n", score, gameDifficulty);
            fflush(stdout);

            if (pipeIter == -1) {
                while (1) {
                    if (kbhit()) {
                        char key = getchar();
                        if (key == 'w') break;
                        if (key == 'q') {
                            gameRun = 0;
                            break;
                        }
                    }
                    usleep(10000);
                }
            }

            if (!gameRun) break;

            long sleepTime = (long)((0.07 - gameDifficulty) * 1000000);
            if (sleepTime > 0) usleep(sleepTime);

            pipeIter += 1;
            if (pipeIter == 19) score += 1;
        }

        if (!gameRun) break;
        printf("You died. Restarting....\n");
        fflush(stdout);
        sleep(1);
    }

    reset_terminal();
    printf("\033[2J\033[H\033[?25h exit executed.\n");
    return 0;
}
