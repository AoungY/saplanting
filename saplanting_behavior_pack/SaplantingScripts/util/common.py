# -*- coding: utf-8 -*-
from copy import deepcopy
from math import floor
from random import random


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def dealunicode(_instance):
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
    更新dict，把new更新到old里
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
    根据default对config查漏补缺
    """
    for key in default:
        if key not in config:
            config[key] = deepcopy(default[key])
        else:
            if isinstance(config[key], dict) and isinstance(default[key], dict):
                filling_dict(config[key], default[key])
    return config


def get_float_color(r, g, b):
    return r / 255.0, g / 255.0, b / 255.0, 1.0


def get_gradient_color(start_color, end_color, progress):
    if start_color == end_color:
        return start_color
    return tuple(int(d[0] + (d[1] - d[0]) * progress) for d in zip(start_color, end_color))


def isRectangleOverlap(rec1, rec2):
    def intersect(p_left, p_right, q_left, q_right):
        return min(p_right, q_right) > max(p_left, q_left)

    return intersect(rec1[0], rec1[2], rec2[0], rec2[2]) and intersect(rec1[1], rec1[3], rec2[1], rec2[3])


def intToRoman(num):
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
    numInt = int(num)
    left = num - numInt
    if left > 0:
        if random() < left:
            numInt += 1
    return numInt


def get_block_pos(pos):
    return int(floor(pos[0])), int(floor(pos[1])), int(floor(pos[2]))


def reformat_item(item, pop=False):
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
