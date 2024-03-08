#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  data_web.py
:time  2024/1/29 9:39
:desc  
"""
import os.path
import numpy as np
import pandas as pd


class DataWeb:
    def __init__(self):
        self.filepath = os.path.dirname(__file__)
        self.column_map = {
            "project": "所属项目",
            "epicCode": "Epic编号",
            "storyCode": "Story编号",
            "projectModule": "所属模块",
            "functionDescribe": "功能点描述",
            "exploitProgress": "开发已完成进度",
            "planStartDate": "计划开始日期",
            "planEndDate": "计划完成日期",
            "realStartDate": "实际开始日期",
            "realEndDate": "实际完成日期",
            "planSubmitTestDate": "计划提交测试日期",
            "realSubmitTestDate": "实际提交测试日期",
            "planLineDate": "预计上线日期",
            "realLineDate": "实际上线日期",
            "realExploiter": "实际开发人员",
            "taskStatus": "任务状态"
        }
        self.excel_df = self.init_excel_data()
        self.excel_df.replace({"taskStatus": np.nan}, "未上线", inplace=True)

    def read_excel(self):
        filepath = f"{self.filepath}/TM整体进度表.xlsx"
        df = pd.read_excel(filepath, header=0, dtype=object, sheet_name="项目视图")
        return df

    def filter_column_data(self, df):
        """
        根据column映射筛选出需要的数据
        :return:
        """
        columns = df.columns
        new_column_map = dict()
        for e_name, c_name in self.column_map.items():
            for column in columns:
                if self.column_map["planSubmitTestDate"] in column and self.column_map["planLineDate"] in column:
                    new_column_map[column] = "planSubmitTestDate"
                else:
                    if c_name in column:
                        new_column_map[column] = e_name
                        break
        return new_column_map

    def init_excel_data(self):
        """
        按所属项目、Epic编号、Story编号、所属模块进行筛选
        展示：开发进度
        计算：
            计划开始日期、计划完成日期
            实际开始日期、实际完成日期
            计划提交测试日期、实际提交测试日期
            预计上线日期、实际上线日期
            实际开发人、
            任务状态
        :return:
        """
        # 按照 人、模块统计 工作量、 缺陷、进度及偏差、
        # 		从Story 维度 分析 开发耗时 测试耗时 整体耗时（立项-上线）
        df = self.read_excel()
        column_map = self.filter_column_data(df)
        df = df.rename(columns=column_map)
        filter_column = list(self.column_map.keys())
        df = df[filter_column]
        return df

    def count_task_status(self):
        """
        统计已上线数量和未上线数量
        :return:
        """
        count_status = self.excel_df["taskStatus"].value_counts()
        # 将数据转为[{"value":num,"name":"已上线"}]的格式
        data = list()
        for index, value in count_status.items():
            data.append(dict(value=value, name=index))
        return data

    def count_num_person(self):
        """
        # 按人统计已上线数量和未上线数量
        :return:
        """
        grouped = self.excel_df.groupby(["taskStatus", "realExploiter"]).groups
        data = dict()
        keys = ["name"]
        for group_key, group_value in grouped.items():
            status_task, name = group_key
            num_task = len(group_value)
            if name in data:
                data[name][status_task] = num_task
            else:
                data[name] = {"name": name, status_task: num_task}
            keys.append(status_task)
        new_data = [value for key, value in data.items()]
        keys = list(set(keys))
        return new_data, keys
