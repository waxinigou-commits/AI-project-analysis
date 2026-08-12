# AI 新产品增长雷达：首发推广包

状态：**草稿，发布前需确认账号、链接和最终文案。**

项目主页：https://waxinigou-commits.github.io/AI-project-analysis/

代码与安装：https://github.com/waxinigou-commits/AI-project-analysis/tree/main/skills/ai-product-growth-agent

## 一句话定位

一个只用 Codex 的 AI 新产品增长 Agent：每天发现并核验新发布的 AI 产品，完成商业化分析，再生成适合不同平台的待审核推广内容。

## 核心卖点

- 不需要 `OPENAI_API_KEY`，在 Codex 中直接安装和使用。
- 从公开 Feed 发现新产品，并把“来源发布时间”和“产品首次上线时间”分开记录。
- 将事实、分析和未知信息分层，避免把推测写成事实。
- 为小红书、知乎、V2EX、X、LinkedIn 和公众号生成差异化草稿。
- 默认停在人工审核，不绕过验证码，不擅自使用用户账号发布。

## V2EX 草稿

标题：做了一个只用 Codex 的 AI 新产品增长 Agent：收集、核验、分析，再生成推广草稿

正文：

最近在做一个 AI 新产品分析项目，遇到两个问题：一是 Product Hunt 首页有时会遇到真人验证，二是国内的 AI 产品信息分散在 V2EX、导航站和产品自己的发布页里。

所以我把流程整理成了一个可安装的 Codex Skill：先从公开 RSS/Feed 找候选产品，再由 Codex 核验官网、定价和发布时间，最后生成结构化商业分析与多平台推广草稿。

它默认不会自动发帖。对外发布前会展示最终文案、账号、链接和素材，确认后才执行。公开 Feed 收集脚本也不调用大模型或私有 API。

目前支持的典型用法：

```text
使用 $ai-product-growth-agent 收集过去 24 小时的新 AI 产品，
核验前 10 名，并为最值得关注的 3 个生成推广草稿；不要自动发布。
```

代码和安装：<代码仓库链接>

想听听大家的意见：你们最希望它增加哪个中文新品来源，或者最需要适配哪个推广渠道？

## 小红书草稿

标题候选：

1. 我做了一个每天找 AI 新产品的 Codex Agent
2. 不用 API Key，自动整理 AI 新品和推广文案
3. 让 Codex 每天替我做 AI 产品情报

正文：

每天刷 Product Hunt、V2EX 和各种 AI 导航，真正费时间的不是“看到新品”，而是核验：它到底什么时候上线？价格是多少？目标用户是谁？哪些是事实，哪些只是宣传？

我把这套流程做成了一个 Codex Agent：

① 从公开 Feed 收集新品线索  
② 打开官网和一手来源核验  
③ 分析定位、目标用户、商业模式、竞品与机会  
④ 自动生成不同平台的推广草稿  
⑤ 人工确认后才发布

它不需要 OpenAI API Key，也不会遇到验证码就硬爬，更不会默认拿账号群发。

适合独立开发者、产品经理、AI 投资研究和内容创作者。

项目链接：<项目主页链接>

#AI工具 #独立开发者 #产品经理 #Codex #AI创业

## 知乎草稿

问题方向：如何持续发现并判断一个新 AI 产品是否值得关注？

开头：

单纯建立一个 AI 工具导航并不难，难的是让数据保持可核验：平台收录日期不等于产品首次发布日期，首页推荐不等于真实增长，定价也不能靠模型猜测。

因此我把它设计成了一个 Codex Agent，而不是另一个只展示卡片的静态目录。它从公开 Feed 获取候选，随后核验产品官网、定价页和发布记录，将结论拆成“事实、分析、未知”三层，再生成商业化报告和待审核推广内容。

后续正文建议围绕以下结构扩写：

1. 为什么新品收集必须区分发现、核验与分析；
2. 国内外数据源的差异；
3. Agent 如何处理验证码、登录墙和信息冲突；
4. 为什么多平台推广不能复制同一篇文案；
5. 人工审核在账号安全和内容准确性上的作用。

结尾 CTA：<代码仓库链接>

## X / LinkedIn 草稿

Built an evidence-first AI product growth agent for Codex.

It discovers new AI products from public feeds, verifies launch and pricing claims against first-party sources, separates facts from analysis, and creates platform-specific promotion drafts.

No `OPENAI_API_KEY`. Publishing stays human-approved by default.

Try it: <repository link>

## 建议首发顺序

1. GitHub README 与 Pages 项目主页；
2. V2EX 分享创造；
3. 小红书；
4. 知乎长文；
5. X / LinkedIn；
6. 根据 UTM 点击与有效反馈调整下一轮内容。
