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
    "general": dict(bg="#13141a", panel="#1b1d25", line="#2c2f3b", ink="#ece8df", muted="#9a9cab",
                    accent="#e6d3a3", accent_ink="#1a1408", glyph="❖",
                    tagline="Focus, markers, mounts, trinkets and interface toggles that every character can use. Put these in the account-wide General tab."),
    "warrior": dict(bg="#18130f", panel="#221b15", line="#3a2f25", ink="#eee5da", muted="#a8998a",
                    accent="#d4a574", accent_ink="#1f1206", glyph="⚔",
                    tagline="Stance-aware buttons: Charge or Intercept, Pummel or Shield Bash, and Heroic Strike queued on top of every attack."),
    "paladin": dict(bg="#1a1217", panel="#251a21", line="#3d2b36", ink="#f1e6ec", muted="#ad97a4",
                    accent="#f29cc3", accent_ink="#2a0b19", glyph="✠",
                    tagline="New for the Forsaken in Forever. Mouseover heals, blessings on your focus, and Judgement with an instant reseal."),
    "hunter": dict(bg="#121610", panel="#1a2017", line="#2d3726", ink="#e8eedf", muted="#9aa58e",
                   accent="#b2d67a", accent_ink="#142007", glyph="➶",
                   tagline="Shots that keep Auto Shot running, traps at your feet, and one button that keeps your pet alive."),
    "rogue": dict(bg="#17160e", panel="#211f14", line="#38351f", ink="#efedd9", muted="#a9a586",
                  accent="#f2e66a", accent_ink="#1f1c03", glyph="☾",
                  tagline="Stealth openers that won't break stealth, kicks and blinds on your focus, and poisons in two clicks."),
    "priest": dict(bg="#141922", panel="#1c2330", line="#2c3546", ink="#ece6d6", muted="#949cae",
                   accent="#d8b25c", accent_ink="#1a1406", glyph="✶",
                   tagline="Mouseover heals, focus dispels and silences, with Undead and Troll racial spells in their own groups."),
    "shaman": dict(bg="#0e1524", panel="#152035", line="#24344f", ink="#e3ebf6", muted="#8fa0bb",
                   accent="#4fa3ef", accent_ink="#03111f", glyph="ϟ",
                   tagline="Totems by element on one key each, Forever's new totem sets, and Earth Shock interrupts on your focus."),
    "mage": dict(bg="#10152a", panel="#182039", line="#2a3556", ink="#e6ecf7", muted="#95a1bd",
                 accent="#6cc6f0", accent_ink="#04131c", glyph="✧",
                 tagline="Sheep and counterspell your focus without losing your target. Orc and Troll mages get their racials on every nuke."),
    "warlock": dict(bg="#16111c", panel="#201829", line="#33283f", ink="#e9e2ee", muted="#a095ae",
                    accent="#94d35a", accent_ink="#0f1a06", glyph="⛧",
                    tagline="Every pet on one key, every curse on your focus, and sacrifice-and-resummon buttons."),
    "druid": dict(bg="#151811", panel="#1e2219", line="#323828", ink="#ece7d9", muted="#9fa290",
                  accent="#f08a2c", accent_ink="#1c0e02", glyph="❦",
                  tagline="Powershift out of roots, heal your focus from any form, and War Stomp on demand."),
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
[hidden] {{ display: none !important; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.55 var(--sans); }}
a {{ color: var(--accent); }}
code {{ font: 0.9em var(--mono); }}
:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
.wrap {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}

header.hero {{ padding: 56px 0 32px; border-bottom: 1px solid var(--line); }}
.hero .switch {{ font-size: 14px; color: var(--muted); }}
.hero h1 {{ font: 600 clamp(40px, 7vw, 76px)/1.02 var(--serif); margin: 12px 0 6px; letter-spacing: -0.01em; }}
.hero h1 .glyph {{ color: var(--accent); font-weight: 400; margin-right: 0.2em; }}
.hero .races {{ color: var(--accent); font-size: 16px; margin: 0 0 10px; }}
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
.setup ul {{ margin: 6px 0 0; padding-left: 18px; }}

.bar {{ position: sticky; top: 0; z-index: 5; background: var(--bg); border-bottom: 1px solid var(--line); }}
.bar .wrap {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; padding-top: 12px; padding-bottom: 12px; }}
.bar input[type=search] {{ flex: 1 1 220px; background: var(--panel); color: var(--ink); border: 1px solid var(--line);
  border-radius: 8px; padding: 9px 12px; font: inherit; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }}
