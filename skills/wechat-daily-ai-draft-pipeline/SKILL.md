---
name: wechat-daily-ai-draft-pipeline
description: Use when the user asks to turn today's AI hot topic into a WeChat Official Account article, generate baoyu infographic-style inline illustrations, and upload the finished article to the WeChat draft box.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wechat, ai-topics, baoyu, infographic, draft-box, publishing]
    related_skills: [wechat-boom-content, wechat-baoyu-infographic-illustrations, baoyu-infographic, baoyu-social-publishing, baoyu-content-workflow]
---

# WeChat Daily AI Draft Pipeline

## Overview

这个 skill 封装“当天 AI 热点 → 公众号选题 → 爆款文章 → 信息图插图 → 微信草稿箱上传”的完整流程。

适合复用今天“豆包收费：免费 AI 时代真的结束了？”这类任务：先用实时来源确认热点，再用公众号爆款逻辑写文，用 baoyu 信息图风格生成正文插图，最后通过 WeChat API 上传到草稿箱。

核心原则：**内容能发、图片能看、草稿箱真实上传、有日志可查**。

---

## When to Use

当用户提出以下需求时使用：

- “采集今天 AI 热门话题，选 5 个公众号选题”
- “根据某个选题写一篇微信公众号文章”
- “用 baoyu skill 写公众号爆款文章”
- “用信息图版公众号插图 / baoyu 信息图 / 公众号文章插图 skill 生成插图”
- “生成 3-4 张正文信息图并上传草稿箱”
- “把文章上传到微信公众号草稿箱”
- “替换草稿箱文章里的某张图，重新上传新版草稿”

不要用于：

- 只需要普通聊天回答、不需要实时采集或上传的任务
- 只做单张封面、不写文章的任务
- 没有微信凭据且用户没有授权上传的场景；这种情况只生成 ready-to-upload 文件和 handoff 元数据

---

## Skill Stack

固定组合使用这些 baoyu/Hermes skills：

| 阶段 | Skill | 用途 |
|---|---|---|
| 热点采集与爆款文章 | `wechat-boom-content` | 今日热点、选题筛选、公众号文章结构和写作 |
| 正文信息图插图 | `wechat-baoyu-infographic-illustrations` | 用户偏好的信息图版正文插图工作流 |
| 信息图规范 | `baoyu-infographic` | `dense-modules` + `craft-handmade` 设计规范 |
| 微信上传 | `baoyu-social-publishing` | `md-to-wechat.ts`、`wechat-api.ts`、草稿箱上传 |
| 内容处理 | `baoyu-content-workflow` | Markdown/微信渲染、内容格式辅助 |

---

## Directory Pattern

为每篇文章创建独立目录：

```text
/home/lighthouse/.hermes/profiles/gzhao-agent/home/wechat-drafts/<topic-slug>-<YYYYMMDD>/
├── article.md                 # 初稿
├── article-v2.md              # 插图/排版修改版
├── article-v3.md              # 后续替换版
├── imgs/
│   ├── cover-*.png|jpg
│   ├── inline-v*-01-real-baoyu-infographic-*.jpg
│   ├── inline-v*-01-real-baoyu-infographic-*-4k-master.jpg
│   └── ...
├── prompts/
│   ├── 01-real-baoyu-infographic-*.md
│   └── ...
├── logs/
│   ├── check-permissions.log
│   ├── render-result.json
│   ├── upload.stderr
│   └── upload.stdout
└── .baoyu-skills/.env          # copied credentials, chmod 600, never printed
```

文件命名要求：

- 替换图片时必须使用**新的唯一文件名**，不要覆盖旧图。
- 正文信息图文件名建议包含：`inline-vN-XX-real-baoyu-infographic-<topic>-YYYYMMDD.jpg`。
- 4K master 只归档，不上传正文；正文上传图必须是 **1080×608**。

---

## Workflow

### 1. 实时采集今日 AI 热点

先确认当前时间：

```bash
date '+%Y-%m-%d %H:%M:%S %Z'
```

采集至少 3 个实时来源，优先：

- Hacker News
- GitHub Trending Today
- Product Hunt
- TechCrunch AI
- 机器之心
- 36氪 / IT之家 / 新浪科技财经 / 百度搜索结果中的新闻源

输出 5 个候选选题，每个包含：

- 话题名称
- 热度来源/信号
- 爆款潜力
- 核心洞察
- 公众号切入角度
- 3-4 个备选标题

如果来源超过 24-48 小时，必须标为“背景信息”，不能冒充“今日热点”。

### 2. 选择一个公众号主选题

优先选择：

- 国内读者有感知的产品/平台变化
- 有争议或价格/职业/效率相关的冲突点
- 能讲给普通人听，而不是只适合技术圈
- 能自然延展到“普通人怎么办”

示例：

```text
豆包收费：免费AI时代真的结束了？
```

