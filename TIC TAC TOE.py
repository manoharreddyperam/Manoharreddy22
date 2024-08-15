import random

def minimax(node, depth, alpha, beta, maximizingPlayer):
    """
    Perform the Minimax algorithm with Alpha-Beta pruning to determine the best move.
    :param node: The current state of the board
    :param depth: The depth of the current node in the game tree
    :param alpha: The best value that the maximizer can guarantee at this level or above
    :param beta: The best value that the minimizer can guarantee at this level or above
    :param maximizingPlayer: Boolean indicating if the current player is the maximizer
    :return: The best value for the current player
    """
    if depth == 0 or is_terminal_node(node):
        return evaluate(node)

    if maximizingPlayer:
        max_eval = -float('inf')
        for child in get_children(node, True):
            eval = minimax(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for child in get_children(node, False):
            eval = minimax(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_children(node, maximizingPlayer):
    """
    Generate all possible child nodes from the current node based on the current player's move.
    :param node: The current state of the board
    :param maximizingPlayer: Boolean indicating if the current player is the maximizer
    :return: A list of child nodes
    """
    children = []
    for x, row in enumerate(node):
        for y, cell in enumerate(row):
            if cell == 0:  # If the cell is empty
                child = [row.copy() for row in node]
                child[x][y] = 1 if maximizingPlayer else -1
                children.append(child)
    return children

def is_terminal_node(node):
    """
    Check if the current node is a terminal node (i.e., the game is over).
    :param node: The current state of the board
    :return: True if the game is over, otherwise False
    """
    return wins(node, 1) or wins(node, -1) or not any(0 in row for row in node)

def evaluate(node):
    """
    Evaluate the score of the current node based on the game outcome.
    :param node: The current state of the board
    :return: +1 for a win, -1 for a loss, 0 for a draw
    """
    if wins(node, 1):
        return 1
    elif wins(node, -1):
        return -1
    return 0

def wins(state, player):
    """
    Check if a specific player has won the game.
    :param state: The current state of the board
    :param player: The player to check (1 for maximizer, -1 for minimizer)
    :return: True if the player has won, otherwise False
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    return [player, player, player] in win_state

def print_board(board):
    """
    Print the board to the console.
    :param board: The current state of the board
    """
    chars = {1: 'O', -1: 'X', 0: ' '}
    print('\n  1 2 3')
    for i, row in enumerate(board):
        print(f'{i + 1} {" ".join(chars[cell] for cell in row)}')

def human_turn(board):
    """
    Allow the human player to make a move.
    :param board: The current state of the board
    """
    while True:
        try:
            move = int(input('Choose your move (1-9): '))
            if move < 1 or move > 9:
                raise ValueError("Move must be between 1 and 9")
            x, y = divmod(move - 1, 3)
            if board[x][y] != 0:
                print('Cell is already occupied. Try again.')
                continue
            board[x][y] = -1
            break
        except (ValueError, IndexError):
            print('Invalid move. Try again.')

def ai_turn(board):
    """
    Allow the AI to make a move using Minimax with Alpha-Beta pruning.
    :param board: The current state of the board
    """
    best_move = None
    best_value = -float('inf')
    for child in get_children(board, True):
        move_value = minimax(child, len(empty_cells(board)), -float('inf'), float('inf'), False)
        if move_value > best_value:
            best_value = move_value
            best_move = child

    if best_move:
        for x in range(3):
            for y in range(3):
                if board[x][y] != best_move[x][y]:
                    board[x][y] = 1
                    return

def empty_cells(board):
    """
    Get a list of empty cells on the board.
    :param board: The current state of the board
    :return: A list of empty cell coordinates
    """
    return [(x, y) for x in range(3) for y in range(3) if board[x][y] == 0]

def main():
    """
    Main function to run the Tic Tac Toe game.
    """
    board = [[0] * 3 for _ in range(3)]
    print("Welcome to Tic Tac Toe!")
    print_board(board)

    while True:
        human_turn(board)
        print_board(board)
        if is_terminal_node(board):
            break

        ai_turn(board)
        print_board(board)
        if is_terminal_node(board):
            break

    if wins(board, -1):
        print("Congratulations, you win!")
    elif wins(board, 1):
        print("AI wins. Better luck next time!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()





