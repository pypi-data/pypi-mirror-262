# coding:utf8


def get_data_similarity(data1, data2):
    char_list1 = [w for w in data1]
    char_list2 = [w for w in data2]
    intersec = set(char_list1).intersection(set(char_list2))
    return len(intersec) / max(len(char_list1), len(char_list2))

