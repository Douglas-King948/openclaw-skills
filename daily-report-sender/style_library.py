"""
Daily Report Style Library - 日报风格库
20种风格，每天随机匹配，让日报不再单调！
"""

from dataclasses import dataclass
from typing import List, Optional
import random

@dataclass
class ReportStyle:
    """日报风格定义"""
    id: str
    name: str
    icon: str
    keywords: List[str]  # 图片搜索关键词
    color: str  # 飞书卡片颜色
    title_template: str  # 标题模板
    header_template: str  # 头部模板
    footer_template: str  # 底部模板
    description: str  # 风格描述


# ============ 风格库 (20种) ============
STYLE_LIBRARY = [
    # 1. 克苏鲁风
    ReportStyle(
        id="cthulhu",
        name="克苏鲁的召唤",
        icon="🐙",
        keywords=["cthulhu", "lovecraft", "eldritch", "cosmic horror", "tentacles", "dark fantasy"],
        color="purple",
        title_template="🐙 {name} - 深渊日报",
        header_template="**🐙 来自深渊的低语**\n\n*在拉莱耶的宫殿中，死去的克苏鲁等待入梦...*",
        footer_template="*Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn*\n\n🦑 不可名状之物生成",
        description="克苏鲁神话风格，神秘恐怖的宇宙恐怖主题"
    ),
    
    # 2. 赛博朋克风
    ReportStyle(
        id="cyberpunk",
        name="赛博朋克2077",
        icon="🌃",
        keywords=["cyberpunk", "neon", "cyber", "future city", "hacker", "synthwave"],
        color="turquoise",
        title_template="🌃 {name} - 夜之城日报",
        header_template="**🌃 欢迎来到夜之城**\n\n*霓虹灯下，数据流中，我们是数字世界的幽灵...*",
        footer_template="*Wake the fuck up, samurai. We have a city to burn.*\n\n⚡ 赛博浪客生成",
        description="赛博朋克风格，霓虹灯下的高科技低生活"
    ),
    
    # 3. 武侠风
    ReportStyle(
        id="wuxia",
        name="江湖日报",
        icon="⚔️",
        keywords=["wuxia", "samurai", "kung fu", "ancient china", "sword", "martial arts"],
        color="red",
        title_template="⚔️ {name} - 武林快讯",
        header_template="**⚔️ 今日江湖战绩**\n\n*十步杀一人，千里不留行。事了拂衣去，深藏身与名。*",
        footer_template="*江湖路远，侠客珍重。*\n\n🗡️ 武林盟主生成",
        description="武侠风格，快意恩仇的江湖世界"
    ),
    
    # 4. 蒸汽朋克风
    ReportStyle(
        id="steampunk",
        name="蒸汽时代",
        icon="⚙️",
        keywords=["steampunk", "victorian", "gears", "steam", "brass", "clockwork"],
        color="orange",
        title_template="⚙️ {name} - 蒸汽日报",
        header_template="**⚙️ 齿轮转动，蒸汽升腾**\n\n*在黄铜与齿轮的世界，时间是最精密的机械...*",
        footer_template="*Time is but a cog in the great machine.*\n\n🎩 蒸汽绅士生成",
        description="蒸汽朋克风格，维多利亚时代的机械美学"
    ),
    
    # 5. 魔法学院风
    ReportStyle(
        id="magic",
        name="霍格沃茨日报",
        icon="🪄",
        keywords=["magic", "wizard", "harry potter", "fantasy", "spell", "enchanted"],
        color="purple",
        title_template="🪄 {name} - 魔法日报",
        header_template="**🪄 欢迎来到魔法世界**\n\n*咒语在指尖跳跃，魔杖挥动间，奇迹发生...*",
        footer_template="*Wingardium Leviosa!*\n\n🧙 大魔法师生成",
        description="魔法风格，哈利波特式的奇幻世界"
    ),
    
    # 6. 星际穿越风
    ReportStyle(
        id="space",
        name="星际日报",
        icon="🚀",
        keywords=["space", "galaxy", "astronaut", "cosmos", "nebula", "planet"],
        color="blue",
        title_template="🚀 {name} - 宇宙通讯",
        header_template="**🚀 来自深空的讯息**\n\n*在星辰大海中，人类的足迹延伸至无尽...*",
        footer_template="*Ad astra per aspera.* (循此苦旅，以达星辰)\n\n👨‍🚀 星际旅人生成",
        description="太空风格，浩瀚宇宙的探索之旅"
    ),
    
    # 7. 日式和风
    ReportStyle(
        id="japanese",
        name="浮世绘日报",
        icon="🌸",
        keywords=["japanese", "ukiyo-e", "sakura", "kimono", "zen", "temple"],
        color="red",
        title_template="🌸 {name} - 大和日报",
        header_template="**🌸 一期一会，世当珍惜**\n\n*樱花飘落，岁月静好，禅意生活中的工作美学...*",
        footer_template="*物哀、幽玄、侘寂*\n\n🎋 茶道大师生成",
        description="日式风格，浮世绘与禅意的结合"
    ),
    
    # 8. 海盗风
    ReportStyle(
        id="pirate",
        name="海盗日报",
        icon="🏴‍☠️",
        keywords=["pirate", "treasure", "ship", "caribbean", "skull", "ocean"],
        color="grey",
        title_template="🏴‍☠️ {name} - 海盗快讯",
        header_template="**🏴‍☠️ 扬帆起航，寻找宝藏**\n\n*七海之上，风帆鼓动，冒险的呼唤永不停止...*",
        footer_template="*Yo ho, yo ho, a pirate's life for me!*\n\n⚓ 海盗船长生成",
        description="海盗风格，加勒比海的冒险精神"
    ),
    
    # 9. 复古像素风
    ReportStyle(
        id="retro",
        name="像素日报",
        icon="👾",
        keywords=["pixel art", "retro gaming", "8bit", "arcade", "nostalgia", "game"],
        color="green",
        title_template="👾 {name} - 8-Bit日报",
        header_template="**👾 INSERT COIN TO CONTINUE**\n\n*回到80年代，像素世界里的工作冒险...*",
        footer_template="*GAME OVER - Press START to continue*\n\n🎮 复古玩家生成",
        description="复古游戏风格，8-bit像素美学"
    ),
    
    # 10. 猫咪王国风
    ReportStyle(
        id="cat",
        name="喵星日报",
        icon="🐱",
        keywords=["cat", "kitten", "cute cat", "neko", "cat kingdom", "meow"],
        color="orange",
        title_template="🐱 {name} - 喵喵通讯",
        header_template="**🐱 喵~ 今日猫片**\n\n*在猫咪的世界里，人类只是铲屎官...*",
        footer_template="*Meow meow meow~ (=^･ω･^=)*\n\n🐾 猫奴生成",
        description="猫咪风格，萌系猫娘与铲屎官的日常"
    ),
    
    # 11. 机械纪元风
    ReportStyle(
        id="mecha",
        name="机甲日报",
        icon="🤖",
        keywords=["mecha", "robot", "gundam", "cyborg", "android", "scifi"],
        color="blue",
        title_template="🤖 {name} - 机甲通讯",
        header_template="**🤖 机甲启动，系统正常**\n\n*钢铁身躯，电子灵魂，为保卫人类而战...*",
        footer_template="*I am the bone of my sword.*\n\n🦾 机甲驾驶员生成",
        description="机甲风格，高达式的科幻战斗"
    ),
    
    # 12. 中世纪风
    ReportStyle(
        id="medieval",
        name="骑士日报",
        icon="🏰",
        keywords=["medieval", "knight", "castle", "dragon", "fantasy", "sword"],
        color="grey",
        title_template="🏰 {name} - 王国快讯",
        header_template="**🏰 为了荣誉与荣耀**\n\n*中世纪的号角响起，骑士的誓言永不褪色...*",
        footer_template="*For honor and glory!*\n\n🛡️ 皇家骑士生成",
        description="中世纪风格，骑士与城堡的奇幻世界"
    ),
    
    # 13. 咖啡师风
    ReportStyle(
        id="coffee",
        name="咖啡日报",
        icon="☕",
        keywords=["coffee", "cafe", "latte art", "barista", "cozy", "morning"],
        color="orange",
        title_template="☕ {name} - 咖啡时光",
        header_template="**☕ 一杯咖啡，一份宁静**\n\n*咖啡豆的芳香中，工作也变得诗意...*",
        footer_template="*But first, coffee.*\n\n🥐 咖啡师生成",
        description="咖啡风格，温暖治愈的咖啡馆氛围"
    ),
    
    # 14. 赛博猫咪风
    ReportStyle(
        id="cybercat",
        name="赛博喵日报",
        icon="😼",
        keywords=["cyber cat", "robot cat", "future cat", "neon cat", "tech cat"],
        color="turquoise",
        title_template="😼 {name} - 赛博喵通讯",
        header_template="**😼 喵呜~ 系统启动**\n\n*在霓虹灯下，机械猫咪优雅地巡逻着数据流...*",
        footer_template="*Meow.exe has stopped working*\n\n🤖🐱 赛博猫娘生成",
        description="赛博朋克猫咪，科技与萌系的结合"
    ),
    
    # 15. 森林精灵风
    ReportStyle(
        id="forest",
        name="森之日报",
        icon="🌲",
        keywords=["forest", "elf", "nature", "fairy", "green", "magical forest"],
        color="green",
        title_template="🌲 {name} - 林间通讯",
        header_template="**🌲 森林深处的低语**\n\n*在古老的树林中，精灵们守护着自然的秘密...*",
        footer_template="*Nature is not a place to visit, it is home.*\n\n🧝 森林精灵生成",
        description="森林风格，精灵与自然的和谐共生"
    ),
    
    # 16. 都市传说风
    ReportStyle(
        id="urban",
        name="都市怪谈",
        icon="🌙",
        keywords=["urban legend", "mystery", "night", "dark", "scary", "ghost"],
        color="grey",
        title_template="🌙 {name} - 午夜频道",
        header_template="**🌙 城市夜晚，真相潜伏**\n\n*霓虹灯背后，都市传说正在悄然发生...*",
        footer_template="*The truth is out there.*\n\n🔦 都市猎人生成",
        description="都市传说风格，神秘诡异的现代怪谈"
    ),
    
    # 17. 甜点王国风
    ReportStyle(
        id="sweet",
        name="甜点日报",
        icon="🍰",
        keywords=["dessert", "cake", "candy", "sweet", "pastry", "cute food"],
        color="orange",
        title_template="🍰 {name} - 甜蜜通讯",
        header_template="**🍰 今天的糖分超标了吗？**\n\n*在甜点王国，每一天都是甜蜜的冒险...*",
        footer_template="*Stressed spelled backwards is desserts!*\n\n🧁 甜点师生成",
        description="甜点风格，治愈系的美食世界"
    ),
    
    # 18. 西部牛仔风
    ReportStyle(
        id="western",
        name="西部日报",
        icon="🤠",
        keywords=["western", "cowboy", "desert", "saloon", "wild west", "cactus"],
        color="orange",
        title_template="🤠 {name} - 西部快讯",
        header_template="**🤠 荒野大镖客**\n\n*在夕阳下的沙漠，牛仔的足迹延伸至地平线...*",
        footer_template="*This town ain't big enough for the two of us.*\n\n🌵 赏金猎人生成",
        description="西部风格，荒野大镖客的冒险"
    ),
    
    # 19. 水族馆风
    ReportStyle(
        id="ocean",
        name="深海日报",
        icon="🐠",
        keywords=["ocean", "aquarium", "fish", "underwater", "coral", "jellyfish"],
        color="blue",
        title_template="🐠 {name} - 海洋通讯",
        header_template="**🐠 深海的秘密**\n\n*在蓝色的深海中，无数生命在静静游弋...*",
        footer_template="*Just keep swimming!*\n\n🐟 海洋探索者生成",
        description="海洋风格，水族馆的治愈世界"
    ),
    
    # 20. 极简主义风
    ReportStyle(
        id="minimal",
        name="极简日报",
        icon="⬜",
        keywords=["minimal", "simple", "clean", "white", "zen", "modern"],
        color="blue",
        title_template="⬜ {name} - 极简通讯",
        header_template="**⬜ 少即是多**\n\n*在简洁中寻找力量，在留白中发现美...*",
        footer_template="*Simplicity is the ultimate sophistication.*\n\n📐 极简主义者生成",
        description="极简风格，less is more的生活美学"
    ),
]


