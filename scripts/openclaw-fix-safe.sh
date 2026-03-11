#!/bin/bash
# OpenClaw 配置安全修复脚本 v2.0
# 适用：WSL2 Ubuntu + OpenClaw
# 功能：诊断问题、安全修复、保守配置

set -e

echo "🔧 OpenClaw 安全配置修复工具 v2.0"
echo "===================================="

# 配置路径
CONFIG_PATH="$HOME/.openclaw/openclaw.json"
BACKUP_DIR="$HOME/.openclaw/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/openclaw.json.bak_$TIMESTAMP"
DRY_RUN=false

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 解析参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN=true
      echo -e "${BLUE}🔍 试运行模式：只显示修改，不实际写入${NC}"
      shift
      ;;
    --help)
      echo "用法: $0 [选项]"
      echo "选项:"
      echo "  --dry-run    试运行，显示将要做的修改但不实际执行"
      echo "  --help       显示帮助"
      exit 0
      ;;
    *)
      echo "未知选项: $1"
      exit 1
      ;;
  esac
done

# 检查配置文件
if [ ! -f "$CONFIG_PATH" ]; then
    echo -e "${RED}❌ 错误：找不到配置文件 $CONFIG_PATH${NC}"
    exit 1
fi

# 创建备份目录并备份
mkdir -p "$BACKUP_DIR"
cp "$CONFIG_PATH" "$BACKUP_FILE"
echo -e "${GREEN}✅ 已备份到：$BACKUP_FILE${NC}"

