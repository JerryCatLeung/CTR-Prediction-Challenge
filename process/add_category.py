# -*- coding:utf-8 -*-
from collections import defaultdict
import marshal

train = "../train"
test = "../test"
new_train = "../new_train"
new_test = "../new_test"


def get_id(device_id, device_ip, device_model):
    """
           用device_id、device_ip和device_model来区分不同的用户，在进行特征工程的时候发现，
           device_id等于a99f214a出现的次数很多，当device_id等于a99f214a时，采用device_ip
           和device_model组合的方式作为区分用户的ID
    """
    if device_id != "i_a99f214a":
        return device_id
    else:
        return device_ip + "_" + device_model


def generate_new_feature(input, output, isTest):
    file = open(input)
    new_file = open(output, "w")
    date = defaultdict(int)
    d2 = {}
    date_hour = defaultdict(int)
    line = file.readline()
    print >> new_file, line[:-2] + ",C22,C23,C24,C25,C26,C27,C28"
    count = 0
    day = "**"
    hour = "**"
    hour_index = 2
    if isTest:
        hour_index = 1
    while True:
        line = file.readline()
        if not line:
            break
        count += 1
        if count % 100000 == 0:
            print count
        category_list = line.split(",")
        if category_list[hour_index][4:6] != day:
            del date
            date = defaultdict(int)
            d2 = {}
            day = category_list[hour_index][4:6]
        if category_list[hour_index][6:] != hour:
            del date_hour
            date_hour = defaultdict(int)
            hour = category_list[hour_index][6:]
        time = int(category_list[hour_index][6:]) * 60 + int(int(category_list[0][:5]) / 100000. * 60)
        new_user_id = get_id("i_" + category_list[hour_index + 9], "j_" + category_list[hour_index + 10],
                             "k_" + category_list[hour_index + 11])
        date[new_user_id + "_d_" + category_list[hour_index + 14]] += 1
        date[new_user_id + "_h_" + category_list[hour_index + 17]] += 1
        date_hour[new_user_id + "_d_" + category_list[hour_index + 14]] += 1
        date_hour[new_user_id + "_h_" + category_list[hour_index + 17]] += 1
        date_hour[new_user_id] += 1

        portal_id = "f_" + category_list[hour_index + 6]
        if category_list[hour_index + 6] == "ecad2386":
            portal_id = "c_" + category_list[hour_index + 3]
        date[new_user_id + "_" + portal_id] += 1
        interval = "-1"

        if new_user_id not in d2:
            d2[new_user_id] = time
        else:
            interval = str(time - d2[new_user_id])
            d2[new_user_id] = time

        """每天不同互联网媒介的数量(app or site)"""
        number_portal_day = date[new_user_id + "_" + portal_id]

        """每天不同广告不同用户的浏览次数"""
        number_ad_day = date[new_user_id + "_d_" + category_list[hour_index + 14]]

        """每天不同广告类别不同用户的浏览次数"""
        number_ad_category_day = date[new_user_id + "_h_" + category_list[hour_index + 17]]

        """每小时不同广告不同用户的浏览次数"""
        number_ad_hour = date_hour[new_user_id + "_d_" + category_list[hour_index + 14]]

        """每小时不同广告类别不同用户的浏览次数"""
        number_ad_category_hour = date_hour[new_user_id + "_h_" + category_list[hour_index + 17]]

        """每小时不同用户出现的次数"""
        number_hour = date_hour[new_user_id]
        print >> new_file, line[:-2] + "," + new_user_id + "," + str(number_portal_day) + "," + str(
            number_ad_category_hour) + "," + str(number_hour) + "," + str(
            number_ad_day) + "," + str(number_ad_category_day) + "," + interval
    file.close()
    new_file.close()


generate_new_feature(train, new_train, False)
generate_new_feature(test, new_test, True)