### 3. 写公众号爆款文章

使用 `wechat-boom-content` 的写作框架：

- 标题有冲突感
- 开头 3 秒抓人
- 正文用“是什么 → 为什么 → 对普通人有什么影响 → 怎么办”
- 用通俗比喻解释 AI 术语
- 避免机械的一句话一段，保持手机端可读
- 结尾必须有评论区互动问题

文章 frontmatter 建议：

```yaml
---
title: "豆包开始收费，免费AI时代真的结束了？"
author: "jk铭点"
summary: "豆包专业版68元起，免费AI没有消失，但真正好用的AI正在开始明码标价。"
cover: "imgs/cover-xxx.png"
original: true
comments: true
---
```

### 4. 生成封面

封面可以用生成背景 + 本地中文标题叠加：

- 封面尺寸建议：`1600×900`
- 生图阶段不要让模型生成中文标题
- 中文标题必须用本地 CJK 字体叠加，例如 `Noto Sans CJK SC`
- 视觉风格：温暖、活泼、非技术、适合普通读者

封面需要 vision QA：标题是否正确、无错字、无伪文字、无水印。

### 5. 生成正文信息图插图

使用 `wechat-baoyu-infographic-illustrations` + `baoyu-infographic`：

固定要求：

```text
layout: dense-modules
style: craft-handmade
output: raster image
final target: 1080×608
archive master: 4K quality
```

每张图生成前，必须写 prompt 文件到 `prompts/`。

建议 3-4 张正文图：

1. 主题总览图
2. 核心变化图
3. 普通人决策图
4. 行业趋势/未来收费模式图

提示词原则：

- 中文短而准
- 1 个标题 + 1 个副标题 + 4-6 个模块
- 避免太多中文，防止乱码
- 不要 logo、水印、假 UI、赛博朋克、代码流
- 要求 `full-bleed / 内容铺满 / no side margins`，避免两侧留白

示例提示词片段：

```text
Use the baoyu-infographic specification exactly:
- layout: dense-modules
- style: craft-handmade
- output: raster image, not SVG, not HTML, not programmatic drawing
- final target: 1080×608, 16:9 horizontal WeChat article illustration
- archive master: 4K quality

IMPORTANT: FULL-BLEED content. Do not leave blank side margins.

Title: 豆包付费分层
Subtitle: 免费还在，效率收费
A 免费问答
B 68元起
C 复杂办公
D 重度任务
E 学生优惠
F 按需选择
Bottom: 不是全部收费，而是能力分层
```

### 6. 图片后处理与 QA

允许：

- resize 到 `1080×608`
- 生成 `4320×2432` 4K master
- JPEG 压缩
- 轻微 contain/crop/resize

不允许：

- 用本地 PIL/SVG/HTML 画一张图然后声称是 baoyu 信息图
- 给正文信息图本地叠加文字修乱码
- 覆盖旧文件名后直接上传

QA 要求：

- 每张生成图先用 `vision_analyze` 检查
- 最终上传版再检查一次
- 确认无明显错字、乱码、伪文字、裁切、边栏留白
- 第一张如果用户要求铺满，就用 full-bleed 生成，并直接 resize 到 1080×608，避免 contain 造成两侧留白

### 7. Patch 文章图片引用

文章正文只引用信息图正文图，不要把封面图插到正文。

检查 markdown 图片引用：

```regex
!\[[^\]]*\]\(([^)]+)\)
```

成功标准：

- 正文所有图片都是 `real-baoyu-infographic` 文件
- 没有 `images/cover.png`
- 没有旧版 `illustration-*.png`
- 替换图使用新 basename，如 `inline-v3-...jpg`

### 8. 微信渲染预检

运行：

```bash
bun /home/lighthouse/.hermes/profiles/gzhao-agent/skills/baoyu-skills/baoyu-social-publishing/scripts/md-to-wechat.ts article-vN.md \
  --theme grace \
  --color orange \
  > logs/render-vN-result.json \
  2> logs/render-vN-stderr.log
```

检查：

- `undefined: false`
- `NaN: false`
- `WBIMGPH_: false`
- `contentImages` 数量正确
- `contentImages` 指向最新图片 basename

### 9. 凭据处理：不要用 write_file 写 secret

Hermes 的 `write_file` 对敏感字段如 `WECHAT_APP_SECRET` 会脱敏/截断，这是系统级机制，不能关闭。

正确做法：

1. 不要让用户在正文里反复发送 secret。
2. 不要用 `write_file` 写 `.env` 里的 secret。
3. 复用已有成功上传目录中的 `.baoyu-skills/.env`。
4. 用 shell `cp` 复制文件到当前草稿目录。
5. `chmod 600 .baoyu-skills/.env`。
6. 上传时在子进程里读取 `.env`，注入 `process.env`，不打印值。

可查找位置：

