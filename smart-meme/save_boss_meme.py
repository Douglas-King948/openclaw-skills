import shutil
from pathlib import Path

# 保存Boss发来的图到本地库存
src = Path("C:/Users/GD/.openclaw/media/inbound/e6112d4d-70ba-411f-a892-ebe75ab5ae93.jpg")
dst = Path("D:/openclaw/skills/smart-meme/local_memes/misc/boss_first_meme.jpg")

if src.exists():
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"✅ 已保存: {dst}")
    
    # 添加到数据库
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from core.store import get_store
    
    store = get_store()
    store.add(dst, "misc", ["boss", "first", "screenshot"])
    print("✅ 已入库")
else:
    print(f"❌ 源文件不存在: {src}")
