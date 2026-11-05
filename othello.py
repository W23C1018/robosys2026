#!/usr/bin/python3
import sys

# 0: 空白, 1: 黒(●), -1: 白(○)
board = [[0] * 8 for _ in range(8)]
board[3][3], board[3][4] = -1, 1  # d4:白, e4:黒
board[4][3], board[4][4] = 1, -1  # d5:黒, e5:白

DIRECTIONS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

def print_board():
    symbols = {0: '.', 1: '●', -1: '○'}
    print("\n  a b c d e f g h")
    for r in range(8):
        row_str = f"{r+1} " + " ".join(symbols[board[r][c]] for c in range(8))
        print(row_str)
    print()

def get_flips(r, c, player):
    if board[r][c] != 0:
        return []
    flips = []
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        line = []
        # 相手の石が続く限り進む
        while 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == -player:
            line.append((nr, nc))
            nr += dr
            nc += dc
        # 最後に自分の石があれば挟めたと判定
        if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == player:
            flips.extend(line)
    return flips

def has_valid_move(player):
    for r in range(8):
        for c in range(8):
            if get_flips(r, c, player):
                return True
    return False

def main():
    current_player = 1 # 1: 黒(●), -1: 白(○)
    symbols = {1: '黒 (●)', -1: '白 (○)'}

    print("=== オセロ (リバーシ) ===")
    print("配置するときは座標を入力してください（例: c5, d3, e6, f4）")
    print("中断するには q を入力します。\n")

    while True:
        print_board()
        
        # 勝敗判定
        if not has_valid_move(1) and not has_valid_move(-1):
            print("--- ゲーム終了 ---")
            b_count = sum(row.count(1) for row in board)
            w_count = sum(row.count(-1) for row in board)
            print(f"結果: 黒(●) {b_count} - 白(○) {w_count}")
            if b_count > w_count:
                print("黒 (●) の勝ちです！")
            elif w_count > b_count:
                print("白 (○) の勝ちです！")
            else:
                print("引き分けです！")
            break

        # パス判定
        if not has_valid_move(current_player):
            print(f"{symbols[current_player]} は置ける場所がないためパスします。")
            current_player *= -1
            continue

        move = input(f"手番 [{symbols[current_player]}]: ").strip().lower()
        if move == 'q':
            print("ゲームを終了します。")
            break

        if len(move) != 2 or not move[0].isalpha() or not move[1].isdigit():
            print("【エラー】'c5' のように列の英字と行の数字を入力してください。")
            continue

        c = ord(move[0]) - ord('a')
        r = int(move[1]) - 1

        if not (0 <= r < 8 and 0 <= c < 8):
            print("【エラー】盤面の範囲内で入力してください（a~h, 1~8）。")
            continue

        flips = get_flips(r, c, current_player)
        if not flips:
            print("【エラー】そこに置くことはできません（相手の石を挟めません）。")
            continue

        # 石を置く
        board[r][c] = current_player
        for fr, fc in flips:
            board[fr][fc] = current_player

        # 交代
        current_player *= -1

if __name__ == "__main__":
    main()
