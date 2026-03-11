#!/usr/bin/env node
/**
 * OpenClaw 诊断工具
 * Usage: node diagnose.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const RESET = '\x1b[0m';

const CHECK = `${GREEN}✓${RESET}`;
const CROSS = `${RED}✗${RESET}`;
const WARN = `${YELLOW}!${RESET}`;

function log(title, content = '') {
  console.log(`\n${'='.repeat(50)}`);
  console.log(title);
  console.log('='.repeat(50));
  if (content) console.log(content);
}

function checkCommand(cmd) {
  try {
    const result = execSync(`which ${cmd}`, { encoding: 'utf8', stdio: 'pipe' });
    return { ok: true, path: result.trim() };
  } catch {
    return { ok: false };
  }
}

function getConfigDir() {
  const home = process.env.HOME || process.env.USERPROFILE;
  return path.join(home, '.openclaw');
}

function main() {
  log('OpenClaw 环境诊断报告', `时间: ${new Date().toISOString()}`);

  // 1. 基础依赖
  console.log('\n【基础依赖检查】');
  const deps = ['openclaw', 'node', 'npm', 'curl', 'tar'];
  deps.forEach(dep => {
    const result = checkCommand(dep);
    console.log(`${result.ok ? CHECK : CROSS} ${dep}: ${result.ok ? result.path : '未安装'}`);
  });

  // 2. Node 版本
  console.log('\n【Node 版本】');
  try {
    const version = execSync('node --version', { encoding: 'utf8' }).trim();
    console.log(`${CHECK} ${version}`);
  } catch {
    console.log(`${CROSS} 无法获取 Node 版本`);
  }

  // 3. 配置目录
  console.log('\n【配置目录】');
  const configDir = getConfigDir();
  if (fs.existsSync(configDir)) {
    console.log(`${CHECK} ${configDir}`);
    const files = fs.readdirSync(configDir);
    console.log('  内容:', files.join(', '));
  } else {
    console.log(`${CROSS} 配置目录不存在`);
  }

  // 4. OpenClaw 配置
  console.log('\n【OpenClaw 配置】');
  const configPath = path.join(configDir, 'openclaw.json');
  if (fs.existsSync(configPath)) {
    try {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

      // Gateway 配置
      if (config.gateway) {
        console.log(`${CHECK} Gateway 配置存在`);
        console.log(`  端口: ${config.gateway.port || '默认'}`);
        console.log(`  模式: ${config.gateway.mode || '未设置'}`);
        console.log(`  绑定: ${config.gateway.bind || '未设置'}`);
      } else {
        console.log(`${CROSS} Gateway 配置缺失`);
      }

      // Kimi-Claw 配置
      const kimiClaw = config.plugins?.entries?.['kimi-claw'];
      if (kimiClaw) {
        console.log(`${CHECK} Kimi-Claw 配置存在`);
        console.log(`  启用: ${kimiClaw.enabled}`);
        if (kimiClaw.config?.bridge?.token) {
          console.log(`${CHECK} Token 已配置`);
        } else {
          console.log(`${CROSS} Token 未配置`);
        }
      } else {
        console.log(`${CROSS} Kimi-Claw 未配置`);
      }

      // 代理配置
      if (config.agents) {
        console.log(`${CHECK} 代理配置存在`);
        console.log(`  默认工作区: ${config.agents.defaults?.workspace || '未设置'}`);
        console.log(`  默认模型: ${config.agents.defaults?.model?.primary || '未设置'}`);
        if (config.agents.list && config.agents.list.length > 0) {
          console.log(`${CHECK} 代理列表: ${config.agents.list.map(a => a.id).join(', ')}`);
        } else {
          console.log(`${WARN} 代理列表为空`);
        }
      } else {
        console.log(`${CROSS} 代理配置缺失`);
      }

      // 绑定配置
      if (config.bindings && config.bindings.length > 0) {
        console.log(`${CHECK} 绑定配置存在`);
        config.bindings.forEach((binding, index) => {
          console.log(`  绑定 ${index + 1}: ${binding.agentId} → ${binding.match?.channel || '所有频道'}${binding.match?.peer?.id ? `:${binding.match.peer.id}` : ''}`);
        });
      } else {
        console.log(`${WARN} 绑定配置为空`);
      }

      // 技能加载配置
      if (config.skills?.load?.extraDirs) {
        console.log(`${CHECK} 技能加载配置存在`);
        console.log(`  额外技能目录: ${config.skills.load.extraDirs.join(', ')}`);
      } else {
        console.log(`${WARN} 技能加载配置缺失`);
      }

    } catch (e) {
      console.log(`${CROSS} 配置文件解析失败: ${e.message}`);
    }
  } else {
    console.log(`${CROSS} 配置文件不存在`);
  }

  // 5. 插件目录
  console.log('\n【插件检查】');
  const extensionsDir = path.join(configDir, 'extensions');
  if (fs.existsSync(extensionsDir)) {
    const plugins = fs.readdirSync(extensionsDir).filter(f => {
      return fs.statSync(path.join(extensionsDir, f)).isDirectory();
    });
    if (plugins.length > 0) {
      console.log(`${CHECK} 已安装插件: ${plugins.join(', ')}`);
    } else {
      console.log(`${WARN} 插件目录为空`);
    }
  } else {
    console.log(`${WARN} 插件目录不存在`);
  }

  // 6. Kimi 同步状态
  console.log('\n【Kimi 同步状态】');
  const kimiDir = path.join(process.env.HOME || process.env.USERPROFILE, '.kimi', 'kimi-claw');
  const kimiConfig = path.join(kimiDir, 'openclaw.json');
  if (fs.existsSync(kimiConfig)) {
    console.log(`${CHECK} 同步配置存在: ${kimiConfig}`);
    const stat = fs.statSync(kimiConfig);
    console.log(`  修改时间: ${stat.mtime.toISOString()}`);
  } else {
    console.log(`${WARN} 同步配置不存在`);
  }

  // 7. 技能目录检查
  console.log('\n【技能目录检查】');
  const skillsDir = 'D:\\openclaw\\skills'; // 默认技能目录
  if (fs.existsSync(skillsDir)) {
    console.log(`${CHECK} 技能目录存在: ${skillsDir}`);
    const skills = fs.readdirSync(skillsDir).filter(f => {
      return fs.statSync(path.join(skillsDir, f)).isDirectory() && fs.existsSync(path.join(skillsDir, f, 'SKILL.md'));
    });
    console.log(`  已加载技能: ${skills.join(', ')}`);
  } else {
    console.log(`${WARN} 技能目录不存在`);
  }

  // 8. 代理目录检查
  console.log('\n【代理目录检查】');
  const agentsDir = path.join(configDir, 'agents');
  if (fs.existsSync(agentsDir)) {
    const agents = fs.readdirSync(agentsDir).filter(f => {
      return fs.statSync(path.join(agentsDir, f)).isDirectory();
    });
    console.log(`${CHECK} 代理目录存在: ${agentsDir}`);
    console.log(`  代理数量: ${agents.length}`);
    agents.forEach(agent => {
      const agentDir = path.join(agentsDir, agent, 'agent');
      if (fs.existsSync(agentDir)) {
        const modelFile = path.join(agentDir, 'models.json');
        const authFile = path.join(agentDir, 'auth-profiles.json');
        const hasModel = fs.existsSync(modelFile);
        const hasAuth = fs.existsSync(authFile);
        console.log(`  ${agent}: ${hasModel ? '✓ 模型' : '✗ 模型'} ${hasAuth ? '✓ 认证' : '✗ 认证'}`);
      }
    });
  } else {
    console.log(`${WARN} 代理目录不存在`);
  }

  log('诊断完成');
}

main();
