from collections import Counter

# 上移
def shift_up(li, index):
    parent = (index-1)//2
    while index > 0 and li[index][0] < li[parent][0]:
        li[index], li[parent] = li[parent], li[index]
        index = parent
        parent = index-1//2


# 下沉
def shift_down(li, low, high):
    target = li[low] # 堆顶元素
    i = low
    j = 2*i+1
    while j <= high:
        if j+1 <= high and li[j+1][0] < li[j][0]:
            j = j+1
        if li[j][0] < target[0]:
            # 如果小于，则放在堆顶
            li[i] = li[j]
            i = j
            j = 2*i+1
        else:
            break
    li[i] = target


def heap_sort(li, k):
    # 建堆
    heap = []
    for key, val in li.items():
        if len(heap) < k:
            heap.append((val, key))
            shift_up(heap, len(heap)-1)
        else:
            # 如果大于堆顶元素，则放进去
            if val > heap[0][0]:
                heap[0] = (val, key)
                shift_down(heap, 0, len(heap)-1)
    res = [_[1]for _ in heap]
    return res


nums = [5,2,5,3,5,3,1,1,3]
k = 2
count = Counter(nums)
print(count)
print(heap_sort(count, k))
