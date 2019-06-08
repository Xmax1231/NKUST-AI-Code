# -*- coding:utf-8 -*-

import random
import time


class node_pool(list):
    def __init__(self, data=[]):
        super(node_pool, self).__init__(data)

    def sort(self):
        return super(node_pool, self).sort(key=lambda x: x.get_collision())


class node:
    def __init__(self, data):
        self.status = data  # [0, 1, 2, 3, 4, 5, 6, 7]
        self.collision = -1
        self.live_time = 1

    def get_collision(self):
        return self.collision if self.collision != -1 else self.get_collision_num()

    def get_collision_num(self):
        num = 0
        status_length = len(self.status)

        for x in range(status_length):
            y = self.status[x]

            for offset_x, offset_y in [[-1, -1], [-1, 0], [-1, 1]]:
                temp_x = x + offset_x
                temp_y = y + offset_y

                while ((status_length-1) >= temp_x >= 0) and ((status_length-1) >= temp_y >= 0):
                    for nx in range(status_length):
                        ny = self.status[nx]
                        if (nx == temp_x) and (ny == temp_y):
                            num += 1
                    temp_x += offset_x
                    temp_y += offset_y

        return num


def crossover(pool, n, mutation):
    now_pool_len = len(pool)
    if now_pool_len <= 1:
        return

    for pn in range(now_pool_len):
        pool[pn].live_time += 1
        p_1 = random.randint(0, now_pool_len-1)
        p_2 = random.randint(0, now_pool_len-1)
        while p_1 == p_2:   # p_1 and p_2 should different
            p_2 = random.randint(0, now_pool_len-1)

        _scale = random.randint(1, n-2)  # 1~6
        try:
            temp_status = pool[p_1].status[:_scale]+pool[p_2].status[_scale:]
        except IndexError:
            print(now_pool_len)
            print(p_1)
            print(p_2)
            print(_scale)
            exit()

        if mutation_flag(mutation):
            z = random.randint(2, 6)
            for x in range(z):
                _x = random.randint(1, n-2)
                y = random.randint(0, n-1)
                while temp_status[((x+_x) % n)] == y:
                    y = random.randint(0, n-1)
                temp_status[((x+_x) % n)] = y

        new_node = node(temp_status)
        pool.append(new_node)

    return


def mutation_flag(rate):
    x = random.randint(1, 10)
    if rate * 10 >= x:
        return True
    return False


def initialization(n, pool_num):
    pool = node_pool()
    for _ in range(pool_num):
        temp_p = []
        for __ in range(n):
            y = random.randint(0, n-1)
            temp_p.append(y)
        pool.append(node(temp_p))
    return pool


def show_best(pool):
    print('Now Best Is {}:{:02} {:02}'.format(
        pool[0].status, pool[0].get_collision(), pool[0].live_time))


def show_all(pool):
    for i, x in enumerate(pool):
        print('{:02} {}:{:02}'.format(i, x.status, x.get_collision()))


if __name__ == "__main__":
    start_time = time.time()
    n = 8   # 8Queen
    pool_num = 10   #
    mutation = 0.2
    live_time_limit = 5

    pool = initialization(n=n, pool_num=pool_num)
    pool.sort()
    show_best(pool)
    turn = 1
    while pool[0].get_collision() != 0:
        print('CROSSOVER. {}T'.format(turn))
        crossover(pool=pool, n=n, mutation=mutation)
        pool.sort()
        pool = node_pool(filter(lambda x: x.live_time < live_time_limit, pool))
        del pool[pool_num:]  # Kill
        show_best(pool)
        turn += 1
    print('{} Trun Ago'.format(turn))
    print('Used: {}s'.format(time.time()-start_time))
