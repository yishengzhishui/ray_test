import ray  # 导入 Ray 库

ray.init()  # 初始化 Ray 运行时

# 使用 @ray.remote 装饰器标记一个函数 f()，以便在 Ray 中作为远程任务执行
# f()可以在集群的不同节点运行
@ray.remote
def f(x):
    return x * x  # 计算传入参数 x 的平方，并将结果返回

# 创建了一个远程任务的列表，每个任务都是调用函数 f()，传入一个不同的参数值 i
futures = [f.remote(i) for i in range(4)]

# 通过 ray.get() 获取并行任务的结果，这个函数会阻塞主线程，直到所有任务都完成并且结果可用
# 在这里，返回的结果是一个列表，包含了每个数字的平方值
print(ray.get(futures))  # 打印并行任务的结果，即每个数字的平方值
