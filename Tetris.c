#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/select.h>
#include <termios.h>

#define BOARD_WIDTH 14
#define BOARD_HEIGHT 20
#define PIECE_COUNT 4
#define ANSI_SIZE 32

// Global Variables
char gameArray[BOARD_HEIGHT][BOARD_WIDTH][ANSI_SIZE];
char backgroundPixel[] = "\033[48;2;1;1;1m \033[0m";
int score = 0;
int gameRun = 1;
char prevColor[10] = "";

// Game Constants
const char* colorNames[] = {"Red", "Green", "Yellow", "Blue", "Orange"};
const int colorCodes[] = {9, 46, 226, 26, 208};
const char* typeList[] = {"Oblock", "Tblock", "Zblock", "Lblock", "Sblock", "Jblock", "Iblock"};

int spawnXcoordinateList[7][4] = {
    {0, 1, 0, 1}, {0, 1, 2, 1}, {0, 1, 1, 2}, {0, 0, 0, 1}, {0, 1, 1, 2}, {0, 1, 1, 1}, {0, 0, 0, 0}
};
int spawnYcoordinateList[7][4] = {
    {0, 0, 1, 1}, {0, 0, 0, 1}, {0, 0, 1, 1}, {0, 1, 2, 2}, {0, 0, 1, 1}, {0, 0, 1, 2}, {0, 1, 2, 3}
};

typedef struct {
    int y, x;
} Point;

typedef struct {
    int colorCode;
    int blockType;
    Point coords[PIECE_COUNT];
} TetrisBlock;

void calculateEndCoordinates(TetrisBlock* block, Point* endCoords);
int updateBlock(TetrisBlock* block, const char* direction);

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

void spawnBlock(TetrisBlock* block, int blockY, int blockX) {
    char blockFormat[ANSI_SIZE];
    sprintf(blockFormat, "\033[48;5;%dm \033[0m", block->colorCode);
    for (int i = 0; i < PIECE_COUNT; i++) {
        int newY = blockY + spawnYcoordinateList[block->blockType][i];
        int newX = blockX + spawnXcoordinateList[block->blockType][i];
        if (newY >= BOARD_HEIGHT || newX < 0 || newX >= BOARD_WIDTH) {
            exit(1); 
        }
        strcpy(gameArray[newY][newX], blockFormat);
        block->coords[i].y = newY;
        block->coords[i].x = newX;
    }
}

void createNewBlock(TetrisBlock* block) {
    int colorIndex;
    do {
        colorIndex = rand() % 5;
    } while (strcmp(colorNames[colorIndex], prevColor) == 0);
    
    strcpy(prevColor, colorNames[colorIndex]);
    block->colorCode = colorCodes[colorIndex];
    block->blockType = rand() % 7;
    spawnBlock(block, 0, 4);
}

int isPartOfBlock(TetrisBlock* block, int y, int x) {
    for (int i = 0; i < PIECE_COUNT; i++) {
        if (block->coords[i].y == y && block->coords[i].x == x) return 1;
    }
    return 0;
}

void getFreeCoordinates(TetrisBlock* block, const char* direction, Point* freeCoords, int* freeCount) {
    int xOffset = 0, yOffset = 0;
    if (strcmp(direction, "down") == 0) yOffset = 1;
    else if (strcmp(direction, "right") == 0) xOffset = 1;
    else if (strcmp(direction, "left") == 0) xOffset = -1;
    else if (strcmp(direction, "Sright") == 0) xOffset = 2;
    else if (strcmp(direction, "Sleft") == 0) xOffset = -2;

    *freeCount = 0;
    for (int i = 0; i < PIECE_COUNT; i++) {
        int ny = block->coords[i].y + yOffset;
        int nx = block->coords[i].x + xOffset;
        if (!isPartOfBlock(block, ny, nx)) {
            freeCoords[*freeCount].y = ny;
            freeCoords[*freeCount].x = nx;
            (*freeCount)++;
        }
    }
}

