class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = None


class MyLinkedList:
    def __init__(self):
        # 创建一个虚拟头节点
        self.head = Node(0)
        self.size = 0

    def get(self, index: int) -> int:
        if 0 <= index < self.size:
            cur = self.head
            for _ in range(index+1):
                cur = cur.next
            return cur.val
        else:
            return -1


    def addAtHead(self, val: int) -> None:
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        if 0 <= index <= self.size:
            cur = self.head
            # 添加我们要知道当前index前面的一个节点
            for _ in range(index):
                cur = cur.next
            # 要添加的节点
            node = Node(val)
            node.next = cur.next
            cur.next = node
            self.size += 1
        else:
            return

    def deleteAtIndex(self, index: int) -> None:
        # 要删除节点，我们需要找到删除前的一个节点
        cur = self.head
        for _ in range(index):
            cur = cur.next
        cur.next = cur.next.next
        self.size -= 1




MyLinkedList = MyLinkedList()
MyLinkedList.addAtHead(1)
MyLinkedList.addAtTail(3)
MyLinkedList.addAtIndex(1, 2)
print(MyLinkedList.get(1))
MyLinkedList.deleteAtIndex(1)
print(MyLinkedList.get(1))
