#!/bin/bash
# MCA Framework 安装脚本
# Usage: ./install.sh

echo "🚀 Installing MCA (Multimodal Capability Awakening) Framework..."

# 检查 OpenClaw 配置目录
OPENCLAW_DIR="${HOME}/.openclaw"
SKILLS_DIR="${OPENCLAW_DIR}/skills"

if [ ! -d "$OPENCLAW_DIR" ]; then
    echo "❌ Error: OpenClaw directory not found at ${OPENCLAW_DIR}"
    echo "Please ensure OpenClaw is installed first."
    exit 1
fi

# 创建 skills 目录（如果不存在）
mkdir -p "$SKILLS_DIR"

# 复制 skill 文件
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${SKILLS_DIR}/multimodal-awakening"

echo "📁 Copying files to ${TARGET_DIR}..."

if [ -d "$TARGET_DIR" ]; then
    echo "⚠️  Directory already exists. Updating..."
    rm -rf "$TARGET_DIR"
fi

cp -r "$SCRIPT_DIR" "$TARGET_DIR"

# 清理不需要的文件
rm -f "${TARGET_DIR}/install.sh"
rm -f "${TARGET_DIR}/.git" -rf 2>/dev/null || true

echo "✅ MCA Framework installed successfully!"
echo ""
echo "📖 Next steps:"
echo "1. Configure Gateway layer interceptor (see scripts/gateway-interceptor.js)"
echo "2. Restart OpenClaw Gateway"
echo "3. Start sending media files to test!"
echo ""
echo "📚 Documentation: ${TARGET_DIR}/SKILL.md"
echo "🐛 Issues: https://github.com/wangguangdong1/multimodal-awakening/issues"