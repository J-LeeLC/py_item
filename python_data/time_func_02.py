"""
读取时间字段 处理时间数据
筛选8:00-12:00数据
"""
import pandas as pd
import os
from pandas.core.frame import DataFrame
import datetime
import numpy as np

# 遍历文件
r_path = r"D:\QGD\data\003"  # 读取文件路径
w_path = r"D:\QGD\data\001"  # 写入文件路径
print('处理数据中...')
for dir_path, dir_name, file_name in os.walk(r_path):
    for file in file_name:
        # 本地文件路径
        full_path = os.path.join(dir_path, file)
        # 读取csv文件
        csv_data = pd.read_csv(full_path)
        # 设置字段名
        set_col = ["year", "month", "day", "hour", "minute", "second", "foF2"]
        # 命名字段
        csv_data.columns = set_col
        # 获取统一时间格式、读取数据
        years = csv_data.loc[:, "year"]
        months = csv_data.loc[:, "month"]
        days = csv_data.loc[:, "day"]
        hours = csv_data.loc[:, "hour"]
        minutes = csv_data.loc[:, "minute"]
        seconds = csv_data.loc[:, "second"]
        foF2s = csv_data.loc[:, "foF2"]
        river_list = []
        for year, month, day, hour, minute, second, foF2 in zip(years, months, days, hours, minutes, seconds, foF2s):
            if ((hour >= 8) and (hour < 12)) or ((hour == 12) and (minute == 0)):
                # 获取时间范围的数据
                temp_list = [year, month, day, hour, minute, second, foF2]
                river_list.append(temp_list)

        # 创建新表
        river_data_list = DataFrame(river_list, columns=set_col)
        # 创建单层级目录
        drName = w_path + "\\" + os.path.basename(os.path.dirname(full_path))
        os.makedirs(drName, exist_ok=True)
        # 写入文件
        full_w_path = drName + "\\" + os.path.basename(full_path)
        river_data_list.to_csv(full_w_path, mode='a', index=False)

print('运行结束！')
