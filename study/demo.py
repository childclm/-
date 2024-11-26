def merge_two_sorted_arrays(left, right):
    i = 0
    j = 0
    res = []

    # 合并两个有序数组
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1

    # 处理剩余元素
    while i < len(left):
        res.append(left[i])
        i += 1
    while j < len(right):
        res.append(right[j])
        j += 1

    return res


def merge_sort(nums):
    # 递归终止条件
    if len(nums) <= 1:
        return nums

    # 划分左右两个部分
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])

    # 合并两个已排序数组
    merge_two_sorted_arrays(left, right)


# 生成测试数组
arr = [_ for _ in range(16)]
import random

random.shuffle(arr)
print("Unsorted array:", arr)
sorted_arr = merge_sort(arr)
print("Sorted array:", sorted_arr)
