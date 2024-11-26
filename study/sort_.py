import random


def count_sort(li, max_count=100):
    count = [0 for _ in range(max_count+1)]
    for val in li:
        count[val] += 1
    li.clear()
    for ind, val in enumerate(count):
        for i in range(val):
            li.append(ind)


def bucket_sort(li, n=10, max_count=100):
    bucket = [[]for _ in range(n)]
    for var in li:
        # 判断当前放几号桶
        # 88-》0号桶 100 对应1号桶
        i = min(var//(max_count//n), n-1)
        bucket[i].append(var)
        # 桶内数据排序
        for j in range(len(bucket[i])-1, 0, -1):
            if bucket[i][j] < bucket[i][j-1]:
                bucket[i][j], bucket[i][j-1] = bucket[i][j-1], bucket[i][j]
            else:
                break
    li.clear()
    for i in bucket:
        for j in i:
            li.append(j)
    print(li)


def cardinal_sort(li):
    max_number = max(li)
    # 88->2次  100->3次  10000->5次
    for i in range(len(str(max_number))):
        bucket = [[] for _ in range(10)]
        for j in li:
            j = str(j)
            try:
                bucket[int(j[-1-i])].append(j)
            except Exception as e:
                bucket[0].append(j)
        li.clear()
        for buck in bucket:
            li.extend(buck)



nums = [random.randint(1, 100) for _ in range(100)]
print(nums)
cardinal_sort(nums)
print(nums)
# bucket_sort(nums)
# count_sort(nums)
# print(nums)