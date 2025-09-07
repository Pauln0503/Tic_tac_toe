import random
from rich.console import Console
from rich.table import Table
from banner import print_banner
import shutil
import readchar
from clear_console import clear_console

console = Console()
cursor = [0, 0]

def init_board(size):
    if size == 'inf':
        return {(0,0): ""}
    else:
        return [["" for _ in range(size)] for _ in range(size)]

board = {}

def insert_letter(board, letter, pos, size):
    if size == 'inf':
        board[pos] = letter
    else:
        r, c = pos
        board[r][c] = letter


def free_space(board,pos,size):
    if size == 'inf':
        return pos not in board or board[pos] == ""
    else:
        r, c = pos
        if 0 <= r < size and 0 <= c < size:
            return board[r][c] == ""
        return False


def print_board(board, size):
    columns, _ = shutil.get_terminal_size()
    table = Table(show_lines=True)

    col_range = size if size != "inf" else 5
    for c in range(col_range):
        table.add_column(str(c), justify="center", style="bold")

    if size == "inf":
        if not board:
            rows = [(0,0)]
        else:
            min_r = min(r for r,_ in board.keys())
            max_r = max(r for r,_ in board.keys())
            rows = range(min_r, max_r+1)
        for r in rows:
            row_cells = []
            min_c = min(c for _,c in board.keys())
            max_c = max(c for _,c in board.keys())
            for c in range(min_c, max_c+1):
                val = board.get((r,c), "")
                if val == "X":
                    val = "[red]X[/red]"
                elif val == "O":
                    val = "[blue]O[/blue]"
                if [r, c] == cursor:   # highlight cursor
                    val = f"[reverse]{val or ' '}[/reverse]"
                row_cells.append(val or "")
            table.add_row(*row_cells)
    else:
        for r in range(size):
            row_cells = []
            for c in range(size):
                val = board[r][c]
                if [r, c] == cursor:   
                    val = f"[reverse]{val or '.'}[/reverse]"
                if val == "X":
                    val = "[red]X[/red]"
                elif val == "O":
                    val = "[blue]O[/blue]"
                row_cells.append(val or "")
            table.add_row(*row_cells)

    # Render table to string to center it
    from io import StringIO
    buf = StringIO()
    temp_console = Console(file=buf)
    temp_console.print(table)
    board_str = buf.getvalue()
    for line in board_str.splitlines():
        print(line.center(columns))


def is_winner(board, pos, letter, size):
    directions = [(1,0),(0,1),(1,1),(1,-1)]
    n = 3 if size == 3 else 5
    for dr, dc in directions:
        count = 1
        for sign in [1, -1]:
            r,c = pos
            while True:
                r += dr * sign
                c += dc * sign
                if size == 'inf':
                    if board.get((r,c)) == letter:
                        count += 1
                    else:
                        break
                else:
                    if 0 <= r < size and 0 <= c < size and board[r][c] == letter:
                        count += 1
                    else:
                        break
        if count >= n:
            return True
    return False

def player_move_arrow(board, letter, size):
    global cursor
    while True:
        clear_console()
        print_board(board, size)
        print(f"Player {letter}'s turn. Use arrows to move, Enter to select.")
        key = readchar.readkey()
        r, c = cursor

        if key == readchar.key.UP:
            cursor[0] = (r - 1) % size
        elif key == readchar.key.DOWN:
            cursor[0] = (r + 1) % size
        elif key == readchar.key.LEFT:
            cursor[1] = (c - 1) % size
        elif key == readchar.key.RIGHT:
            cursor[1] = (c + 1) % size
        elif key == readchar.key.ENTER or key == readchar.key.SPACE:
            if free_space(board, tuple(cursor), size):
                insert_letter(board, letter, tuple(cursor), size)
                return tuple(cursor)
            else:
                print("That cell is already taken! Try another.")

def comp_move(board, letter, size):
    if size == 'inf':
        if not board:
            pos = (0,0)
        else:
            key = list(board.keys())
            r0, c0 = random.choice(key)
            pos = (r0 + random.randint(-1,1), c0 + random.randint(-1,1))
            while not free_space(board, pos, size):
                r0, c0 = random.choice(key)
                pos = (r0 + random.randint(-1,1), c0 + random.randint(-1,1))
    else:
        empty = [(r,c) for r in range(size) for c in range(size) if board[r][c] == ""]
        pos = random.choice(empty)
    insert_letter(board, letter, pos, size)
    print(f"Comp move is:  {pos}")
    return pos

def is_full(board, size):
    if size == "inf":
        return False
    else:
        for row in board:
            if "" in row:
                return False
        return True
    

def main():
    print("Choose board size (3,5,7,9 or 'inf'):")
    size_input = input()
    size = int(size_input) if size_input.isdigit() else "inf"

    print("Choose mode: 1 = 2 players, 2 = vs computer")
    mode = input()

    board = init_board(size)
    current_player = "X"

    while True:
        print_board(board, size)
        if mode == "2" and current_player == "O":
            last_move = comp_move(board, current_player, size)
        else:
            last_move = player_move_arrow(board, current_player, size)

        if is_winner(board, last_move, current_player, size):
            print_board(board, size)
            print(f"Player {current_player} wins!")
            break
        if is_full(board, size):
            print_board(board, size)
            print("Draw!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    print_banner()
    main()


