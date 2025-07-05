# -*- coding: utf-8 -*-
# @Time    : 2023/12/8 9:45
# @Author  : taokyla
# @File    : sapling.py
default_saplings = {
    ("minecraft:warped_fungus", 0),
    ("minecraft:crimson_fungus", 0),
    ("minecraft:sapling", 0),
    ("minecraft:sapling", 1),
    ("minecraft:sapling", 2),
    ("minecraft:sapling", 3),
    ("minecraft:sapling", 4),
    ("minecraft:sapling", 5),
    ("minecraft:azalea", 0),
    ("minecraft:flowering_azalea", 0),
    ("minecraft:bamboo", 0),
    ("minecraft:wheat_seeds", 0),
    ("minecraft:pumpkin_seeds", 0),
    ("minecraft:melon_seeds", 0),
    ("minecraft:beetroot_seeds", 0),
    ("minecraft:potato", 0),
    ("minecraft:carrot", 0),
    ("minecraft:sweet_berries", 0),
    ("minecraft:sugar_cane", 0),
    ("minecraft:torchflower_seeds", 0),
    ("minecraft:pitcher_pod", 0),
}

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

BLOCKSURROUNDINGS = [
    (1, 0, 0), (0, 0, 1), (0, 0, -1), (-1, 0, 0), (0, 1, 0),
    (-1, 1, 0), (0, 1, 1), (-1, 0, -1), (1, 0, -1), (1, 0, 1),
    (-1, 0, 1), (0, 1, -1), (1, 1, 0),
    (1, 1, -1), (-1, 1, 1), (-1, 1, -1), (1, 1, 1)
]

LEAVE_BLOCKS = {
    "minecraft:leaves",
    "minecraft:leaves2",
    "minecraft:mangrove_leaves",
    "minecraft:cherry_leaves",
    "minecraft:azalea_leaves",
    "minecraft:azalea_leaves_flowered"
}
