#!/bin/bash
# 豆包文生图调用脚本
# 用法: bash scripts/doubao_image.sh "<描述>" [尺寸]
# 环境变量: DOUBAO_API_KEY

set -e

PROMPT="${1:-}"
SIZE="${2:-2K}"

if [ -z "$PROMPT" ]; then
  echo "用法: doubao_image.sh <描述> [尺寸]" >&2
  exit 1
fi

API_KEY="${DOUBAO_API_KEY:-$(cat ~/.config/doubao-api-key 2>/dev/null)}"

if [ -z "$API_KEY" ]; then
  echo "错误: 未设置 DOUBAO_API_KEY 环境变量" >&2
  echo "请执行: export DOUBAO_API_KEY=你的API密钥" >&2
  exit 1
fi

RESPONSE=$(curl -s -X POST "https://ark.cn-beijing.volces.com/api/v3/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "doubao-seedream-4-5-251128",
    "prompt": "'"${PROMPT}"'",
    "sequential_image_generation": "disabled",
    "response_format": "url",
    "size": "'"${SIZE}"'",
    "stream": false,
    "watermark": true
  }')

# 提取 URL
echo "$RESPONSE" | jq -r '.data[0].url // .error.message // empty'
