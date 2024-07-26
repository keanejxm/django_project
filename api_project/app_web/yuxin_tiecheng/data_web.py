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
            "planStartDate": "计划开始日期（必填）",
            "planEndDate": "计划完成日期（必填）",
            "realStartDate": "实际开始日期",
            "realEndDate": "实际完成日期",
            "planSubmitTestDate": "计划提交测试日期（必填）【原则上应比预计上线日期提前15天】",
            "realSubmitTestDate": "实际提交测试日期（非必填）[完成上线 必填]",
            "planLineDate": "预计上线日期（必填）",
            "realLineDate": "实际上线日期（非必填）",
            "realExploiter": "开发人员",
            "startDateSit": "实际SIT开始时间",
            "endDateSit": "实际SIT结束时间",
            "startDateUat": "实际UAT开始时间",
            "endDateUat": "实际UAT结束时间",
            "testPerson": "测试人员",
            "taskStatus": "任务状态",
        }
        self.excel_df = self.init_excel_data()
        self.excel_df.replace({"taskStatus": np.nan}, "未上线", inplace=True)
        self.excel_df.replace({"realExploiter": np.nan}, "未分配", inplace=True)

    def read_excel(self):
        filepath = f"{self.filepath}/TM整体进度表.xlsx"
        df = pd.read_excel(filepath, header=0, dtype=object, sheet_name="新版")
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
        keys = []
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
        keys.insert(0, "name")
        return new_data, keys

    def count_num_module(self):
        """
        # 按人统计已上线数量和未上线数量
        :return:
        """
        grouped = self.excel_df.groupby(["taskStatus", "projectModule"]).groups
        data = dict()
        keys = []
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
        keys.insert(0, "name")
        return new_data, keys

    def date_use_story(self):
        """
        # 从Story 维度 分析 开发耗时 测试耗时 整体耗时（立项-上线）
        :return:
        """
        df = self.excel_df[self.excel_df["realSubmitTestDate"].notnull()]
        df = df[df["realStartDate"].notnull()]
        df = df[df["endDateSit"].notnull()]
        # 将时间转为时间戳
        df['realSubmitTestDate'] = df['realSubmitTestDate'].apply(lambda x: x.timestamp())
        df['realStartDate'] = df['realStartDate'].apply(lambda x: x.timestamp())
        df['endDateSit'] = df['endDateSit'].apply(lambda x: x.timestamp())
        # 开发耗时
        df["useTimeExploit"] = df["realSubmitTestDate"] - df["realStartDate"]
        # 测试耗时
        df["useTimeTest"] = df["endDateSit"] - df["realSubmitTestDate"]
        # 整体耗时
        df["useTimeTotal"] = df["endDateSit"] - df["realStartDate"]

        # 计算多少小时
        df["useTimeExploit"] = df["useTimeExploit"] / 3600
        df["useTimeTest"] = df["useTimeTest"] / 3600
        df["useTimeTotal"] = df["useTimeTotal"] / 3600
        df["useTimeExploit"] = df["useTimeExploit"].astype("float")
        df["useTimeTest"] = df["useTimeTest"].astype("float")
        df["useTimeTotal"] = df["useTimeTotal"].astype("float")
        use_time_exploit = df.groupby(["storyCode"])["useTimeExploit"].sum()
        use_time_test = df.groupby(["storyCode"])["useTimeTest"].sum()
        use_time_total = df.groupby(["storyCode"])["useTimeTotal"].sum()
        use_time_static = dict()
        keys_list = []
        for key_item, value_item in {
            "测试耗时": use_time_test,
            "开发耗时": use_time_exploit,
            "整体耗时": use_time_total
        }.items():
            for key_use, value_use in value_item.items():
                if key_use in use_time_static:
                    use_time_static[key_use][key_item] = value_use
                else:
                    use_time_static[key_use] = {"name": key_use, key_item: value_use}
            keys_list.append(key_item)
        keys_list = list(set(keys_list))
        keys_list.insert(0, "name")
        value_list = [value for value in use_time_static.values()]
        return value_list, keys_list

    def schedule_story(self):
        """
        按story统计进度（求进度平均值）
        :return:
        """
        # 进度为空的设置为0
        self.excel_df.replace({"exploitProgress": np.nan}, 0, inplace=True)
        group = self.excel_df.groupby(["storyCode"])["exploitProgress"].mean()
        new_data = list()
        for key, value in group.items():
            new_data.append({"name": key, "进度": round(value * 100, 2)})
        keys = ["name", "进度"]
        return new_data, keys

    def flaw_count(self):
        """
        按story统计缺陷
        :return:
        """
        filepath = f"{self.filepath}/TM整体进度表.xlsx"
        df = pd.read_excel(filepath, header=0, dtype=object, sheet_name="上线内容")
        # 筛选Story不为0的数据
        df = df[(df["Story"].notna()) & (df["上线类型"] == "修正")]
        group = df.groupby(["Story"])["上线类型"].count()
        new_data = list()
        keys = ["name", "数量"]
        if df.empty:
            new_data.append({"name": "空", "数量": 0})
            return new_data, keys
        else:
            for key, value in group.items():
                new_data.append({"name": key, "数量": value})
            return new_data, keys
