import random
def fetch(li, left, right, pivot_index):
    pivot_value = li[pivot_index]
    li[pivot_index], li[right] = li[right], li[pivot_index]
    sort_index = left
    for i in range(left, right):
        if li[i] > pivot_value:
            li[i], li[sort_index] = li[sort_index], li[i]
            sort_index += 1
    li[right], li[sort_index] = li[sort_index], li[right]
    return sort_index


def quick_select_sort(li, left, right, k):
    pivot = random.randint(left, right)
    mid = fetch(li, left, right, pivot)
    if mid+1 == k:
        return li[mid]
    elif mid+1 < k:
        return quick_select_sort(li, mid+1, right, k)
    else:
        return quick_select_sort(li, left, mid-1, k)



nums = [3, 2, 1, 5, 6, 4]

k = 2
print(quick_select_sort(nums, 0, len(nums) - 1, k))