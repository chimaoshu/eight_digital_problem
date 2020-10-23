from os import error
from os import system
import time
import copy
import sys

# 设置最大递归深度
sys.setrecursionlimit(100000000)

class status():
    """
    八数码问题中任意一个状态
    """

    up_movable: bool = True
    down_movable: bool = True
    left_movable: bool = True
    right_movable: bool = True

    # next_direction: str = ""

    # 0的坐标
    x: int = 0
    y: int = 0

    # 数据
    data: list = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
    ]

    # # 用于存储下一个移动方向
    # next_direction : str = ""

    def __init__(self, data: list):
        """
        传入二维数组3x3
        """
        self.data = data

        # 寻找0的坐标
        for i in range(3):
            if 0 in data[i]:
                self.y = i
                for j in range(3):
                    if data[i][j] == 0:
                        self.x = j

        self.reflash_movable_status()

    def reflash_movable_status(self):
        """
        刷新状态（上下左右可移动性）
        """

        if self.x == 0:
            self.left_movable = False

        if self.x == 2:
            self.right_movable = False

        if self.y == 2:
            self.down_movable = False

        if self.y == 0:
            self.up_movable = False

    def movable(self):
        """
        是否存在可移动的位置
        """
        return self.up_movable or self.down_movable or self.left_movable or self.right_movable

    def move(self, direction: str):
        """
        移动到下一个位置
        移动成功返回new_status
        否则返回False
        该函数会在移动成功后，把移动前的状态送入栈中
        """
        # print("移动方向：" + direction)
        global path, back_up

        if direction == "up":

            new_data = copy.deepcopy(self.data)
            new_data[self.y][self.x
                             ] = new_data[self.y - 1][self.x]
            new_data[self.y - 1][self.x] = 0

            if new_data in path:
                # print("该位置已经走过了")
                self.up_movable = False
                return False
            else:
                new_status = status(new_data)
                new_status.down_movable = False
                path.append(copy.deepcopy(self.data))

                # self.next_direction = "up"
                self.up_movable = False  # 如果有回退，可以防止左右横跳

                # 如果是第一个，由于栈里已经有了，则不用重复入栈
                if self.data == back_up[0].data:
                    back_up[0] = copy.deepcopy(self)
                else:
                    back_up.append(copy.deepcopy(self))

                return new_status

        elif direction == "down":

            new_data = copy.deepcopy(self.data)
            new_data[self.y][self.x
                             ] = new_data[self.y + 1][self.x]
            new_data[self.y + 1][self.x] = 0

            if new_data in path:
                # print("该位置已经走过了")
                self.down_movable = False
                return False
            else:
                new_status = status(new_data)
                new_status.up_movable = False
                path.append(copy.deepcopy(self.data))

                # self.next_direction = "down"
                self.down_movable = False

                # 如果是第一个，由于栈里已经有了，则不用重复入栈
                if self.data == back_up[0].data:
                    back_up[0] = copy.deepcopy(self)
                else:
                    back_up.append(copy.deepcopy(self))

                return new_status

        elif direction == "left":

            new_data = copy.deepcopy(self.data)
            new_data[self.y][self.x
                             ] = new_data[self.y][self.x - 1]
            new_data[self.y][self.x - 1] = 0

            if new_data in path:
                # print("该位置已经走过了")
                self.left_movable = False
                return False
            else:
                new_status = status(new_data)
                new_status.right_movable = False
                path.append(copy.deepcopy(self.data))

                # self.next_direction = "left"
                self.left_movable = False

                # 如果是第一个，由于栈里已经有了，则不用重复入栈
                if self.data == back_up[0].data:
                    back_up[0] = copy.deepcopy(self)
                else:
                    back_up.append(copy.deepcopy(self))

                return new_status

        elif direction == "right":

            new_data = copy.deepcopy(self.data)
            new_data[self.y][self.x
                             ] = new_data[self.y][self.x + 1]
            new_data[self.y][self.x + 1] = 0

            if new_data in path:
                # print("该位置已经走过了")
                self.right_movable = False
                return False
            else:
                new_status = status(new_data)
                new_status.left_movable = False
                path.append(copy.deepcopy(self.data))

                # self.next_direction = "right"
                self.right_movable = False

                # 如果是第一个，由于栈里已经有了，则不用重复入栈
                if self.data == back_up[0].data:
                    back_up[0] = copy.deepcopy(self)
                else:
                    back_up.append(copy.deepcopy(self))

                return new_status

        else:
            print("非法的移动方向参数")
            raise error

    def auto_move(self):
        """
        让实例自己决定一个可行方向进行移动
        移动成功返回new_status
        移动失败（前进后又退回）返回False
        """
        # if not self.movable():
        #     return False

        if self.up_movable:
            return self.move("up")

        elif self.down_movable:
            return self.move("down")

        elif self.left_movable:
            return self.move("left")

        elif self.right_movable:
            return self.move("right")
        else:
            print("如果程序走到这里，那么有bug")
            raise error

    def show(self, searching:bool):
        if searching:
            return
        for i2 in self.data:
            for i3 in i2:
                if i3 == 0:
                    print('\033[1;37m0\033[0m', " ", end="")
                    continue
                print(i3, " ", end="")
            else:
                print()

