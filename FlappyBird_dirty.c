/*
 * FlappyBird_dirty.c
 * ---------------------------------------------------------------------------
 * Same game as FlappyBird.c (same bird physics, pipe generation, difficulty
 * ramp, scoring, keys), but with a "change list" renderer that replaces the
 * old prevFrameArray full-grid comparison:
 *
 *   - Every mutation of gameArray (bird moves, pipes shift, pipe spawned,
 *     cell reset to background) records its coordinate on changeList[] via
 *     markDirty(y, x). When the bird or a pipe moves, both its PAST cell
 *     (reset to background) and its FUTURE cell are listed. A dirtyFlag grid
 *     de-duplicates within one frame.
 *   - Cells in the hidden spawn strip (x >= W - 3) are never listed because
 *     the original never drew them either.
 *   - printGame() walks ONLY changeList[], converts game (y, x) to terminal
 *     (row n, col m) with  n = y + 1,  m = x * 2 + 1  (each cell is 2 columns
 *     wide), jumps there with CSI n;m H ("\033[%d;%dH"), and prints that cell.
 *   - The score line is placed on row H + 1 and the cursor is left on row
 *     H + 2, which is exactly where the original left it, so the
 *     "Player hit ..." / "You died" messages appear in the same place.
 *
 * Gameplay logic is otherwise identical to the original.
 * ---------------------------------------------------------------------------
 */
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
#define VISIBLE_W (W - 3)      /* columns actually drawn, as in the original */
#define CELL_COLS 2            /* each game cell is 2 terminal columns wide  */

// Struct to handle multi-datatype grid natively
typedef struct {
    int val;                  // 0, 1, 2, 3 for pipes/bird
    char bg[BUFFER_SIZE];    // stores custom ANSI bg pixel string
    int is_bg;                // flag indicating grid cell is background
} Cell;

// Global Variables
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

/* ------------------------------------------------------------------ */
/* Change-list (dirty cell) tracking                                   */
/* ------------------------------------------------------------------ */
typedef struct {
    int y;
    int x;
} Change;

static Change changeList[H * W];
static int    changeCount = 0;
static int    dirtyFlag[H][W];

static void markDirty(int y, int x) {
    if (y < 0 || y >= H || x < 0 || x >= VISIBLE_W) return;   /* off-screen strip ignored */
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

/* Two cells look the same on screen if is_bg and val agree
   (this is the exact test the original prevFrameArray compare used). */
static int cellsLookSame(const Cell* a, const Cell* b) {
    return a->is_bg == b->is_bg && a->val == b->val;
}

// Terminal management functions
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

/* Helper: reset a grid cell to background AND list the change. */
static void setBackground(int y, int x) {
    getBGpixel(y, x, &gameArray[y][x]);
    markDirty(y, x);
}

/* Helper: put a pipe/bird value into a grid cell AND list the change. */
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
                    setBackground(y, x);                       /* PAST cell leaves screen */
                } else {
                    if (!gameArray[y][x - 1].is_bg && gameArray[y][x - 1].val == 3) {
                        printf("Player hit pipe\n");
                        return 0; // Collision crash trigger
                    }
                    /* FUTURE cell: copy pipe one column left, list it only if it changes */
                    if (!cellsLookSame(&gameArray[y][x - 1], &gameArray[y][x])) {
                        gameArray[y][x - 1] = gameArray[y][x];
                        markDirty(y, x - 1);
                    } else {
                        gameArray[y][x - 1] = gameArray[y][x];
                    }
                    /* PAST cell: trailing edge of the pipe becomes background */
                    if (x + 1 >= W || gameArray[y][x + 1].is_bg) {
                        setBackground(y, x);
                    }
                }
            }
        }
    }
    return 1;
}

/* ------------------------------------------------------------------ */
/* Rendering                                                           */
/* ------------------------------------------------------------------ */
static void drawCell(int y, int x) {
    int n = y + 1;                 /* terminal row    (1-based) */
    int m = x * CELL_COLS + 1;     /* terminal column (1-based) */
    printf("\033[%d;%dH", n, m);   /* CSI n ; m H */

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

    /* If only the bird's eye glyph changed, that cell still needs a repaint. */
    if (birdEye != prevBirdEye) {
        markDirty(birdY, 8);
        prevBirdEye = birdEye;
    }

    /* Walk ONLY the listed changes and repaint them in place. */
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
            setBackground(birdY, 8);     /* PAST bird cell   */
            birdY = newY;
            setValue(birdY, 8, 3);       /* FUTURE bird cell */
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

        /* Fresh board: fill with background, then list every visible cell
           once so the first frame paints the full screen. After that, only
           changed cells are ever written. */
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

            /* Score line on the row under the board; cursor ends on row H+2
               (same place the original left it). */
            printf("\033[%d;1H\033[2K", H + 1);
            printf("Score=%d GameDifficulty=%.2f\n", score, gameDifficulty);
            fflush(stdout);

            // Match Python's exact starting loop pause until space/w is hit
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

            // Microsecond pacing conversion math
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
