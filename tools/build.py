"""Build the class macro pages and the index hub from pages.py.

Usage: python3 -I tools/build.py   (writes into the folder above tools/)
"""
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pages import PAGES  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent.parent

THEMES = {
    "priest": dict(bg="#141922", panel="#1c2330", line="#2c3546", ink="#ece6d6", muted="#949cae",
                   accent="#d8b25c", accent_ink="#1a1406", glyph="✶",
                   tagline="Undercity-trained healer and shadow caster. Mouseover heals, focus dispels, and one key for every way out of crowd control."),
    "warlock": dict(bg="#16111c", panel="#201829", line="#33283f", ink="#e9e2ee", muted="#a095ae",
                    accent="#94d35a", accent_ink="#0f1a06", glyph="⛧",
                    tagline="Orgrimmar demon-binder. Every pet on one key, every curse on your focus, and Blood Fury that never sits idle."),
    "druid": dict(bg="#151811", panel="#1e2219", line="#323828", ink="#ece7d9", muted="#9fa290",
                  accent="#f08a2c", accent_ink="#1c0e02", glyph="❦",
                  tagline="Thunder Bluff shapeshifter. Shift out of roots without leaving form, heal your focus from bear, and War Stomp on demand."),
    "mage": dict(bg="#10152a", panel="#182039", line="#2a3556", ink="#e6ecf7", muted="#95a1bd",
                 accent="#6cc6f0", accent_ink="#04131c", glyph="✧",
                 tagline="Orgrimmar battle-mage. Sheep and counterspell your focus without losing your target, with Blood Fury riding every nuke."),
}

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} macros — WoW: Forever</title>
<style>
:root {{
  --bg: {bg}; --panel: {panel}; --line: {line}; --ink: {ink}; --muted: {muted};
  --accent: {accent}; --accent-ink: {accent_ink}; --warn: #e3a05b;
  --serif: "Iowan Old Style", "Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.55 var(--sans); }}
a {{ color: var(--accent); }}
:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
.wrap {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}

header.hero {{ padding: 56px 0 32px; border-bottom: 1px solid var(--line); }}
.hero .switch {{ font-size: 14px; color: var(--muted); }}
.hero h1 {{ font: 600 clamp(40px, 7vw, 76px)/1.02 var(--serif); margin: 12px 0 10px; letter-spacing: -0.01em; }}
.hero h1 .glyph {{ color: var(--accent); font-weight: 400; margin-right: 0.2em; }}
.hero p.lede {{ max-width: 62ch; color: var(--muted); font-size: 18px; margin: 0 0 28px; }}

.keys {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px; }}
.keys .k {{ display: flex; gap: 14px; align-items: center; }}
.cap {{ display: inline-block; min-width: 2.4em; padding: 0.15em 0.6em; border: 1px solid var(--line);
  border-bottom-width: 3px; border-radius: 6px; background: var(--panel); font: 600 0.85em var(--sans);
  text-align: center; white-space: nowrap; }}
.keys .cap {{ font-size: 20px; padding: 8px 14px; border-color: var(--accent); color: var(--accent); }}
.keys .k span:last-child {{ font-size: 15px; }}
.setup {{ margin: 26px 0 0; padding: 14px 18px; border-left: 3px solid var(--accent); background: var(--panel);
  max-width: 80ch; font-size: 15px; }}
code {{ font: 0.9em var(--mono); }}
.setup ul {{ margin: 6px 0 0; padding-left: 18px; }}

.bar {{ position: sticky; top: 0; z-index: 5; background: var(--bg); border-bottom: 1px solid var(--line); }}
.bar .wrap {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; padding-top: 12px; padding-bottom: 12px; }}
.bar input {{ flex: 1 1 220px; background: var(--panel); color: var(--ink); border: 1px solid var(--line);
  border-radius: 8px; padding: 9px 12px; font: inherit; }}
