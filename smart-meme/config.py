#!/usr/bin/env python3
"""
Smart Meme v3 - 配置模块
集中管理所有配置和安全限制
"""

from pathlib import Path

# 基础路径
BASE_DIR = Path(__file__).parent
MEME_DIR = BASE_DIR / "local_memes"
DB_FILE = BASE_DIR / "memes.json"

# 安全限制
MAX_STORAGE_MB = 500           # 最大存储500MB
MAX_RETRY = 3                  # 最大重试3次
COOLDOWN_SECONDS = 300         # 失败后冷却5分钟
MAX_FILE_SIZE_MB = 25          # 单文件最大25MB
CHUNK_SIZE = 8192              # SHA256分块8KB

# 功能开关（默认关闭，需手动开启）
FEATURES = {
    "auto_restock": False,     # 自动补充（默认关闭，安全第一）
    "health_check": True,      # 健康检查（只读，安全）
    "dedup": True,             # 去重（推荐开启）
    "strict_mode": False,      # 严格模式（更多检查，稍慢）
}

# 表情包源（受控列表）- 每个分类10张
MEME_SOURCES = {
    "panda": [
        ("https://www.diydoutu.com/bq/251.jpg", "panda_001.jpg"),
        ("https://www.diydoutu.com/bq/006mowZngy1fxj3kcd1pbj309q05naak.jpg", "panda_002.jpg"),
        ("https://www.diydoutu.com/bq/006mowZngy1fypsbinpfgj306o06owey.jpg", "panda_003.jpg"),
        ("https://www.diydoutu.com/bq/006mowZngy1fypsbhpu4hj309q09qdh0.jpg", "panda_004.jpg"),
        ("https://www.diydoutu.com/bq/006mowZngy1fypsbipnmkj306o06oaag.jpg", "panda_005.jpg"),
        ("https://www.diydoutu.com/bq/251.jpg", "panda_006.jpg"),
        ("https://www.diydoutu.com/bq/252.jpg", "panda_007.jpg"),
        ("https://www.diydoutu.com/bq/253.jpg", "panda_008.jpg"),
        ("https://www.diydoutu.com/bq/254.jpg", "panda_009.jpg"),
        ("https://www.diydoutu.com/bq/255.jpg", "panda_010.jpg"),
    ],
    "programmer": [
        ("https://api.memegen.link/images/drake/PHP/Python.jpg", "prog_001.jpg"),
        ("https://api.memegen.link/images/gru/plan/sleep.jpg", "prog_002.jpg"),
        ("https://api.memegen.link/images/fine/bug/still_fixing.jpg", "prog_003.jpg"),
        ("https://api.memegen.link/images/success/finished/on_time.jpg", "prog_004.jpg"),
        ("https://api.memegen.link/images/distracted-boyfriend/new_feature/old_code.jpg", "prog_005.jpg"),
        ("https://api.memegen.link/images/always-has-been/bugs/everywhere.jpg", "prog_006.jpg"),
        ("https://api.memegen.link/images/expanding-brain/coding/not_coding.jpg", "prog_007.jpg"),
        ("https://api.memegen.link/images/buttons/ship_it/fix_bugs.jpg", "prog_008.jpg"),
        ("https://api.memegen.link/images/change-my-mind/comments/are_useless.jpg", "prog_009.jpg"),
        ("https://api.memegen.link/images/hide-the-pain/boss/can_you_fix.jpg", "prog_010.jpg"),
    ],
    "anime": [
        ("https://api.waifu.pics/sfw/neko", "anime_001.jpg"),
        ("https://api.waifu.pics/sfw/happy", "anime_002.jpg"),
        ("https://api.waifu.pics/sfw/cry", "anime_003.jpg"),
        ("https://api.waifu.pics/sfw/smile", "anime_004.jpg"),
        ("https://api.waifu.pics/sfw/wink", "anime_005.jpg"),
        ("https://api.waifu.pics/sfw/waifu", "anime_006.jpg"),
        ("https://api.waifu.pics/sfw/megumin", "anime_007.jpg"),
        ("https://api.waifu.pics/sfw/shinobu", "anime_008.jpg"),
        ("https://api.waifu.pics/sfw/hug", "anime_009.jpg"),
        ("https://api.waifu.pics/sfw/kiss", "anime_010.jpg"),
    ],
    "misc": [
        ("https://api.memegen.link/images/success/today/finished.jpg", "misc_001.jpg"),
        ("https://api.memegen.link/images/drake/no/yes.jpg", "misc_002.jpg"),
        ("https://api.memegen.link/images/fine/this/is_fine.jpg", "misc_003.jpg"),
        ("https://api.memegen.link/images/rollsafe/can't_fail/if_you_don't_try.jpg", "misc_004.jpg"),
        ("https://api.memegen.link/images/bad-luck-brian/makes_meme/nobody_likes.jpg", "misc_005.jpg"),
        ("https://api.memegen.link/images/success-kid/started_from/bottom.jpg", "misc_006.jpg"),
        ("https://api.memegen.link/images/10-guy/can't_remember/what_i_said.jpg", "misc_007.jpg"),
        ("https://api.memegen.link/images/y-u-no/just/work.jpg", "misc_008.jpg"),
        ("https://api.memegen.link/images/ancient-aliens/aliens/did_it.jpg", "misc_009.jpg"),
        ("https://api.memegen.link/images/one-does-not-simply/walk_into/mordor.jpg", "misc_010.jpg"),
    ],
    "cats": [
        ("https://cataas.com/cat/cute", "cat_001.jpg"),
        ("https://cataas.com/cat/funny", "cat_002.jpg"),
        ("https://cataas.com/cat/angry", "cat_003.jpg"),
        ("https://cataas.com/cat/sleepy", "cat_004.jpg"),
        ("https://cataas.com/cat/happy", "cat_005.jpg"),
        ("https://cataas.com/cat/surprised", "cat_006.jpg"),
        ("https://cataas.com/cat/sad", "cat_007.jpg"),
        ("https://cataas.com/cat/playing", "cat_008.jpg"),
        ("https://cataas.com/cat/jumping", "cat_009.jpg"),
        ("https://cataas.com/cat/silly", "cat_010.jpg"),
    ],
    "dogs": [
        ("https://dog.ceo/api/breeds/image/random", "dog_001.jpg"),
        ("https://dog.ceo/api/breeds/image/random", "dog_002.jpg"),
        ("https://dog.ceo/api/breeds/image/random", "dog_003.jpg"),
        ("https://dog.ceo/api/breeds/image/random", "dog_004.jpg"),
        ("https://dog.ceo/api/breeds/image/random", "dog_005.jpg"),
        ("https://dog.ceo/api/breeds/image/random", "dog_006.jpg"),
        ("https://dog.ceo/api/breeds/image/random", "dog_007.jpg"),
        ("https://dog.ceo/api/breeds/image/random", "dog_008.jpg"),
        ("https://dog.ceo/api/breeds/image/random", "dog_009.jpg"),
        ("https://dog.ceo/api/breeds/image/random", "dog_010.jpg"),
    ],
    "wuxia": [
        ("https://api.memegen.link/images/success/练成了/绝世武功.jpg", "wuxia_001.jpg"),
        ("https://api.memegen.link/images/drake/入门弟子/掌门.jpg", "wuxia_002.jpg"),
        ("https://api.memegen.link/images/expanding-brain/外功/内功/心法.jpg", "wuxia_003.jpg"),
        ("https://api.memegen.link/images/fine/被偷袭/ still_alive.jpg", "wuxia_004.jpg"),
        ("https://api.memegen.link/images/bad-luck-brian/练功/走火入魔.jpg", "wuxia_005.jpg"),
        ("https://api.memegen.link/images/distracted-boyfriend/师妹/师傅.jpg", "wuxia_006.jpg"),
        ("https://api.memegen.link/images/always-has-been/正道/魔教.jpg", "wuxia_007.jpg"),
        ("https://api.memegen.link/images/hide-the-pain/闭关/突破失败.jpg", "wuxia_008.jpg"),
        ("https://api.memegen.link/images/change-my-mind/武功秘籍/都是假的.jpg", "wuxia_009.jpg"),
        ("https://api.memegen.link/images/gru/偷师/被发现了.jpg", "wuxia_010.jpg"),
    ],
    "animals": [
        ("https://some-random-api.com/img/panda", "animal_001.jpg"),
        ("https://some-random-api.com/img/fox", "animal_002.jpg"),
        ("https://some-random-api.com/img/birb", "animal_003.jpg"),
        ("https://some-random-api.com/img/kangaroo", "animal_004.jpg"),
        ("https://some-random-api.com/img/koala", "animal_005.jpg"),
        ("https://some-random-api.com/img/red_panda", "animal_006.jpg"),
        ("https://some-random-api.com/img/pikachu", "animal_007.jpg"),
        ("https://some-random-api.com/img/cat", "animal_008.jpg"),
        ("https://some-random-api.com/img/dog", "animal_009.jpg"),
        ("https://some-random-api.com/img/whale", "animal_010.jpg"),
    ],
}

# 分类目录
CATEGORIES = list(MEME_SOURCES.keys())
