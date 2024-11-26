def partition(nums, left, right):
    # 使用 nums[left] 作为枢轴元素
    pivot = nums[left]

    while left < right:
        # 从右侧开始，寻找比枢轴小的元素
        while left < right and nums[right] >= pivot:
            right -= 1
        nums[left] = nums[right]

        # 从左侧开始，寻找比枢轴大的元素
        while left < right and nums[left] <= pivot:
            left += 1
        nums[right] = nums[left]

    # 把枢轴元素放回正确的位置
    nums[left] = pivot
    return left


def quick_sort(nums, left, right):
    if left < right:
        # 将数组分区，找到枢轴的位置
        mid = partition(nums, left, right)

        # 递归地对左右子数组进行排序
        quick_sort(nums, left, mid - 1)
        quick_sort(nums, mid + 1, right)


# 示例数组
nums = [3, 2, 8, 1]
quick_sort(nums, 0, len(nums) - 1)
print(nums)
