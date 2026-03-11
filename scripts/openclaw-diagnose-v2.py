#!/usr/bin/env python3
"""
OpenClaw Config Diagnostic Tool
Cross-platform: Windows / Linux / macOS
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Model capabilities database (based on official docs and testing)
MODEL_DB = {
    'kimi-coding/k2p5': {'input': ['text', 'image'], 'vision': True},
    'kimi/moonshot-v1-128k': {'input': ['text'], 'vision': False},
    'kimi/moonshot-v1-8k': {'input': ['text'], 'vision': False},
    'deepseek/deepseek-chat': {'input': ['text'], 'vision': False},
    'deepseek/deepseek-reasoner': {'input': ['text'], 'vision': False},
    'openai/gpt-4o': {'input': ['text', 'image', 'audio'], 'vision': True},
    'openai/gpt-4o-mini': {'input': ['text', 'image'], 'vision': True},
    'anthropic/claude-3-opus': {'input': ['text', 'image', 'pdf'], 'vision': True},
    'anthropic/claude-3-sonnet': {'input': ['text', 'image'], 'vision': True},
}

def load_config(path):
    """Load JSON config"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(path, config):
    """Save JSON config"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def backup_config(path):
    """Create timestamped backup"""
    backup_dir = path.parent / 'backups'
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f'openclaw.json.bak_{timestamp}'
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return backup_path

def diagnose(config):
    """Diagnose configuration issues"""
    issues = []
    suggestions = []
    
    primary = config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary', '')
    print(f"\n[INFO] Primary model: {primary}")
    
    # Check model capabilities
    if primary in MODEL_DB:
        caps = MODEL_DB[primary]
        print(f"[INFO] Known capabilities: input={caps['input']}, vision={caps['vision']}")
        if not caps['vision']:
            issues.append(f"WARNING: Primary model {primary} does NOT support vision (image analysis)")
            suggestions.append("Consider adding imageModel fallback or changing primary model")
    else:
        issues.append(f"WARNING: Unknown model {primary}, cannot determine capabilities")
    
    # Check providers config
    providers = config.get('models', {}).get('providers', {})
    print(f"[INFO] Configured providers: {list(providers.keys())}")
    
    if primary:
        provider_name = primary.split('/')[0] if '/' in primary else primary
        if provider_name not in providers:
            issues.append(f"ERROR: Provider '{provider_name}' not defined in models.providers!")
            suggestions.append(f"Add provider config for {provider_name}")
        else:
            # Check if model input is declared
            model_id = primary.split('/')[-1] if '/' in primary else ''
            models_list = providers[provider_name].get('models', [])
            found = False
            for m in models_list:
                if m.get('id') == model_id:
                    found = True
                    input_types = m.get('input', [])
                    print(f"[INFO] Model {model_id} input: {input_types}")
                    
                    # Check if image is missing but model supports it
                    if 'image' not in input_types and primary in MODEL_DB:
                        if MODEL_DB[primary]['vision']:
                            issues.append(f"WARNING: Model {primary} supports vision but 'image' not in input")
                            suggestions.append(f"Add 'image' to input for {primary}")
                    break
            
            if not found:
                issues.append(f"WARNING: Model {model_id} config not found in provider {provider_name}")
    
    # Check imageModel fallback
    image_model = config.get('agents', {}).get('defaults', {}).get('imageModel')
    if image_model:
        print(f"[INFO] imageModel fallback: {image_model}")
    else:
        print(f"[INFO] imageModel fallback: NOT configured")
        if issues:
            suggestions.append("Add imageModel fallback for vision tasks")
    
    # Check tools profile
    tools = config.get('tools', {})
    profile = tools.get('profile', 'minimal')
    print(f"[INFO] Tools profile: {profile}")
    if profile == 'minimal':
        issues.append("WARNING: tools.profile is 'minimal', may lack image tool")
        suggestions.append("Change tools.profile to 'full' or add image to tools.allow")
    
    return issues, suggestions

def fix_image_fallback(config):
    """Add imageModel fallback"""
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
    
    # Ensure Kimi config exists
    ensure_kimi_config(config)
    print("[OK] Added imageModel fallback")

def fix_change_primary(config):
    """Change primary model to Kimi"""
    if 'agents' not in config:
        config['agents'] = {'defaults': {'model': {}}}
    
    old = config['agents']['defaults']['model'].get('primary', '')
    config['agents']['defaults']['model']['primary'] = 'kimi-coding/k2p5'
    
    ensure_kimi_config(config)
    print(f"[OK] Changed primary model from {old} to kimi-coding/k2p5")

def fix_add_input(config, model_path):
    """Add input declaration to model"""
    provider = model_path.split('/')[0] if '/' in model_path else model_path
    model_id = model_path.split('/')[-1] if '/' in model_path else ''
    
    # Get suggested input from database
    if model_path in MODEL_DB:
        suggested = MODEL_DB[model_path]['input']
    else:
        suggested = ['text']  # Conservative default
    
    if 'models' not in config:
        config['models'] = {'providers': {}}
    if provider not in config['models']['providers']:
        print(f"[ERROR] Provider {provider} not found")
        return False
    
    provider_cfg = config['models']['providers'][provider]
    if 'models' not in provider_cfg:
        provider_cfg['models'] = []
    
    # Find and update model
    for m in provider_cfg['models']:
        if m.get('id') == model_id:
            m['input'] = suggested
            print(f"[OK] Added input {suggested} to {model_path}")
            return True
    
    # Add new model entry
    provider_cfg['models'].append({'id': model_id, 'input': suggested})
    print(f"[OK] Created model config with input {suggested}")
    return True

def ensure_kimi_config(config):
    """Ensure Kimi provider config exists"""
    if 'models' not in config:
        config['models'] = {'providers': {}}
    
    if 'kimi-coding' not in config['models']['providers']:
        config['models']['providers']['kimi-coding'] = {
            'baseUrl': 'https://api.kimi.com/coding/',
            'api': 'anthropic-messages',
            'models': [{
                'id': 'k2p5',
                'name': 'Kimi for Coding',
                'reasoning': True,
                'input': ['text', 'image'],
                'cost': {'input': 0, 'output': 0, 'cacheRead': 0, 'cacheWrite': 0},
                'contextWindow': 262144,
                'maxTokens': 32768
            }]
        }
        print("[OK] Added Kimi provider config")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='OpenClaw Config Diagnostic Tool')
    parser.add_argument('--config', '-c', default='~/.openclaw/openclaw.json',
                       help='Config file path')
    parser.add_argument('--dry-run', '-n', action='store_true',
                       help='Diagnose only, do not modify')
    args = parser.parse_args()
    
    config_path = Path(args.config).expanduser()
    
    print("=" * 60)
    print("OpenClaw Config Diagnostic Tool")
    print("=" * 60)
    
    # Load config
    try:
        config = load_config(config_path)
        print(f"\n[OK] Loaded config: {config_path}")
    except Exception as e:
        print(f"\n[ERROR] Failed to load config: {e}")
        return 1
    
    # Backup
    try:
        backup_path = backup_config(config_path)
        print(f"[OK] Backup created: {backup_path}")
    except Exception as e:
        print(f"[ERROR] Backup failed: {e}")
        return 1
    
    # Diagnose
    print("\n" + "=" * 60)
    print("DIAGNOSIS")
    print("=" * 60)
    issues, suggestions = diagnose(config)
    
    print("\n" + "-" * 60)
    if issues:
        print(f"Found {len(issues)} issues:")
        for i in issues:
            print(f"  - {i}")
    else:
        print("No issues found")
    
    if suggestions:
        print(f"\nSuggestions:")
        for s in suggestions:
            print(f"  - {s}")
    
    # Dry run mode
    if args.dry_run:
        print("\n[DRY-RUN] No changes made")
        print(f"\nBackup location: {backup_path}")
        return 0
    
    # Interactive fix
    if not issues:
        print("\n[OK] Configuration looks good")
        return 0
    
    print("\n" + "=" * 60)
    print("FIX OPTIONS")
    print("=" * 60)
    print("\n1. Add imageModel fallback (RECOMMENDED)")
    print("   - Keep current primary model")
    print("   - Use Kimi/OpenAI for image analysis only")
    print("\n2. Change primary model to Kimi")
    print("   - Use kimi-coding/k2p5 for everything")
    print("\n3. Add input declaration to current model")
    print("   - Only if you're SURE the model supports images")
    print("\nn. Cancel (no changes)")
    
    try:
        choice = input("\nSelect option (1/2/3/n): ").strip().lower()
    except EOFError:
        print("\n[No input - running in non-interactive mode]")
        return 0
    
    if choice == '1':
        fix_image_fallback(config)
    elif choice == '2':
        fix_change_primary(config)
    elif choice == '3':
        primary = config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary', '')
        confirm = input(f"Confirm {primary} supports images? (yes/no): ")
        if confirm == 'yes':
            fix_add_input(config, primary)
        else:
            print("[CANCELLED]")
            return 0
    else:
        print("[CANCELLED]")
        return 0
    
    # Save
    try:
        save_config(config_path, config)
        print(f"\n[OK] Config saved to {config_path}")
        print("\n[IMPORTANT] Run: openclaw gateway restart")
    except Exception as e:
        print(f"\n[ERROR] Failed to save: {e}")
        return 1
    
    print(f"\n[NOTE] Backup: {backup_path}")
    print("[NOTE] To rollback: copy backup to config path")
    return 0

if __name__ == '__main__':
    sys.exit(main())
