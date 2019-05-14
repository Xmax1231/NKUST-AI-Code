#-*- coding:utf-8 -*-
'''
This Is Full Random Version.
'''
import copy
import time
import os
import random

## Check Collision
def get_collision_num(status):
	num = 0
	for pn in range(len(status)):
		other_status = status[:pn] + status[pn+1:]
		x = status[pn][0]
		y = status[pn][1]

		# for p in other_status:	# 重疊
		# 	if [x, y] == p:
		# 		num += 1

		# for offset_x, offset_y in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
		for offset_x, offset_y in [[0, -1], [-1, -1], [-1, 0], [-1, 1]]:
			temp_x = x #+ offset_x
			temp_y = y #+ offset_y

			while ((len(status)-1) >= temp_x >= 0) and ((len(status)-1) >= temp_y >= 0):
				# for p in other_status:
				# 	if [temp_x, temp_y] == p:
				# 		num += 1
				if [temp_x, temp_y] in other_status:
						num += 1
				temp_x += offset_x
				temp_y += offset_y

	return num


def hill_climbing(status):
	original_collision_num = get_collision_num(status=status)
	anser_offset = []

	best_collision_num = original_collision_num
	for pn in range(len(status)):
		for y in range(len(status)):
			for x in range(len(status)):
				# if [x, y] in status:
				# 	continue
				# continue_flag = False
				# break_flag = False
				# for p in status:
				# 	if y == p[1]:
				# 		break_flag = True
				# 		break
				# 	elif x == p[0]:
				# 		continue_flag = True
				# 		break
				# if continue_flag:
				# 	continue
				# if break_flag:
				# 	break

				temp_status = copy.deepcopy(status)
				temp_status[pn] = [x, y]
				temp_collision_num = get_collision_num(status=temp_status)
				if temp_collision_num < original_collision_num:
					if temp_collision_num < best_collision_num:
						best_collision_num = temp_collision_num
						anser_offset = [[pn, x, y]]
					elif temp_collision_num == best_collision_num:
						anser_offset.append([pn, x, y])

	if len(anser_offset) > 0:
		random.seed(time.time())
		r = random.randint(0, len(anser_offset)-1)
		anser = anser_offset[r]
		status[anser[0]] = [anser[1], anser[2]]
		return best_collision_num
	else:
		return initialization(status=status)


def initialization(status):
	# random.seed(time.time())
	for p in range(len(status)):
		x = random.randint(0, len(status)-1)
		y = random.randint(0, len(status)-1)
		status[p] = [x, y]

	return get_collision_num(status=status)


def show_info(status):
	# _ = os.system('cls' if os.name == 'nt' else 'clear')
	print(status)
	print('Now Collision Num: {}'.format(get_collision_num(status=status)))

	n = len(status)
	cb = [[0]*n for i in range(n)]
	for y in range(len(cb)):
		for x in range(len(cb[y])):
			for p in status:
				if [x, y] == p:
					cb[y][x] = 1
	for y in cb:
		print(y)


if __name__ == '__main__':
	start_time = time.time()
	current_turn = 0
	current_collision_num = 0
	restart_count = 0
	n = 8

	## Initialization
	status = [[0]*2 for i in range(n)]	# [x, y] * n
	checkerboard = [[0]*n for i in range(n)]
	initialization(status=status)
	# status[0] = [0, 6]
	# status[1] = [1, 4]
	# status[2] = [2, 2]
	# status[3] = [3, 0]
	# status[4] = [4, 5]
	# status[5] = [5, 7]
	# status[6] = [6, 1]
	# status[7] = [7, 3]

	current_collision_num = get_collision_num(status=status)
	while current_collision_num > 0:
		current_turn += 1
		print('Turn:{}'.format(current_turn), end='\r')
		best_collision_num = hill_climbing(status=status)
		if best_collision_num >= current_collision_num:
			restart_count += 1
		# current_collision_num = get_collision_num(status=status)
		# if current_collision_num != best_collision_num:
		# 	exit('[!] Error')
		current_collision_num = best_collision_num

	show_info(status=status)
	print('Used: {0:6.4f}s'.format(time.time()-start_time))
	print('Turn: {0}'.format(current_turn))
	print('ReStart: {0}'.format(restart_count))