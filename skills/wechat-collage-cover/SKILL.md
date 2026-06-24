---
name: wechat-collage-cover
description: >-
  Generate WeChat Official Account cover images in a premium editorial collage style: torn-paper collage, visual magazine cover, vintage print grain, mixed media layers, bold Chinese/English typography, and conceptual visual metaphors. Use when the user asks for 微信公众号封面图, 公众号封面, 封面海报, 剪贴画风格海报, 手撕拼贴, 视觉杂志感, retro editorial collage poster, or provides a style/title/subtitle/aspect ratio and wants an image generated with image_generate / GPT Image 2. Supports style direction, main title, subtitle, aspect ratio, language, context, mood, and forbidden elements.
---

# WeChat Editorial Collage Cover

Create a final WeChat Official Account cover image, not just a prompt. Default to `image_generate` with the current configured GPT Image 2 backend. If the tool does not expose explicit model selection, do not claim a different model; use the configured `image_generate` backend.

## Input Fields

Accept any of these fields from the user:

- `主题词 / 主标题` or `主标题`: required.
- `副标题`: optional.
- `尺寸`: default WeChat Official Account cover target size is **900×383 px**. Treat this as the final composition/crop target even when the generation tool only supports coarse aspect ratios.
- `画幅比例`: optional. Default for WeChat cover: approximately **900:383 ≈ 2.35:1**, mapped to `landscape` in `image_generate` unless the user explicitly gives another ratio. If the user gives 5:2, 3:2, 4:5, 1:1, or 3:4, map to the closest supported tool aspect ratio:
  - 5:2, 3:2, 900×383 → `landscape`
  - 4:5, 3:4 → `portrait`
  - 1:1 → `square`
- `安全区`: important title and face/object details should stay within the central safe area; avoid placing critical text at the extreme edges because WeChat may crop previews differently.
- `语言`: default `中英混排`.
- `用途`: default `微信公众号封面图`.
- `补充语境`: optional.
- `情绪倾向 / 风格`: optional; integrate into color and layout.
- `禁用元素`: optional; enforce explicitly.

If the user omits non-critical fields, proceed with defaults instead of asking. Ask only if the main title/theme is missing.

## Mandatory Visual Direction

Produce a premium concept poster with:

- hand-torn paper collage, irregular ripped edges, analog paper scraps
- visual magazine cover / independent zine / street poster energy
- vintage print grain, risograph texture, photocopy grain, halftone dots, slight misregistration, scan marks, folds, tape, labels, tickets, old newspaper textures
- strong title typography with clear hierarchy
- mixed-media layers that feel deliberately casual but compositionally balanced
- one clear visual center, not full-screen noise
- conceptual visual metaphor tied to the theme

Never make it look like an ecommerce banner, PPT template, generic tech poster, cheap cyberpunk neon, or random asset pile.

## Theme-to-Metaphor Selection

Before generating, silently infer the theme type and choose image anchors:

- AI / knowledge / writing / methods: manuscript, computer screen, prompt slips, editing marks, search box, index cards, typewriter, file folder, eye, magnifier, brain texture, cut-out sentences. Avoid robot faces and cheap blue-purple neon.
- Growth / self / cognition / flow: plants, stairs, old photos, back view, diary fragments, mirror, window, light, torn paper layers revealing images.
- Women / community / visibility: female illustration, gauze, eyes, flowers, hands, group photos, warm paper, stickers, handwritten notes, life scenes.
- Web3 / finance / trading / risk: charts, torn graphs, tickets, chips, trading UI, red/blue signals, warning labels, city fragments, financial newspaper.
- Social phenomenon / conflict / satire: old newspapers, portraits, red warning notes, torn slogans, questions, black-white photos, judgement labels, damaged edges.
- City / travel / culture: buildings, maps, tickets, postcards, road signs, vintage photos, landmarks, stamps, travel stickers.
- AI video / creative tools / media technology: 30-second filmstrip, timeline ruler, frame strips, editing interface fragments, camera aperture, motion blur frames, Seedance/AI video notes, prompt cards, countdown labels, video storyboard panels.

## Long Title Hierarchy

If the title is long, split into three layers:

1. **A-layer giant visual text**: extract the strongest 2–6 Chinese characters or 1–3 English words. This is the first visual read.
2. **B-layer full title**: preserve the complete user title in a readable mid-size title, paper strip, newspaper headline, label, or information bar.
3. **C-layer microcopy system**: subtitle, keywords, issue number, date, column name, English annotation, handwritten notes, stickers, arrows, stamps.

