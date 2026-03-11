# AI_README.md

<!-- 
  AI Agent Protocol Document
  This file is optimized for machine parsing
  Human readability is secondary
-->

## Repository Metadata

```json
{
  "repository": {
    "name": "openclaw-skills",
    "type": "skill_collection",
    "version": "1.0.0",
    "protocol_version": "openclaw-agent-v1",
    "last_updated": "2026-03-06T00:55:00Z"
  },
  "skills": {
    "total_count": 10,
    "categories": ["general", "feishu", "debug"],
    "installation_method": "copy_to_skills_directory"
  }
}
```

## Quick Actions

### Install Skill
```bash
# Method 1: Direct copy
cp -r skills/{skill_name} ~/openclaw/skills/

# Method 2: Git submodule
git submodule add https://github.com/Douglas-King948/openclaw-skills.git
```

### Verify Installation
```python
import os
from pathlib import Path

def verify_skill(skill_name: str) -> dict:
    skill_path = Path.home() / "openclaw" / "skills" / skill_name
    
    required_files = ["SKILL.md", "_meta.json"]
    optional_files = ["index.js", "__init__.py", "README.md"]
    
    result = {
        "skill_name": skill_name,
        "installed": skill_path.exists(),
        "has_documentation": (skill_path / "SKILL.md").exists(),
        "has_metadata": (skill_path / "_meta.json").exists(),
        "entry_point": None,
        "triggers": [],
        "status": "unknown"
    }
    
    if (skill_path / "index.js").exists():
        result["entry_point"] = "index.js"
        result["language"] = "javascript"
    elif (skill_path / "__init__.py").exists():
        result["entry_point"] = "__init__.py"
        result["language"] = "python"
    
    # Parse triggers from SKILL.md
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding='utf-8')
        # Extract triggers using regex patterns
        import re
        trigger_patterns = [
            r'[触发词|关键词]\s*[:：]\s*(.+)',
            r'trigger[s]?\s*[:：]\s*(.+)',
            r'-\s+["\']([^"\']+)["\']'  # Bullet point triggers
        ]
        for pattern in trigger_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            result["triggers"].extend(matches)
    
    result["status"] = "ready" if result["has_documentation"] and result["has_metadata"] else "incomplete"
    return result
```

## Skill Manifest

### Category: General

| ID | Name | Triggers | Language | Entry Point |
|----|------|----------|----------|-------------|
| skill_001 | unified-search | ["搜索", "search", "查找", "query"] | Python | `__init__.py` |
| skill_002 | smart-meme | ["表情包", "meme", "马喽", "来个"] | Python | `smart_meme.py` |
| skill_003 | find-skills | ["找技能", "技能", "skill"] | Python | `__init__.py` |
| skill_004 | uv-priority | ["uv", "pip", "python"] | Markdown | N/A (config) |
| skill_005 | openclaw-debugger | ["诊断", "debug", "修复"] | JavaScript | `diagnose.js` |

### Category: Feishu

| ID | Name | Triggers | Language | Entry Point |
|----|------|----------|----------|-------------|
| feishu_001 | feishu-doc-manager | ["文档", "doc", "上传"] | Python | `feishu_uploader.py` |
| feishu_002 | feishu-sheets-skill | ["表格", "sheets", "多维"] | Python | `scripts/feishu_sheets.py` |
| feishu_003 | feishu-messaging | ["消息", "发送", "通知"] | JavaScript | `index.js` |
| feishu_004 | feishu-bridge | ["桥接", "bridge", "连接"] | JavaScript | `bridge.mjs` |
| feishu_005 | feishu-md-uploader | ["md上传", "markdown", "md转"] | Python | `feishu_uploader.py` |

## Protocol Compliance

### SKILL.md Required Fields

```yaml
---
name: string           # Skill identifier (kebab-case)
description: string    # Natural language description with triggers
version: string        # SemVer format
author: string         # Creator identifier
---
```

### _meta.json Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["name", "version", "triggers"],
  "properties": {
    "name": {"type": "string"},
    "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
    "description": {"type": "string"},
    "triggers": {
      "type": "array",
      "items": {"type": "string"}
    },
    "entry_point": {"type": "string"},
    "language": {"enum": ["python", "javascript", "typescript"]},
    "dependencies": {
      "type": "array",
      "items": {"type": "string"}
    },
    "permissions": {
      "type": "array",
      "items": {"type": "string"}
    }
  }
}
```

## Automation Scripts

### Auto-Install All Skills

```bash
#!/bin/bash
# auto_install.sh

REPO_URL="https://github.com/Douglas-King948/openclaw-skills.git"
SKILLS_DIR="$HOME/openclaw/skills"

# Clone or pull
cd /tmp
if [ -d "openclaw-skills" ]; then
    cd openclaw-skills && git pull
else
    git clone "$REPO_URL"
    cd openclaw-skills
fi

# Install each skill
for skill in */; do
    if [ -d "$skill" ] && [ -f "$skill/SKILL.md" ]; then
        echo "Installing: $skill"
        cp -r "$skill" "$SKILLS_DIR/"
    fi
done

echo "Installation complete!"
```

### Skill Health Check

```python
#!/usr/bin/env python3
# health_check.py

import json
from pathlib import Path

def check_all_skills():
    skills_dir = Path.home() / "openclaw" / "skills"
    results = []
    
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
            
        skill_name = skill_dir.name
        status = {
            "name": skill_name,
            "has_skill_md": (skill_dir / "SKILL.md").exists(),
            "has_meta_json": (skill_dir / "_meta.json").exists(),
            "has_entry_point": any([
                (skill_dir / "index.js").exists(),
                (skill_dir / "__init__.py").exists()
            ])
        }
        
        status["healthy"] = all([
            status["has_skill_md"],
            status["has_meta_json"]
        ])
        
        results.append(status)
    
    return results

if __name__ == "__main__":
    results = check_all_skills()
    print(json.dumps(results, indent=2))
```

## API Endpoints (GitHub)

### List Repository Contents
```
GET https://api.github.com/repos/Douglas-King948/openclaw-skills/contents
Accept: application/vnd.github.v3+json
```

### Get Skill Metadata
```
GET https://api.github.com/repos/Douglas-King948/openclaw-skills/contents/{skill_name}/_meta.json
Accept: application/vnd.github.v3+json
```

### Raw Skill Documentation
```
GET https://raw.githubusercontent.com/Douglas-King948/openclaw-skills/main/{skill_name}/SKILL.md
```

## Error Handling

### Common Issues

1. **Skill Not Found**
   - Check skill name spelling
   - Verify skill is in repository
   - Check local skills directory path

2. **Missing Dependencies**
   - Read SKILL.md for requirements
   - Check _meta.json dependencies field
   - Install missing packages

3. **Permission Denied**
   - Verify file permissions
   - Check OpenClaw agent permissions
   - Review SKILL.md permission requirements

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-06 | Initial release with 10 skills |

## Contact

- Repository: https://github.com/Douglas-King948/openclaw-skills
- Issues: https://github.com/Douglas-King948/openclaw-skills/issues