int updateBlock(TetrisBlock* block, const char* direction) {
    char blockFormat[ANSI_SIZE];
    sprintf(blockFormat, "\033[48;5;%dm \033[0m", block->colorCode);

    if (strcmp(direction, "down") == 0 || strcmp(direction, "left") == 0 || strcmp(direction, "right") == 0 ||
        strcmp(direction, "Sleft") == 0 || strcmp(direction, "Sright") == 0) {
        
        int yOffset = 0, xOffset = 0;
        if (strncmp(direction, "S", 1) == 0) {
            xOffset = (strcmp(direction, "Sleft") == 0) ? -2 : 2;
        } else {
            if (strcmp(direction, "down") == 0) yOffset = 1;
            else xOffset = (strcmp(direction, "left") == 0) ? -1 : 1;
        }

        Point freeCoords[PIECE_COUNT];
        int freeCount = 0;
        getFreeCoordinates(block, direction, freeCoords, &freeCount);

        for (int i = 0; i < freeCount; i++) {
            int y = freeCoords[i].y;
            int x = freeCoords[i].x;
            if (y >= BOARD_HEIGHT || x < 0 || x >= BOARD_WIDTH || strcmp(gameArray[y][x], backgroundPixel) != 0) {
                if (strcmp(direction, "Sleft") == 0) return updateBlock(block, "left");
                if (strcmp(direction, "Sright") == 0) return updateBlock(block, "right");
                return 0;
            }
        }

        for (int i = 0; i < PIECE_COUNT; i++) {
            strcpy(gameArray[block->coords[i].y][block->coords[i].x], backgroundPixel);
        }
        for (int i = 0; i < PIECE_COUNT; i++) {
            block->coords[i].y += yOffset;
            block->coords[i].x += xOffset;
            strcpy(gameArray[block->coords[i].y][block->coords[i].x], blockFormat);
        }
        return 1;
    }
    else if (strcmp(direction, "c") == 0 || strcmp(direction, "cc") == 0) {
        if (strcmp(typeList[block->blockType], "Oblock") == 0) return 0;
        
        int pivotY = block->coords[1].y;
        int pivotX = block->coords[1].x;
        Point newCoordinates[PIECE_COUNT];

        for (int i = 0; i < PIECE_COUNT; i++) {
            int y = block->coords[i].y;
            int x = block->coords[i].x;
            if (strcmp(direction, "c") == 0) {
                newCoordinates[i].x = pivotX - y + pivotY;
                newCoordinates[i].y = pivotY + x - pivotX;
            } else {
                newCoordinates[i].x = pivotX + y - pivotY;
                newCoordinates[i].y = pivotY - x + pivotX;
            }
        }

        for (int i = 0; i < PIECE_COUNT; i++) {
            int ny = newCoordinates[i].y;
            int nx = newCoordinates[i].x;
            if (!isPartOfBlock(block, ny, nx)) {
                if (ny >= BOARD_HEIGHT || nx < 0 || nx >= BOARD_WIDTH || strcmp(gameArray[ny][nx], backgroundPixel) != 0) {
                    return 0;
                }
            }
        }

        for (int i = 0; i < PIECE_COUNT; i++) {
            strcpy(gameArray[block->coords[i].y][block->coords[i].x], backgroundPixel);
        }
        for (int i = 0; i < PIECE_COUNT; i++) {
            block->coords[i] = newCoordinates[i];
            strcpy(gameArray[block->coords[i].y][block->coords[i].x], blockFormat);
        }
        return 1;
    }
    else { 
        Point shadowCoords[PIECE_COUNT];
        calculateEndCoordinates(block, shadowCoords);
        for (int i = 0; i < PIECE_COUNT; i++) {
            strcpy(gameArray[block->coords[i].y][block->coords[i].x], backgroundPixel);
        }
        for (int i = 0; i < PIECE_COUNT; i++) {
            block->coords[i] = shadowCoords[i];
            strcpy(gameArray[block->coords[i].y][block->coords[i].x], blockFormat);
        }
        return 1;
    }
}

void calculateEndCoordinates(TetrisBlock* block, Point* endCoords) {
    for (int i = 0; i < PIECE_COUNT; i++) endCoords[i] = block->coords[i];
    while (1) {
        int valid = 1;
        for (int i = 0; i < PIECE_COUNT; i++) {
            int ny = endCoords[i].y + 1;
            int nx = endCoords[i].x;
            if (ny >= BOARD_HEIGHT || nx < 0 || nx >= BOARD_WIDTH || 
               (strcmp(gameArray[ny][nx], backgroundPixel) != 0 && !isPartOfBlock(block, ny, nx))) {
                valid = 0;
                break;
            }
        }
        if (!valid) break;
        for (int i = 0; i < PIECE_COUNT; i++) endCoords[i].y += 1;
    }
}

