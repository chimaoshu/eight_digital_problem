from os import error
from os import system
import time
import copy

def find_index_of_a_number_in_a_two_dimension_list(list:list, element):

    x = None
    y = None
    data = list
    for i in range(3):
        if element in data[i]:
            y = i
            for j in range(3):
                if data[i][j] == element:
                    x = j
    if x != None and y != None:
        return x,y
    else:
        print('数据错误')
        raise error

def get_manhattan_distance(self):

    # 0~8
    global goal_status
    manhattan_distance = 0
    for i in range(9):
        if i == 0:
            continue
        x1, y1 = find_index_of_a_number_in_a_two_dimension_list(self.data, i)
        x2, y2 = find_index_of_a_number_in_a_two_dimension_list(goal_status.data, i)
        manhattan_distance += abs(x1 - x2) + abs(y1 - y2)

    # print(manhattan_distance)
    return manhattan_distance

# 5min
def get_amount_of_different_number(self):

    global goal_status
    amount_of_different_number = 0
    for i in range(9):
        if i == 0:
            continue
        if find_index_of_a_number_in_a_two_dimension_list(self.data, i) != find_index_of_a_number_in_a_two_dimension_list(goal_status.data, i):
            amount_of_different_number += 1
    
    print(amount_of_different_number)
    return amount_of_different_number

# 半小时以上时间找不出答案
def get_difference_of_zero(self):

    global goal_status
    x1, y1 = find_index_of_a_number_in_a_two_dimension_list(self.data, 0)
    x2, y2 = find_index_of_a_number_in_a_two_dimension_list(goal_status.data, 0)
    return abs(x1 - x2) + abs(y1 - y2)


class status():
    """
    八数码问题中任意一个状态
    """

    up_movable: bool = True
    down_movable: bool = True
    left_movable: bool = True
    right_movable: bool = True

    # 0的坐标
    x: int
    y: int

    # 父结点
    parent_status = None

    # 预测值
    f_value: int
    g_value: int
    h_value: int

    # 数据
    data: list

    def __init__(self, data: list, g_value : list, parent_status=None, calculate_g_h_f=True):
        """
        传入二维数组3x3
        """
        self.data = data
        self.parent_status = parent_status

        # 寻找0的坐标
        for i in range(3):
            if 0 in data[i]:
                self.y = i
                for j in range(3):
                    if data[i][j] == 0:
                        self.x = j

        self.refresh_movable_status()
        
        if not calculate_g_h_f:
            return

        # self.g_value = self.calculate_g_value()\
        self.g_value = g_value
        self.h_value = self.calculate_h_value()
        self.f_value = self.calculate_f_value()

    def calculate_h_value(self):
        """启发式算法"""
        return get_manhattan_distance(self)
        # return get_amount_of_different_number(self)
        # return get_difference_of_zero(self)


    def calculate_f_value(self):
        return self.g_value + self.h_value

    def refresh_movable_status(self):
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

    def get_movable_status(self):
        """返回一个列表（包含status）"""
        movable_direction: list = []
        if self.up_movable:
            movable_direction.append(self.move("up"))
        if self.down_movable:
            movable_direction.append(self.move("down"))
        if self.left_movable:
            movable_direction.append(self.move("left"))
        if self.right_movable:
            movable_direction.append(self.move("right"))
        return movable_direction

    def movable(self):
        """
        是否存在可移动的位置
        """
        return self.up_movable or self.down_movable or self.left_movable or self.right_movable

    def move(self, direction: str):
        """
        移动到下一个位置，不改变当前实例
        返回一个新的状态new_status
        """
        global explored
        #print("移动方向：" + direction)
        if direction == "up":

            new_data = copy.deepcopy(self.data)
            new_data[self.y][self.x
                             ] = new_data[self.y - 1][self.x]
            new_data[self.y - 1][self.x] = 0

            new_status = status(new_data, parent_status=self,g_value=self.g_value + 1)
            return new_status

        elif direction == "down":

            new_data = copy.deepcopy(self.data)
            new_data[self.y][self.x
                             ] = new_data[self.y + 1][self.x]
            new_data[self.y + 1][self.x] = 0

            new_status = status(new_data, parent_status=self,g_value=self.g_value + 1)
            return new_status

        elif direction == "left":

            new_data = copy.deepcopy(self.data)
            new_data[self.y][self.x
                             ] = new_data[self.y][self.x - 1]
            new_data[self.y][self.x - 1] = 0

            new_status = status(new_data, parent_status=self,g_value=self.g_value+1)
            return new_status

        elif direction == "right":

            new_data = copy.deepcopy(self.data)
            new_data[self.y][self.x
                             ] = new_data[self.y][self.x + 1]
            new_data[self.y][self.x + 1] = 0

            new_status = status(new_data, parent_status=self,g_value=self.g_value+1)
            return new_status

        else:
            print("非法的移动方向参数")
            raise error

    def show(self):
        """显示"""
        for i2 in self.data:
            for i3 in i2:
                # if i3 == 0:
                #     # print('\033[1;37m0\033[0m', " ", end="")
                #     print('0 ',end="")
                #     continue
                print(i3, " ", end="")
            else:
                print()


