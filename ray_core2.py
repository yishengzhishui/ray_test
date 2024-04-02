import ray  # 导入 Ray 库

ray.init()  # 初始化 Ray 运行时。只调用一次即可。

# 使用 @ray.remote 装饰器标记一个类 Counter，表示这个类可以在 Ray 中作为远程对象使用
@ray.remote
class Counter(object):
    def __init__(self):
        self.n = 0  # 初始化计数器的值为 0

    def increment(self):
        self.n += 1  # 将计数器的值加一

    def read(self):
        return self.n  # 返回计数器的当前值

# 创建了一个远程计数器对象的列表，每个对象都是 Counter 类的一个实例
counters = [Counter.remote() for i in range(4)]

# 对每个计数器对象执行增加操作，使用远程调用 increment 方法
[c.increment.remote() for c in counters]

# 对每个计数器对象执行读取操作，使用远程调用 read 方法，并将结果存储在 futures 列表中
futures = [c.read.remote() for c in counters]

# 使用 ray.get() 获取并行任务的结果，这个函数会阻塞主线程，直到所有任务都完成并且结果可用
# 在这里，返回的结果是一个列表，包含了每个计数器的当前值
print(ray.get(futures))  # 打印并行任务的结果，即每个计数器的当前值
