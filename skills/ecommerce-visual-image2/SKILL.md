---
name: ecommerce-visual-image2
description: Use when the user wants to turn product photos, product copy, selling points, or brief product information into high-quality e-commerce images with image-2. Covers main images, lifestyle scenes, A+ detail pages, infographics, JD/Tmall/Amazon-style product visuals, and multi-screen 9:16 vertical detail pages.
---

# E-Commerce Visual Image-2

Create professional e-commerce visuals from any combination of product images, product name, selling points, copy, platform requirements, and style notes. This skill is especially suited for JD/Tmall detail pages, main images, lifestyle scenes, A+ images, and product infographics.

## Non-Negotiables

- Use `image_gen` / image-2 for the actual image generation. If image-2 is unavailable, say so instead of silently switching to local-only layout, SVG, HTML, or another model.
- If the user says “停止”, “好了”, “不用继续”, or otherwise interrupts, stop generating immediately.
- Treat product images as strict product references unless the user explicitly asks for creative redesign.
- Preserve product identity: shape, color, packaging structure, logo placement, label hierarchy, and key visible claims.
- For Chinese packaging or dense label text, do not rely on the model to perfectly reproduce small text. Keep generated overlay text short, large, and simple; tell the user that fine product-label text should be checked.
- Default to a complete commercial set when the user asks for a detail page: 9-10 screens, 9:16 vertical, consistent style.

## Input Handling

Accept any of these:

- Product image only
- Product image plus copy/selling points
- Product information only
- Product name plus target platform
- Rough style direction such as “古风”, “科技感”, “高级黑金”, “母婴温柔风”

If key details are missing, infer conservatively:

- Product category from the image or text
- Likely use scenes
- Reasonable benefit hierarchy
- Platform-friendly dimensions
- Style palette from the product packaging

Ask a question only when the missing information would materially change the output, such as a regulated claim, exact ingredient, medical efficacy, or brand slogan.

## Default Output Strategy

For a 9-10 screen detail-page request:

1. Hero cover: premium first impression, product large, brand/product name prominent.
2. Clean main-image screen: white or light background, product centered, platform-safe.
3. Lifestyle scene: product in a plausible use/gifting/home/outdoor context.
4. Product detail screen: close-up panels for material, texture, package, accessories, or structure.
5. Core selling point screen: 2-4 key benefits, clear icons/cards.
6. Use scenario screen: real environment and target user context.
7. Process/quality screen: craft, technology, origin, formula, quality control, or construction.
8. Specification screen: product parameters and purchase confirmation details.
9. Trust/summary screen: suitable occasions, package contents, after-sales, or guarantees.
10. Closing conversion screen: product beauty shot plus concise final value proposition.

For smaller requests:

- Main image only: one clean product shot.
- Main image + A+ image: generate a white-background main image plus one structured infographic.
- Scene image only: focus on one natural use environment.
- Prompt-only request: output image-2 prompts without generating, if the user explicitly asks for prompts.

## Visual Direction Rules

- Make the image platform-ready: clear product, strong hierarchy, natural shadows, commercial polish.
- Keep copy concise: headline, subtitle, 2-4 feature labels, parameters where needed.
- Use product-tone palettes: match package color, material, audience, category, and price point.
- Avoid generic stock-ad clutter. Every prop must support use, scale, material, mood, or selling point.
- Use consistent visual system across multi-screen sets: palette, typography style, borders, icon language, lighting, and composition rhythm.
- For regulated products such as alcohol, supplements, cosmetics, baby products, medical devices, or finance-related products, avoid unsupported efficacy claims.

## Prompt Workflow

Before generating, mentally create a screen map:

- Product category
- Target platform and dimensions
- Required image count
- Visual style
- Copy hierarchy
- Feature hierarchy
- Risky claims to avoid

Then call `image_gen` once per distinct screen. Distinct screens need distinct prompts; do not ask for many different layouts in one prompt.

Each prompt should include:

- Use case: e-commerce image / JD detail page / A+ infographic
- Output size/aspect: 9:16 vertical when requested
- Product reference instruction
- Screen number and purpose
- Scene/background
- Product placement
- Lighting and material direction
- Exact short overlay text
- Constraints and avoid list

Use reference examples in `references/prompt-templates.md` when useful.

## Product Reference Language

When a product image is provided, include wording like:

```text
Use the provided product image as the strict visual reference. Preserve the product shape, proportions, packaging color, logo area, label hierarchy, material finish, and key visible details as much as possible.
```

For low-quality images:

```text
Improve the e-commerce presentation quality while keeping the product identity faithful to the reference. Clean lighting, sharper premium finish, natural shadows, commercial product photography.
```

For text-only inputs:

```text
Create a plausible premium product render based on the product information. Do not invent unsupported certifications, ingredients, claims, or brand marks.
```

## JD 9:16 Detail Page Defaults

Use these defaults unless the user overrides them:

- Aspect ratio: 9:16 vertical
- Recommended copy density: low to medium
- Style: premium commercial with clear product visibility
- Screen count: 10
- Include: main visual, white-background product view, scene view, A+ detail panels, feature infographic, specification screen
- Footer for alcohol: `理性饮酒 · 未成年人禁止饮酒`

## Quality Check

After generation, inspect whether:

- The product is recognizable and not redesigned beyond the request.
- Overlay text is readable and not misspelled.
- The image fits the requested aspect ratio.
- The visual style is consistent across screens.
- Claims are supported by user input or clearly phrased as visual/tasting/usage expression.
- No watermark, extra logo, random brand, broken UI, or unrelated object appears.

If a screen fails, regenerate only that screen with a targeted correction prompt.
