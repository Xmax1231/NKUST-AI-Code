#-*- coding:utf-8 -*-
import os

class BWC:
	def __init__(self):
		self.rows = ['1', '2', '3', '4', '5', '6', '7', '8']
		self.cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
		self.checkerboard = [[None]*8 for i in range(8)]	## None:空 0:白 1:黑
		self.need_flip = []
		self.can_put_pos = []

	def game_start(self):
		self.checkerboard[3][3] = self.checkerboard[4][4] = 0
		self.checkerboard[3][4] = self.checkerboard[4][3] = 1
		self.turn = 1	## Whose round? 
		self.next_turn()

	def next_turn(self):
		self.clear_screen()
		self.show_now_status()
		print('{} Turn'.format('黑' if self.turn == 1 else '白'))
		self.show_checkerboard()
		
		if not self.turn_check():	## You will pass this turn
			self.turn = (self.turn + 1) % 2
			self.next_turn()
		print(self.can_put_pos)

		put = input('下哪邊? ')	## EX: f5
		while not self.put_check(put):
			put = input('請輸入有效值? ')	

		self.flip(self.need_flip)
		self.turn = (self.turn + 1) % 2
		self.next_turn()

	def turn_check(self):
		self.can_put_pos = []
		for y in self.rows:
			for x in self.cols:
				if self.put_check('{}{}'.format(x, y)):
					self.can_put_pos.append([x, y])
		if len(self.can_put_pos) == 0:
			return False
		return True



	def flip(self, need_flip):
		for x, y in need_flip:
			self.checkerboard[y][x] = self.turn	## 將需要的位置翻色


	def put_check(self, put):
		row = put[1]
		col = put[0]
		## Easy Check
		if row not in self.rows or col not in self.cols:
			return False
		row = self.rows.index(row)
		col = self.cols.index(col)

		## Hard Check
		other_color = (self.turn + 1) % 2
		self.need_flip = []

		if self.checkerboard[row][col] != None:
			return False
		##                 上      右上    右       右下     下       左下       左       左上
		check_position = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]## dx, dy
		for dx, dy in check_position:
			start_x = col
			start_y = row

			temp_x = start_x + dx
			temp_y = start_y + dy
			if (not (7 >= temp_x >= 0 and 7 >= temp_y >= 0) or
							self.checkerboard[temp_y][temp_x] == None):
				continue

			while 7 >= temp_x >= 0 and 7 >= temp_y >= 0:
				if self.checkerboard[temp_y][temp_x] == other_color: ## 若遇到對方
					break
				temp_x += dx
				temp_y += dy
			if not (7 >= temp_x >= 0 and 7 >= temp_y >= 0):
				continue

			while 7 >= temp_x >= 0 and 7 >= temp_y >= 0:
				if self.checkerboard[temp_y][temp_x] == self.turn: ## 若遇到己方
					break
				temp_x += dx
				temp_y += dy
			if not (7 >= temp_x >= 0 and 7 >= temp_y >= 0):
				continue

			while True:
				temp_x -= dx
				temp_y -= dy
				if temp_x == start_x and temp_y == start_y: ## 若回到目標位置
					break
				self.need_flip.append([temp_x, temp_y])

		if len(self.need_flip) == 0:
			return False	# 若沒有能翻色的排則回傳 False

		self.need_flip.append([col, row])
		return True

	def show_now_status(self):
		black_num = 0
		white_num = 0
		for y in self.checkerboard:
			for x in y:
				if x == 0:
					white_num += 1
				elif x == 1:
					black_num += 1
		print('Now Status: Black {}, White {}'.format(black_num, white_num))

	def show_checkerboard(self):
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

	def clear_screen(self):
		# Clear Screen
		_ = os.system('cls' if os.name == 'nt' else 'clear')
