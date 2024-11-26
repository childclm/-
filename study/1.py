# 堆排序
# 建立堆
# 得到堆顶元素，为最大元素
# 去除堆顶元素，将堆最后一个元素放在堆顶，通过一次调整使堆重新有序
# 堆顶元素为第二大元素
# 重复步骤3


def sift(li, low, high):
    """

    :param li: 列表
    :param low: 堆顶元素的位置
    :param high: 堆最后一个元素的位置
    :return:
    """
    i = low  # 最开始指向根节点
    j = 2*i+1  # 指向左节点
    temp = li[low]
    while j <= high:
        # 如果右节点存在且右节点更大，则j指向右节点
        if j+1 <= high and li[j+1] > li[j]:
            j = j+1
        if li[j] > temp:  # 如果大于堆顶元素，则放上去
            li[i] = li[j]
            # 放上去之后更新下i，j  i到j的位置，j重新指向i的下一个左节点
            i = j
            j = 2*i+1
        else:
            li[i] = temp  # 把temp放到某一级领导的位置
            break
    # 当循环后发现j>high,则把temp赋值给当前i指向的位置
    else:
        li[i] = temp


def heap_sort(li):
    n = len(li)
    # 孩子对应的下标为i则，他的父亲对应的下标为(i-1)//2
    for i in range(n//2-1, -1, -1):
        sift(li, i, n-1)
    # 建堆完成了
    for i in range(n-1, -1, -1):
        li[0], li[i] = li[i], li[0]
        # 去除根节点，把最后一个节点放到根节点上去再进行排序
        sift(li, 0, i-1)



li = [_ for _ in range(7)]
import random
random.shuffle(li)
print(li)
heap_sort(li)
print(li)



