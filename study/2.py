def merge_sort(nums):
    if len(nums) <= 1:
        return nums
    mid = len(nums)//2
    # 递归左右部分
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])

    return merge(left, right)


def merge(left, right):
    # 合并左右部分
    i = 0
    j = 0
    res = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    while i < len(left):
        res.append(left[i])
        i += 1
    while j < len(right):
        res.append(right[j])
        j += 1
    return res


import random

# 测试代码
arr = [random.randint(1, 100) for _ in range(8)]
random.shuffle(arr)
print("Unsorted array:", arr)
sorted_arr = merge_sort(arr)
print("Sorted array:", sorted_arr)
