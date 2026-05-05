# 安装指南

## 📥 安装到 VS Code

### 方法一：复制到项目（推荐团队共享）

1. 在项目根目录创建 `.github/skills/` 文件夹
2. 将本仓库的 `.github/skills/doctor/` 整个文件夹复制到你的 `.github/skills/` 中
3. 在 VS Code Chat 中输入 `/doctor` 即可使用

### 方法二：安装到个人配置（个人使用）

```bash
# Windows
xcopy /E /I .github\skills\doctor %USERPROFILE%\.copilot\skills\doctor\

# macOS / Linux
cp -r .github/skills/doctor ~/.copilot/skills/doctor/
```

### 方法三：Git Submodule（推荐团队）

```bash
git submodule add https://github.com/YOUR_USERNAME/doctor.skill.git .github/skills/doctor
```

## 📥 安装到 Claude Code

复制到 Claude Code 的 skills 目录：

```bash
# macOS / Linux
cp -r .github/skills/doctor ~/.claude/skills/doctor/
```

## ✅ 验证安装

在 VS Code Chat 中：

1. 输入 `/doctor` — 应该能看到技能提示
2. 或直接发送医疗相关问题（如"解释一下什么是心肌梗死"）

如果技能正确加载，你会收到结构化的医疗信息回复。

## 🔄 更新

```bash
# Git Submodule 方式
git submodule update --remote .github/skills/doctor

# 手动方式
# 重新复制最新版本的 skill 文件夹即可
```
