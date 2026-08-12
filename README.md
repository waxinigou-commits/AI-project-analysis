# AI Signal

每日追踪 Product Hunt 与 WhatLaunched 新发布 AI 产品，并使用 GitHub Models 生成定位、目标用户、商业模式、竞品、收费模式与增长机会分析。

仓库同时提供可安装的 **AI 新产品增长雷达 Codex Agent**。它只使用 Codex，不需要 `OPENAI_API_KEY`：负责发现与核验新品、生成商业分析，并制作小红书、知乎、V2EX、X、LinkedIn、公众号等平台的待审核推广内容。

## 功能

- 产品雷达：分类、时间与关键词检索
- 商业分析：定位、客群、定价、竞品、机会、风险、置信度
- 趋势统计：赛道发布密度与商业潜力
- 数据留存：SQLite 为分析存档，JSON 快照驱动 GitHub Pages
- 每日更新：GitHub Actions 定时采集并提交新数据
- 事实/分析分层：名称、标语、日期、官网与发布页为来源事实；商业判断明确标记为分析

## 本地运行

```bash
npm install
npm run dev
```

数据校验与生产构建：

```bash
npm test
```

## 安装 Codex Agent

将 [`skills/ai-product-growth-agent`](skills/ai-product-growth-agent) 文件夹复制到个人 Codex skills 目录，或者让 Codex 从本仓库安装该 Skill。安装后可这样使用：

```text
使用 $ai-product-growth-agent 收集过去 24 小时的新 AI 产品，核验前 10 名，
并为最值得关注的 3 个产品生成多平台推广草稿；不要自动发布。
```

Agent 默认工作流为“采集 → 核验 → 分析 → 生成草稿 → 人工确认 → 发布”。采集与生成草稿可以定时运行；向外部平台发帖必须使用用户已授权的账号，并在发布前获得明确确认。

无需大模型即可单独运行公开 Feed 收集器：

```bash
python3 skills/ai-product-growth-agent/scripts/collect_sources.py \
  --hours 48 \
  --output outputs/product-candidates.json
```

## 自动化设置

1. 在仓库 **Settings → Models** 启用 GitHub Models。
2. 在 **Settings → Pages → Build and deployment** 选择 **GitHub Actions**。
3. 手动运行 `Daily product intelligence` 工作流验证采集；之后每天 UTC 00:30（北京时间 08:30）自动执行。

无需 OpenAI API key。工作流使用 GitHub 自动提供的 `GITHUB_TOKEN`，权限严格限制为 `models: read` 与 `contents: write`。GitHub Models 目前属于公开预览，并有调用额度限制。

## 数据源说明

- Product Hunt 使用公开 RSS feed。
- WhatLaunched 使用公开 AI 产品目录；解析器只接受能稳定解析的结构化卡片，防止误写。
- 每条静态记录必须有直达发布页、官网、核验日期与事实状态，构建前由 `scripts/validate_data.py` 强制检查。
- 未经来源披露的价格一律显示“来源未披露”。定位、目标用户、竞品、商业模式、评分和机会属于分析层，不代表产品方确认。
- 所有推断均应视为研究辅助，不构成投资建议。

## 技术栈

React 19 · TypeScript · Vite · Python 标准库 · SQLite · GitHub Actions · GitHub Pages · GitHub Models