def get_minimum_f_value_in_frontier(frontier: list):
    """
    从frontier中获取最小的F值的元素
    """
    get_f_value = lambda x: x.f_value
    frontier.sort(key=get_f_value)
    return frontier[0]

def status_in_list(st: status, list_of_status: list):
    """
    看某个状态是否已经存在
    存在：返回status
    不存在：返回None
    """
    for each_status in list_of_status:
        if each_status.data == st.data:
            return each_status
    else:
        return None


def A_star(initial_status: status, goal_status: status):
    """
    docstring
    """
    # 初始时间
    start_time = time.time()

    # 存储走过的路(status)，相当于close
    global explored

    # 存储某个节点的邻居节点(status)，相当于open
    global frontier
    frontier.append(initial_status)

    # 不为空
    while len(frontier):

        current_status: status = get_minimum_f_value_in_frontier(frontier)
        if current_status.data == goal_status.data:
            # explored.append(minimum_f_value_in_frontier)
            break

        for children_status in current_status.get_movable_status():

            children_status: status

            # 是否已经存在于frontier，确实有可能出现这种情况
            the_same_status_in_frontier = status_in_list(children_status, frontier)
            if the_same_status_in_frontier != None and current_status.g_value + 1 < the_same_status_in_frontier.g_value:

                # 更新父节点、g、h、f的值
                the_same_status_in_frontier.parent_status = current_status
                the_same_status_in_frontier.g_value = current_status.g_value + 1
                the_same_status_in_frontier.h_value = the_same_status_in_frontier.calculate_h_value()
                the_same_status_in_frontier.f_value = the_same_status_in_frontier.calculate_f_value()

            # 是否已经存在于explored
            the_same_status_in_explored = status_in_list(children_status, explored)
            if the_same_status_in_explored != None and current_status.g_value + 1 < the_same_status_in_explored.g_value:

                # 更新父节点、g、h、f的值
                the_same_status_in_explored.parent_status = current_status
                the_same_status_in_explored.g_value = current_status.g_value + 1
                the_same_status_in_explored.h_value = the_same_status_in_explored.calculate_h_value()
                the_same_status_in_explored.f_value = the_same_status_in_explored.calculate_f_value()

                # 把children_status从explored取出，放进frontier
                frontier.append(copy.deepcopy(children_status))
                explored.remove(children_status)

            # 如果不在explored也不在frontier
            if  (the_same_status_in_explored == None ) and (the_same_status_in_frontier == None):

                # 设置父节点
                children_status.parent_status = current_status

                # 将children_status插入frontier中
                frontier.append(children_status)

        # 最后把minimum_f_value_in_frontier插入explored中
        # print('启发值%d' %minimum_f_value_in_frontier.f_value)
        explored.append(current_status)
        frontier.remove(current_status)

    # 结束时间
    end_time = time.time()

    print("已经找到解")
    answer :list = []
    while current_status:
        answer.append(current_status)
        current_status = current_status.parent_status

    answer.reverse()
    for i in answer:
        print("第%d步，启发值：%d" %(i.g_value, i.f_value))
        i.show()
        print()
    else:
        print("一共搜索%d次，最终答案%d步，耗时%.5f秒" %(len(explored), len(answer), end_time - start_time))

def get_inverse_number(a:str):
    """逆序数"""
    output = 0
    
    for i1 in range(len(a)):

        # 跳过0
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

    a = input("输出初始状态：")
    b = input("输入末尾状态：")
    
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

    frontier = [] #open
    explored = [] #close

    # goal_status = status([
    #     [2, 0, 8],
    #     [1, 4, 3],
    #     [7, 6, 5],
    # ], calculate_g_h_f=False)

    # initial_status = status([
    #     [2, 0, 8],
    #     [1, 4, 3],
    #     [7, 6, 5],
    # ])  

    goal_status = status(goal_data, calculate_g_h_f=False,g_value=None)
    initial_status = status(init_data,g_value=0)  

    A_star(initial_status, goal_status)