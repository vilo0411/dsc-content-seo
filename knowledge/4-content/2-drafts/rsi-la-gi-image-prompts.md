# Image Prompts — rsi-la-gi
Generated: 2026-05-18
Style: abstract-finance

## Manifest
- featured-01: RSI oscillator line on dark navy       → đầu bài
- inline-01:   3-zone oscillator concept              → H2 "3 vùng đọc RSI"
- inline-02:   divergence split panel (price vs RSI)  → H2 "4 tín hiệu RSI thực chiến"

---

## featured-01

```
[BRAND] {
  name: DSC Securities (Chứng khoán DSC)
  tagline: Đồng Hành Cùng Thành Công
  audience: Vietnamese investors, age 25–45, urban, beginner to experienced traders
  voice: trustworthy, professional, approachable
  palette: {
    green:  #00AD14   primary accent
    bright: #2BE841   gradient start
    teal:   #10E7B3   gradient end
    navy:   #0D1B2A   dark bg
    white:  #FFFFFF   primary bg
  }
  gradient: { from: #2BE841, to: #10E7B3, direction: linear horizontal }
  mood: modern Vietnamese finance
  forbidden: [red, neon-outside-brand, competitor-colors, rainbow-gradients, glassmorphism]
}

[IMAGE] {
  type: featured
  size: 1200 × 630 px
  ratio: 16:9
  output: single image — no collage, no border, no frame
}

[STYLE: abstract-finance] {
  ref: Bloomberg Terminal dark + TradingView + Nikkei Asia data viz
  objects: {
    type: abstract chart elements — oscillating line, threshold bands
    weight: bold and readable — NOT decorative hairlines
    color: { primary: #00AD14, peak-gradient: #2BE841 → #10E7B3 }
  }
  bg: { color: #0D1B2A, overlay: dotted grid 5% opacity }
  lighting: { source: glow from chart lines — bioluminescent, direction: right side brighter }
  grain: 4–6% film
  decoration: [dashed threshold lines teal 20% opacity, faint trend arrow depth only]
  vibe: seasoned trader's screen — clinical, every element is data
}

[SCENE] {
  subject: RSI momentum oscillator — smooth flowing line between two threshold bands

  bg: { color: #0D1B2A, mood: deep analytical }

  fg: {
    element: single oscillating line sweeping left → right across full frame
    color:   #00AD14 solid, transitions #2BE841 → #10E7B3 at upper peak zone
    detail:  two thin dashed horizontal lines = threshold bands (teal 25% opacity)
  }

  accent: { element: soft green glow emanating from line on right side, max: 15% canvas }

  depth: faint candlestick silhouette at 8% opacity — background layer only

  composition: {
    focus:   oscillating line — center 60% of frame, enters lower-left → peaks upper-center → settles mid-right
    balance: asymmetric — left darker, right brighter
    space:   airy
  }

  mood: analytical, confident
  tone: cinematic editorial

  constraints: {
    no-text:    true
    no-faces:   true
    no-red:     true
    no-collage: true
  }
}

[NEGATIVE] {
  visual: [
    no watermarks or third-party logos,
    no clichés: handshakes / pointing-at-laptop / forced smiles,
    no red — market loss signal in VN trading culture,
    no competitor colors: SSI orange / VPS dark navy,
    no neon or electric outside DSC green family,
    no rainbow gradients / glassmorphism / crypto aesthetics,
    no blurry / pixelated / artifact-heavy output,
    no border or frame
  ]
  text: [no words / labels / captions / axis numbers, no placeholder text / URLs]
  culture: [no $ — use ₫ or omit]
}
```

---

## inline-01

