# -*- coding:utf-8 -*-
from module import BlackWriteChess
import random


def search_DFS(now_app, now_level, limit_level, parent_h=None):
    if now_level >= limit_level:
        return now_app.heuristic()
    if not now_app.turn_check():  # You will pass this turn
        return now_app.heuristic()

    can_put_pos = now_app.can_put_pos

    if (now_level % 2) == 0:    # max
        now_h = float("-inf")
    elif (now_level % 2) == 1:  # min
        now_h = float("inf")

    for pos in can_put_pos:
        # now_level += 1
        child_app = BlackWriteChess.BWC(human_color=now_app.human_color,
                                        checkerboard=now_app.checkerboard, turn=now_app.turn)
        child_app.put_check(pos)
        child_app.previous_put = pos
        child_app.flip(app.need_flip)
        child_app.turn = (app.turn + 1) % 2

        temp = search_DFS(child_app, now_level+1, limit_level, now_h)

        if (now_level % 2) == 0:    # max
            if temp > now_h:
                now_h = temp
                best_pos = pos
            if now_level != 0:
                alpha = now_h
                beta = parent_h    #
                if ((alpha != float("-inf")) and (beta != float("inf")) and (beta <= alpha)):
                    break

        elif (now_level % 2) == 1:  # min
            if temp < now_h:
                now_h = temp
                best_pos = pos
            if now_level != 0:
                alpha = parent_h    #
                beta = now_h
                if ((alpha != float("-inf")) and (beta != float("inf")) and (beta <= alpha)):
                    break

    if now_level != 0:
        return now_h
    else:
        return best_pos


if __name__ == '__main__':
    enemy_color = 0  # 敵人的顏色 None:空 0:白 1:黑
    AI_color = (enemy_color + 1) % 2

    app = BlackWriteChess.BWC(human_color=AI_color)
    app.a_new_game_start()

    while True:
        if sum(x.count(None) for x in app.checkerboard) == 0:
            app.clear_screen()
            app.show_now_status()
            app.show_checkerboard()
            print('End Game')
            break
        if app.turn == enemy_color:  # 輪到對手了
            app.next_turn()
        else:  # 輪到 AI 了
            if not app.turn_check():  # You will pass this turn
                app.turn = (app.turn + 1) % 2
                continue

            # x = random.randint(0, len(app.can_put_pos)-1)  # Random的部分
            x = search_DFS(app, 0, 7)
            print(x)

            # put = app.can_put_pos[x]
            app.put_check(x)
            app.previous_put = x
            app.flip(app.need_flip)
            app.turn = (app.turn + 1) % 2

    # app.next_turn()
    # app.show_now_status()

    # app2 = BlackWriteChess.BWC(checkerboard=app.checkerboard, turn=app.turn)
    # app2.next_turn()

    # app.clear_screen()

    # print('show app')
    # app.show_checkerboard()

    # print('show app2')
    # app2.show_checkerboard()
