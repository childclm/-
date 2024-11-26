class A:
    def __init__(self):
        self.aaa = 111

    def __setattr__(self, name, value):
        # print(name, value)
        super().__setattr__(name, value)

    def __getattr__(self, name):
        # 获取不到属性时间触发
        print(name)

    # def __getattribute__(self, item):
    #     # 属性拦截器
    #     print('__getattribute__', item)



a = A()
print(a.b)