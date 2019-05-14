# -*- coding:utf-8 -*-
import time


class MyTree:
    def __init__(self, child_number, level_number, data):
        self.child_number = int(child_number)
        self.level_number = int(level_number)
        # Convert into int
        self.data = list(map(lambda x: int(x), data.split(',')))  # MemoryError
        # self.data = data.split(',')
        # for x in range(len(self.data)):
        #     self.data[x] = int(self.data[x])

        self.total_tree_node_count = int((
            self.child_number**(self.level_number+1)-1)/(self.child_number-1))
        # a^(n+1)-1 / (a-1)
        # 等比級數和公式
        # self.node_status = [0]*self.total_tree_node_count
        self.visited_node = 0
        self.inline_node = [None]*(self.total_tree_node_count-len(self.data))

        self.tree = self.inline_node + self.data
        self.root = 0   # root index number

    def get_child_index(self, index):
        if index >= len(self.inline_node):
            return None
        return [index*self.child_number+i for i in range(1, self.child_number+1)]

    def get_parent_index(self, index):
        if index == self.root:
            return None
        return int((index-1)/self.child_number)


def readData(filename):
    with open(filename, 'r') as f:
        result_data = f.read()
    return result_data.split('\n')[:-1]


def tree_DFS(t, index, maxflag, abs):
    childs = t.get_child_index(index)
    # t.node_status[index] = 1
    t.visited_node += 1
    if childs is None:
        # print('t.tree[{0}] = {1}'.format(index, t.tree[index]))
        return t.tree[index]

    if maxflag:
        t.tree[index] = float("-inf")
    else:
        t.tree[index] = float("inf")

    next_maxflag = maxflag is False  # Reverse

    for x in childs:
        temp = tree_DFS(t, x, next_maxflag, abs)
        if maxflag:
            if temp > t.tree[index]:
                t.tree[index] = temp
            if index != t.root and abs:
                alpha = t.tree[index]
                beta = t.tree[t.get_parent_index(index)]    #
                if beta <= alpha:
                    break
        else:
            if temp < t.tree[index]:
                t.tree[index] = temp
            if index != t.root and abs:
                alpha = t.tree[t.get_parent_index(index)]   #
                beta = t.tree[index]
                if beta <= alpha:
                    break
    return t.tree[index]


if __name__ == "__main__":
    start_time = time.time()
    alpha_beta_switch = False
    filename = '4-9-100.txt'
    data = readData(filename=filename)

    atree = MyTree(child_number=data[0], level_number=data[1], data=data[2])
    print('Create Tree Done.')
    tree_DFS(t=atree, index=atree.root, maxflag=True, abs=alpha_beta_switch)

    print('')
    print('ReadData From {}'.format(filename))
    print('visited: {}'.format(atree.visited_node))
    print('not visited: {}'.format(len(atree.tree)-atree.visited_node))
    print('root result: {}'.format(atree.tree[atree.root]))
    print('Used: {}s'.format(time.time()-start_time))
