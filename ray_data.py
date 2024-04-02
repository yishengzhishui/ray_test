# 从 typing 模块导入 Dict 类型，用于定义字典类型的注解
from typing import Dict
# 导入 NumPy 库，并将其命名为 np，用于处理数据
import numpy as np
# 导入 Ray 库，用于执行并行计算任务
import ray

# 使用 Ray Data 的 read_csv 函数从指定的 S3 存储桶中读取 iris.csv 文件，并将其加载到名为 ds 的数据集中
ds = ray.data.read_csv("s3://anonymous@ray-example-data/iris.csv")

# 定义了一个名为 compute_area 的函数，接受一个字典类型的参数 batch，其中包含键值对为字符串和 NumPy 数组的数据。函数返回一个字典类型的对象
def compute_area(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    # 从批次数据中获取名为 "petal length (cm)" 的数据，存储在变量 length 中
    length = batch["petal length (cm)"]
    # 从批次数据中获取名为 "petal width (cm)" 的数据，存储在变量 width 中
    width = batch["petal width (cm)"]
    # 计算花瓣面积，并将结果存储在 batch 字典中的 "petal area (cm^2)" 键中
    batch["petal area (cm^2)"] = length * width
    # 返回更新后的数据字典
    return batch

# 对数据集 ds 中的每个批次应用 compute_area 函数，生成一个转换后的数据集 transformed_ds
transformed_ds = ds.map_batches(compute_area)

# 迭代遍历 transformed_ds 数据集的每个批次，其中每个批次包含 4 条数据
# batch_size就是数组中元素的个数
for batch in transformed_ds.iter_batches(batch_size=4):
    # 打印当前批次的数据
    print(batch)

# 将转换后的数据集 transformed_ds 写入到本地磁盘的 /tmp/iris/ 目录下，使用 Parquet 格式保存数据
# 目录不存在会自动创建
transformed_ds.write_parquet("local:///tmp/iris/")
