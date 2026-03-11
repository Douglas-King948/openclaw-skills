import shutil
from pathlib import Path

# 复制Boss的截图到本地库存
src = Path("C:/Users/GD/.openclaw/media/inbound/e6112d4d-70ba-411f-a892-ebe75ab5ae93.jpg")
dst = Path("D:/openclaw/skills/smart-meme/local_memes/misc/boss_screenshot_001.jpg")

dst.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(src, dst)
print(f"✅ 已保存Boss的截图: {dst}")

# 添加到数据库
import sys
sys.path.insert(0, str(Path(__file__).parent))
from core.store import get_store

store = get_store()
store.add(dst, "misc", ["boss", "screenshot", "chat"])
print("✅ 已入库，第一张本地表情包诞生！")

# 显示统计
stats = store.get_stats()
print(f"\n📊 当前库存: {stats['total_count']} 张")
