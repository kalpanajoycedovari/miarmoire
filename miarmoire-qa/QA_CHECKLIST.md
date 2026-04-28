# 🪞 Mi Armoire — Image Generation QA Checklist
**Version 1.0 | Manual Review Guide**

---

## How to Use This Checklist

Run Mi Armoire with each test input from `test_prompts.py`. For every generated image, score each dimension 1–5. Record totals in the score sheet at the bottom. A score below 3 on any single dimension flags that output as a **fail**.

---

## Dimension Definitions

### 1. Prompt Adherence (1–5)
Does the image actually contain what the prompt asked for?

| Score | Meaning |
|-------|---------|
| 5 | All garments, colours, and accessories match exactly |
| 4 | Minor discrepancy — one item colour slightly off |
| 3 | 1–2 items missing or substituted |
| 2 | Significant mismatch — wrong garment types |
| 1 | Image bears no relation to the prompt |

**Check:** Open the image prompt (expandable in Mi Armoire). Compare each item listed to what's visible.

---

### 2. Visual Quality (1–5)
Is the image technically good?

| Score | Meaning |
|-------|---------|
| 5 | Sharp, clean, professional — no artifacts |
| 4 | Very minor softness or noise, non-distracting |
| 3 | Visible artifacts but the look is legible |
| 2 | Noticeable distortion — hands, face, or fabric warped |
| 1 | Unusable — broken anatomy, severe artifacts |

**Watch for:** distorted hands, merged fingers, strange facial geometry, fabric blending into background.

---

### 3. Fashion Coherence (1–5)
Does the outfit make sense as a real look?

| Score | Meaning |
|-------|---------|
| 5 | Cohesive, editorial-quality look — you'd see this in a magazine |
| 4 | Styled well, minor clashing |
| 3 | Passable but safe / uninspired |
| 2 | Items clash in colour or style — wouldn't be worn together |
| 1 | Incoherent — random garments with no logic |

**Check:** Does the colour palette work? Are the silhouettes balanced?

---

### 4. Occasion Fit (1–5)
Does the image match the stated occasion?

| Score | Meaning |
|-------|---------|
| 5 | Image perfectly reflects the occasion setting and mood |
| 4 | Mostly fitting — one element slightly off |
| 3 | Neutral, could work for multiple occasions |
| 2 | Wrong vibe — casual in a formal prompt or vice versa |
| 1 | Completely wrong context |

---

### 5. Body Awareness (1–5)
Did the image respect the height/weight input?

| Score | Meaning |
|-------|---------|
| 5 | Body proportions clearly informed by the input |
| 4 | Roughly appropriate |
| 3 | Generic body type — input ignored |
| 2 | Opposite to described body type |
| 1 | Inconsistent across looks in same session |

---

### 6. Consistency (1–5)
Across all 4 looks in one session, are outputs consistent in style?

| Score | Meaning |
|-------|---------|
| 5 | Same aesthetic, lighting, model type across all looks |
| 4 | Minor variation |
| 3 | Noticeable shifts in style/lighting between looks |
| 2 | Looks feel like different models / different shoots |
| 1 | No consistency at all |

*Score this once per session, not per image.*

---

## Score Sheet

Copy this table for each test run:

```
Test Input ID: ___________
Date/Time: _______________
HF Token used: Yes / No

| Look | Prompt Adherence | Visual Quality | Fashion Coherence | Occasion Fit | Body Awareness | Notes         |
|------|-----------------|----------------|-------------------|--------------|----------------|---------------|
| 01   |     /5          |     /5         |       /5          |     /5       |      /5        |               |
| 02   |     /5          |     /5         |       /5          |     /5       |      /5        |               |
| 03   |     /5          |     /5         |       /5          |     /5       |      /5        |               |
| 04   |     /5          |     /5         |       /5          |     /5       |      /5        |               |

Session Consistency: /5

Total Session Score: ____ / 105
Pass threshold: 70+
```

---

## Common Failure Patterns to Watch For

- **"Merged fabric" bug** — two garments blending into one texture (common in FLUX with layered outfits)
- **Jewellery disappears** — gold/silver accessories often drop from prompt; check explicitly
- **Generic body** — model always looks the same regardless of height/weight input
- **Occasion bleed** — "evening formal" looks identical to "casual weekend"
- **Prompt truncation** — very long item lists get cut off, last items don't appear