import importlib.util, os, webbrowser

# Load zip-game.py despite the hyphen in its name
_spec = importlib.util.spec_from_file_location(
    "zip_game",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "zip-game.py"),
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

WALKABLE = _mod.WALKABLE
NUMBERS  = _mod.NUMBERS
solve    = _mod.solve

print("Solving...")
sol = solve()
total = len(sol)
print(f"Done - path length: {total}")

# ── Direction arrows ──────────────────────────────────────────────────────────
ARROW = {(1, 0): '&#x2193;',   # ↓
         (-1, 0): '&#x2191;',  # ↑
         (0, 1):  '&#x2192;',  # →
         (0, -1): '&#x2190;'}  # ←

idx_of = {cell: i for i, cell in enumerate(sol)}  # 0-based

# ── Build cell HTML ──────────────────────────────────────────────────────────
cells_html = []
for r in range(8):
    for c in range(8):
        cell = (r, c)
        num  = NUMBERS.get(cell)

        if cell not in WALKABLE:
            cells_html.append('<div class="cell wall"></div>')
            continue

        idx  = idx_of[cell]
        step = idx + 1

        # Gradient: cool blue (start) → warm amber (end)
        t   = idx / (total - 1)
        hue = int(210 - t * 170)          # 210 (blue) → 40 (amber)
        sat = 55 + int(t * 20)            # 55 % → 75 %
        lit = 24 + int(t * 14)            # 24 % → 38 %
        bg  = f"hsl({hue},{sat}%,{lit}%)"

        # Arrow pointing toward the NEXT cell in the path
        if idx < total - 1:
            nr, nc  = sol[idx + 1]
            arrow   = ARROW.get((nr - r, nc - c), '?')
        else:
            arrow = '&#x25CF;'  # ● end marker

        # Start marker overlay
        start_mark = '<span class="start-mark">START</span>' if idx == 0 else ''

        badge = f'<span class="badge">{num}</span>' if num else ''
        step_label = f'<span class="step-num">{step}</span>'

        cells_html.append(
            f'<div class="cell" style="background:{bg}" title="Step {step}">'
            f'<span class="arrow">{arrow}</span>'
            f'{step_label}'
            f'{badge}'
            f'{start_mark}'
            f'</div>'
        )

# ── HTML ─────────────────────────────────────────────────────────────────────
html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Zip 344 - Grid Visualizer</title>
<style>
  :root {
    --bg:   #0f0f1a;
    --wall: #0d0d18;
    --text: #e0e0e0;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Segoe UI', system-ui, sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1.4rem;
    padding: 2rem 1rem;
  }
  h1   { font-size: 1.8rem; letter-spacing: .12em; color: #e94560; }
  .sub { color: #556; font-size: .82rem; }

  /* ── Grid ── */
  .grid {
    display: grid;
    grid-template-columns: repeat(8, 68px);
    grid-template-rows:    repeat(8, 68px);
    gap: 4px;
  }

  .cell {
    border-radius: 8px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: default;
    transition: transform .12s, filter .12s;
  }
  .cell:hover { transform: scale(1.1); filter: brightness(1.3); z-index: 2; }
  .wall { background: var(--wall) !important; }

  /* Large centred direction arrow */
  .arrow {
    font-size: 26px;
    line-height: 1;
    color: rgba(255,255,255,.85);
    pointer-events: none;
  }

  /* Small step number — bottom-left */
  .step-num {
    position: absolute;
    bottom: 3px; left: 5px;
    font-size: 10px;
    font-weight: 700;
    color: rgba(255,255,255,.55);
    pointer-events: none;
  }

  /* Checkpoint badge — top-right corner */
  .badge {
    position: absolute;
    top: 3px; right: 5px;
    font-size: 13px;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 1px 3px rgba(0,0,0,.7);
    pointer-events: none;
  }

  /* START label — top-left */
  .start-mark {
    position: absolute;
    top: 3px; left: 4px;
    font-size: 7px;
    font-weight: 900;
    letter-spacing: .04em;
    color: rgba(255,255,255,.8);
    pointer-events: none;
  }

  /* ── Gradient legend bar ── */
  .legend-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: .35rem;
  }
  .grad-bar {
    width: 300px; height: 12px;
    border-radius: 6px;
    background: linear-gradient(to right,
      hsl(210,55%,24%), hsl(125,65%,28%), hsl(40,75%,38%));
  }
  .grad-labels {
    width: 300px;
    display: flex;
    justify-content: space-between;
    font-size: .75rem;
    color: #556;
  }

  /* ── Symbol legend ── */
  .sym-legend {
    display: flex; gap: 1.6rem;
    font-size: .78rem; color: #556;
    flex-wrap: wrap; justify-content: center;
  }
  .sym-legend span { display: flex; align-items: center; gap: .35rem; }
  .swatch { width: 13px; height: 13px; border-radius: 3px; }
</style>
</head>
<body>

<h1>ZIP 344</h1>
<p class="sub">
  Arrow = next step &nbsp;|&nbsp;
  small number = step index &nbsp;|&nbsp;
  bold corner = checkpoint &nbsp;|&nbsp;
  colour = progress (blue &rarr; amber)
</p>

<div class="grid">
""" + "\n".join(cells_html) + """
</div>

<div class="legend-wrap">
  <div class="grad-bar"></div>
  <div class="grad-labels"><span>Step 1 (start)</span><span>Step """ + str(total) + """ (end)</span></div>
</div>

<div class="sym-legend">
  <span>&#x2191;&#x2193;&#x2190;&#x2192; direction to next cell</span>
  <span>&#x25CF; end of path</span>
  <span><div class="swatch" style="background:#0d0d18"></div> wall</span>
</div>

</body>
</html>
"""

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grid_viz.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Saved: {out}")
webbrowser.open(f"file:///{out}")
