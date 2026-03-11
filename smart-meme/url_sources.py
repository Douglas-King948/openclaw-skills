# URL 表情包源
# 按分类整理，用于直接通过 URL 发送表情包
# ✅ = 已验证可用
# ⚠️ i.pixiv.re 需要真实Pixiv作品ID，暂不使用

MEME_URLS = {
    "panda": [
        "https://www.diydoutu.com/bq/251.jpg",
        "https://www.diydoutu.com/bq/006mowZngy1fxj3kcd1pbj309q05naak.jpg",
    ],
    "cats": [
        "https://cataas.com/cat/cute",
        "https://cataas.com/cat/funny",
    ],
    "dogs": [
        "https://loremflickr.com/400/300/dog",
    ],
    "anime": [
        # ✅ Pic.re - 二次元默认图源
        "https://pic.re/image?q=anime",           # 动漫
        "https://pic.re/image?q=beautiful",       # 美图
        "https://pic.re/image?q=kawaii",          # 可爱
        "https://pic.re/image?q=neko",            # 猫娘
        "https://pic.re/image?q=nekomimi",        # 猫耳
        "https://pic.re/image?q=moe",             # 萌系
        "https://pic.re/image?q=girl",            # 少女
        "https://pic.re/image?q=illustration",    # 插画
        "https://pic.re/image?q=cute",            # 可爱系
        "https://pic.re/image?q=sleepy",        #  sleepy
        "https://pic.re/image?q=bed",             #  bed
        "https://pic.re/image?q=goodnight",       #  goodnight
        "https://pic.re/image?q=honkai+star+rail",  #  星穹铁道
        "https://pic.re/image?q=star+rail",         #  Star Rail
        "https://pic.re/image?q=masterpiece",       #  杰作/神作
        "https://pic.re/image?q=best+quality",      #  最高质量
        "https://pic.re/image?q=detailed",          #  精细细节
        "https://pic.re/image?q=official+art",      #  官方插画
        "https://pic.re/image?q=fanart",            #  同人图
        "https://pic.re/image?q=highres",           #  高分辨率
        # ✅ 机械少女猫娘风格（猫屋/NEKOYA风格）
        "https://pic.re/image?q=mecha+musume",      # 机械少女
        "https://pic.re/image?q=cyber+catgirl",     # 赛博猫娘
        "https://pic.re/image?q=robot+girl",        # 机器人少女
        "https://pic.re/image?q=mechanical+girl",   # 机械女孩
        "https://pic.re/image?q=cyberpunk+neko",    # 赛博朋克猫娘
    ],
    "programmer": [
        "https://api.memegen.link/images/drake/PHP/Python.jpg",
    ],
    "wuxia": [
        "https://api.memegen.link/images/success/练成了/绝世武功.jpg",
    ],
    "animals": [
        "https://loremflickr.com/400/300/fox",
    ],
    "misc": [
        "https://picsum.photos/400/300",
    ],
    "touhou": [
        "https://media.tenor.com/4rK8d3v8bN0AAAAC/touhou-reimu.gif",
    ],
    "doro": [
        "https://media.tenor.com/_zQx4AsjmK0AAAAi/doro-doro-nikke.gif",
    ],
    "ducks": [
        # 鸭子表情包源
        "https://pic.re/image?q=duck",
        "https://pic.re/image?q=duck+cute",
        "https://pic.re/image?q=duck+meme",
    ],
    "monkeys": [
        # 马喽/猴子表情包源
        "https://pic.re/image?q=monkey",           # 猴子
        "https://pic.re/image?q=monkey+meme",      # 猴子梗图
        "https://pic.re/image?q=funny+monkey",     # 搞笑猴子
        "https://pic.re/image?q=monkey+reaction",  # 猴子反应图
        "https://pic.re/image?q=surprised+monkey", # 震惊猴子
    ],
}

KEYWORD_MAP = {
    "熊猫头": "panda", "熊猫": "panda", "panda": "panda", "滚滚": "panda",
    "斗图": "panda", "梗图": "panda", "好笑": "panda", "搞笑": "panda", "乐": "panda",
    "猫咪": "cats", "猫": "cats", "cat": "cats", "cats": "cats", "喵喵": "cats", "kitty": "cats",
    "狗狗": "dogs", "狗": "dogs", "dog": "dogs", "dogs": "dogs", "汪汪": "dogs", "puppy": "dogs",
    # 好看的 = 高质量二次元美图
    "好看的": "anime", "美图": "anime", "漂亮": "anime", "精致": "anime", "美": "anime",
    "动漫": "anime", "anime": "anime", "二次元": "anime", "动画": "anime", 
    "猫娘": "anime", "萌": "anime", "少女": "anime", "美少女": "anime", 
    "pixiv": "anime", "p站": "anime",
    "猫耳": "anime", "兽耳": "anime", "萌系": "anime", "插画": "anime",
    "壁纸": "anime", "可爱": "anime", "晚安": "anime", "睡觉": "anime", "好梦": "anime",
    "星穹铁道": "anime", "铁道": "anime", "starrail": "anime", "honkai": "anime",
    "哈基米": "anime", "hachimi": "anime",
    "杰作": "anime", "神作": "anime", "masterpiece": "anime",
    "高清": "anime", "高画质": "anime", "高质量": "anime", "bestquality": "anime",
    "精细": "anime", "细节": "anime", "detailed": "anime",
    "官方": "anime", "official": "anime", "官图": "anime",
    "同人": "anime", "fanart": "anime",
    # 机械少女猫娘
    "机械": "anime", "机械少女": "anime", "mecha": "anime", "mechamusume": "anime",
    "赛博": "anime", "赛博朋克": "anime", "cyber": "anime", "cyberpunk": "anime",
    "机器人": "anime", "robot": "anime", "android": "anime",
    "猫屋": "anime", "NEKOYA": "anime", "nekoya": "anime",
    "武侠": "wuxia", "wuxia": "wuxia", "功夫": "wuxia",
    "动物": "animals", "animals": "animals", "animal": "animals",
    "程序员": "programmer", "programmer": "programmer", "码农": "programmer", "coding": "programmer", "code": "programmer", "梗图": "programmer",
    "杂项": "misc", "misc": "misc", "其他": "misc", "other": "misc", "表情包": "misc",
    "东方": "touhou", "东方project": "touhou", "touhou": "touhou", "车万": "touhou",
    "doro": "doro", "多洛": "doro", "nikke": "doro", "妮姬": "doro",
    # 鸭子
    "鸭子": "ducks", "鸭": "ducks", "duck": "ducks", "ducks": "ducks",
    "嘎嘎": "ducks", "小鸭子": "ducks", "ducky": "ducks",
    # 马喽/猴子
    "猴子": "monkeys", "猴": "monkeys", "monkey": "monkeys", "monkeys": "monkeys",
    "马喽": "monkeys", "吗喽": "monkeys", "马猴": "monkeys", "猴哥": "monkeys",
    "马楼": "monkeys", "吗楼": "monkeys",  # 常见错别字
    "猩猩": "monkeys", "猿": "monkeys", "ape": "monkeys", "orangutan": "monkeys",
}

categories = list(MEME_URLS.keys())