.bar button {{ background: transparent; color: var(--ink); border: 1px solid var(--line); border-radius: 999px;
  padding: 7px 14px; font: 500 14px var(--sans); cursor: pointer; }}
.bar button[aria-pressed="true"] {{ background: var(--accent); color: var(--accent-ink); border-color: var(--accent); }}
.bar nav {{ display: flex; flex-wrap: wrap; gap: 4px 14px; width: 100%; font-size: 14px; }}
.bar nav a {{ color: var(--muted); text-decoration: none; }}
.bar nav a:hover {{ color: var(--accent); }}

section {{ padding: 36px 0 8px; scroll-margin-top: 120px; }}
section h2 {{ font: 600 30px/1.2 var(--serif); margin: 0 0 18px; }}
section h2 small {{ font: 400 15px var(--sans); color: var(--muted); margin-left: 10px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 520px), 1fr)); gap: 18px; }}

article {{ background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 18px 20px;
  display: flex; flex-direction: column; gap: 10px; }}
article h3 {{ font: 600 20px/1.25 var(--serif); margin: 0; }}
.tags {{ display: flex; gap: 6px; flex-wrap: wrap; }}
.tag {{ font-size: 12px; padding: 1px 8px; border-radius: 999px; border: 1px solid var(--line); color: var(--muted); }}
.tag.pvp {{ color: #f0a5a5; border-color: #6b3a3a; }}
.tag.pve {{ color: #9fc4f0; border-color: #33506e; }}
.tag.talent {{ color: var(--accent); border-color: var(--accent); }}
article p {{ margin: 0; color: var(--muted); max-width: 70ch; }}
dl.mods {{ display: grid; grid-template-columns: max-content 1fr; gap: 6px 12px; margin: 2px 0; font-size: 14px; align-items: baseline; }}
dl.mods dt {{ margin: 0; }} dl.mods dd {{ margin: 0; }}
.code {{ position: relative; }}
pre {{ margin: 0; background: rgba(0,0,0,0.35); border: 1px solid var(--line); border-radius: 8px;
  padding: 14px 16px; font: 13.5px/1.6 var(--mono); white-space: pre-wrap; word-break: break-word; color: var(--ink); }}
.copy {{ position: absolute; top: 8px; right: 8px; background: var(--accent); color: var(--accent-ink); border: 0;
  border-radius: 6px; padding: 5px 12px; font: 600 13px var(--sans); cursor: pointer; }}
.foot {{ display: flex; justify-content: space-between; gap: 12px; font-size: 13px; color: var(--muted); flex-wrap: wrap; }}
.count.over {{ color: #ff7b7b; font-weight: 600; }}
.status.ok {{ color: var(--accent); }}
.status.verify {{ color: var(--warn); }}
.note {{ font-size: 14px; border-left: 3px solid var(--warn); padding: 6px 12px; color: var(--ink); background: rgba(227,160,91,0.08); }}
.note.info {{ border-left-color: var(--line); background: transparent; color: var(--muted); }}
footer {{ border-top: 1px solid var(--line); margin-top: 40px; padding: 24px 0 48px; color: var(--muted); font-size: 14px; }}
.empty {{ color: var(--muted); padding: 40px 0; }}
@media (prefers-reduced-motion: no-preference) {{ .copy {{ transition: transform .12s; }} .copy:active {{ transform: scale(.96); }} }}
</style>
</head>
<body>
<header class="hero">
  <div class="wrap">
    <div class="switch"><a href="index.html">All characters</a>. Also: {others}</div>
    <h1><span class="glyph" aria-hidden="true">{glyph}</span>{title}</h1>
    <p class="lede">{tagline}</p>
    <div class="keys" aria-label="Modifier conventions">
      <div class="k"><span class="cap">Click</span><span>Your target, or what's under your mouse</span></div>
      <div class="k"><span class="cap">Shift</span><span>Your focus target</span></div>
      <div class="k"><span class="cap">Alt</span><span>Yourself</span></div>
      <div class="k"><span class="cap">Ctrl</span><span>Alternate spell or an extra cooldown</span></div>
    </div>
    <div class="setup">
      Before you start:
      <ul>
        <li>Turn on the focus frame: Esc → Edit Mode → Focus Frame. Set focus with the <a href="#set-focus">Set focus</a> macro.</li>
        <li>Put your PvP trinket in the top trinket slot (13). Macros use the slot, so they keep working when you upgrade it.</li>
        <li>Paste into Esc → Macros, then pick the question-mark icon so the button shows the spell it will cast.</li>
        <li>Shortcuts: spell names have no abbreviations, but commands do. <code>/spell</code> is <code>/cast</code>, <code>/tar</code> is <code>/target</code>, <code>/a</code> is <code>/assist</code>, <code>/script</code> is <code>/run</code>. Use them when a macro is near 255 characters. <code>/cast !Shadowform</code> never toggles a form off, and <code>/use item:12345</code> uses an item by ID if its name changes.</li>
        <li>Spells and names are from the Forever beta (October 2026). Cards marked <em>check in-game</em> have one detail to confirm at launch.</li>
      </ul>
    </div>
  </div>
</header>
<div class="bar">
  <div class="wrap">
    <input id="q" type="search" placeholder="Search macros or spells" aria-label="Search macros">
    <button data-f="all" aria-pressed="true">All</button>
    <button data-f="PvP" aria-pressed="false">PvP</button>
    <button data-f="PvE" aria-pressed="false">PvE</button>
    <button data-f="verify" aria-pressed="false">Check in-game</button>
    <nav id="toc" aria-label="Sections"></nav>
  </div>
</div>
<main class="wrap" id="main"></main>
<footer><div class="wrap">Every macro is checked for the 255-character limit, valid commands and conditionals, and spell names from the Forever beta spellbook. Cards marked check in-game depend on something the beta hasn't settled.</div></footer>
<script type="application/json" id="macro-data">{data}</script>
<script>
(function () {{
  const data = JSON.parse(document.getElementById('macro-data').textContent);
  const main = document.getElementById('main');
  const toc = document.getElementById('toc');
  const el = (tag, cls, text) => {{ const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }};
  const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

  data.sections.forEach(name => {{
    const items = data.macros.filter(x => x.section === name);
    const sec = el('section'); sec.id = 's-' + slug(name);
    const h = el('h2', null, name); h.appendChild(el('small', null, items.length + (items.length === 1 ? ' macro' : ' macros')));
    sec.appendChild(h);
    const grid = el('div', 'grid');
    items.forEach(x => grid.appendChild(card(x)));
    sec.appendChild(grid); main.appendChild(sec);
    const a = el('a', null, name); a.href = '#' + sec.id; toc.appendChild(a);
  }});
  const empty = el('p', 'empty', 'No macros match. Clear the search or pick All.'); empty.hidden = true; main.appendChild(empty);

  function card(x) {{
    const c = el('article'); c.id = x.id;
    c.dataset.tags = x.tags.join(' ') + (x.status === 'verify' ? ' verify' : '');
    c.dataset.search = (x.title + ' ' + x.desc + ' ' + x.text).toLowerCase();
    c.appendChild(el('h3', null, x.title));
    const tags = el('div', 'tags'); x.tags.forEach(t => tags.appendChild(el('span', 'tag ' + t.toLowerCase(), t))); c.appendChild(tags);
    c.appendChild(el('p', null, x.desc));
    const dl = el('dl', 'mods');
    x.mods.forEach(([k, v]) => {{ const dt = el('dt'); dt.appendChild(el('span', 'cap', k)); dl.appendChild(dt); dl.appendChild(el('dd', null, v)); }});
    c.appendChild(dl);
    const wrap = el('div', 'code'); const pre = el('pre', null, x.text); wrap.appendChild(pre);
    const btn = el('button', 'copy', 'Copy'); btn.type = 'button'; btn.setAttribute('aria-label', 'Copy ' + x.title + ' macro');
    btn.addEventListener('click', () => copy(x.text, btn)); wrap.appendChild(btn); c.appendChild(wrap);
    if (x.note) c.appendChild(el('div', 'note' + (x.status === 'verify' ? '' : ' info'), x.note));
    const foot = el('div', 'foot');
    const n = x.text.length;
    foot.appendChild(el('span', 'count' + (n > 255 ? ' over' : ''), n + ' / 255 characters'));
    foot.appendChild(el('span', 'status ' + x.status, x.status === 'ok' ? 'Checked against the Forever spellbook' : 'Check in-game'));
    c.appendChild(foot);
    return c;
  }}

  function copy(text, btn) {{
    const done = () => {{ btn.textContent = 'Copied'; setTimeout(() => (btn.textContent = 'Copy'), 1400); }};
    if (navigator.clipboard && window.isSecureContext) {{ navigator.clipboard.writeText(text).then(done, fallback); }} else fallback();
    function fallback() {{
      const t = document.createElement('textarea'); t.value = text; document.body.appendChild(t); t.select();
      try {{ document.execCommand('copy'); done(); }} catch (e) {{ btn.textContent = 'Select the text and copy'; }}
      t.remove();
    }}
  }}

  let filter = 'all';
  const q = document.getElementById('q');
  document.querySelectorAll('.bar button').forEach(b => b.addEventListener('click', () => {{
    filter = b.dataset.f;
    document.querySelectorAll('.bar button').forEach(o => o.setAttribute('aria-pressed', String(o === b)));
    apply();
  }}));
  q.addEventListener('input', apply);
  function apply() {{
    const term = q.value.trim().toLowerCase(); let shown = 0;
    document.querySelectorAll('article').forEach(c => {{
      const ok = (filter === 'all' || c.dataset.tags.split(' ').includes(filter)) && (!term || c.dataset.search.includes(term));
      c.hidden = !ok; if (ok) shown++;
    }});
    document.querySelectorAll('section').forEach(s => {{ s.hidden = !s.querySelector('article:not([hidden])'); }});
    empty.hidden = shown > 0;
  }}
}})();
</script>
</body>
</html>
"""


def build(key):
    page = PAGES[key]
    payload = json.dumps({"sections": page["sections"], "macros": page["macros"]}, ensure_ascii=False, indent=1)
    payload = payload.replace("</", "<\\/")
    others = ", ".join(f'<a href="{p["file"]}">{html.escape(p["title"])}</a>' for k, p in PAGES.items() if k != key)
    out = TEMPLATE.format(title=html.escape(page["title"]), others=others, data=payload, **THEMES[key])
    (OUT / page["file"]).write_text(out, encoding="utf-8")
    print(f"wrote {OUT / page['file']} ({len(page['macros'])} macros)")


INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>WoW: Forever macros</title>
<style>
:root {{
  --bg: #13141a; --panel: #1b1d25; --line: #2c2f3b; --ink: #ece8df; --muted: #9a9cab; --accent: #e6d3a3;
  --serif: "Iowan Old Style", "Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.55 var(--sans); }}
:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 3px; }}
.wrap {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}
header {{ padding: 64px 0 36px; }}
h1 {{ font: 600 clamp(44px, 8vw, 88px)/1 var(--serif); margin: 0 0 14px; letter-spacing: -0.015em; }}
.lede {{ max-width: 60ch; color: var(--muted); font-size: 18px; margin: 0 0 30px; }}
.keys {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px; }}
.keys .k {{ display: flex; gap: 14px; align-items: center; }}
.cap {{ display: inline-block; min-width: 2.4em; padding: 8px 14px; border: 1px solid var(--accent); border-bottom-width: 3px;
  border-radius: 6px; background: var(--panel); color: var(--accent); font: 600 20px var(--sans); text-align: center; }}
.keys .k span:last-child {{ font-size: 15px; }}
.classes {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 520px), 1fr)); gap: 20px; padding: 20px 0 8px; }}
a.cls {{ display: flex; flex-direction: column; gap: 10px; padding: 26px 28px; border-radius: 12px; text-decoration: none;
  color: var(--c-ink); background: var(--c-bg); border: 1px solid var(--c-line); border-top: 4px solid var(--c-accent); }}
a.cls:hover {{ border-color: var(--c-accent); }}
a.cls h2 {{ font: 600 40px/1.05 var(--serif); margin: 0; }}
a.cls h2 .glyph {{ color: var(--c-accent); font-weight: 400; margin-right: 0.2em; }}
a.cls p {{ margin: 0; color: var(--c-muted); max-width: 60ch; }}
a.cls .stats {{ color: var(--c-ink); font-size: 15px; }}
a.cls .stats b {{ color: var(--c-accent); }}
a.cls ul {{ display: flex; flex-wrap: wrap; gap: 6px; list-style: none; margin: 4px 0 0; padding: 0; }}
a.cls li {{ font-size: 13px; padding: 2px 10px; border-radius: 999px; border: 1px solid var(--c-line); color: var(--c-muted); }}
a.cls .go {{ margin-top: auto; padding-top: 8px; color: var(--c-accent); font-weight: 600; }}
footer {{ border-top: 1px solid var(--line); margin-top: 40px; padding: 24px 0 48px; color: var(--muted); font-size: 14px; }}
footer p {{ max-width: 80ch; margin: 0 0 8px; }}
</style>
</head>
<body>
<header class="wrap">
  <h1>WoW: Forever macros</h1>
  <p class="lede">Copy-ready PvP and PvE macros for {count} characters, written for Forever's spellbook and checked against the 255-character limit. Every page uses the same keys, so your hands learn it once.</p>
  <div class="keys" aria-label="Modifier conventions">
    <div class="k"><span class="cap">Click</span><span>Your target, or what's under your mouse</span></div>
    <div class="k"><span class="cap">Shift</span><span>Your focus target</span></div>
    <div class="k"><span class="cap">Alt</span><span>Yourself</span></div>
    <div class="k"><span class="cap">Ctrl</span><span>Alternate spell or an extra cooldown</span></div>
  </div>
</header>
<main class="wrap classes">
{cards}
</main>
<footer><div class="wrap">
  <p>Spell names come from the Forever beta (October 2026). Macros marked check in-game depend on a detail the beta hasn't settled.</p>
  <p>Turn on the focus frame first: Esc → Edit Mode → Focus Frame.</p>
</div></footer>
</body>
</html>
"""

CARD = """<a class="cls" href="{file}" style="--c-bg:{panel};--c-line:{line};--c-ink:{ink};--c-muted:{muted};--c-accent:{accent}">
  <h2><span class="glyph" aria-hidden="true">{glyph}</span>{title}</h2>
  <p>{tagline}</p>
  <div class="stats"><b>{n}</b> macros, {v} to check in-game</div>
  <ul>{sections}</ul>
  <span class="go">Open {title} macros</span>
</a>"""


def build_index():
    cards = []
    for key, page in PAGES.items():
        t = THEMES[key]
        cards.append(CARD.format(
            file=page["file"], title=html.escape(page["title"]), n=len(page["macros"]),
            v=sum(x["status"] == "verify" for x in page["macros"]),
            sections="".join(f"<li>{html.escape(s)}</li>" for s in page["sections"]),
            **{k: t[k] for k in ("panel", "line", "ink", "muted", "accent", "glyph")},
            tagline=html.escape(t["tagline"])))
    (OUT / "index.html").write_text(INDEX.format(count=len(PAGES), cards="\n".join(cards)), encoding="utf-8")
    print(f"wrote {OUT / 'index.html'}")


if __name__ == "__main__":
    for k in PAGES:
        build(k)
    build_index()
