#include <cstdio>
#include <cstring>
#include <cassert>

#include <queue>
#include <vector>
#include <utility>
#include <algorithm>
using namespace std;

const int MAXN = 4013;
const int MAXM = 10013;
const int DX[4] = {-1, 0, 1, 0};
const int DY[4] = {0, 1, 0, -1};

// Divide the entire NxM matrix into smaller square blocks of this size
const int BLOCK_SIZE = 16;
const int MAX_BLOCKS_ROWS = MAXN / BLOCK_SIZE + 2;
const int MAX_BLOCKS_COLS = MAXM / BLOCK_SIZE + 2;

bool is_empty[MAX_BLOCKS_ROWS][MAX_BLOCKS_COLS];
bool visited_block[MAX_BLOCKS_ROWS][MAX_BLOCKS_COLS];
bool visited_cell[MAXN][MAXM];
int N, M, B;

#define inside(i, j) (0 <= i && i < N && 0 <= j && j < M)

queue< pair<pair<int, int>, bool> > q;

void read() {
    assert(scanf("%d %d %d", &N, &M, &B) == 3);

    memset(visited_cell, false, MAXN * MAXM);
    memset(visited_block, false, MAX_BLOCKS_ROWS * MAX_BLOCKS_COLS);
    memset(is_empty, true, MAX_BLOCKS_ROWS * MAX_BLOCKS_COLS);
    // for (int i = 0; i < M; i++)
    //     visited_cell[0][i] = visited_cell[N-1][i] = true;
    // for (int i = 0; i < N; i++)
    //     visited_cell[i][0] = visited_cell[i][M-1] = true;

    for (int i = 0; i < B; i++) {
        int x, y;
        assert(scanf("%d %d", &x, &y) == 2);
        visited_cell[x][y] = true;
        is_empty[x / BLOCK_SIZE][y / BLOCK_SIZE] = false;
    }
}

inline bool inside_block(int bx, int by) {
    return 0 <= bx && bx <= (N - 1) / BLOCK_SIZE &&
           0 <= by && by <= (M - 1) / BLOCK_SIZE;
}

inline bool should_visit(int i, int j) {
    if (is_empty[i / BLOCK_SIZE][j / BLOCK_SIZE])
        return !visited_block[i / BLOCK_SIZE][j / BLOCK_SIZE];
    else
        return !visited_cell[i][j];
}

inline void visit_block(int bx, int by) {
    // printf("   visit_block(%d, %d)\n", bx, by);
    visited_block[bx][by] = true;
    q.push(make_pair(make_pair(bx, by), true));
}

inline void visit_cell(int x, int y) {
    // printf("   visit_cell(%d, %d)\n", x, y);
    visited_cell[x][y] = true;
    q.push(make_pair(make_pair(x, y), false));
}

inline void visit_and_push(int x, int y) {
    // Should I visit the entire block, or just this cell?
    if (is_empty[x / BLOCK_SIZE][y / BLOCK_SIZE])
        visit_block(x / BLOCK_SIZE, y / BLOCK_SIZE);
    else
        visit_cell(x, y);
}

inline void visit_cell_neighbours(int x, int y) {
    int nx, ny;
    for (int i = 0; i < 4; i++) {
        nx = x + DX[i];
        ny = y + DY[i];
        if (inside(nx, ny) && should_visit(nx, ny)) visit_and_push(nx, ny);
    }
}

inline void visit_block_neighbours(int bx, int by) {
    int nbx, nby, cx, cy, nx, ny;

    // printf("{visit_block_neighbours(%d, %d)\n", bx, by);
    for (int i = 0; i < 4; i++) {
        // If the adjacent neighbouring block is also empty, visit the entire
        // block, otherwise visit all neighbouring cells in this direction.
        nbx = bx + DX[i];
        nby = by + DY[i];

        // Is this a valid block?
        if (!inside_block(nbx, nby)) continue;

        if (is_empty[nbx][nby]) {
            // DUPLICATE CODE
            if (!visited_block[nbx][nby]) visit_block(nbx, nby);
        } else {
            // Upper left corner of block containing (x, y).
            cx = bx * BLOCK_SIZE;
            cy = by * BLOCK_SIZE;
            for (int j = 0; j < BLOCK_SIZE; j++) {
                if (DX[i] == 0) nx = cx + j;
                else if (DX[i] == -1) nx = cx - 1;
                else nx = cx + BLOCK_SIZE;
                if (DY[i] == 0) ny = cy + j;
                else if (DY[i] == -1) ny = cy - 1;
                else ny = cy + BLOCK_SIZE;

                // printf("(%d, %d) --[%d]--> (%d, %d)\n", bx, by, i, nx, ny);
                if (!visited_cell[nx][ny]) visit_cell(nx, ny);
            }
        }
    }
    // printf("} #end of visit_block_neighbours(%d, %d)\n", bx, by);
}

void lee(int sx, int sy) {
    int x, y;
    bool is_block;

    assert(q.empty());

    visit_and_push(sx, sy);

    while (!q.empty()) {
        x = q.front().first.first;
        y = q.front().first.second;
        is_block = q.front().second;
        q.pop();

        if (is_block) visit_block_neighbours(x, y);
        else visit_cell_neighbours(x, y);
    }
}

int count_connected_components() {
    int count = 0;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < M; j++)
            if (should_visit(i, j)) {
                count += 1;
                lee(i, j);
            }
    return count;
}

int main(int argc, const char* argv[]) {
    const char* fname;
    if (argc == 2)
        fname = argv[1];
    else
        fname = "mars_explorer.txt";
    assert(freopen(fname, "r", stdin));

    int P;
    assert(scanf("%d", &P) == 1);

    for (int i = 0; i < P; i++) {
        read();
        printf("%d\n", count_connected_components());
    }

    return 0;
}