Rules:

- Main visual text must be eye-catching and readable.
- Full title must preserve the original meaning and avoid typos.
- Chinese/English mixing should feel editorial and natural.
- Do not let the title be obscured beyond recognition.
- Avoid repeating the same main title/name multiple times unnecessarily.

## Composition Options

Choose one composition that fits the title and aspect ratio:

- central explosive collage: giant title in center, paper scraps radiate outward
- magazine cover layout: huge title + hero image + information bars
- horizontal torn band: one ripped paper band cuts across the image
- dossier/archive collage: central object/person with labels and annotations
- street poster wall: layered posters, torn overlays, exposed underlayers
- scrapbook/ticket handbook: open manual, folder, tickets, index cards
- retro event poster: title + date/number + image fragments + offset print texture

Use 1–3 key visual image anchors only. Connect text and images physically: text on torn strips, image emerging behind text, tape fixing scraps, annotations around image edges, misprinted duplicated typography, paper layers overlapping.

## Color Strategy

Pick one bold but refined palette:

- red / black / white for conflict, viewpoint, warning, risk
- orange / yellow / blue for knowledge, tutorial, city, lifestyle
- pink / yellow / blue for youth, AI life, creation, community
- black / white / gray plus one saturated accent for serious analysis
- vintage cream paper plus high-contrast stickers for guides and knowledge cards
- for AI video and tech media: bright orange/yellow + electric blue + silver gray + black text, with clean modern contrast and vintage paper grain

Ensure at least one strong memory color. Avoid gray, dull, dirty, or low-contrast results.

## Image Prompt Template

When calling `image_generate`, produce a single detailed prompt in this structure:

```text
Create a premium editorial torn-paper collage poster for a WeChat Official Account cover.
Target final cover size: 900×383 px, ultra-wide WeChat cover composition, approximately 2.35:1. Keep all important title text and key visual anchors inside the central safe area for WeChat preview cropping.
Theme / full title: "{full_title}"
Subtitle: "{subtitle or none}"
Language: {language}
Use case: WeChat cover image.

Text hierarchy:
A-layer giant main visual text: "{2-6 char core phrase or 1-3 English words}", huge, bold, readable, high-impact.
B-layer complete title: "{full_title}", readable mid-size, placed as a newspaper headline / torn paper strip / editorial info bar.
C-layer micro typography: concise editorial notes such as ISSUE 001, VISUAL NOTES, FIELD REPORT, CUT & PASTE, date/number, keywords, handwritten annotations, short English labels relevant to the theme.

Visual metaphor and image anchors:
{specific anchors selected from theme, 1-3 key objects only}.

Style:
hand-torn paper collage, handmade magazine layout, independent zine aesthetic, vintage print texture, mixed media poster, ripped paper edges, layered paper scraps, risograph grain, photocopy grain, halftone dots, scanned magazine cutouts, analog collage, street poster design, strong bold typography, modern editorial balance.

Composition:
{chosen composition}. One clear visual center, rich layers but not chaotic. Text and images physically interact: paper tears cut through typography, image fragments emerge behind letters, tape and labels attach scraps, small annotations sit on image edges.

Materials:
irregular torn paper, old newspaper fragments, tech magazine scraps, filmstrip/timeline/storyboard fragments when relevant, tape, sticker labels, tickets, scan marks, folds, ink misregistration, subtle stains, tactile paper grain.

Color palette:
{chosen palette}. High contrast, premium, modern, bright enough for social feed stopping power.

Strict requirements:
No typos in Chinese or English. Keep the main title readable. No generic robot face. No cheap cyberpunk neon. No ecommerce banner style. No PPT template look. No random clutter. No large explanatory paragraphs. No rectangular-only paper pieces. Preserve a sophisticated editorial design order.
```

## Output Behavior

- If the user asks to generate directly, call `image_generate` immediately.
- Generate one image by default unless the current message explicitly asks for multiple.
- After successful generation, show only the generated image unless a blocker or important limitation must be reported.
- For WeChat cover, use the target size **900×383 px** as the design/crop standard; map it to `landscape` when using `image_generate` because the tool supports coarse aspect ratios only.
- Keep critical typography within the central safe area so the cover remains readable after WeChat preview cropping.
- All externally published visuals still require user confirmation before posting or publishing.
