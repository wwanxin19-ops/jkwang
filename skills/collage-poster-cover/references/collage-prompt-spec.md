# Collage Poster/Cover Prompt Spec

## Core Goal

Generate a premium concept poster or cover with:

- hand-torn paper collage
- visual magazine cover feeling
- vintage print grain
- mixed materials
- strong title typography
- image metaphor
- deliberate casualness with balanced design order

The work should feel like an independent magazine cover, music poster, youth culture zine, retro film poster, art exhibition poster, or street poster wall. It should not feel like a normal template, PPT page, ecommerce banner, or generic social media cover.

## Input Handling

Expected inputs may include:

- `主题词 / 主标题`
- `副标题`
- `画幅比例`
- `语言`
- `用途`
- `可选补充语境`
- `可选情绪倾向`
- `可选禁用元素`

Do not force the user to fill a fixed form. Infer missing fields from context. If only a theme is supplied, create a complete visual direction from it.

## Theme Strategy

Choose the visual metaphor from the topic:

- **AI / knowledge / writing / method**: manuscripts, computer output, prompt slips, editor notes, search boxes, index cards, typewriters, folders, eyes, magnifiers, brain-like textures, clipped sentences. Avoid robot faces, cheap tech brains, blue-purple neon.
- **Growth / self / cognition / flow**: plants, stairs, old photos, back-view figures, diary scraps, mirrors, windows, light, torn paper layers, gradually revealed images.
- **Women / community / being seen**: feminine illustration, gauze, eyes, flowers, group photos, hands, curtains, soft fabric, stickers, handwriting, warm living scenes.
- **Web3 / finance / trading / risk**: charts, torn graphs, receipts, chips, trading screens, signal colors, warning labels, city fragments, financial paper, risk markers.
- **Social phenomenon / conflict / satire**: newspaper layers, portraits, warning slips, torn slogans, question marks, black-white photos, judgment-like labels, damaged edges.
- **City / travel / culture**: architecture, maps, tickets, postcards, road signs, retro photos, landmarks, handwritten place names, postmarks, travel stickers.
- **Visual poster vs plain text**: giant eye, magnifier, torn text layers, image breaking out from text, visual elements overpowering plain copy.
- **Tutorial / methodology**: manuals, step cards, path diagrams, clipped UI screenshots, arrows, numbered stickers, index cards. Keep it tactile, not an infographic template.

## Text Hierarchy

If the title is long, split into:

- **A layer**: giant visual title, usually 2-6 Chinese characters or 1-3 English words.
- **B layer**: complete title, kept legible as a medium title, paper strip, headline block, label, or information bar.
- **C layer**: subtitle, keywords, issue number, date, column name, English annotation, handwritten note, sticker text.

Rules:

- The A layer must be the first visual.
- The B layer must preserve the complete meaning.
- Keep provided proper nouns, handles, brands, people, events, and titles exact.
- English labels should be meaningful editorial system details, such as `ISSUE 001`, `VISUAL NOTES`, `FIELD REPORT`, `EDITORIAL FILE`, `CUT & PASTE`, `OBSERVATION`, `GUIDE`, `METHOD`, `SYSTEM`.
- Do not use random filler pseudo text.

## Collage DNA

Include several of these elements:

- irregular hand-torn edges
- layered paper scraps
- magazine photo fragments
- handwritten sticky notes
- printed labels
- tickets or receipts
- tape and stickers
- photocopy paper
- colored paper
- photo fragments
- doodle lines
- halftone dots
- risograph grain
- ink misregistration
- scan traces
- folds, glue shadows, paper fibers

The collage must have a clear center and readable title. Rich layers are good; noisy dumping is not.

## Composition Options

Pick one composition type that fits the theme:

- central burst collage: title centered, paper fragments radiate outward.
- magazine cover: large title + main image + information bar.
- horizontal tear: torn paper band crosses the frame.
- dossier/profile: central person or object surrounded by labels and notes.
- poster wall: layered street posters, overpaste, torn reveals.
- manual/file book: open handbook, archive folder, scrapbook spread.
- retro event poster: strong title, date/number, image fragments, offset print texture.

Layering order:

1. giant title as the structural skeleton
2. 1-3 image anchors
3. paper fragments and information labels
4. textured paper background

## Image/Text Fusion

Use at least one fusion method:

- text split by torn paper
- image peeking behind type
- object partly overlapping a title without hurting legibility
- title printed on a torn band
- small notes attached to the image edge
- image treated as magazine cutout or printed silhouette
- title repeated as photocopy/offset/overprint texture
- paper layers visibly cover each other
- tape, paper clips, or stickers as fixation devices

## Color Strategy

Generate palette from the theme, not from a default vintage look.

- **Red / black / white**: satire, conflict, risk, warning, hard opinion.
- **Orange / yellow / blue**: growth, knowledge, tutorial, lifestyle, city, travel.
- **Pink / yellow / blue**: women, community, AI life, creation, youth, relaxed energy.
- **Black/white/gray + one saturated accent**: serious opinion, social observation, long-form X cover.
- **Cream paper + collision stickers**: manual, methodology, guide, knowledge card.

Requirements:

- Use at least one strong memory color.
- Keep contrast high between background, paper, text, and image.
- Avoid all-low-saturation grayness.
- Avoid default old beige/black/red unless the topic justifies it.

## Texture Control

- Add paper grain, uneven ink, halftone, slight registration shift, scan marks, fold marks, and glue shadows.
- Texture must fade behind titles.
- Dark areas need layered detail, not dead black.
- Torn edges should be irregular and tactile, not clean rectangles.

## Strict Negatives

Avoid:

- clutter with no visual center
- all elements competing equally
- main title hidden or unreadable
- fake torn edges that look too neat
- ecommerce poster, PPT template, ordinary public-account cover
- pure big text without metaphor
- typo, misspelling, broken Chinese characters
- overly gray or weak color
- cheap messy punk without order
- AI robot face
- cheap cyberpunk neon
- unrelated doorway scenes
- stuffed explanatory paragraphs
- random pseudo text
- all-rectangular paper pieces
- no paper grain or handmade trace

## Final Prompt Checklist

Before calling image generation, the prompt should specify:

- aspect ratio and use case
- exact visible text
- main title hierarchy
- theme interpretation
- visual metaphor
- composition
- material/texture system
- palette
- typography behavior
- strict negative constraints
