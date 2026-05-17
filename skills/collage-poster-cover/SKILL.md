---
name: collage-poster-cover
description: Use when the user wants to create or generate high-end collage-style cover/poster images, especially requests mentioning 剪贴画, 手撕纸, 撕纸拼贴, 杂志拼贴, 视觉杂志感, 复古印刷颗粒, independent magazine cover, X封面, 公众号封面, 海报图, 知识卡片, 活动海报, or image-2/image generation from a title, subtitle, theme, or article idea.
---

# Collage Poster Cover

## Overview

Use this skill to turn a user's theme/title into a premium editorial collage poster or cover image: torn paper, magazine layout, print grain, mixed materials, bold typography, image metaphor, and deliberate handmade imbalance with clear design order.

The output is normally a raster image. Use the built-in `image_gen` tool by default, and treat requests for `image-2` as a request to generate with the available image generation path unless the user explicitly asks for a CLI/API workflow.

## Workflow

1. Extract the real brief from the user's message:
   - title/theme, subtitle, language, use case, aspect ratio, mood, forbidden elements.
   - If the user leaves template placeholders unchanged, infer reasonable defaults from the rest of the message. Ask a question only when no theme/title can be inferred.
2. Choose the visual strategy from the theme, not from a fixed template. Use `references/collage-prompt-spec.md` when building or refining the prompt.
3. Preserve exact visible text:
   - Do not invent extra large text.
   - Keep all provided proper nouns, handles, brands, names, and event titles exact.
   - If the title is long, split into A/B/C text layers while preserving the complete title somewhere legible.
4. Build a generation prompt with:
   - exact visible text list,
   - aspect ratio and use case,
   - title hierarchy,
   - visual metaphor,
   - composition,
   - materials and print texture,
   - palette,
   - negative constraints.
5. Generate directly with `image_gen`.
6. If the user says not to explain, do not add analysis or commentary after the generation.

## Defaults

- X封面: `5:2`
- 公众号封面 or social cover: use the user-specified ratio; otherwise choose `3:4` or `4:5` for vertical feed covers.
- 海报: `3:4` or `4:5` unless specified.
- 知识卡片: `1:1` or `4:5` unless specified.
- Language: follow the user; use Chinese for core meaning and English only as editorial system labels when 中英混排 is requested.

## Prompt Rules

- Make the main title the first visual. It may be torn, offset, overprinted, or partially woven into imagery, but it must remain instantly readable.
- Prefer 1-3 strong image anchors over many unrelated scraps.
- Background texture must serve the text; weaken grain and clutter behind important words.
- Avoid defaulting to old newspaper style. Use newspaper/archive/red-label materials only when the theme is social conflict, satire, history, investigation, or critique.
- Avoid AI robot faces, cheap cyberpunk neon, ecommerce layouts, PPT templates, random pseudo text, and low-quality messy punk.

## Prompt Template

Use this shape, then adapt it to the user's actual theme:

```text
Create one premium conceptual collage poster/cover, [aspect ratio].

TEXT ACCURACY IS CRITICAL. Use only the following visible text, fully legible, no pseudo text, no typo:
- Main title, huge first visual: “[title or extracted core title]”
- Full title / secondary title: “[complete title if needed]”
- Subtitle: “[subtitle if provided]”
- Optional small editorial labels only if perfectly legible: “[short English labels]”

Theme: [one-sentence interpretation].
Visual metaphor: [image anchor and story].
Composition: [cover/banner/poster hierarchy, title placement, breathing space].
Materials: torn paper, tape, printed labels, scanned scraps, paper fibers, halftone dots, risograph/photocopy grain, slight ink misregistration, glue shadows.
Color palette: [theme-specific palette with one memory color].
Typography: [Chinese/English type behavior; legibility constraints].
Avoid: [forbidden elements plus generic negatives].
Final result: high-end editorial collage, tactile paper depth, clear title recognition, modern magazine order, strong visual impact.
```

## Reference

Read `references/collage-prompt-spec.md` when you need the full style system, theme mapping, text hierarchy, palette logic, or negative constraints.
