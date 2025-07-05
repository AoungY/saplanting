# -*- coding: utf-8 -*-
from copy import deepcopy
from math import floor
from random import random


class Singleton(type):
    """
    单例模式的元类实现。
    任何将此类作为元类的类，在整个程序生命周期中都只会创建一个实例。
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def dealunicode(_instance):
    """
    递归处理数据结构中的unicode字符串，将其编码为utf-8。
    这在处理从外部（如json文件）读取的数据时非常有用，可以避免编码问题。
    支持处理列表、字典、元组、集合等多种数据结构。
    """
    if isinstance(_instance, unicode):
        return _instance.encode('utf8')
    elif isinstance(_instance, list):
        result = []
        for value in _instance:
            result.append(dealunicode(value))
        return result
    elif isinstance(_instance, dict):
        result = {}
        for key, value in _instance.items():
            result[dealunicode(key)] = dealunicode(value)
        return result
    elif isinstance(_instance, tuple):
        return tuple(dealunicode(d) for d in _instance)
    elif isinstance(_instance, set):
        return set(dealunicode(d) for d in _instance)
    elif isinstance(_instance, frozenset):
        return frozenset(dealunicode(d) for d in _instance)
    return _instance


def update_dict(old, new):
    # type: (dict, dict) -> dict
    """
    递归地将`new`字典中的内容更新到`old`字典中。
    与dict.update()不同，如果键的值是字典，它会合并子字典而不是直接覆盖。
    """
    for key in new:
        if key in old:
            if isinstance(old[key], dict) and isinstance(new[key], dict):
                update_dict(old[key], new[key])
                continue
        old[key] = deepcopy(new[key])
    return old


def filling_dict(config, default):
    # type: (dict, dict) -> dict
    """
    根据`default`字典，为`config`字典补充缺失的键值对。
    此函数会递归检查，确保`config`拥有`default`中所有的键。
    常用于加载配置后，用默认配置来补全可能缺失的选项。
    """
    for key in default:
        if key not in config:
            config[key] = deepcopy(default[key])
        else:
            if isinstance(config[key], dict) and isinstance(default[key], dict):
                filling_dict(config[key], default[key])
    return config


def get_float_color(r, g, b):
    """将0-255范围的RGB颜色值转换为0.0-1.0范围的浮点数颜色值。"""
    return r / 255.0, g / 255.0, b / 255.0, 1.0


def get_gradient_color(start_color, end_color, progress):
    """
    根据进度值，计算在起始颜色和结束颜色之间的渐变色。
    :param start_color: tuple, 起始颜色 (r, g, b)
    :param end_color: tuple, 结束颜色 (r, g, b)
    :param progress: float, 进度 (0.0 到 1.0)
    :return: tuple, 计算出的中间颜色 (r, g, b)
    """
    if start_color == end_color:
        return start_color
    return tuple(int(d[0] + (d[1] - d[0]) * progress) for d in zip(start_color, end_color))


def isRectangleOverlap(rec1, rec2):
    """检查两个矩形是否重叠（AABB碰撞检测）。"""
    def intersect(p_left, p_right, q_left, q_right):
        return min(p_right, q_right) > max(p_left, q_left)

    return intersect(rec1[0], rec1[2], rec2[0], rec2[2]) and intersect(rec1[1], rec1[3], rec2[1], rec2[3])


def intToRoman(num):
    """将整数转换为罗马数字字符串。"""
    num = int(num)
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    numerals = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    res, i = "", 0
    while num:
        res += (num / values[i]) * numerals[i]
        num %= values[i]
        i += 1
    return res


def randomFloatToInt(num):
    """
    将浮点数转换为整数，并根据小数部分进行随机取整。
    例如，4.7有70%的概率变为5，30%的概率变为4。
    """
    numInt = int(num)
    left = num - numInt
    if left > 0:
        if random() < left:
            numInt += 1
    return numInt


def get_block_pos(pos):
    """将浮点数坐标（实体坐标）转换为整数坐标（方块坐标）。"""
    return int(floor(pos[0])), int(floor(pos[1])), int(floor(pos[2]))


def reformat_item(item, pop=False):
    """
    格式化和清理从引擎获取的物品字典。
    引擎返回的物品信息可能包含很多瞬时或不必要的数据，此函数用于提取核心数据。
    :param item: dict, 原始物品字典
    :param pop: bool, 如果为True，则在原字典上删除多余键；否则，创建一个新的干净字典。
    :return: dict, 格式化后的物品字典
    """
    if item:
        if pop:
            if 'userData' in item:
                for key in item.keys():
                    if key not in {"newItemName", "newAuxValue", "count", "userData"}:
                        item.pop(key)
            else:
                for key in item.keys():
                    if key not in {"newItemName", "newAuxValue", "count", "modEnchantData", "enchantData", "durability", "customTips", "extraId", "showInHand"}:
                        item.pop(key)
            return item
        else:
            result = {'newItemName': item['newItemName'], 'newAuxValue': item['newAuxValue'], 'count': item['count']}
            if 'userData' in item:
                if item['userData']:
                    result['userData'] = deepcopy(item['userData'])
            else:
                if 'modEnchantData' in item:
                    result['modEnchantData'] = deepcopy(item['modEnchantData'])
                if 'enchantData' in item:
                    result['enchantData'] = deepcopy(item['enchantData'])
                if 'durability' in item:
                    result['durability'] = item['durability']
                if 'customTips' in item:
                    result['customTips'] = item['customTips']
                if 'extraId' in item:
                    result['extraId'] = item['extraId']
                if 'showInHand' in item:
                    result['showInHand'] = item['showInHand']
            return result
    return item
