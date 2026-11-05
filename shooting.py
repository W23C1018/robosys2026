#!/usr/bin/python3
import curses
import random
import time

def main(stdscr):
    # カーソルを非表示にし、入力待ちのタイムアウトを設定 (30ms)
    curses.curs_set(0)
    stdscr.timeout(30)
    
    # 画面サイズの取得
    sh, sw = stdscr.getmaxyx()
    
    # 自機の初期位置
    player_y = sh // 2
    player_x = 2
    
    bullets = []   # 弾のリスト [(y, x)]
    enemies = []   # 敵のリスト [(y, x)]
    score = 0
    
    while True:
        stdscr.clear()
        
        # 画面枠とスコア描画
        stdscr.addstr(0, 0, f" SCORE: {score} | [W/S] or [Arrow Keys]: Move | [Space]: Shoot | [Q]: Quit ")
        
        # キー入力処理
        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            break
        elif (key == curses.KEY_UP or key == ord('w')) and player_y > 1:
            player_y -= 1
        elif (key == curses.KEY_DOWN or key == ord('s')) and player_y < sh - 2:
            player_y += 1
        elif key == ord(' '):
            bullets.append([player_y, player_x + 2])

        # 敵の生成 (ランダム)
        if random.random() < 0.2:
            enemies.append([random.randint(1, sh - 2), sw - 2])

        # 弾の移動
        new_bullets = []
        for b in bullets:
            b[1] += 2
            if b[1] < sw - 1:
                new_bullets.append(b)
        bullets = new_bullets

        # 敵の移動
        new_enemies = []
        game_over = False
        for e in enemies:
            e[1] -= 1
            # 自機との当たり判定
            if e[1] <= player_x + 1 and abs(e[0] - player_y) <= 0:
                game_over = True
            elif e[1] > 0:
                new_enemies.append(e)
        enemies = new_enemies

        if game_over:
            stdscr.clear()
            msg = f" GAME OVER! Final Score: {score} "
            stdscr.addstr(sh // 2, (sw - len(msg)) // 2, msg)
            stdscr.refresh()
            time.sleep(2)
            break

        # 弾と敵の当たり判定
        for b in bullets[:]:
            for e in enemies[:]:
                if b[0] == e[0] and abs(b[1] - e[1]) <= 1:
                    if b in bullets: bullets.remove(b)
                    if e in enemies: enemies.remove(e)
                    score += 100
                    break

        # 描画処理
        # 自機
        stdscr.addstr(player_y, player_x, "=>")
        
        # 弾
        for b in bullets:
            stdscr.addstr(b[0], b[1], "-")
            
        # 敵
        for e in enemies:
            stdscr.addstr(e[0], e[1], "<=")

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
