# -*- coding: utf-8 -*-
# @Time    : 2023/12/8 9:45
# @Author  : taokyla
# @File    : sapling.py

# 默认的可自动种植的物品白名单。
# 包含各种树苗、菌类、种子、作物等。
# 格式为 (物品ID, 辅助值) 的元组集合。
default_saplings = {
    ("minecraft:warped_fungus", 0),
    ("minecraft:crimson_fungus", 0),
    ("minecraft:sapling", 0),  # 橡树苗
    ("minecraft:sapling", 1),  # 云杉树苗
    ("minecraft:sapling", 2),  # 白桦树苗
    ("minecraft:sapling", 3),  # 丛林树苗
    ("minecraft:sapling", 4),  # 金合欢树苗
    ("minecraft:sapling", 5),  # 深色橡树苗
    ("minecraft:azalea", 0),  # 杜鹃花丛
    ("minecraft:flowering_azalea", 0),  # 盛开的杜鹃花丛
    ("minecraft:bamboo", 0),  # 竹子
    ("minecraft:wheat_seeds", 0),  # 小麦种子
    ("minecraft:pumpkin_seeds", 0),  # 南瓜种子
    ("minecraft:melon_seeds", 0),  # 西瓜种子
    ("minecraft:beetroot_seeds", 0),  # 甜菜根种子
    ("minecraft:potato", 0),  # 马铃薯
    ("minecraft:carrot", 0),  # 胡萝卜
    ("minecraft:sweet_berries", 0),  # 甜浆果
    ("minecraft:sugar_cane", 0),  # 甘蔗
    ("minecraft:torchflower_seeds", 0),  # 火把花种子
    ("minecraft:pitcher_pod", 0),  # 瓶子草荚
}

# 特殊种植物映射表。
# 用于处理“种子物品”和“长成的方块”ID不一致的情况。
# 键为物品(item)，值为方块(block)。
# 例如，小麦种子(wheat_seeds)种下后变成小麦方块(wheat)。
special_saplings = {
    ("minecraft:wheat_seeds", 0): ("minecraft:wheat", 0),
    ("minecraft:pumpkin_seeds", 0): ("minecraft:pumpkin_stem", 0),
    ("minecraft:melon_seeds", 0): ("minecraft:melon_stem", 0),
    ("minecraft:beetroot_seeds", 0): ("minecraft:beetroot", 0),
    ("minecraft:potato", 0): ("minecraft:potatoes", 0),
    ("minecraft:carrot", 0): ("minecraft:carrots", 0),
    ("minecraft:sweet_berries", 0): ("minecraft:sweet_berry_bush", 0),
    ("minecraft:glow_berries", 0): ("minecraft:cave_vines", 0),
    ("minecraft:sugar_cane", 0): ("minecraft:reeds", 0),
    ("minecraft:bamboo", 0): ("minecraft:bamboo_sapling", 0),
    ("minecraft:torchflower_seeds", 0): ("minecraft:torchflower_crop", 0),
    ("minecraft:pitcher_pod", 0): ("minecraft:pitcher_crop", 0),
}

# 被连锁砍树功能识别为“木头”的方块ID集合。
LOG_BLOCKS = {
    "minecraft:log",
    "minecraft:log2",
    "minecraft:oak_log",
    "minecraft:spruce_log",
    "minecraft:birch_log",
    "minecraft:jungle_log",
    "minecraft:acacia_log",
    "minecraft:dark_oak_log",
    "minecraft:cherry_log",
    "minecraft:mangrove_log",
}

# 用于连锁砍树算法的周围方块偏移量列表。
# 这个列表只包含同层及上方的17个邻近方块，不包含下方方块。
# 这样设计是为了让算法向上和向侧方搜索，符合树木的生长形态。
BLOCKSURROUNDINGS = [
    (1, 0, 0), (0, 0, 1), (0, 0, -1), (-1, 0, 0), (0, 1, 0),
    (-1, 1, 0), (0, 1, 1), (-1, 0, -1), (1, 0, -1), (1, 0, 1),
    (-1, 0, 1), (0, 1, -1), (1, 1, 0),
    (1, 1, -1), (-1, 1, 1), (-1, 1, -1), (1, 1, 1)
]

# 被连锁砍树功能识别为“树叶”的方块ID集合。
# 用于判断一个木头方块是否属于“自然生成的树”。
LEAVE_BLOCKS = {
    "minecraft:leaves",
    "minecraft:leaves2",
    "minecraft:mangrove_leaves",
    "minecraft:cherry_leaves",
    "minecraft:azalea_leaves",
    "minecraft:azalea_leaves_flowered"
}
