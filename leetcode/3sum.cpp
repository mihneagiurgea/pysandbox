#include <cstdio>
#include <cstring>
#include <cassert>
#include <iostream>

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

vector<vector<int> > threeSum(vector<int> &num) {



}


int main(int argc, const char* argv[]) {
    int input[] = {-1, 0, 1, 2, -1, 4};
    vector<int> V (input, input + sizeof(input) / sizeof(int));

    for (int i = 0; i < V.size(); i++)
        cout << V[i] << " ";
    cout << endl;

    return 0;
}