```
[BRAND] {
  name: DSC Securities (Chứng khoán DSC)
  palette: {
    green:  #00AD14
    bright: #2BE841
    teal:   #10E7B3
    navy:   #0D1B2A
    white:  #FFFFFF
  }
  gradient: { from: #2BE841, to: #10E7B3, direction: linear horizontal }
  forbidden: [red, neon-outside-brand, competitor-colors, rainbow-gradients]
}

[IMAGE] {
  type: inline
  size: 800 × 450 px
  ratio: 16:9
  purpose: visual metaphor for section "3 vùng đọc RSI"
  output: single image — no collage, no border, no frame
}

[STYLE: abstract-finance] {
  ref: Bloomberg Terminal dark + TradingView + Nikkei Asia data viz
  objects: {
    type: oscillating line through 3 horizontal zone bands
    weight: bold and readable
    color: { base: #00AD14, upper-zone: #2BE841, lower-bounce: #10E7B3 }
  }
  bg: { color: #FFFFFF, overlay: none }
  lighting: { source: none — flat clinical clarity }
  grain: none
  decoration: [
    2 dashed zone boundary lines: navy 20% opacity,
    translucent zone fills: { upper: faint amber, middle: white, lower: faint teal }
  ]
  vibe: textbook clarity with brand polish
}

[SCENE] {
  subject: momentum oscillator divided into 3 reading zones

  bg: { color: #FFFFFF, mood: clean instructional }

  fg: {
    element: single smooth curved line oscillating full width left → right
    color:   #00AD14 base, #2BE841 at upper zone, #10E7B3 bouncing from lower zone
    detail:  dips low → rises high → settles middle — one complete oscillation
  }

  accent: { element: line color transitions at zone crossings, max: 15% canvas }

  depth: 2 dashed zone boundary lines (navy 20% opacity)

  composition: {
    focus:   oscillating line centered, full width
    balance: center — equal visual weight in all 3 zones
    space:   airy — generous white margin top and bottom
  }

  mood: calm, instructional
  tone: clean editorial

  constraints: {
    no-text:    true
    no-faces:   true
    no-red:     true
    no-collage: true
  }
}

[NEGATIVE] {
  visual: [
    no watermarks or third-party logos,
    no clichés,
    no red,
    no competitor colors,
    no neon outside DSC green family,
    no rainbow gradients / glassmorphism,
    no blurry or artifact-heavy output,
    no border or frame
  ]
  text: [no words / labels / axis numbers / captions, no placeholder text / URLs]
  culture: [no $ — use ₫ or omit]
}
```

---

## inline-02

```
[BRAND] {
  name: DSC Securities (Chứng khoán DSC)
  palette: {
    green:  #00AD14
    bright: #2BE841
    teal:   #10E7B3
    navy:   #0D1B2A
    white:  #FFFFFF
  }
  gradient: { from: #2BE841, to: #10E7B3, direction: linear horizontal }
  forbidden: [red, neon-outside-brand, competitor-colors, rainbow-gradients]
}

[IMAGE] {
  type: inline
  size: 800 × 450 px
  ratio: 16:9
  purpose: visual metaphor for section "RSI Divergence"
  output: single image — intentional 2-panel split top/bottom, no outer frame
}

[STYLE: abstract-finance] {
  ref: Bloomberg Terminal dark + TradingView + Nikkei Asia data viz
  objects: {
    type: two chart lines in split panels — ascending price vs descending oscillator
    weight: bold and readable
    color: { top-panel: #FFFFFF ascending, bottom-panel: #00AD14 → #10E7B3 descending }
  }
  bg: { color: #0D1B2A, overlay: none }
  lighting: { source: glow from chart lines }
  grain: 4–6% film
  decoration: [
    thin horizontal divider: teal 30% opacity between panels,
    faint directional arrows: { up: white 35% opacity, down: teal 35% opacity }
  ]
  vibe: two opposing forces — tension is the message
}

[SCENE] {
  subject: RSI divergence — price and momentum moving in opposite directions

  bg: { color: #0D1B2A, mood: dramatic analytical }

  fg: {
    element: split panel — top ascending price line / bottom descending oscillator
    color: {
      top:    #FFFFFF ascending left → right
      bottom: #00AD14 fading to #10E7B3 descending left → right
    }
    detail: thin teal divider 30% opacity separates panels
  }

  accent: { element: DSC green + teal gradient on bottom oscillator line, max: 15% canvas }

  depth: none — dark navy bg provides depth

  composition: {
    focus:   two equally weighted panels — neither dominates
    balance: split top/bottom symmetric
    space:   balanced — lines have breathing room in each panel
  }

  mood: analytical, alert
  tone: dramatic editorial

  constraints: {
    no-text:    true
    no-faces:   true
    no-red:     true
    no-collage: intentional 2-panel split only — no outer frame
  }
}

[NEGATIVE] {
  visual: [
    no watermarks or third-party logos,
    no clichés,
    no red,
    no competitor colors,
    no neon outside DSC green family,
    no rainbow gradients / glassmorphism / crypto aesthetics,
    no blurry or artifact-heavy output,
    no outer border or frame (inner divider is intentional)
  ]
  text: [no words / labels / axis numbers / captions, no placeholder text / URLs]
  culture: [no $ — use ₫ or omit]
}
```

---

## QA Checklist

- [ ] Không có text trong ảnh
- [ ] Màu xanh DSC #00AD14 xuất hiện tự nhiên
- [ ] Không có màu đỏ
- [ ] Ratio đúng: featured 16:9 / inline 16:9
- [ ] Không watermark, không logo lạ
- [ ] Tone khớp bài: analytical, trader-focused

Regen: `"Regenerate. Fix: [vấn đề]. Keep everything else identical."`
