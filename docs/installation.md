# 安装指南

## 📥 从 SkillsMP 安装（推荐）

[SkillsMP](https://skillsmp.com) 是全球最大的 Agent Skills 市场，拥有 120 万+ 技能。

### 方式一：使用 skills.sh CLI（推荐）

```bash
npx skills add liliwen88/doctor.skill
```

### 方式二：通过 Claude Code

```bash
/plugin add https://github.com/liliwen88/doctor.skill
```

### 方式三：从网站安装

访问 [skillsmp.com](https://skillsmp.com) 搜索 "doctor"，找到本技能后一键安装。

---

## 📥 从腾讯 SkillHub 安装

[腾讯 SkillHub](https://skillhub.cn) 是专为中国用户优化的 AI Skills 社区。

### 方式一：使用 SkillHub CLI（推荐）

```bash
# 先安装 SkillHub CLI（如未安装）
curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash

# 搜索并安装
skillhub search doctor
skillhub install doctor
```

### 方式二：从网站安装

访问 [skillhub.cn](https://skillhub.cn) 搜索 "doctor"，找到本技能后一键安装。

---

## 📥 手动安装（通用方式）

### 复制到项目（团队共享）

```bash
# 在项目根目录创建 .github/skills/ 文件夹
mkdir -p .github/skills/
# 将本技能复制到项目中
cp -r doctor.skill/.github/skills/doctor /path/to/your/project/.github/skills/
```

### 安装到个人配置（个人使用）

```bash
# Windows
xcopy /E /I .github\skills\doctor %USERPROFILE%\.copilot\skills\doctor\

# macOS / Linux
cp -r .github/skills/doctor ~/.copilot/skills/doctor/
```

### Git Submodule（推荐团队协作）

```bash
git submodule add https://github.com/liliwen88/doctor.skill.git .github/skills/doctor
```

---

## ✅ 验证安装

在支持 Agent Skills 的 AI 工具中：

1. 输入医疗相关问题（如"解释一下什么是心肌梗死"）
2. 或描述症状（如"我头痛三天了"）

如果技能正确加载，你会收到结构化的医疗信息回复。

## 🔄 更新

```bash
# Git Submodule 方式
git submodule update --remote .github/skills/doctor

# 手动方式
# 重新复制最新版本的 skill 文件夹即可
```

## 🌐 平台兼容性

| 平台 | 支持情况 | 安装方式 |
|------|---------|----------|
| [SkillsMP](https://skillsmp.com) | ✅ 已上架 | `npx skills add` |
| [腾讯 SkillHub](https://skillhub.cn) | ✅ 已上架 | `skillhub install` |
| Claude Code | ✅ 兼容 | `/plugin add` 或复制到 skills 目录 |
| OpenAI Codex CLI | ✅ 兼容 | 复制到 `~/.codex/skills/` |
| Cursor | ✅ 兼容 | 复制到 `.cursor/skills/` |
| VS Code (1.98+) | ✅ 兼容 | 复制到 `.github/skills/` 或 `~/.copilot/skills/` |
| Manus | ✅ 兼容 | 从 SkillsMP 一键运行 |
