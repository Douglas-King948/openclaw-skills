@echo off
chcp 65001 >nul
echo ========================================
echo Smart Meme v3 - 批量下载表情包
echo ========================================
echo.

cd /d "D:\openclaw\skills\smart-meme"

echo [1/4] 正在下载熊猫头表情包...
python main.py download panda
echo.

echo [2/4] 正在下载程序员梗图...
python main.py download programmer
echo.

echo [3/4] 正在下载二次元表情包...
python main.py download anime
echo.

echo [4/4] 正在下载其他梗图...
python main.py download misc
echo.

echo ========================================
echo 下载完成！查看统计：
python main.py stats
echo ========================================

pause
