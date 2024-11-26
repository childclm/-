class A:
    def __init__(self):
        self.a = 1

    @property
    def fetch(self):
        return self.a

    def __call__(self, num):
        print(type(num))
        print(*num)

a = A()
print(a.fetch)
print(a(['xiaochai', 'xioacou']))