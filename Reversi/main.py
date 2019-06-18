# -*- coding:utf-8 -*-
from module import BlackWriteChess
import random
from time import time


def search_DFS(now_app, now_level, limit_level, parent_h=None):
    if now_level >= limit_level:
        # now_app.show_now_status()
        # now_app.show_checkerboard()
        return now_app.heuristic()
    if not now_app.turn_check():  # You will pass this turn
        if (now_level % 2) == 0:    # max
            return -999  # float("-inf")
        elif (now_level % 2) == 1:  # min
            return 999  # float("inf")
        return now_app.heuristic()

    can_put_pos = now_app.can_put_pos

    if (now_level % 2) == 0:    # max
        now_h = float("-inf")
    elif (now_level % 2) == 1:  # min
        now_h = float("inf")

    for pos in can_put_pos:
        # print(pos)
        # now_level += 1
        child_app = BlackWriteChess.BWC(human_color=now_app.human_color,
                                        checkerboard=now_app.checkerboard, turn=now_app.turn)
        child_app.put_check(pos)
        child_app.previous_put = pos
        child_app.flip(child_app.need_flip)
        child_app.turn = (child_app.turn + 1) % 2

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
        return now_h, best_pos


if __name__ == '__main__':
    color_list = ['白', '黑']

    pos_history = []
    enemy_color = int(input('請問對手是黑色先手[1]或是白色後手[0]:'))  # 敵人的顏色 None:空 0:白 1:黑
    AI_color = (enemy_color + 1) % 2

    app = BlackWriteChess.BWC(human_color=AI_color)
    app.a_new_game_start()
    get_h = ''
    pass_number = 0
    while True:
        # input('pos_history:{}'.format(pos_history))
        if sum(x.count(None) for x in app.checkerboard) == 0 or pass_number == 2:
            app.clear_screen()
            app.show_now_status()
            app.show_checkerboard()
            print('End Game')
            if app.black_num > app.white_num:
                print('Black Win')
                if AI_color == 1:
                    print('AI Win')
                else:
                    print('AI Lose')
            elif app.black_num < app.white_num:
                print('White Win')
                if AI_color == 0:
                    print('AI Win')
                else:
                    print('AI Lose')
            else:
                print('平手')

            print('\n\npos_history')
            for x in pos_history:
                if x['pos'] is None:
                    print('{} {}'.format(x['turn'], 'PASS'))
                else:
                    print('{} {}'.format(x['turn'], x['pos']))
            break
        if app.turn == enemy_color:  # 輪到對手了
            enemy_pos = app.next_turn()
            if enemy_pos is None:
                pos_history.append(
                    {'turn': color_list[enemy_color], 'pos': None})
                print('Enemy pass a turn!\n')
                pass_number += 1
            else:
                pos_history.append(
                    {'turn': color_list[enemy_color], 'pos': list(enemy_pos)})
                pass_number = 0
            print('\n')
        else:  # 輪到 AI 了
            if not app.turn_check():  # You will pass this turn
                app.turn = (app.turn + 1) % 2
                pos_history.append({'turn': color_list[AI_color], 'pos': None})
                print('AI pass a turn!\n')
                pass_number += 1
                continue

            pass_number = 0

            # print(len(app.can_put_pos))
            if len(pos_history) <= 5:
                x = app.can_put_pos[random.randint(
                    0, len(app.can_put_pos)-1)]  # Random的部分
                get_h = 'Random'
            else:
                temp_time = time()
                # limit_level = min([len(app.can_put_pos), 5])
                limit_level = 5 if len(app.can_put_pos) <= 5 else 3
                # print(type(limit_level))
                get_h, x = search_DFS(app, 0, limit_level)
                print('This DFS Used {}'.format(time()-temp_time))

            print('AI Chose: {}  //h: {}'.format(x, get_h))

            pos_history.append({'turn': color_list[AI_color], 'pos': x})
            app.put_check(x)
            app.previous_put = x
            app.flip(app.need_flip)
            app.turn = (app.turn + 1) % 2
            print('\n')
