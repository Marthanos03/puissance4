def check_winner(board, row, column, player):
    """check if there is a winner"""
    return (
        check_direction(board, row, column, player, 1, 0) or
        check_direction(board, row, column, player, 0, 1) or
        check_direction(board, row, column, player, 1, 1) or
        check_direction(board, row, column, player, 1, -1)
    )


def check_direction(board, row, column, player, delta_row, delta_col):
    """subfunction for check_winner"""
    count = 0
    for d in range(-3, 4):
        r = row + d * delta_row
        c = column + d * delta_col
        if 0 <= r < 6 and 0 <= c < 7 and board[r][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False
