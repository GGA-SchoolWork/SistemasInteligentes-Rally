# %% [markdown]
# # Rally 1 - Agente Inteligente para TicTacToe

# %% [markdown]
# ## Funciones para MinMax

# %%
# Usamos np para manejar matrices mas eficientemente
import numpy as np
import math

# %%
# En este programa el jugador siempre es 'X' y la IA es 'O'
player, opponent = 'X', 'O'

MIN, MAX = -math.inf, math.inf

# Funcion para ver si ya no hay movimientos posibles, se llama si eval es 0


def no_more_moves(board: np.array):
    return '_' not in board

# Evalua el estado del juego para ver si hay ganadores


def eval(board: np.array):
    # Checar victoria con fila horizontal
    for row in board:
        if len(set(row)) == 1:
            if row[0] == 'X':
                return 10
            if row[0] == 'O':
                return -10

    # Checar victoria con columna vertical
    for col in board.T:
        if len(set(col)) == 1:
            if col[0] == 'X':
                return 10
            if col[0] == 'O':
                return -10

    # Checar victoria con diagonal
    diag = np.diagonal(board)
    if len(set(diag)) == 1:
        if diag[0] == 'X':
            return 10
        if diag[0] == 'O':
            return -10

    # Checar victoria con anti-diagonal
    # La anti-diagonal es la diagonal principal de la matriz invertida de izquierda a derecha
    anti = np.diagonal(np.fliplr(board))
    if len(set(anti)) == 1:
        if anti[0] == 'X':
            return 10
        if anti[0] == 'O':
            return -10

    # Nadie ha ganado
    return 0

# Funcion MiniMax, explora todos los caminos posibles y regresa el valor del tablero.


def minimax(board: np.array, isMax, alpha, beta):
    score = eval(board)

    # Si score no es 0 ya hay ganador
    if score != 0:
        return score
    # Si score es 0 evaluamos que sea un empate sin movimientos posibles
    elif no_more_moves(board):
        return score

    best = MIN if isMax else MAX

    # Itera sobre las celdas
    for i in range(3):
        for j in range(3):
            if (board[i][j] == '_'):  # Celda Vacia
                # Hace el movimiento
                board[i][j] = player if isMax else opponent

                # Llama minimax recursivo
                if isMax:
                    best = max(best, minimax(board, not isMax, alpha, beta))
                    alpha = max(alpha, best)
                else:
                    best = min(best, minimax(board, not isMax, alpha, beta))
                    beta = min(beta, best)

                # Deshace movimiento
                board[i][j] = '_'

                # alpha-beta pruning
                if beta <= alpha:
                    return best
    return best


def find_best_move(board: np.array):
    # best_score es MAX pq la IA siempre es min
    best_score = MAX
    best_move = (None, None)

    for i in range(3):
        for j in range(3):
            if (board[i][j] == '_'):  # Celda vacia

                # Hace el movimiento
                board[i][j] = opponent

                # Evalua el movimiento
                move_score = minimax(board, True, MIN, MAX)

                # Deshace el movimiento
                board[i][j] = '_'

                # Si el valor es menor al ultimo mejor, cambia el mejor movimiento
                if (move_score < best_score):
                    best_move = (i, j)
                    best_score = move_score
    return best_move


# %% [markdown]
# ## Juego

# %%
input_to_cell = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 9: (2, 2)
}

# Funcion para ver si ya se acabo el juego


def game_is_over(board: np.array):
    if eval(board) != 0:
        return True
    elif no_more_moves(board):
        return True
    else:
        return False


def make_player_move(board: np.array):
    player_input = 0
    valid_inputs = set()
    print("En qué celda quieres poner 'X'?")
    n = 1
    for i in range(3):
        endchar = '\t'
        for j in range(3):
            if j == 2:
                endchar = '\n'
            if board[i][j] == "_":
                valid_inputs.add(n)
                print(f"[{n}]", end=endchar)
            else:
                print(f" {board[i][j]} ", end=endchar)
            n += 1

    # Lee entrada y valida
    while player_input not in valid_inputs:
        try:
            player_input = int(input())
        except ValueError:
            print("Debe ser un entero de los lugares disponibles.")
        if player_input not in valid_inputs:
            print(f"La celda {player_input} ya esta tomada!")

    # Traduce a coordenada y hace el movimiento
    player_move = input_to_cell[player_input]
    board[player_move[0], player_move[1]] = player
    print()

    return board


def make_ai_move(board: np.array):
    bestMove = find_best_move(board)
    board[bestMove[0]][bestMove[1]] = opponent
    return board


def run_game():
    board = np.array([
        ['_', '_', '_'],
        ['_', '_', '_'],
        ['_', '_', '_']])

    while not game_is_over(board):
        board = make_player_move(board)
        if game_is_over(board):
            break
        board = make_ai_move(board)

    print("Tablero Final:")
    for i in range(3):
        endchar = '\t'
        for j in range(3):
            if j == 2:
                endchar = '\n'
            if board[i][j] == "_":
                print(f"[ ]", end=endchar)
            else:
                print(f" {board[i][j]} ", end=endchar)
    print()

    result = eval(board)

    if result > 0:
        print("Ganaste! :D")
    elif result < 0:
        print("Perdiste :(")
    else:
        print("Empate :|")


run_game()