.chips .lbl {{ font-size: 13px; color: var(--muted); margin-right: 2px; }}
.bar button {{ background: transparent; color: var(--ink); border: 1px solid var(--line); border-radius: 999px;
  padding: 7px 14px; font: 500 14px var(--sans); cursor: pointer; }}
.bar button[aria-pressed="true"] {{ background: var(--accent); color: var(--accent-ink); border-color: var(--accent); }}
.bar nav {{ display: flex; flex-wrap: wrap; gap: 4px 14px; width: 100%; font-size: 14px; }}
.bar nav a {{ color: var(--muted); text-decoration: none; }}
.bar nav a:hover {{ color: var(--accent); }}

.dl {{ margin: 28px 0 0; background: var(--panel); border: 1px solid var(--line); border-radius: 10px; }}
.dl summary {{ cursor: pointer; padding: 16px 20px; font: 600 20px var(--serif); }}
.dl summary small {{ font: 400 14px var(--sans); color: var(--muted); margin-left: 8px; }}
.dl .body {{ padding: 0 20px 20px; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 28px; }}
.dl fieldset {{ border: 0; padding: 0; margin: 0 0 14px; }}
.dl legend {{ font-weight: 600; margin-bottom: 6px; }}
.dl label {{ display: block; margin: 4px 0; }}
.dl .hint {{ color: var(--muted); font-size: 14px; margin: 2px 0 0 24px; }}
.dl .row {{ display: flex; gap: 10px; flex-wrap: wrap; margin: 12px 0; }}
.dl button {{ background: var(--accent); color: var(--accent-ink); border: 0; border-radius: 8px; padding: 10px 16px;
  font: 600 15px var(--sans); cursor: pointer; }}
.dl button.ghost {{ background: transparent; color: var(--ink); border: 1px solid var(--line); }}
.dl ol {{ margin: 0; padding-left: 20px; font-size: 15px; }}
.dl ol li {{ margin-bottom: 8px; }}
#dl-status {{ font-size: 14px; margin: 8px 0 0; white-space: pre-line; }}
#dl-status.warn {{ color: var(--warn); }}
@media (max-width: 760px) {{ .dl .body {{ grid-template-columns: 1fr; }} }}

section {{ padding: 36px 0 8px; scroll-margin-top: 140px; }}
section h2 {{ font: 600 30px/1.2 var(--serif); margin: 0 0 18px; }}
section h2 small, .race-group h3 small {{ font: 400 15px var(--sans); color: var(--muted); margin-left: 10px; }}
.race-group {{ margin: 0 0 26px; }}
.race-group h3 {{ font: 600 22px var(--serif); color: var(--accent); margin: 0 0 12px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 520px), 1fr)); gap: 18px; }}

article {{ background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 18px 20px;
  display: flex; flex-direction: column; gap: 10px; }}