void clearFullRow() {
    for (int i = 0; i < BOARD_HEIGHT; i++) {
        int full = 1;
        for (int j = 0; j < BOARD_WIDTH; j++) {
            if (strcmp(gameArray[i][j], backgroundPixel) == 0) {
                full = 0;
                break;
            }
        }
        if (full) {
            for (int j = 0; j < BOARD_WIDTH; j++) strcpy(gameArray[i][j], backgroundPixel);
            for (int row = i; row > 0; row--) {
                for (int col = 0; col < BOARD_WIDTH; col++) {
                    strcpy(gameArray[row][col], gameArray[row - 1][col]);
                }
            }
            score += 9;
        }
    }
}

int checkLoss(TetrisBlock* block) {
    for (int i = 0; i < BOARD_WIDTH; i++) {
        if (strcmp(gameArray[0][i], backgroundPixel) != 0 && !isPartOfBlock(block, 0, i)) {
            return 1;
        }
    }
    return 0;
}

void printGame(int z, TetrisBlock* block) {
    printf("\033[H\033[?25l");
    Point shadowCoords[PIECE_COUNT];
    calculateEndCoordinates(block, shadowCoords);

    for (int y = 0; y < BOARD_HEIGHT; y++) {
        for (int x = 0; x < BOARD_WIDTH; x++) {
            int isShadow = 0;
            if (!isPartOfBlock(block, y, x)) {
                for (int i = 0; i < PIECE_COUNT; i++) {
                    if (shadowCoords[i].y == y && shadowCoords[i].x == x) {
                        isShadow = 1;
                        break;
                    }
                }
            }
            if (isShadow) printf("\033[48;5;240m  \033[0m");
            else {
                printf("%s", gameArray[y][x]);
                printf("%s", gameArray[y][x]);
            }
        }
        printf("\n");
    }
    if (z == 0) {
        printf("Score: %d | [x] Quit\n", score);
    } else {
        printf("Your Final Score was: %d\n", score);
        printf("\033[1;32mGAME OVER! Press [r] to Restart or [x] to Exit\033[0m\n\033[?25h");
    }
    fflush(stdout);
}

void initGame(TetrisBlock* block) {
    score = 0;
    prevColor[0] = '\0';
    printf("\033[2J\033[H\033[?25l");
    for (int i = 0; i < BOARD_HEIGHT; i++) {
for (int j = 0; j < BOARD_WIDTH; j++) strcpy(gameArray[i][j], backgroundPixel);
}
createNewBlock(block);
}
int main() {
srand(time(NULL));
init_terminal();
TetrisBlock currentBlock;
initGame(&currentBlock);
int tick_counter = 0;
int gravity_ticks = 10;
int stateLoss = 0;
while (gameRun) {
if (!stateLoss && checkLoss(&currentBlock)) {
stateLoss = 1;
printGame(1, &currentBlock);
}
if (kbhit()) {
char ch = getchar();
// Standard Menu Actions
if (ch == 'x' || ch == 27) { // 'x' key or ESC key
gameRun = 0;
break;
}
if (stateLoss && ch == 'r') {
stateLoss = 0;
initGame(&currentBlock);
tick_counter = 0;
continue;
}
// Gameplay inputs (disabled if game is over)
if (!stateLoss) {
if (ch == 's') {
if (!updateBlock(&currentBlock, "down")) {
clearFullRow();
createNewBlock(&currentBlock);
}
tick_counter = 0;
}
else if (ch == 'a') updateBlock(&currentBlock, "left");
else if (ch == 'd') updateBlock(&currentBlock, "right");
else if (ch == 'q') updateBlock(&currentBlock, "c");
else if (ch == 'e') updateBlock(&currentBlock, "cc");
else if (ch == ' ') {
updateBlock(&currentBlock, "space");
clearFullRow();
createNewBlock(&currentBlock);
tick_counter = 0;
}
}
}
if (!stateLoss) {
tick_counter++;
if (tick_counter >= gravity_ticks) {
tick_counter = 0;
if (!updateBlock(&currentBlock, "down")) {
clearFullRow();
createNewBlock(&currentBlock);
}
}
printGame(0, &currentBlock);
}
usleep(30000);
}
reset_terminal();
printf("\033[2J\033[HThanks for playing!\n");
return 0;
}
