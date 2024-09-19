#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
:author: keane
:file  question_answer.py
:time  2024/9/19 15:07
:desc  
"""
import pandas as pd
def question_answer():
    df = pd.read_excel(r"E:\keane_python\github\django_project\api_project\app_web\question_answer\桥梁与地下工程复习题.xlsx", sheet_name="单选题")
    id_num = 0
    question_list = list()
    for df_index, df_value in df.iterrows():
        ismultiple = False
        name = df_value["题目"]
        answer = df_value["答案"]
        score = 2
        option = [
            {
                "id": 1,
                "name": df_value["A"],
                "checked": False,
                "letter": 'A'
            },
            {
                "id": 2,
                "name": df_value["B"],
                "checked": False,
                "letter": 'B'
            },
            {
                "id": 3,
                "name": df_value["C"],
                "checked": False,
                "letter": 'C'
            },
            {
                "id": 4,
                "name": df_value["D"],
                "checked": False,
                "letter": 'D'
            }
        ]
        question_list.append(
            dict(
                id=id_num,
                ismultiple=False,
                name=name,
                answer=answer,
                score=score,
                option=option
            )
        )

    return question_list