class storage_status():
    """
    用于在达到最大搜索深度时存储临时状态
    """

    def __init__(self, path: list, current_status: status):
        """
        只需path和当前状态，便可恢复原来状态
        current_status会变成新的初始状态，若无路则该支路无效
        """
        self.path = path
        self.current_status = current_status


def limited_dfs(initial_storage_status: storage_status, goal_status: status, max_depth: int):
    """
    有限制的深度优先搜索
    返回True表示成功找到
    返回False表示暂时没找到解
    返回None表示已经明确无解了
    :param max_depth
    当最大搜索深度为1，则为宽度优先搜索
    当最大搜索深度为无穷，则为深度优先搜索
    否则就介于两者之间
    """

    global storage_status_queue, answer, back_up, path

    # 需要深拷贝，否则只是引用
    # path只在本次函数中使用，用完存到status，不再需要全局了
    path = copy.deepcopy(initial_storage_status.path)
    initial_status = initial_storage_status.current_status
    current_status = copy.deepcopy(initial_status)

    # back_up也只需在本次函数中用到，考虑到让类中用，就全局了
    # back_up用于备份每一个走过的状态节点，方便回滚（存储类）
    # back_up就是dfs中用到的栈了
    # 当一个根节点的小于搜索深度的子孙节点都遍历完时（即该函数完成时），back_up中的数据就没用了
    # 这里必须对back_up清空，然后加上第一个
    # 走出第一步的时候，函数会进行判断，back_up不会再次存储一次初始元素
    back_up = []
    back_up.append(copy.deepcopy(current_status))

    # print("新的初始状态：")
    current_status.show(searching=True)

    #print("搜索深度为%d" % max_depth)

    # 当根节点不可移动时，意味着这个函数已经结束了他的使命（该方向无解）
    # 只要不符合上述条件，就说明还有一些节点没有遍历到，就可以继续递归
    while current_status.movable() or current_status.data != initial_status.data:

        # 虽然不可移动，但不是根节点，因此可以回退
        if not current_status.movable() and current_status.data != initial_status.data:

            # print("无路可走，往回退")

            path.pop()

            # 如果上一个就是根节点了，回退时保留栈底
            if len(back_up) == 1:
                current_status = back_up[0]
            else:
                current_status: status = back_up.pop()

            current_status.show(searching=True)
            continue

        # 找到解
        if current_status.data == goal_status.data:

            # 加上最后一个数据
            path.append(copy.deepcopy(current_status.data))
            answer = path
            print("已找到解")
            return True

        # 移动
        new_status: status = current_status.auto_move()
        if new_status:
            # 上一个状态已存储入栈
            current_status = new_status
        else:
            # print("原路返回，状态不变")
            continue
        current_status.show(searching=True)

        # 达到最大搜索深度后回溯（搜索深度为多少，back_up就有多少个元素）
        if len(back_up) == max_depth:

            # print("在这个方向上已达到最大的搜索深度，存储当前状态，回溯")

            # 存储当前走过的路径
            temp = storage_status(path, copy.deepcopy(current_status))

            # 在队尾存储下这个状态
            storage_status_queue.append(copy.deepcopy(temp))

            # 回溯到上个节点
            path.pop()

            # 如果上一个就是根节点了，回退时保留栈底
            if len(back_up) == 1:
                current_status = back_up[0]
            else:
                current_status: status = back_up.pop()

            current_status.show(searching=True)
            continue

    # 程序走到这里，说明已经遍历完了
    # 检查可移动性（若不可移动，则说明该点(根节点)的所有小于最大搜索深度的子节点都已经遍历完成）
    # 若可移动就让他自己去移动
    # 一旦进入这个循环，除非找到结果或者确定无解，否则不会再跳出该循环
    if current_status.movable():
        raise error

    # 首先删除队列中这个无法继续移动的“根”节点
    storage_status_queue.pop(0)

    # 此时若无存储，说明无解
    if len(storage_status_queue) == 0:
        # 问题无解
        return None

    else:
        # 若有存储，按队列顺序，以队头为新的初始节点递归调用
        # print("当前根节点已经遍历完成，从队列首节点继续",end='')
        success: bool = limited_dfs(
            storage_status_queue[0], goal_status, max_depth)
        if success:
            return True  # 找到解
        elif success == None:
            return None  # 问题无解
        else:  # 暂时没找到解
            storage_status_queue.pop(0)  # 删除失败的队头状态

