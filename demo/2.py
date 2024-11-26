def quick_sort(nums, left, right):
    tmp = nums[left]
    while left < right:
        while left < right and nums[right] >= tmp:
            right -= 1
        nums[left] = nums[right]
        while left < right and nums[left] <= tmp:
            left += 1
        nums[right] = nums[left]
    nums[left] = tmp
    return left


def merge(nums, left, right):
    if left < right:
        mid = quick_sort(nums, left, right)
        merge(nums, left, mid-1)
        merge(nums, mid+1, right)

import random
nums = [random.randint(1, 100) for _ in range(100)]
print(nums)
merge(nums, 0, len(nums) - 1)
print(nums)