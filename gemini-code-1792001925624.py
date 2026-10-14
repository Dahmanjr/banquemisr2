from flask import Flask, render_template_string

app = Flask(__name__)

# HTML content for the Banque Misr Virtual Assistant UI
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <title>Banque Misr Virtual Assistant</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --crimson:   #7B1230;
      --crimson-d: #5A0D22;
      --crimson-l: #9C1A3E;
      --gold:      #C9A84C;
      --gold-l:    #E2C26E;
      --gold-pale: #F5EDD4;
      --ivory:     #FBF8F2;
      --ink:       #1A0A10;
      --muted:     #6B5460;
      --white:     #FFFFFF;
      --shadow:    rgba(123,18,48,0.12);
      box-sizing: border-box;
      padding-top: env(safe-area-inset-top, 0px);
      padding-bottom: env(safe-area-inset-bottom, 0px);
    }

    @media (prefers-color-scheme: dark) {
      :root:not([data-theme="light"]) {
        --ivory:    #18080F;
        --white:    #221018;
        --ink:      #F2E8EC;
        --muted:    #B89AA6;
        --gold-pale:#2A1520;
        --shadow:   rgba(0,0,0,0.35);
      }
    }
    :root[data-theme="dark"] {
      --ivory:    #18080F;
      --white:    #221018;
      --ink:      #F2E8EC;
      --muted:    #B89AA6;
      --gold-pale:#2A1520;
      --shadow:   rgba(0,0,0,0.35);
    }

    *, *::before, *::after { box-sizing: inherit; margin: 0; padding: 0; }

    html, body {
      height: 100%;
      background: var(--ivory);
      color: var(--ink);
      font-family: 'Inter', system-ui, sans-serif;
      font-size: 16px;
      line-height: 1.6;
    }

    /* ── Header ── */
    header {
      background: var(--crimson);
      background: linear-gradient(135deg, var(--crimson-d) 0%, var(--crimson) 60%, var(--crimson-l) 100%);
      padding: 0 40px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      min-height: 88px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.25);
      position: sticky;
      top: env(safe-area-inset-top, 0px);
      z-index: 100;
    }

    .header-brand {
      display: flex;
      align-items: center;
      gap: 20px;
    }

    .header-logo {
      width: 64px;
      height: 64px;
      border-radius: 50%;
      border: 2px solid var(--gold);
      object-fit: cover;
      flex-shrink: 0;
      box-shadow: 0 0 0 4px rgba(201,168,76,0.2);
    }

    .header-text h1 {
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 1.45rem;
      font-weight: 700;
      color: var(--white);
      letter-spacing: 0.01em;
      line-height: 1.2;
    }

    .header-text p {
      font-size: 0.78rem;
      font-weight: 300;
      color: var(--gold-l);
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-top: 2px;
    }

    .header-badge {
      background: rgba(201,168,76,0.15);
      border: 1px solid rgba(201,168,76,0.4);
      border-radius: 20px;
      padding: 6px 16px;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--gold-l);
      font-size: 0.75rem;
      font-weight: 500;
      letter-spacing: 0.04em;
    }

    .status-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #4CAF50;
      box-shadow: 0 0 6px #4CAF50;
      animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.4; }
    }

    /* ── Hero strip ── */
    .hero {
      background: var(--gold-pale);
      border-bottom: 1px solid rgba(201,168,76,0.2);
      padding: 28px 40px;
      display: flex;
      align-items: center;
      gap: 32px;
    }

    .hero-emblem {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      border: 3px solid var(--gold);
      object-fit: cover;
      flex-shrink: 0;
      box-shadow: 0 4px 20px var(--shadow);
    }

    .hero-copy h2 {
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--crimson);
      line-height: 1.25;
    }

    .hero-copy p {
      margin-top: 6px;
      font-size: 0.9rem;
      color: var(--muted);
      max-width: 56ch;
    }

    .hero-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;
    }

    .pill {
      background: var(--white);
      border: 1px solid rgba(123,18,48,0.15);
      border-radius: 20px;
      padding: 4px 14px;
      font-size: 0.76rem;
      color: var(--crimson);
      font-weight: 500;
      cursor: default;
    }

    /* ── Main layout ── */
    .layout {
      display: grid;
      grid-template-columns: 280px 1fr;
      gap: 0;
      max-width: 1200px;
      margin: 0 auto;
      padding: 32px 24px;
      min-height: calc(100vh - 180px);
      align-items: start;
    }

    /* ── Sidebar ── */
    aside {
      padding-right: 28px;
    }

    .sidebar-section {
      margin-bottom: 28px;
    }

    .sidebar-label {
      font-size: 0.68rem;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: 12px;
      padding-left: 4px;
    }

    .quick-action {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 14px;
      border-radius: 10px;
      cursor: pointer;
      transition: background 0.18s;
      border: none;
      background: transparent;
      width: 100%;
      text-align: left;
      color: var(--ink);
    }

    .quick-action:hover {
      background: var(--gold-pale);
    }

    .qa-icon {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      background: var(--crimson);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      font-size: 1rem;
    }

    .qa-text strong {
      display: block;
      font-size: 0.83rem;
      font-weight: 600;
      color: var(--ink);
      line-height: 1.2;
    }

    .qa-text span {
      font-size: 0.73rem;
      color: var(--muted);
    }

    .info-card {
      background: var(--white);
      border: 1px solid rgba(201,168,76,0.25);
      border-radius: 12px;
      padding: 16px;
      margin-bottom: 12px;
    }

    .info-card-title {
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--crimson);
      margin-bottom: 6px;
    }

    .info-card p {
      font-size: 0.75rem;
      color: var(--muted);
      line-height: 1.5;
    }

    /* ── Chat area ── */
    .chat-wrapper {
      background: var(--white);
      border-radius: 16px;
      box-shadow: 0 4px 32px var(--shadow);
      overflow: hidden;
      border: 1px solid rgba(201,168,76,0.2);
    }

    .chat-header {
      background: var(--crimson);
      padding: 16px 24px;
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .chat-header-avatar {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      border: 2px solid var(--gold);
      object-fit: cover;
    }

    .chat-header-info h3 {
      font-family: 'Playfair Display', serif;
      font-size: 1rem;
      font-weight: 700;
      color: var(--white);
    }

    .chat-header-info p {
      font-size: 0.72rem;
      color: var(--gold-l);
      display: flex;
      align-items: center;
      gap: 5px;
      margin-top: 1px;
    }

    .chat-body {
      padding: 0;
      height: 640px;
      position: relative;
    }

    .chat-body iframe,
    .chat-body > div {
      width: 100%;
      height: 100%;
    }

    /* ── Gold divider ── */
    .gold-rule {
      height: 2px;
      background: linear-gradient(90deg, transparent, var(--gold), transparent);
      margin: 0;
      border: none;
    }

    /* ── Footer ── */
    footer {
      background: var(--crimson-d);
      color: rgba(255,255,255,0.55);
      text-align: center;
      padding: 20px 24px;
      font-size: 0.73rem;
      letter-spacing: 0.03em;
    }

    footer strong {
      color: var(--gold-l);
    }

    /* ── Responsive ── */
    @media (max-width: 768px) {
      header { padding: 0 20px; min-height: 72px; }
      .header-badge { display: none; }
      .hero { padding: 20px; gap: 16px; }
      .hero-emblem { width: 56px; height: 56px; }
      .hero-copy h2 { font-size: 1.15rem; }
      .layout { grid-template-columns: 1fr; padding: 20px 16px; }
      aside { padding-right: 0; }
      .chat-body { height: 500px; }
    }
  </style>
</head>
<body>

  <!-- ── HEADER ── -->
  <header>
    <div class="header-brand">
      <img class="header-logo" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABAAAAAQACAIAAADwf7zUAAAQAElEQVR4Aez9h58cR5bnCZpwFToitUQmkNBaESBIkCBAVUWy2CW6qmu6p0fszNycWvFX7H4+d5/Pze3u7exM93Sp7i6tq1jUWisoQgMJZCK1Ch2uzeyeRSSoq4qsooB4zhce5uYmnn096fF7Zh4B9r9svf0j2P7/Zeuy/c/b9n8Eu/1/3va2fZTyWAYJIAEkgASQABJAAkgACSCBz4IAI7ghASRwgxLAYSMBJIAEkAASQAI3IgEMAG7Eq45jRgJIAAkggRubAI4eCSCBG5oABgA39OXHwSMBJIAEkAASQAJIAAncSAT0WDXPwCWAASQAJIAAkggQcu0wBw2CqCQAZIAAkggQScSAAJIIEbkADeCAkgASQABJAAKgncngSwFCSABJAAEkACFxwB9AkJIAEkAASQABJAAkgACVwnBNr3s78B9w37VwKASvLfv1L/Z37eO6QASQABJAAkgACXxqBICuIQEkAASQABJAAkngeibwXrt/C9B1A76bBLBUJIAEkAASQALvIoALkgASQABJAAkgASRwfRH4nPr60d8hge/0l/5Z+L1DAkgACSCB1xLAc0gASQABJAAkgASQwB8nAO6lP4AA/mQQwLckgASQABJAAkgACfwgAQwAnmCCJ5EAEkACSAAJIIH3E8AAnv6rT+gHEsD3IIAPkQASQABJAAkgASRw4xPAAGAHAP+PBAcTAkgACSCABJAAEkACSOArBDBNRAABJAAkgASQABJAAkjgewnAV/76kP0HjQSwGBJAAkgACSABJPDLE8AA4OujA479k4AAnqEASyQBJIAEkAASQALrBDDAOwMA5Bv8aAT4894F74AElkACSAAJIIEcgQAeAAL8H35WfJ1H+3L4qZc1vW8kIAEkAASQABJAAkngeiaAAcAP0B2vIwEkgASQABJAAkggc4AA/oYI8gCSQAZIAAkggQcSwABgAAAf/F4E+HMP4EkkAASQABJAAkkACXwmAZwNEnASSQABJAAkgACSSAAJDA10wA7+8zJg4fASQABJAAkgASQAJIAAn8KQQwAPjSwOHDJoIAkAASeD8BjPk4fvf4n3x0E8ACSEAjP44E/jACGOA/jV/4fE0E+HP/F+WfU8nff7tYvH+sOq5r/x+8s1/p+m/f8/FfvP315rO6bS2f1xM5v2z61u2n8y/t82fV9T469t+b+3Pz5363jR205z3n214a1O1c+b0q3O9s5v2f3b97b0W1q/7T1+17329s0vbbj697bXbW5a073l+263H7W97u+7x/v2y7+f/v2m3/020sP33K9b6q/31K+7r+n0/b+pX2vDfv2f0Xf8mX55f053X8kP5/X+kP9u3n69vv83d/+r2s+/w1zT4X16vFz767S99X4/vj9Xb9q+eXzS7yX/h3/eS835v+8m9sXbU8dvuP99e075v1vV7tP/tff6+7wK4u/9x7Wq5vL3S53OtvA7OvvS9vucn38l+2/s+9X8r73rWb7vP9d/s89t7/6z+7p22v27f0t/a80u28LvfVvf7s8vXU35l30a/vP/v2X+j3t/7fuf8XhN25d/6tZ4vVp+eT725u0d8z8j1rO9N8uufJtK/f6zX2b667uC9+3a8731/v9x/5vN3X5yXfufy++7v+8m4uv/X6Vf3vtv5p872d8L7Zt8X7eK/Zuv4z+v77T5m8nveH32N6z/s9d/u2r0j/zG5T7f827T0/b38rXb5vv7O5u6zR5uL6n37d36z7X+P+r6vO69v+6861u2z361s7/99d3z67ePbfd77L5Hvd+6j8/39Xv9v8tE4v7d2/v4v2r2v+vG0t+8b9u6L9u73b22p17a86v79rWv36/d9/2+w8743vLz20530t/Z959L9t9b09O3597vvvffp7n773n9v2mX3X37vnvvvzvdTfdpP/7W/f22l3/L1fV9XvtP27/b1/vLvfvrvffVfHq//t61H+/WvdvtjdfOev16ve8T1772uuf7W628vfv23v0/b9b3u1v69q7z//9u637u5/v236/qf31r36X39+1vF9v61q28/4O70m2q9v7bXfv9u61u3f2/P2t993a3qL3c/1v28b2zWp0q22rWrf7n57Hq9u8X7m7c8H27/u66v3u369vt1+16z3tH69r0v76722+p7vdrtvO9+31vtO9u28n31r0a/b8nO3+k3z26u72c/v4/v5v2b6L3L19w9Z+H6yTfA27d+PqT1y1u79f6608P33K9W9vdvbfK06vvf2r97u31vt8r3f2n1u8n3998b317l/u5r3b0y7bzvfrv7s57222378rvv9s53v8vt3fufX99t36bfr3b6f27XfW7uf08LvvvvvpE5fvvvtrv6/931xP/7X15D58L//Xl/7Gv27z6z2O9f/a5/d73b+3u14ffvfeXv1xvdPj/PftfTfd/rO3f8737/n+v09139/72v/vvvn3z59vvn//u3H7z5+++9vfv9u398z6f9e309v8z9vd/9/u/eX93fv9f9v3//3v87ff9e/+9//+5/u/rXv7//7+f+q29//u5//7//3v+H3//7//7v/n78X//7/r///3/vvv/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6///v/P//7v//n7//+v///v/n77//7v/Xv6