def get_random_style(exclude_ids: List[str] = None) -> ReportStyle:
    """随机获取一种风格（可排除已使用）"""
    exclude_ids = exclude_ids or []
    available = [s for s in STYLE_LIBRARY if s.id not in exclude_ids]
    
    if not available:
        # 如果都排除完了，返回全部
        available = STYLE_LIBRARY
    
    return random.choice(available)


def get_style_by_id(style_id: str) -> Optional[ReportStyle]:
    """根据ID获取风格"""
    for style in STYLE_LIBRARY:
        if style.id == style_id:
            return style
    return None


def format_report_with_style(items: List[str], style: ReportStyle) -> str:
    """使用风格格式化日报内容"""
    lines = [style.header_template, ""]
    
    for i, item in enumerate(items, 1):
        lines.append(f"**{i}.** {item}")
    
    lines.extend(["", style.footer_template])
    
    return "\n".join(lines)


# 风格统计信息
def get_style_stats():
    """获取风格库统计"""
    return {
        "total": len(STYLE_LIBRARY),
        "categories": list(set(s.color for s in STYLE_LIBRARY)),
        "styles": [s.name for s in STYLE_LIBRARY]
    }


if __name__ == "__main__":
    # 测试
    print("Style Library Test")
    print("=" * 50)
    
    stats = get_style_stats()
    print(f"Total styles: {stats['total']}")
    print(f"Colors: {', '.join(stats['categories'])}")
    print()
    
    # 随机选一个
    style = get_random_style()
    print(f"Random style: {style.icon} {style.name}")
    print(f"Keywords: {', '.join(style.keywords[:3])}")
    print(f"Color: {style.color}")
    
    # 格式化示例
    content = format_report_with_style(
        ["Task 1 completed", "Task 2 in progress", "Task 3 planned"],
        style
    )
    print("\nFormatted content preview:")
    print(content[:200] + "...")
