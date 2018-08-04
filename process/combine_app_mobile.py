# -*- coding:utf-8 -*-
import math
import sys


def load_data(result):
    result_file = open(result)
    result_score = []
    while True:
        score = result_file.readline()
        if not score:
            break
        result_score.append(float(score))
    result_file.close()
    return result_score


def merge(out_file, in_file_1, in_file_2):
    result_1 = load_data(in_file_1)
    result_2 = load_data(in_file_2)
    primary_file = "../test_pre"
    index = 1

    file = open(primary_file)
    final_result = open(out_file, "w")
    line = file.readline()

    cnt1 = -1
    cnt2 = -1
    while True:
        line = file.readline()
        if not line:
            break
        category_list = line.split(",")
        if category_list[index + 3] == "c_85f751fd":
            cnt2 += 1
            print >> final_result, str(result_2[cnt2])
        else:
            cnt1 += 1
            print >> final_result, str(result_1[cnt1])
    file.close()


merge(sys.argv[1], sys.argv[2], sys.argv[3])
