DX = [-1, -1, 0, 1, 1, 1, 0, -1]
DY = [0, 1, 1, 1, 0, -1, -1, -1]
DIRECTIONS = zip(DX, DY)

KNIGHT_DIRECTIONS = [
    (-2, -1), (-2, +1), (-1, +2), (+1, +2),
    (+2, +1), (+2, -1), (+1, -2), (-1, -2)
]

# List of pieces that can only move once in their direction.
MOVES_ONCE = 'PNK'

def get_move_directions(piece, white):
    if piece == 'P':
        if white:
            return [DIRECTIONS[1], DIRECTIONS[7]]
        else:
            return [DIRECTIONS[3], DIRECTIONS[5]]
    elif piece == 'R':
        return [DIRECTIONS[0], DIRECTIONS[2], DIRECTIONS[4], DIRECTIONS[6]]
    elif piece == 'N':
        return KNIGHT_DIRECTIONS
    elif piece == 'B':
        return [DIRECTIONS[1], DIRECTIONS[3], DIRECTIONS[5], DIRECTIONS[7]]
    elif piece == 'Q' or piece == 'K':
        return DIRECTIONS
    else:
        raise ValueError('Invalid piece: %r' % piece)

def is_inside(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def threatens(table, i, j, king_pos):
    piece = table[i][j].upper()
    directions = get_move_directions(piece, table[i][j].isupper())
    for direction in directions:
        x = i + direction[0]
        y = j + direction[1]
        if piece not in MOVES_ONCE:
            while is_inside(x, y) and table[x][y] == '.':
                x += direction[0]
                y += direction[1]
        if (x, y) == king_pos:
            return True
    return False

def find_piece(table, piece):
    for i in range(8):
        for j in range(8):
            if table[i][j] == piece:
                return i, j
    return None

def is_check_for_player(table, king_pos):
    is_white_king = table[king_pos[0]][king_pos[1]].isupper()
    for i in range(8):
        for j in range(8):
            if table[i][j] != '.' and table[i][j].isupper() != is_white_king:
                if threatens(table, i, j, king_pos):
                    return True
    return False

def _is_check(table):
    # Find position of 'k' and 'K'
    black_king = find_piece(table, 'k')
    white_king = find_piece(table, 'K')

    if is_check_for_player(table, black_king):
        return 'Black'
    if is_check_for_player(table, white_king):
        return 'White'
    return None

def is_check(table_str):
    # Convert table to an array of strings.
    table = []
    start = 0
    while start < len(table_str):
        table.append(table_str[start:start+8])
        start += 8
    print _is_check(table)






