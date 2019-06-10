# -*- coding:utf-8 -*-
import os
import random
from copy import deepcopy


class BWC:
    '''
    黑白棋棋盤物件
    '''

    def __init__(self, human_color=1, checkerboard=[[None]*8 for i in range(8)], turn=1):
        '''
        初始化物件
        human_color - 玩家顏色設定，目前還不確定如何實做得好，好像也用不到 (?)
        checkerboard - 得以繼承父棋盤的棋盤狀態，預設為8*8的None
        turn - 得以繼承父棋盤目前的回合是誰
        '''
        self.rows = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.human_color = human_color
        self.human = '黑' if self.human_color == 1 else '白'
        self.checkerboard = deepcopy(checkerboard)  # None:空 0:白 1:黑
        self.turn = turn
        self.need_flip = []  # 由 self.put_check() 刷新
        self.can_put_pos = []   # 由 self.turn_check() 刷新
        self.previous_put = None

    def a_new_game_start(self):
        '''
        開始新的一局
        中間四個擺上黑白交錯的棋盤
        '''
        self.checkerboard[3][3] = self.checkerboard[4][4] = 0
        self.checkerboard[3][4] = self.checkerboard[4][3] = 1
        self.turn = 1  # Whose round?
        # self.next_turn()

    def next_turn(self):
        '''
        下個回合

        '''
        self.clear_screen()
        self.show_now_status()
        print('{} Turn'.format('黑' if self.turn == 1 else '白'))
        self.show_checkerboard()

        if not self.turn_check():  # You will pass this turn
            self.turn = (self.turn + 1) % 2
            return
            # self.next_turn()
        print(self.can_put_pos)

        if not self.previous_put is None:
            print('Previous Turn Put: {}'.format(self.previous_put))

        put = input('下哪邊? ')  # EX: f5
        while not self.put_check(put):
            put = input('請輸入有效值? ')

        self.previous_put = put
        self.flip(self.need_flip)
        self.turn = (self.turn + 1) % 2
        # self.next_turn()

    def turn_check(self):
        '''
        回合確認
        若該回合無任何可放位置，則回傳 false 表示 pass

        self.can_put_pos 這個成員由此方法刷新
        '''
        self.can_put_pos = []
        for y in self.rows:
            for x in self.cols:
                if self.put_check('{}{}'.format(x, y)):
                    self.can_put_pos.append([x, y])
        if len(self.can_put_pos) == 0:
            return False
        return True

    def flip(self, need_flip):
        '''
        翻面
        need_flip - 哪些位置需要翻成與該回合同色
        '''
        for x, y in need_flip:
            self.checkerboard[y][x] = self.turn  # 將需要的位置翻色

    def put_check(self, put):
        '''
        放下確認
        此方法判斷放下位置是否為有效值
        self.need_flip 由此方法刷新
        '''
        row = put[1]
        col = put[0]
        # Easy Check
        if row not in self.rows or col not in self.cols:
            return False
        row = self.rows.index(row)
        col = self.cols.index(col)

        # Hard Check
        other_color = (self.turn + 1) % 2
        self.need_flip = []

        if self.checkerboard[row][col] != None:
            return False
        # 上      右上    右       右下     下       左下       左       左上
        check_position = [[0, 1], [1, 1], [1, 0], [1, -1],
                          [0, -1], [-1, -1], [-1, 0], [-1, 1]]  # dx, dy
        for dx, dy in check_position:
            continue_flag = False
            start_x = col
            start_y = row

            temp_x = start_x + dx
            temp_y = start_y + dy
            if (not (7 >= temp_x >= 0 and 7 >= temp_y >= 0) or
                (self.checkerboard[temp_y][temp_x] == None) or
                    (self.checkerboard[temp_y][temp_x] == self.turn)):
                continue

            while 7 >= temp_x >= 0 and 7 >= temp_y >= 0:
                if self.checkerboard[temp_y][temp_x] == other_color:  # 若遇到對方
                    break
                elif self.checkerboard[temp_y][temp_x] == None:  # 若遇到空
                    continue_flag = True
                temp_x += dx
                temp_y += dy
            if not (7 >= temp_x >= 0 and 7 >= temp_y >= 0) or continue_flag:
                continue

            while 7 >= temp_x >= 0 and 7 >= temp_y >= 0:
                if self.checkerboard[temp_y][temp_x] == self.turn:  # 若遇到己方
                    break
                elif self.checkerboard[temp_y][temp_x] == None:  # 若遇到空
                    continue_flag = True
                temp_x += dx
                temp_y += dy
            if not (7 >= temp_x >= 0 and 7 >= temp_y >= 0) or continue_flag:
                continue

            while True:
                temp_x -= dx
                temp_y -= dy
                if temp_x == start_x and temp_y == start_y:  # 若回到目標位置
                    break
                self.need_flip.append([temp_x, temp_y])

        if len(self.need_flip) == 0:
            return False  # 若沒有能翻色的排則回傳 False

        self.need_flip.append([col, row])
        return True

    def show_now_status(self):
        '''
        顯示當前狀態
        由此方法顯示出現在的黑棋與白棋之數量，之後可能把黑棋與白棋當作參數方便外部存取
        '''
        black_num = 0
        white_num = 0
        for y in self.checkerboard:
            for x in y:
                if x == 0:
                    white_num += 1
                elif x == 1:
                    black_num += 1
        print('Now Status: Black {}, White {}'.format(black_num, white_num))
        print('heuristic {} to human[{}]'.format(self.heuristic(), self.human))

    def show_checkerboard(self):
        '''
        顯示當前棋盤
        '''
        print('{0:^2} '.format(chr(12288)), end='')
        for c in self.cols:
            print('{0:{1}^2} '.format(c, chr(12288)), end='')

        for r, y in enumerate(self.checkerboard):
            print('\n{0:^2} '.format(r+1), end='')
            for x in y:
                if x == None:
                    print('[{0:{1}^1}]'.format('', chr(12288)), end='')
                if x == 0:
                    print('[{0:{1}^1}]'.format('白', chr(12288)), end='')
                if x == 1:
                    print('[{0:{1}^1}]'.format('黑', chr(12288)), end='')
            print('')

    def heuristic(self):
        h = 0
        n = len(self.checkerboard)
        for x in range(n):
            for y in range(n):
                if not self.checkerboard[y][x] is None:
                    # V2 參考了別人的評估表  還是被我打敗  = =
                    if [x, y] in [[0, 0], [0, 7], [7, 0], [7, 7]]:  # Good
                        h += 90 if self.checkerboard[y][x] == self.human_color else -90
                    elif [x, y] in [[1, 0], [0, 1], [6, 0], [7, 1], [0, 6], [1, 7], [7, 6], [6, 7]]:    # Bad
                        h += - \
                            60 if self.checkerboard[y][x] == self.human_color else 60
                    elif [x, y] in [[1, 1], [6, 6], [1, 6], [6, 1]]:    # Very Bad
                        h += - \
                            80 if self.checkerboard[y][x] == self.human_color else 80
                    elif ((x == 0) or (x == 7) or (y == 0) or (y == 7)):
                        h += 10 if self.checkerboard[y][x] == self.human_color else -10
                    elif ((x == 1) or (x == 6) or (y == 1) or (y == 6)):
                        h += 5 if self.checkerboard[y][x] == self.human_color else -5
                    else:
                        h += 1 if self.checkerboard[y][x] == self.human_color else -1

                    # V1 2019/06/08 17:10 被淘汰
                    # if [x, y] in [[0, 0], [0, 7], [7, 0], [7, 7]]:
                    #     h += 10 if self.checkerboard[y][x] == self.human_color else -10
                    # elif ((x == 0) or (x == 7) or (y == 0) or (y == 7)):
                    #     h += 3 if self.checkerboard[y][x] == self.human_color else -3
                    # else:
                    #     h += 1 if self.checkerboard[y][x] == self.human_color else -1
        return h

    def clear_screen(self):
        '''
        迷之清除畫面
        本該實現在其他地方的，但我原先只有這個 class，所以就先實現在這邊了
        '''
        # Clear Screen
        _ = os.system('cls' if os.name == 'nt' else 'clear')
