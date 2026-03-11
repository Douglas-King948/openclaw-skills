# Smart Meme - PowerShell 脚本
# 使用 ; 代替 && 以兼容 PowerShell

param(
    [Parameter(Position=0)]
    [string]$Command,
    
    [Parameter(Position=1)]
    [string]$Argument
)

# 获取脚本所在目录
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

function Show-Help {
    Write-Host "Smart Meme v3 - 表情包系统" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "用法:"
    Write-Host "  .\run.ps1 download          下载所有表情包"
    Write-Host "  .\run.ps1 download [分类]   下载指定分类"
    Write-Host "  .\run.ps1 random            随机获取表情包路径"
    Write-Host "  .\run.ps1 random [分类]     从指定分类随机获取"
    Write-Host "  .\run.ps1 stats             显示统计信息"
    Write-Host "  .\run.ps1 check             健康检查"
    Write-Host "  .\run.ps1 heal              执行自愈"
    Write-Host "  .\run.ps1 heal --dry-run    预演自愈"
    Write-Host "  .\run.ps1 config            显示配置信息"
    Write-Host "  .\run.ps1 send              发送随机表情包（返回路径）"
    Write-Host "  .\run.ps1 send [关键词]     根据关键词发送"
    Write-Host "  .\run.ps1 stock             查看库存"
    Write-Host "  .\run.ps1 list              列出所有分类"
    Write-Host ""
    Write-Host "示例:"
    Write-Host "  .\run.ps1 download panda"
    Write-Host "  .\run.ps1 send 熊猫头"
    Write-Host "  .\run.ps1 send 猫咪"
}

switch ($Command) {
    "download" {
        if ($Argument) {
            python main.py download $Argument
        } else {
            python main.py download
        }
    }
    
    "random" {
        if ($Argument) {
            python send.py random $Argument
        } else {
            python send.py random
        }
    }
    
    "stats" {
        python main.py stats
    }
    
    "check" {
        python main.py check
    }
    
    "heal" {
        if ($Argument -eq "--dry-run") {
            python main.py heal --dry-run
        } else {
            python main.py heal
        }
    }
    
    "config" {
        python main.py config
    }
    
    "send" {
        if ($Argument) {
            python send.py keyword $Argument
        } else {
            python send.py random
        }
    }
    
    "stock" {
        python send.py stock
    }
    
    "list" {
        python send.py list
    }
    
    default {
        Show-Help
    }
}