def get_inverse_number(a:str):
    """逆序数"""
    output = 0
    for i1 in range(len(a)):
        if a[i1] == '0':
            continue
        for i2 in range(i1):
            if int(a[i1]) < int(a[i2]):
                output += 1
    return output
            
def has_solution(a, b):
    """
    是否有解
    """
    x = get_inverse_number(a) % 2
    y = get_inverse_number(b) % 2
    return x == y

if __name__ == "__main__":

    while 1:

        system("cls")

        a = input("输入初始状态：")
        b = input("输入末尾状态：")
        print()

        if not has_solution(a, b):
            print("无解")
            raise error

        init_data = [
            [int(a[0]),int(a[1]),int(a[2])],
            [int(a[3]),int(a[4]),int(a[5])],
            [int(a[6]),int(a[7]),int(a[8])]
        ]
        
        goal_data = [
            [int(b[0]),int(b[1]),int(b[2])],
            [int(b[3]),int(b[4]),int(b[5])],
            [int(b[6]),int(b[7]),int(b[8])]
        ]

        # initial_status = status([
        #     [2, 8, 3],
        #     [1, 6, 4],
        #     [7, 0, 5],
        # ])

        # goal_status = status([
        #     [8, 3, 4],
        #     [2, 0, 1],
        #     [7, 6, 5],
        # ])

        # 测试用例：
        # 283164705 
        # 208143765

        initial_status = status(init_data)
        goal_status = status(goal_data)

        # 全局变量，path存状态中的data，方便识别是否是已走过的路，是close
        path = []

        # 全局变量，dfs中的栈，为了让类中修改容易，直接全局变量
        back_up = []

        # 全局变量，最后的答案
        answer = []

        # 每次搜索到最大深度后回溯时就把状态存储下来
        # 这个队列其实就是广度优先搜索用到的队列（只不过这里是有限制的深度搜索）
        # 这里把第一个状态送入队列
        # 全局变量，这个其实是open
        storage_status_queue = []
        storage_status_queue.append(copy.deepcopy(
            storage_status(path, initial_status)))

        MAX_DEPTH = int(input("最大搜索深度(1~无穷)："))

        start_time = time.time()
        # 传入的参数永远是队列的队头
        success: bool = limited_dfs(
            initial_storage_status=storage_status_queue[0],
            goal_status=goal_status,
            max_depth=MAX_DEPTH
        )
        end_time = time.time()
        total_step = len(answer)
        print("步数：%d 花费时间：%.5f" %(total_step, end_time-start_time))

        if success:
            input()
            system("cls")
            for i1 in range(total_step):
                print("第%d步：（共%d步）" % (i1, total_step - 1))
                for i2 in answer[i1]:
                    for i3 in i2:
                        if i3 == 0:
                            print('\033[1;37m0\033[0m', " ", end="")
                            continue
                        print(i3, " ", end="")
                    else:
                        print()
                else:
                    print("\n目标状态")
                    goal_status.show(searching=False)

                    if i1 == total_step - 1:
                        print("已移动至正确答案")
                    
                    input()
                    system("cls")
        else:
            print("问题无解")
