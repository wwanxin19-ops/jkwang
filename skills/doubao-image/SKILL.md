---
name: doubao-image
version: 1.0.0
description: "豆包文生图 API 调用封装。通过 Volcengine ARK API 生成图片，支持 text-to-image。当用户需要用中文描述生成图片、创意图、配图、封面图时使用此技能。"
metadata:
  requires:
    bins: ["curl"]
---

# 豆包文生图

调用豆包 Doubao Seedream 文生图模型，生成 2K 高质量图片。

## API 信息

- **端点**: `https://ark.cn-beijing.volces.com/api/v3/images/generations`
- **模型**: `doubao-seedream-4-5-251128`
- **认证**: Bearer Token（见下方配置）

## 配置

首次使用前，在 `.env` 或环境变量中设置 `DOUBAO_API_KEY`：

```bash
export DOUBAO_API_KEY="your-api-key"
```

## 调用方式

### 基础调用

```bash
curl -X POST "https://ark.cn-beijing.volces.com/api/v3/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DOUBAO_API_KEY}" \
  -d '{
    "model": "doubao-seedream-4-5-251128",
    "prompt": "<中文描述>",
    "response_format": "url",
    "size": "2K",
    "stream": false,
    "watermark": true
  }'
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prompt` | string | **必填** | 中文/英文图片描述，建议 50-500 字 |
| `size` | string | `"2K"` | 输出尺寸：`1K`/`2K`/`4K` 或具体如 `1024x1024` |
| `response_format` | string | `"url"` | 返回格式：`url`（在线URL）或 `b64_json`（Base64） |
| `watermark` | boolean | `true` | 是否添加水印 |
| `stream` | boolean | `false` | 是否流式返回 |

### 返回处理

响应为 JSON，图片 URL 在 `data[0].url` 字段：

```bash
# 提取图片 URL
curl -s -X POST ... | jq -r '.data[0].url'
```

## 完整示例

生成"星际穿越"风格封面图：

```bash
PROMPT="星际穿越，黑洞，黑洞里冲出一辆快支离破碎的复古列车，抢视觉冲击力，电影大片，末日既视感，动感，对比色，oc渲染，光线追踪，动态模糊，景深，超现实主义，深蓝，画面通过细腻的丰富的色彩层次塑造主体与场景，质感真实，暗黑风背景的光影效果营造出氛围，整体兼具艺术幻想感，夸张的广角透视效果，耀光，反射，极致的光影，强引力，吞噬"

curl -s -X POST "https://ark.cn-beijing.volces.com/api/v3/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DOUBAO_API_KEY}" \
  -d '{
    "model": "doubao-seedream-4-5-251128",
    "prompt": "'"${PROMPT}"'",
    "sequential_image_generation": "disabled",
    "response_format": "url",
    "size": "2K",
    "stream": false,
    "watermark": true
  }' | jq -r '.data[0].url'
```

## 脚本封装

推荐将调用封装为脚本：

```bash
#!/bin/bash
# scripts/doubao_image.sh

PROMPT="$1"
SIZE="${2:-2K}"
API_KEY="${DOUBAO_API_KEY:-$(cat ~/.config/doubao-api-key 2>/dev/null)}"

curl -s -X POST "https://ark.cn-beijing.volces.com/api/v3/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "doubao-seedream-4-5-251128",
    "prompt": "'"${PROMPT}"'",
    "response_format": "url",
    "size": "'"${SIZE}"'",
    "stream": false,
    "watermark": true
  }'
```

使用：`bash scripts/doubao_image.sh "你的描述" [尺寸]`