# 创建 Python 诊断脚本
PYTHON_SCRIPT=$(cat << 'EOF'
import json
import sys
from pathlib import Path

config_path = sys.argv[1]
dry_run = sys.argv[2] == "true"

with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

changes = []
warnings = []

# 1. 检查主模型
primary = config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary', '')
print(f"\n📊 当前主模型: {primary}")

# 2. 检查 models.providers 配置
providers = config.get('models', {}).get('providers', {})
print(f"📊 已配置的 providers: {list(providers.keys())}")

# 3. 检查主模型是否在 providers 中定义
if primary:
    provider_name = primary.split('/')[0] if '/' in primary else primary
    if provider_name not in providers:
        warnings.append(f"⚠️  主模型 {primary} 的 provider '{provider_name}' 未在 models.providers 中定义！")
        changes.append(f"需要添加 provider: {provider_name}")
    else:
        # 检查 input 配置
        models_list = providers[provider_name].get('models', [])
        model_id = primary.split('/')[-1] if '/' in primary else ''
        
        found_model = None
        for m in models_list:
            if m.get('id') == model_id:
                found_model = m
                break
        
        if found_model:
            input_types = found_model.get('input', [])
            print(f"📊 模型 {model_id} 的 input: {input_types}")
            if 'image' not in input_types:
                warnings.append(f"⚠️  模型 {primary} 未声明支持 image 输入")
                changes.append(f"建议：添加 'image' 到 input，或配置 imageModel fallback")
        else:
            warnings.append(f"⚠️  在 provider {provider_name} 中未找到模型 {model_id} 的详细配置")

# 4. 检查 imageModel 配置
image_model = config.get('agents', {}).get('defaults', {}).get('imageModel')
if image_model:
    print(f"📊 imageModel: 已配置 {image_model}")
else:
    if 'image' not in str(config):
        changes.append("建议：添加 imageModel 配置作为 vision fallback")

# 5. 检查 tools
if 'image' not in str(config.get('tools', {})):
    changes.append("建议：确保 tools 包含 'image'")

# 输出诊断结果
print("\n" + "="*50)
print("📋 诊断结果：")
print("="*50)

if warnings:
    print("\n⚠️  发现的问题：")
    for w in warnings:
        print(f"  {w}")

if changes:
    print("\n🔧 建议的修改：")
    for c in changes:
        print(f"  {c}")
else:
    print("\n✅ 配置看起来正常")

# 安全修复建议
print("\n" + "="*50)
print("💡 修复方案（保守模式）：")
print("="*50)

if warnings:
    print("\n方案1: 配置 imageModel fallback（推荐，安全）")
    print("  - 保留当前主模型")
    print("  - 图片分析使用专门的 vision 模型")
    
    print("\n方案2: 修改主模型为支持 vision 的模型")
    print("  - 例如：kimi-coding/k2p5")
    print("  - 所有分析都走这个模型")
    
    print("\n方案3: 给当前模型添加 input 声明（如果确实支持）")
    print("  - 需要确认模型 API 支持图片输入")

# 如果是 dry-run，到此结束
if dry_run:
    print("\n🔍 试运行完成，未实际修改配置")
    sys.exit(0)

# 实际修复（询问用户）
print("\n" + "="*50)
response = input("\n是否执行修复？(1: imageModel方案 / 2: 换主模型 / 3: 添加input / n: 取消): ")

if response == '1':
    # 方案1: 添加 imageModel
    if 'agents' not in config:
        config['agents'] = {}
    if 'defaults' not in config['agents']:
        config['agents']['defaults'] = {}
    if 'model' not in config['agents']['defaults']:
        config['agents']['defaults']['model'] = {}
    
    config['agents']['defaults']['model']['imageModel'] = {
        'primary': 'kimi-coding/k2p5',
        'fallbacks': ['openai/gpt-4o']
    }
    
    # 确保 Kimi 配置存在
    if 'models' not in config:
        config['models'] = {'providers': {}}
    if 'kimi-coding' not in config['models']['providers']:
        config['models']['providers']['kimi-coding'] = {
            'baseUrl': 'https://api.kimi.com/coding/',
            'api': 'anthropic-messages',
            'models': [{
                'id': 'k2p5',
                'name': 'Kimi for Coding',
                'input': ['text', 'image'],
                'cost': {'input': 0, 'output': 0},
                'contextWindow': 262144,
                'maxTokens': 32768
            }]
        }
    
    print("✅ 已添加 imageModel fallback 配置")

elif response == '2':
    # 方案2: 换主模型
    config['agents']['defaults']['model']['primary'] = 'kimi-coding/k2p5'
    
    # 确保 Kimi 配置存在
    if 'models' not in config:
        config['models'] = {'providers': {}}
    if 'kimi-coding' not in config['models']['providers']:
        config['models']['providers']['kimi-coding'] = {
            'baseUrl': 'https://api.kimi.com/coding/',
            'api': 'anthropic-messages',
            'models': [{
                'id': 'k2p5',
                'name': 'Kimi for Coding',
                'input': ['text', 'image'],
                'cost': {'input': 0, 'output': 0},
                'contextWindow': 262144,
                'maxTokens': 32768
            }]
        }
    
    print("✅ 已将主模型改为 kimi-coding/k2p5")

elif response == '3':
    # 方案3: 给当前模型添加 input（需要用户确认）
    print("⚠️  警告：这需要确认模型 API 确实支持图片输入")
    confirm = input("确认要添加 image 支持吗？(yes/no): ")
    if confirm == 'yes' and primary:
        provider_name = primary.split('/')[0] if '/' in primary else primary
        model_id = primary.split('/')[-1] if '/' in primary else ''
        
        if provider_name in config.get('models', {}).get('providers', {}):
            for m in config['models']['providers'][provider_name]['models']:
                if m.get('id') == model_id:
                    if 'input' not in m:
                        m['input'] = ['text']
                    if 'image' not in m['input']:
                        m['input'].append('image')
                    print(f"✅ 已为 {primary} 添加 image 支持")
                    break
else:
    print("❌ 取消修改")
    sys.exit(0)

# 写入配置
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"\n✅ 配置已保存")
print(f"📁 备份位置: {sys.argv[1]}.bak_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}")
print(f"\n⚠️  请运行: openclaw gateway restart")
EOF
)

# 保存并执行 Python 脚本
TMP_PY=$(mktemp)
echo "$PYTHON_SCRIPT" > "$TMP_PY"

# 先运行诊断（不修改）
echo -e "\n${BLUE}🔍 第一步：诊断当前配置...${NC}"
python3 "$TMP_PY" "$CONFIG_PATH" "true" || true

# 询问是否继续
echo ""
echo -e "${YELLOW}以上是诊断结果。${NC}"
read -p "是否继续执行修复？(yes/no): " CONTINUE

if [ "$CONTINUE" != "yes" ]; then
    echo "❌ 已取消"
    rm "$TMP_PY"
    exit 0
fi

# 执行修复
echo -e "\n${GREEN}🔧 执行修复...${NC}"
python3 "$TMP_PY" "$CONFIG_PATH" "false"

# 清理
rm "$TMP_PY"

echo ""
echo "🎉 完成！"
echo ""
echo "🧪 测试步骤："
echo "   1. openclaw gateway restart"
echo "   2. 发送一张图片"
echo "   3. 观察是否自动分析"
echo ""
echo "🔄 如需回滚："
echo "   cp $BACKUP_FILE $CONFIG_PATH"
echo "   openclaw gateway restart"