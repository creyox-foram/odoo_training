# -*- coding: utf-8 -*-
# Part of Creyox Technologies.

num = 1
formatted_num = f"{num:05d}"  # 5 is the total number of digits, including leading zeros
# print(formatted_num)  # Output: 00001
for i in range(5):
    print(str(i).zfill(5))
