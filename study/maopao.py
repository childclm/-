import heapq
def fetch(arr):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
    return arr


def select_sort(arr):
    for i in range(len(arr)-1):
        min_ = i
        for j in range(i, len(arr)):
            if min_ > arr[j]:
                min_ = j
        arr[i], arr[min_] = arr[min_], arr[i]


def insert_sort(arr):
    for i in range(1, len(arr)):
        right = i-1
        while right >= 0:
            if arr[right] > arr[i] and right >= 0:
                right -= 1
            else:
                break
        arr.insert(right+1, arr.pop(i))

def merge(li, low ,mid, high):
    i = low
    j = mid + 1
    list_ = []
    # 两边都有元素
    while i <= mid and j <= high:
        if li[i] < li[j]:
            list_.append(li[i])
            i += 1
        else:
            list_.append(li[j])
            j += 1
    # 一边没有元素
    while i <= mid:
        list_.append(li[i])
        i += 1
    while j <= high:
        list_.append(li[j])
        j += 1
    li[low:high+1] = list_


def merge_sort(li, low, high):
    if low < high:
        mid = (low + high) // 2
        merge_sort(li, low, mid)
        merge_sort(li, mid+1, high)
        merge(li, low, mid, high)
        # print(li[low:high+1])


arr = [3, 4, 5, 3, 8, 2, 4]
merge_sort(arr, 0, len(arr)-1)
print(arr)

# print(fetch(arr))
# select_sort(arr)
# insert_sort(arr)
# heapq.heapify(arr)  # 建堆的过程
# print(arr)
# for i in range(len(arr)):
#     print(heapq.heappop(arr),end=',')