article h3 {{ font: 600 20px/1.25 var(--serif); margin: 0; }}
.tags {{ display: flex; gap: 6px; flex-wrap: wrap; }}
.tag {{ font-size: 12px; padding: 1px 8px; border-radius: 999px; border: 1px solid var(--line); color: var(--muted); }}
.tag.pvp {{ color: #f0a5a5; border-color: #6b3a3a; }}
.tag.pve {{ color: #9fc4f0; border-color: #33506e; }}
.tag.talent, .tag.race {{ color: var(--accent); border-color: var(--accent); }}
article p {{ margin: 0; color: var(--muted); max-width: 70ch; }}
dl.mods {{ display: grid; grid-template-columns: max-content 1fr; gap: 6px 12px; margin: 2px 0; font-size: 14px; align-items: baseline; }}
dl.mods dt {{ margin: 0; }} dl.mods dd {{ margin: 0; }}
.code {{ position: relative; }}
pre {{ margin: 0; background: rgba(0,0,0,0.35); border: 1px solid var(--line); border-radius: 8px;
  padding: 14px 16px; font: 13.5px/1.6 var(--mono); white-space: pre-wrap; word-break: break-word; color: var(--ink); }}
.copy {{ position: absolute; top: 8px; right: 8px; background: var(--accent); color: var(--accent-ink); border: 0;
  border-radius: 6px; padding: 5px 12px; font: 600 13px var(--sans); cursor: pointer; }}
.foot {{ display: flex; justify-content: space-between; gap: 6px 12px; font-size: 13px; color: var(--muted); flex-wrap: wrap; }}
.foot label {{ color: var(--ink); cursor: pointer; }}
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
    <div class="switch"><a href="index.html">All pages</a>. Also: {others}</div>
    <h1><span class="glyph" aria-hidden="true">{glyph}</span>{title}</h1>
    {races_line}
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
        <li>Turn on the focus frame: Esc → Edit Mode → Focus Frame. Set focus with the <a href="general.html#set-focus">Set focus</a> macro.</li>
        <li>Put your PvP trinket in the top trinket slot (13). Macros use the slot, so they keep working when you upgrade it.</li>
        <li>Copy single macros into Esc → Macros, or download a whole set as a macro file below. Pick the question-mark icon so the button shows the spell it will cast.</li>
        <li>Shortcuts: spell names have no abbreviations, but commands do. <code>/spell</code> is <code>/cast</code>, <code>/tar</code> is <code>/target</code>, <code>/a</code> is <code>/assist</code>, <code>/script</code> is <code>/run</code>. <code>/cast !Shadowform</code> never toggles a form off, and <code>/use item:12345</code> uses an item by ID if its name changes.</li>
        <li>Spells and names are from the Forever beta (October 2026). Cards marked <em>check in-game</em> have one detail to confirm at launch.</li>
      </ul>
    </div>
    <details class="dl" id="download">
      <summary>Download as a WoW macro file <small id="dl-count"></small></summary>
      <div class="body">
        <div>
          <fieldset>
            <legend>Where should these macros go?</legend>
            <label><input type="radio" name="scope" value="character" checked> This character only</label>
            <p class="hint">The per-character tab. Classic clients allow 18 here; Forever's limit isn't confirmed.</p>
            <label><input type="radio" name="scope" value="account"> All characters (General tab)</label>
            <p class="hint">The account-wide tab, up to 120 macros, shared by every character.</p>
          </fieldset>
          <fieldset>
            <legend>Keep your existing macros (optional)</legend>
            <label>Your current macros-cache.txt: <input type="file" id="merge" accept=".txt,text/plain"></label>
            <p class="hint">Pick the file you're replacing and the download keeps everything in it, adding these macros after. Without it, the download replaces all macros in that tab.</p>
          </fieldset>
          <p>Only macros that are showing and ticked are included. Use the race and PvP/PvE filters above, or untick cards you don't want.</p>
          <div class="row">
            <button type="button" id="dl-go">Download macros-cache.txt</button>
            <button type="button" class="ghost" id="sel-all">Tick all</button>
            <button type="button" class="ghost" id="sel-none">Untick all</button>
          </div>
          <p id="dl-status" role="status"></p>
        </div>
        <div>
          <strong>Install the file</strong>
          <ol>
            <li>In game, type <code>/console synchronizeMacros 0</code>. Otherwise Blizzard's server copy of your macros can overwrite the file when you log in. Then exit WoW completely.</li>
            <li>Open your Forever game folder (in the beta it's <code>_classic_beta_</code>):<br>
              Windows: <code>C:\\Program Files (x86)\\World of Warcraft\\_classic_beta_\\</code><br>
              Mac: <code>/Applications/World of Warcraft/_classic_beta_/</code></li>
            <li>Go to <code>WTF/Account/&lt;your account&gt;/</code>. For <em>All characters</em>, the file goes right there. For <em>This character only</em>, go on into <code>&lt;Realm&gt;/&lt;Character&gt;/</code>. The folders appear after you've logged in once.</li>
            <li>Rename the old <code>macros-cache.txt</code> to <code>macros-cache.bak</code> as a backup, then copy the downloaded file in.</li>
            <li>Start WoW and type <code>/macro</code> to check they're there. Drag them onto your bars. You can turn sync back on with <code>/console synchronizeMacros 1</code>.</li>
          </ol>
        </div>
      </div>
    </details>
  </div>
</header>
<div class="bar">
  <div class="wrap">
    <input id="q" type="search" placeholder="Search macros or spells" aria-label="Search macros">
    <div class="chips" id="tag-chips">
      <button data-f="all" aria-pressed="true">All</button>
      <button data-f="PvP" aria-pressed="false">PvP</button>
      <button data-f="PvE" aria-pressed="false">PvE</button>
      <button data-f="verify" aria-pressed="false">Check in-game</button>
    </div>
    <div class="chips" id="race-chips" hidden><span class="lbl">Race</span></div>
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
  const plural = n => n + (n === 1 ? ' macro' : ' macros');
  const ticked = new Set(data.macros.map(x => x.id));
  const cards = new Map();

  data.sections.forEach(name => {{
    const items = data.macros.filter(x => x.section === name);
    const sec = el('section'); sec.id = 's-' + slug(name);
    const h = el('h2', null, name); const small = el('small'); h.appendChild(small); sec.appendChild(h);
    sec._count = small;
    if (name === 'Racials') {{
      data.races.forEach(race => {{
        const group = items.filter(x => x.race === race); if (!group.length) return;
        const wrap = el('div', 'race-group'); wrap.dataset.race = race;
        const gh = el('h3', null, race); const gs = el('small'); gh.appendChild(gs); wrap._count = gs; wrap.appendChild(gh);
        const grid = el('div', 'grid'); group.forEach(x => grid.appendChild(card(x))); wrap.appendChild(grid); sec.appendChild(wrap);
      }});
    }} else {{
      const grid = el('div', 'grid'); items.forEach(x => grid.appendChild(card(x))); sec.appendChild(grid);
    }}
    main.appendChild(sec);
    const a = el('a', null, name); a.href = '#' + sec.id; toc.appendChild(a);
  }});
  const empty = el('p', 'empty', 'No macros match. Clear the search or pick All.'); empty.hidden = true; main.appendChild(empty);

  function card(x) {{
    const c = el('article'); c.id = x.id; cards.set(x.id, c);
    c.dataset.tags = x.tags.join(' ') + (x.status === 'verify' ? ' verify' : '');
    c.dataset.race = x.race || '';
    c.dataset.search = (x.title + ' ' + x.desc + ' ' + x.text + ' ' + (x.race || '')).toLowerCase();
    c.appendChild(el('h3', null, x.title));
    const tags = el('div', 'tags');
    if (x.race) tags.appendChild(el('span', 'tag race', x.race));
    x.tags.forEach(t => tags.appendChild(el('span', 'tag ' + t.toLowerCase(), t))); c.appendChild(tags);
    c.appendChild(el('p', null, x.desc));
    const dl = el('dl', 'mods');
    x.mods.forEach(([k, v]) => {{ const dt = el('dt'); dt.appendChild(el('span', 'cap', k)); dl.appendChild(dt); dl.appendChild(el('dd', null, v)); }});
    c.appendChild(dl);
    const wrap = el('div', 'code'); wrap.appendChild(el('pre', null, x.text));
    const btn = el('button', 'copy', 'Copy'); btn.type = 'button'; btn.setAttribute('aria-label', 'Copy ' + x.title + ' macro');
    btn.addEventListener('click', () => copy(x.text, btn)); wrap.appendChild(btn); c.appendChild(wrap);
    if (x.note) c.appendChild(el('div', 'note' + (x.status === 'verify' ? '' : ' info'), x.note));
    const foot = el('div', 'foot');
    const n = x.text.length;
    foot.appendChild(el('span', 'count' + (n > 255 ? ' over' : ''), n + ' / 255 characters'));
    foot.appendChild(el('span', 'status ' + x.status, x.status === 'ok' ? 'Checked against the Forever spellbook' : 'Check in-game'));
    const lab = el('label'); const box = el('input'); box.type = 'checkbox'; box.checked = true;
    box.addEventListener('change', () => {{ box.checked ? ticked.add(x.id) : ticked.delete(x.id); updateCount(); }});
    c._box = box; lab.appendChild(box); lab.appendChild(document.createTextNode(' Include in download as "' + x.name + '"'));
    foot.appendChild(lab);
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

  // Filters: tag, race, search
  let filter = 'all';
  let race = 'all';
  const q = document.getElementById('q');
  document.querySelectorAll('#tag-chips button').forEach(b => b.addEventListener('click', () => {{
    filter = b.dataset.f;
    document.querySelectorAll('#tag-chips button').forEach(o => o.setAttribute('aria-pressed', String(o === b)));
    apply();
  }}));
  q.addEventListener('input', apply);

  const raceChips = document.getElementById('race-chips');
  if (data.races.length > 1) {{
    raceChips.hidden = false;
    ['all'].concat(data.races).forEach(r => {{
      const b = el('button', null, r === 'all' ? 'All races' : r); b.dataset.race = r; b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', () => setRace(r, true)); raceChips.appendChild(b);
    }});
    const m = location.hash.match(/race=([a-z]+)/i);
    const fromHash = m && data.races.find(r => r.toLowerCase() === m[1].toLowerCase());
    let saved = null; try {{ saved = localStorage.getItem('wfm-race-' + data.page); }} catch (e) {{}}
    race = fromHash || (data.races.includes(saved) ? saved : 'all');
  }}
  function setRace(r, user) {{
    race = r;
    raceChips.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.race === r)));
    if (user) {{
      try {{ localStorage.setItem('wfm-race-' + data.page, r); }} catch (e) {{}}
      history.replaceState(null, '', r === 'all' ? location.pathname : '#race=' + r.toLowerCase());
    }}
    apply();
  }}

  function visible(c) {{
    return (filter === 'all' || c.dataset.tags.split(' ').includes(filter))
      && (race === 'all' || !c.dataset.race || c.dataset.race === race)
      && (!q.value.trim() || c.dataset.search.includes(q.value.trim().toLowerCase()));
  }}
  function apply() {{
    let shown = 0;
    cards.forEach(c => {{ const ok = visible(c); c.hidden = !ok; if (ok) shown++; }});
    document.querySelectorAll('.race-group').forEach(g => {{
      const n = g.querySelectorAll('article:not([hidden])').length; g.hidden = !n; g._count.textContent = plural(n);
    }});
    document.querySelectorAll('main section').forEach(s => {{
      const n = s.querySelectorAll('article:not([hidden])').length; s.hidden = !n; s._count.textContent = plural(n);
    }});
    empty.hidden = shown > 0;
    updateCount();
  }}

  // Download as macros-cache.txt
  const LIMITS = {{ character: 18, account: 120 }};
  const BASE = {{ character: 0x1000001, account: 1 }};
  const hex = n => n.toString(16).toUpperCase().padStart(16, '0');
  function chosen() {{ return data.macros.filter(x => ticked.has(x.id) && !cards.get(x.id).hidden); }}
  function updateCount() {{ document.getElementById('dl-count').textContent = chosen().length + ' selected'; }}

  function buildCache(macros, scope, existing) {{
    const warnings = [];
    let head = '', names = new Set(), maxId = 0, count = 0;
    if (existing) {{
      const lines = existing.replace(/\\r\\n?/g, '\\n').split('\\n');
      const ver = lines.filter(l => /^VER 3 [0-9A-Fa-f]{{16}} ".*" ".*"\\s*$/.test(l));
      if (!ver.length && lines.some(l => /^MACRO /.test(l))) {{
        return {{ error: 'That file uses an older macro format this page can\\'t merge into. Download without merging, or copy macros in by hand.' }};
      }}
      ver.forEach(l => {{
        const p = l.match(/^VER 3 ([0-9A-Fa-f]{{16}}) "(.*)" "(.*)"/);
        maxId = Math.max(maxId, parseInt(p[1], 16)); names.add(p[2]); count++;
      }});
      const isChar = maxId >= 0x1000000;
      if (count && isChar !== (scope === 'character')) warnings.push('Your file looks like ' + (isChar ? 'a per-character' : 'an account-wide') + ' file, but you picked ' + (scope === 'character' ? 'This character only' : 'All characters') + '.');
      head = lines.join('\\r\\n').replace(/(\\r\\n)*$/, '');
      if (head) head += '\\r\\n';
    }}
    let id = Math.max(BASE[scope], maxId + 1);
    const added = [], skipped = [];
    let out = head;
    macros.forEach(x => {{
      const name = x.name.replace(/"/g, "'");
      if (names.has(name)) {{ skipped.push(name); return; }}
      names.add(name);
      out += 'VER 3 ' + hex(id++) + ' "' + name + '" "INV_Misc_QuestionMark"\\r\\n' + x.text.split('\\n').join('\\r\\n') + '\\r\\nEND\\r\\n';
      added.push(name);
    }});
    const total = count + added.length;
    if (total > LIMITS[scope]) warnings.push('That makes ' + total + ' macros, over the ' + LIMITS[scope] + ' allowed in ' + (scope === 'character' ? 'the per-character tab (Classic limit; Forever may allow more)' : 'the General tab') + '. WoW may drop the extras.');
    return {{ text: out, added, skipped, kept: count, total, warnings }};
  }}
  window.WFM = {{ buildCache, chosen }};

  const status = document.getElementById('dl-status');
  function say(msg, warn) {{ status.textContent = msg; status.className = warn ? 'warn' : ''; }}
  document.getElementById('dl-go').addEventListener('click', async () => {{
    const scope = document.querySelector('input[name=scope]:checked').value;
    const list = chosen();
    if (!list.length) return say('Nothing is selected. Tick some cards or clear the filters.', true);
    const file = document.getElementById('merge').files[0];
    const existing = file ? await file.text() : '';
    const r = buildCache(list, scope, existing);
    if (r.error) return say(r.error, true);
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([r.text], {{ type: 'text/plain' }}));
    a.download = 'macros-cache.txt'; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
    let msg = 'Downloaded ' + plural(r.added.length) + (r.kept ? ', keeping your ' + plural(r.kept) : '') + '.';
    if (r.skipped.length) msg += '\\nSkipped because you already have a macro with that name: ' + r.skipped.join(', ') + '.';
    if (r.warnings.length) msg += '\\n' + r.warnings.join('\\n');
    say(msg, r.warnings.length > 0);
  }});
  document.getElementById('sel-all').addEventListener('click', () => setAll(true));
  document.getElementById('sel-none').addEventListener('click', () => setAll(false));
  function setAll(on) {{ cards.forEach((c, id) => {{ c._box.checked = on; on ? ticked.add(id) : ticked.delete(id); }}); updateCount(); }}

  if (data.races.length > 1) setRace(race, false); else apply();
}})();
</script>
</body>
</html>
"""


def build(key):
    page = PAGES[key]
    payload = json.dumps({"page": key, "races": page["races"], "sections": page["sections"], "macros": page["macros"]},
                         ensure_ascii=False, indent=1)
    payload = payload.replace("</", "<\\/")
    others = ", ".join(f'<a href="{p["file"]}">{html.escape(p["title"])}</a>' for k, p in PAGES.items() if k != key)
    races_line = f'<p class="races">Horde: {", ".join(page["races"])}</p>' if page["races"] else ""
    out = TEMPLATE.format(title=html.escape(page["title"]), others=others, races_line=races_line,
                          data=payload, **THEMES[key])
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
a.cls.wide {{ grid-column: 1 / -1; }}
a.cls h2 {{ font: 600 40px/1.05 var(--serif); margin: 0; }}
a.cls h2 .glyph {{ color: var(--c-accent); font-weight: 400; margin-right: 0.2em; }}
a.cls .races {{ color: var(--c-accent); font-size: 15px; }}
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
  <p class="lede">Copy-ready PvP and PvE macros for every Horde class, written for Forever's spellbook and checked against the 255-character limit. Every page uses the same keys, so your hands learn it once.</p>
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
  <p>Every page can download its macros as a macros-cache.txt file to drop into your WoW folder, and class pages can filter by race.</p>
  <p>Turn on the focus frame first: Esc → Edit Mode → Focus Frame.</p>
</div></footer>
</body>
</html>
"""

CARD = """<a class="cls{wide}" href="{file}" style="--c-bg:{panel};--c-line:{line};--c-ink:{ink};--c-muted:{muted};--c-accent:{accent}">
  <h2><span class="glyph" aria-hidden="true">{glyph}</span>{title}</h2>
  {races}
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
            wide=" wide" if key == "general" else "",
            file=page["file"], title=html.escape(page["title"]), n=len(page["macros"]),
            v=sum(x["status"] == "verify" for x in page["macros"]),
            races=f'<div class="races">Horde: {", ".join(page["races"])}</div>' if page["races"] else "",
            sections="".join(f"<li>{html.escape(s)}</li>" for s in page["sections"]),
            **{k: t[k] for k in ("panel", "line", "ink", "muted", "accent", "glyph")},
            tagline=html.escape(t["tagline"])))
    (OUT / "index.html").write_text(INDEX.format(cards="\n".join(cards)), encoding="utf-8")
    print(f"wrote {OUT / 'index.html'}")


if __name__ == "__main__":
    for k in PAGES:
        build(k)
    build_index()
