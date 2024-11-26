def merge_sort(li, low, mid, high):
    i = low
    j = mid+1
    while i <= mid and j <= high:
        if li[i] < li[j]:
            i += 1
        else:
            # 右边有序更小
            temp = li[j]
            # 左边右移一位，把temp插进去
            for k in range(mid, i-1, -1):
                li[k+1] = li[k]
            li[i] = temp
            i += 1
            mid += 1
            j = mid + 1


def merge(li, low, high):
    if low < high:
        mid = (low + high) // 2
        merge(li, low, mid)
        merge(li, mid+1, high)
        merge_sort(li, low, mid, high)

import random
a = [random.randint(1, 100) for _ in range(10)]
random.shuffle(a)
print(a)
merge(a, 0, len(a)-1)
print(a)