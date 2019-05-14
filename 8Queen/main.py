#-*- coding:utf-8 -*-
import copy
import time
# import os
import random

## Check Collision
def get_collision_num(cb):
	num = 0
	for x in range(len(cb)):
		for p in range(len(cb[x])):
			y = p
			if cb[y][x] == 1:
				break
		# for offset_x, offset_y in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
		# for offset_x, offset_y in [[1, 1], [1, 0], [1, -1], [-1, -1], [-1, 0], [-1, 1]]:
		for offset_x, offset_y in [[-1, -1], [-1, 0], [-1, 1]]:
			temp_x = x + offset_x
			temp_y = y + offset_y

			while ((len(cb)-1) >= temp_x >= 0) and ((len(cb)-1) >= temp_y >= 0):
				if cb[temp_y][temp_x] == 1:
					num += 1
				temp_x += offset_x
				temp_y += offset_y
	return num


def hill_climbing(cb, status):
	best_collision_num = get_collision_num(cb)
	anser_offset = []

	for x in range(len(cb)):
		for y in range(1, len(cb[x])):
			temp_cb = copy.deepcopy(cb)
			temp_cb[status[x]][x] = 0
			temp_cb[(status[x]+y)%len(cb[x])][x] = 1
			temp_collision_num = get_collision_num(temp_cb)
			if temp_collision_num < best_collision_num:
			# if temp_collision_num <= best_collision_num:
				best_collision_num = temp_collision_num
				# anser_offset.append([x, (status[x]+y)%len(cb[x])])
				anser_offset = [x, (status[x]+y)%len(cb[x])]

	# input(len(anser_offset))
	if len(anser_offset) > 0:
		# r = random.randint(0, len(anser_offset)-1)
		# anser = anser_offset[r]
		anser = anser_offset

		cb[status[anser[0]]][anser[0]] = 0
		cb[anser[1]][anser[0]] = 1

		status[anser[0]] = anser[1]
		return best_collision_num
	else:
		# input('Init')
		return initialization(cb=cb, status=status)


def initialization(cb, status):
	for x in range(len(status)):
		r = random.randint(0, len(status)-1)
		status[x] = r

	for y in range(len(cb)):
		for x in range(len(cb[y])):
			if status[x] == y:
				cb[y][x] = 1
			else:
				cb[y][x] = 0

	return get_collision_num(cb)


def show_info(cb, status):
	# _ = os.system('cls' if os.name == 'nt' else 'clear')
	print(status)
	print('Now Collision Num: {}'.format(get_collision_num(cb=cb)))
	for y in cb:
		print(y)


if __name__ == '__main__':
	start_time = time.time()
	current_turn = 0
	current_collision_num = 0
	restart_count = 0
	n = 8

	## Initialization
	status = [0]*n
	checkerboard = [[0]*n for i in range(n)]
	initialization(cb=checkerboard, status=status)
	# input('初始化 衝突數量：{}'.format(initialization(cb=checkerboard, status=status)))

	current_collision_num = get_collision_num(cb=checkerboard)
	while current_collision_num > 0:
		# print(status)
		current_turn += 1
		best_collision_num = hill_climbing(cb=checkerboard,
										status=status)
		if best_collision_num >= current_collision_num:
			# print('[#] ReStart\n')
			restart_count += 1
		# current_collision_num = get_collision_num(cb=checkerboard)
		# if current_collision_num != best_collision_num:
		# 	exit('[!] Error')
		current_collision_num = best_collision_num

		# show_info(cb=checkerboard, status=status)
		# input()

	show_info(cb=checkerboard, status=status)
	print('Used: {0:6.4f}s'.format(time.time()-start_time))
	print('Turn: {0}'.format(current_turn))
	print('ReStart: {0}'.format(restart_count))