```text
/home/lighthouse/.hermes/profiles/gzhao-agent/workspace/*/.baoyu-skills/.env
/home/lighthouse/.hermes/profiles/gzhao-agent/home/wechat-drafts/*/.baoyu-skills/.env
```

预检必须显示：

```text
✅ API credentials: Found in .../.baoyu-skills/.env
```

日志里只允许出现：

```text
Credentials source: process.env
```

不要输出 AppSecret、access_token 或完整 `.env` 内容。

### 10. 上传到微信公众号草稿箱

使用 `wechat-api.ts`，不要上传预转好的 HTML：

```bash
bun /home/lighthouse/.hermes/profiles/gzhao-agent/skills/baoyu-skills/baoyu-social-publishing/scripts/wechat-api.ts article-vN.md \
  --theme grace \
  --color orange \
  --title "标题" \
  --summary "摘要" \
  --author "jk铭点" \
  --cover imgs/cover-xxx.png \
  --no-cite
```

上传日志必须保存：

```text
logs/upload-vN.stdout
logs/upload-vN.stderr
logs/upload-vN.combined.log
```

成功标准：

```json
{
  "success": true,
  "media_id": "...",
  "title": "...",
  "articleType": "news",
  "method": "api"
}
```

### 11. 用户要求改图时

如果用户说：

- “第一张重生成”
- “两侧不要留边”
- “跟第三、四张一样铺满”
- “重新上传草稿箱”

执行：

1. 只重生指定图片
2. 用新文件名，如 `inline-v3-01-...full-bleed...jpg`
3. patch 出 `article-v3.md`
4. 跑 `md-to-wechat.ts` 预检
5. 直接上传新草稿
6. 回复最新 `media_id`，提醒旧草稿可能还在

---

## Reporting Format

最终回复保持简洁，避免重复长文。

推荐格式：

```markdown
已完成并上传新版草稿。

## 最新草稿箱 media_id

```text
...
```

## 最新封面 media_id

```text
...
```

## 本次更新

- 正文插图：4 张
- 尺寸：1080×608
- 风格：baoyu-infographic / craft-handmade / dense-modules
- 已替换第 1 张为满版无留边版本

## 预检结果

```text
contentImages: 4
undefined: false
NaN: false
WBIMGPH: false
upload: success
```

请以这版最新草稿为准，旧草稿可能仍在草稿箱里。
```

如需发送图片给用户，附：

```text
MEDIA:/absolute/path/to/image.jpg
```

---

## Common Pitfalls

1. **用 `write_file` 写 APP_SECRET。** 会触发脱敏/截断。应复制已有 `.env` 文件，或让用户通过安全渠道配置凭据。

2. **声明上传成功但没有 `media_id`。** 只有 `wechat-api.ts` 返回 `success: true` 和草稿 `media_id` 才算上传成功。

3. **正文图不是信息图。** 用户偏好是信息图版公众号插图，不要用普通卡通故事图替代。

4. **用本地绘图冒充 baoyu 信息图。** 不允许。必须走 raster image backend；本地处理只做尺寸/压缩/裁切。

5. **正文信息图中文太多。** 容易乱码。每张图短文案，4-6 模块即可。

6. **复用旧文件名。** 微信后台/缓存容易混淆。每次替换图都用新 basename。

7. **contain 造成两侧留白。** 如果用户要求铺满，直接 full-bleed prompt，并对最终图 resize 到 1080×608；不要 letterbox。

8. **上传 4K master 到正文。** 正文上传图必须是 1080×608，4K master 只归档。

9. **旧草稿仍在草稿箱。** 如果没有删除旧 media_id，回复时明确“请以最新 media_id 为准”。

---

## Verification Checklist

- [ ] 已确认当天日期时间
- [ ] 至少交叉参考 3 个实时来源
- [ ] 选题包含热度信号和公众号角度
- [ ] 文章 frontmatter 完整：title/author/summary/cover
- [ ] 作者为 `jk铭点`
- [ ] 封面已生成并 QA
- [ ] 每张正文信息图 prompt 已保存到 `prompts/`
- [ ] 正文信息图为 raster backend 生成
- [ ] 正文信息图风格为 `dense-modules + craft-handmade`
- [ ] 正文上传图为 1080×608
- [ ] 4K master 已归档
- [ ] Markdown 正文图片均为信息图，无封面图混入正文
- [ ] `md-to-wechat.ts` 预检无 `undefined`、`NaN`、`WBIMGPH_`
- [ ] `contentImages` 数量和文件名正确
- [ ] `.baoyu-skills/.env` 通过复制复用，未用 `write_file` 写 secret
- [ ] `check-permissions.ts` 显示 API credentials found
- [ ] `wechat-api.ts` 上传成功并返回草稿 `media_id`
- [ ] 回复用户最新草稿 `media_id`、封面 `media_id`、更新点和图片路径
