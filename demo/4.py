# 分
def merge_sort(nums, left, right):
    if left == right:
        return
    middle = (left + right) // 2
    merge_sort(nums, left, middle)
    merge_sort(nums, middle + 1, right)
    merge(nums, left, middle, right)


def merge(nums, start, mid, end):
    # 合
    res = []
    l = start
    r = mid + 1
    while l <= mid and r <= end:
        if nums[l] < nums[r]:
            res.append(nums[l])
            l += 1
        else:
            res.append(nums[r])
            r += 1
    res.extend(nums[l:mid+1])
    res.extend(nums[r:end+1])
    for i in range(start, end+1):
        nums[i] = res[i-start]
    print(nums)


# 生成测试数组
arr = [2, 0, 3, 1, 4]

print("Unsorted array:", arr)
sorted_arr = merge_sort(arr, 0, len(arr) - 1)