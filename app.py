"""
સીઝર સાયફર વ્હીલ - વિજ્ઞાન મેળા માટે ગુજરાતી ડેમો (ધોરણ 10) - એનિમેશન વર્ઝન

ચલાવવા માટે:   pip install flask
               python app.py
લેપટોપ:  http://localhost:5000
મોબાઇલ:  એ જ Wi-Fi પર  http://<લેપટોપ-IP>:5000  (IP ચાલુ કરતાં છપાશે)
"""
import socket
from flask import Flask, Response, jsonify, request

app = Flask(__name__)


def caesar(text: str, key: int, decrypt: bool = False) -> str:
    shift = -key if decrypt else key
    out = []
    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)


@app.route("/api/cipher", methods=["POST"])
def cipher():
    data = request.get_json(force=True)
    text = str(data.get("text", ""))[:500]
    try:
        key = int(data.get("key", 3)) % 26
    except (TypeError, ValueError):
        key = 3
    mode = data.get("mode", "encrypt")
    return jsonify(result=caesar(text, key, decrypt=(mode == "decrypt")), key=key)


PAGE = r"""<!doctype html>
<html lang="gu">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>સીઝર સાયફર વ્હીલ</title>
<style>
  :root {
    --bg1:#0b1026; --bg2:#1a1147; --bg3:#0d3b66;
    --glass:rgba(255,255,255,.07); --glass-b:rgba(255,255,255,.16);
    --txt:#eef2ff; --mut:#a9b8d6; --acc:#ffd84a; --acc2:#ff6bd6; --acc3:#52e5ff; --ok:#6dffb0;
  }
  * { box-sizing:border-box; -webkit-tap-highlight-color:transparent; }
  html { scroll-behavior:smooth; }
  body {
    margin:0; color:var(--txt); line-height:1.65; min-height:100vh;
    font-family:"Nirmala UI","Shruti","Noto Sans Gujarati",system-ui,sans-serif;
    background:linear-gradient(135deg,var(--bg1),var(--bg2),var(--bg3),var(--bg1));
    background-size:300% 300%; animation:bgmove 18s ease infinite;
    overflow-x:hidden;
  }
  @keyframes bgmove { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
  canvas#bg, canvas#fx { position:fixed; inset:0; width:100%; height:100%; pointer-events:none; }
  canvas#bg { z-index:0; opacity:.55; }
  canvas#fx { z-index:50; }

  /* glowing blobs */
  .blob { position:fixed; border-radius:50%; filter:blur(70px); opacity:.35; z-index:0; pointer-events:none;
          animation:float 14s ease-in-out infinite; }
  .b1 { width:340px; height:340px; background:var(--acc2); top:-80px; left:-80px; }
  .b2 { width:380px; height:380px; background:var(--acc3); bottom:-100px; right:-100px; animation-delay:-5s; }
  .b3 { width:260px; height:260px; background:var(--acc); top:45%; left:55%; animation-delay:-9s; opacity:.18; }
  @keyframes float { 0%,100%{transform:translate(0,0) scale(1)} 33%{transform:translate(40px,-30px) scale(1.12)} 66%{transform:translate(-30px,40px) scale(.92)} }

  main { position:relative; z-index:2; max-width:800px; margin:0 auto; padding:18px 14px 50px; }

  header { text-align:center; padding:18px 0 8px; }
  .lock { font-size:3.2rem; display:inline-block; animation:bob 3s ease-in-out infinite; filter:drop-shadow(0 0 18px var(--acc)); }
  @keyframes bob { 0%,100%{transform:translateY(0) rotate(-6deg)} 50%{transform:translateY(-10px) rotate(6deg)} }
  h1 {
    margin:4px 0; font-size:clamp(1.7rem,6vw,2.6rem); font-weight:900;
    background:linear-gradient(90deg,var(--acc),var(--acc2),var(--acc3),var(--acc));
    background-size:300% 100%; -webkit-background-clip:text; background-clip:text; color:transparent;
    animation:shine 6s linear infinite;
  }
  @keyframes shine { to { background-position:300% 0 } }
  p.sub { margin:0; color:var(--mut); font-size:1.05rem; }
  .typing { display:inline-block; border-right:3px solid var(--acc); padding-right:4px; animation:caret .8s step-end infinite; }
  @keyframes caret { 50%{border-color:transparent} }

  .card {
    position:relative; background:var(--glass); border:1px solid var(--glass-b); border-radius:22px;
    padding:18px; margin:18px 0; backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px);
    box-shadow:0 10px 40px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.12);
    transition:transform .35s ease, box-shadow .35s ease, border-color .35s ease;
  }
  .card:hover { transform:translateY(-4px); border-color:rgba(255,216,74,.5);
                box-shadow:0 18px 50px rgba(0,0,0,.45), 0 0 30px rgba(255,216,74,.15); }
  .card::before { content:""; position:absolute; inset:-1px; border-radius:22px; padding:1px; pointer-events:none;
    background:linear-gradient(120deg,transparent 30%,rgba(255,255,255,.55),transparent 70%); background-size:250% 100%;
    -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0); -webkit-mask-composite:xor; mask-composite:exclude;
    animation:sweep 6s linear infinite; opacity:.5; }
  @keyframes sweep { from{background-position:200% 0} to{background-position:-100% 0} }

  .reveal { opacity:0; transform:translateY(40px) scale(.97); transition:opacity .8s ease, transform .8s cubic-bezier(.2,.8,.2,1); }
  .reveal.in { opacity:1; transform:none; }

  h2 { font-size:1.25rem; margin:0 0 8px; color:var(--acc); text-shadow:0 0 14px rgba(255,216,74,.45); }
  .card p { margin:6px 0; }
  ol, ul { margin:6px 0; padding-left:22px; }
  li { margin:6px 0; }
  li::marker { color:var(--acc2); font-weight:800; }
  b { color:#fff; }

  .formula { text-align:center; font-size:1.15rem; background:rgba(0,0,0,.35); border-radius:14px; padding:12px; margin:10px 0;
             border:1px dashed rgba(255,255,255,.25); }
  .formula b { color:var(--acc); }
  .tip { background:rgba(255,216,74,.1); border-left:4px solid var(--acc); padding:10px 14px; border-radius:10px; margin-top:10px; }

  /* wheel */
  #wheelWrap { width:100%; max-width:430px; margin:6px auto 0; touch-action:none; position:relative; }
  #wheelWrap::after { content:""; position:absolute; inset:6%; border-radius:50%; z-index:-1;
    background:radial-gradient(circle,rgba(255,216,74,.35),transparent 70%); filter:blur(18px); animation:glow 3s ease-in-out infinite; }
  @keyframes glow { 0%,100%{opacity:.5; transform:scale(.95)} 50%{opacity:1; transform:scale(1.05)} }
  svg { width:100%; height:auto; display:block; overflow:visible; filter:drop-shadow(0 12px 22px rgba(0,0,0,.55)); }
  #inner { transform-box:fill-box; transform-origin:center; transition:transform .8s cubic-bezier(.2,1.1,.3,1); cursor:grab; }
  #inner.drag { transition:none; cursor:grabbing; }
  .olet { cursor:pointer; transition:fill .2s; }
  .olet:hover { fill:#d9008f; }
  #wedge { fill:rgba(255,107,214,.35); stroke:#ff6bd6; stroke-width:2.5; opacity:0; transition:opacity .25s; pointer-events:none;
           filter:drop-shadow(0 0 8px #ff6bd6); }
  #wedge.on { opacity:1; }
  #pointer { animation:point 1.4s ease-in-out infinite; transform-box:fill-box; transform-origin:center; }
  @keyframes point { 0%,100%{transform:translateY(0)} 50%{transform:translateY(5px)} }

  #pair { text-align:center; min-height:2.2rem; font-size:1.2rem; margin:6px 0 4px; color:var(--mut); }
  #pair b { color:var(--acc); font-size:1.5rem; }

  .row { display:flex; gap:10px; align-items:center; flex-wrap:wrap; justify-content:center; }
  button {
    position:relative; overflow:hidden; border:0; border-radius:14px; padding:11px 18px; font-size:1rem; font-weight:800;
    font-family:inherit; cursor:pointer; color:#1a1200;
    background:linear-gradient(135deg,var(--acc),#ffb02e); box-shadow:0 6px 18px rgba(255,176,46,.35);
    transition:transform .2s ease, box-shadow .2s ease, filter .2s;
  }
  button:hover { transform:translateY(-3px) scale(1.04); box-shadow:0 10px 26px rgba(255,176,46,.55); filter:brightness(1.08); }
  button:active { transform:scale(.95); }
  button.alt { color:var(--txt); background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.25); box-shadow:none; }
  button.alt:hover { background:rgba(255,255,255,.22); box-shadow:0 8px 22px rgba(82,229,255,.3); }
  button.enc { background:linear-gradient(135deg,#6dffb0,#26c6a2); box-shadow:0 6px 18px rgba(38,198,162,.4); color:#032; }
  button.dec { background:linear-gradient(135deg,var(--acc2),#a259ff); box-shadow:0 6px 18px rgba(162,89,255,.45); color:#fff; }
  .ripple { position:absolute; border-radius:50%; background:rgba(255,255,255,.6); transform:scale(0); animation:rip .6s linear; pointer-events:none; }
  @keyframes rip { to { transform:scale(4); opacity:0 } }

  .big { font-size:2.6rem; font-weight:900; min-width:2.3ch; text-align:center; color:var(--acc);
         text-shadow:0 0 20px rgba(255,216,74,.7); display:inline-block; }
  .big.pop { animation:pop .45s cubic-bezier(.2,2,.4,1); }
  @keyframes pop { 0%{transform:scale(.4) rotate(-15deg)} 100%{transform:scale(1) rotate(0)} }

  input[type=range] { -webkit-appearance:none; appearance:none; width:100%; height:12px; border-radius:99px; margin:14px 0 4px;
    background:linear-gradient(90deg,var(--acc3),var(--acc2),var(--acc)); outline:none; }
  input[type=range]::-webkit-slider-thumb { -webkit-appearance:none; width:30px; height:30px; border-radius:50%; background:#fff;
    border:4px solid var(--acc2); box-shadow:0 0 16px var(--acc2); cursor:pointer; transition:transform .15s; }
  input[type=range]::-webkit-slider-thumb:hover { transform:scale(1.2); }
  input[type=range]::-moz-range-thumb { width:26px; height:26px; border-radius:50%; background:#fff; border:4px solid var(--acc2); cursor:pointer; }

  .map { font-family:ui-monospace,Consolas,monospace; font-size:.85rem; color:var(--mut); text-align:center; line-height:1.8; margin-top:8px; word-break:break-word; }
  .map span { display:inline-block; padding:0 3px; border-radius:6px; animation:fadeup .5s both; }

  label { color:var(--mut); font-size:.95rem; }
  textarea {
    width:100%; min-height:84px; border-radius:14px; border:1px solid rgba(255,255,255,.25); background:rgba(0,0,0,.35);
    color:var(--txt); padding:12px; font-size:1.15rem; font-family:inherit; margin-top:6px; transition:border-color .25s, box-shadow .25s; resize:vertical;
  }
  textarea:focus { outline:none; border-color:var(--acc3); box-shadow:0 0 0 4px rgba(82,229,255,.2), 0 0 24px rgba(82,229,255,.3); }

  .out { background:rgba(0,0,0,.4); border:1px solid rgba(109,255,176,.35); border-radius:14px; padding:14px; min-height:60px; margin-top:6px;
         font-size:1.7rem; letter-spacing:3px; word-break:break-word; color:var(--ok); font-weight:900; text-shadow:0 0 14px rgba(109,255,176,.6); }
  .out .ch { display:inline-block; animation:charin .45s cubic-bezier(.2,2,.4,1) both; }
  .out .ph { color:var(--mut); font-size:1.1rem; letter-spacing:0; font-weight:600; text-shadow:none; }
  @keyframes charin { 0%{opacity:0; transform:translateY(-22px) scale(.3) rotate(-30deg)} 100%{opacity:1; transform:none} }

  .chips { display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
  .chip { background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.22); border-radius:14px; padding:7px 11px; text-align:center;
          font-size:1rem; min-width:72px; animation:fadeup .5s cubic-bezier(.2,1.6,.4,1) both; transition:transform .2s; }
  .chip:hover { transform:translateY(-4px) scale(1.08); }
  .chip b { color:var(--acc); font-size:1.2rem; }
  .chip small { display:block; color:var(--mut); font-size:.75rem; }
  @keyframes fadeup { from{opacity:0; transform:translateY(14px) scale(.8)} to{opacity:1; transform:none} }

  .steps li { animation:none; }

  /* ---------- pictures ---------- */
  .flow { display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:8px; margin:14px 0; }
  .node { background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.25); border-radius:16px; padding:10px 12px;
          text-align:center; font-size:1.5rem; min-width:84px; animation:floaty 4s ease-in-out infinite; }
  .node.sm { min-width:70px; padding:8px 10px; }
  .node b { display:block; font-size:1.05rem; letter-spacing:2px; color:var(--acc); }
  .node small { display:block; font-size:.78rem; color:var(--mut); font-weight:600; }
  .node.sec { border-color:rgba(109,255,176,.6); }
  .node.sec b { color:var(--ok); }
  .node.bad { border-color:#ff5d7a; }
  .node.bad b { color:#ff5d7a; }
  .node.hl { border-color:var(--acc); box-shadow:0 0 18px rgba(255,216,74,.5); }
  .arrow { font-size:1.4rem; color:var(--acc3); text-align:center; animation:nudge 1.2s ease-in-out infinite; }
  .arrow small { display:block; font-size:.78rem; color:var(--acc); font-weight:800; }
  @keyframes floaty { 50% { transform:translateY(-5px) } }
  @keyframes nudge { 50% { transform:translateX(5px) } }

  .strip { display:flex; justify-content:center; gap:4px; flex-wrap:wrap; margin:10px 0 4px; }
  .col { display:flex; flex-direction:column; align-items:center; width:30px; animation:fadeup .5s both; }
  .col .p, .col .c { width:30px; height:30px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:.95rem; }
  .col .p { background:#f8fafc; color:#0b1026; }
  .col .c { background:var(--acc); color:#7c2d12; }
  .col .c.num { background:var(--acc3); color:#04323b; }
  .col .ar { color:var(--acc2); font-size:.75rem; line-height:1.1; animation:drop 1.4s ease-in-out infinite; }
  @keyframes drop { 50% { transform:translateY(4px) } }
  .cap { text-align:center; color:var(--mut); font-size:.88rem; margin:2px 0 8px; }

  .legend { display:flex; flex-wrap:wrap; gap:8px 16px; justify-content:center; margin:8px 0; font-size:.95rem; }
  .legend i { display:inline-block; width:16px; height:16px; border-radius:50%; vertical-align:middle; margin-right:6px; border:2px solid #0b1026; }

  .dash { stroke:#ffd84a; stroke-width:3; fill:none; stroke-dasharray:6 5; animation:dashmove 1s linear infinite; }
  @keyframes dashmove { to { stroke-dashoffset:-22 } }
  #clockWrap { max-width:300px; margin:8px auto; }

  .grid25 { display:grid; grid-template-columns:repeat(9,1fr); gap:5px; margin:10px 0; }
  .cell { text-align:center; padding:6px 0; border-radius:8px; background:rgba(255,255,255,.1); font-weight:800; font-size:.9rem; transition:all .2s; }
  .cell.try { background:var(--acc); color:#222; transform:scale(1.2); box-shadow:0 0 14px var(--acc); }
  .cell.bad { background:rgba(255,93,122,.35); color:#ffb3c0; }
  .cell.ok { background:var(--ok); color:#032; transform:scale(1.25); box-shadow:0 0 18px var(--ok); }
  .bar { margin:10px 0; font-size:.92rem; }
  .bar i { display:block; height:14px; border-radius:99px; margin-top:4px; background:linear-gradient(90deg,#ff5d7a,#ffb02e); }
  .bar i.long { width:100%; background:repeating-linear-gradient(45deg,#6dffb0 0 12px,#26c6a2 12px 24px); background-size:34px 34px; animation:stripe 1s linear infinite; }
  @keyframes stripe { to { background-position:34px 0 } }
  footer { text-align:center; color:var(--mut); margin-top:26px; font-size:.95rem; }

  @media (prefers-reduced-motion:reduce) {
    *, *::before, *::after { animation-duration:.01ms !important; animation-iteration-count:1 !important; transition-duration:.01ms !important; }
  }
</style>
</head>
<body>
<canvas id="bg"></canvas>
<canvas id="fx"></canvas>
<div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>

<main>
  <header>
    <div class="lock">🔐</div>
    <h1>સીઝર સાયફર વ્હીલ</h1>
    <p class="sub"><span class="typing" id="typer"></span></p>
  </header>

  <section class="card reveal">
    <h2>📖 સીઝર સાયફર એટલે શું?</h2>
    <p>જૂના સમયમાં રોમના રાજા <b>જુલિયસ સીઝર</b> યુદ્ધના સંદેશા ગુપ્ત રાખવા માટે દરેક અક્ષરને
       આગળ ખસેડીને લખતા હતા. આને <b>સીઝર સાયફર</b> કહેવાય છે.</p>
    <p>ઉદાહરણ: ચાવી (Key) = <b>3</b> હોય તો <b>A → D</b>, <b>B → E</b>, <b>C → F</b>.
       એટલે કે દરેક અક્ષર <b>3 સ્થાન આગળ</b> જાય છે.</p>
    <div class="flow">
      <div class="node">🧑‍💼<small>મોકલનાર</small></div>
      <div class="arrow">➜</div>
      <div class="node sm">📜<b>HELLO</b><small>મૂળ સંદેશ</small></div>
      <div class="arrow">🔑<small>Key +3</small></div>
      <div class="node sm sec">📜<b>KHOOR</b><small>ગુપ્ત સંદેશ</small></div>
      <div class="arrow">➜</div>
      <div class="node sm bad">🕵️<b>???</b><small>ચાવી વગર સમજાય નહીં</small></div>
      <div class="node sm hl">👩‍💼<b>HELLO</b><small>ચાવી હોય તો ખુલે</small></div>
    </div>
    <div class="strip" id="shiftStrip"></div>
    <div class="cap">ઉપર સફેદ = મૂળ અક્ષર &nbsp;|&nbsp; નીચે પીળો = 3 સ્થાન આગળનો ગુપ્ત અક્ષર</div>
    <div class="formula">મૂળ સંદેશ <b>HELLO</b> &nbsp;➜&nbsp; ગુપ્ત સંદેશ <b>KHOOR</b></div>
    <div class="tip">🔑 <b>Key</b> = કેટલા સ્થાન ખસેડવા તે નંબર (0 થી 25). આ નંબર ફક્ત મોકલનાર અને લેનારને ખબર હોય!</div>
  </section>

  <section class="card reveal">
    <h2>🎡 વ્હીલ ફેરવો</h2>
    <p>બહારના અક્ષર = <b>મૂળ (Plaintext)</b>, અંદરના પીળા અક્ષર = <b>ગુપ્ત (Ciphertext)</b>.
       પીળા વ્હીલને <b>આંગળીથી ફેરવો</b>, સ્લાઇડર ખસેડો, અથવા બહારના કોઈ પણ અક્ષર પર <b>ટેપ કરો</b>!</p>
    <div class="legend">
      <span><i style="background:#f8fafc"></i>બહારનું સફેદ = મૂળ</span>
      <span><i style="background:#ffd84a"></i>અંદરનું પીળું = ગુપ્ત</span>
      <span><i style="background:#ff4d6d"></i>લાલ તીર = શરૂઆત</span>
      <span><i style="background:#ff6bd6"></i>ગુલાબી = જોડી</span>
    </div>
    <div id="pair">કોઈ અક્ષર પર ટેપ કરો 👆</div>
    <div id="wheelWrap"><svg id="wheel" viewBox="-210 -210 420 420"></svg></div>
    <div class="row" style="margin-top:12px">
      <button class="alt" id="minus">◀ −1</button>
      <span>ચાવી (Key) =</span>
      <span class="big" id="keyBig">3</span>
      <button class="alt" id="plus">+1 ▶</button>
    </div>
    <input type="range" id="key" min="0" max="25" value="3" aria-label="Key">
    <div class="map" id="map"></div>
  </section>

  <section class="card reveal">
    <h2>✍️ તમારો સંદેશ લખો</h2>
    <div class="flow">
      <div class="node sm">✍️<b>HELLO</b><small>મૂળ</small></div>
      <div class="arrow">🔒<small>+ Key</small></div>
      <div class="node sm sec">📜<b>KHOOR</b><small>ગુપ્ત</small></div>
      <div class="arrow">🔓<small>− Key</small></div>
      <div class="node sm">✍️<b>HELLO</b><small>પાછું મૂળ</small></div>
    </div>
    <label for="inp">અંગ્રેજી (A–Z) માં સંદેશ લખો</label>
    <textarea id="inp" placeholder="ઉદા. HELLO SCIENCE FAIR"></textarea>
    <div class="row" style="margin:12px 0">
      <button class="alt" id="ex">💡 ઉદાહરણ</button>
      <button class="enc" id="enc">🔒 ગુપ્ત બનાવો</button>
      <button class="dec" id="dec">🔓 ખોલો</button>
      <button class="alt" id="cp">📋 કૉપી</button>
    </div>
    <label>પરિણામ</label>
    <div class="out" id="out"><span class="ph">અહીં જાદુ દેખાશે ✨</span></div>
    <div class="chips" id="chips"></div>
  </section>

  <section class="card reveal">
    <h2>🧮 ગણિત સાથે સમજો</h2>
    <p>દરેક અક્ષરને નંબર આપો: A=0, B=1, C=2 ... Z=25.</p>
    <div class="strip" id="numStrip"></div>
    <div class="cap">ઉપર અક્ષર (સફેદ) &nbsp;|&nbsp; નીચે તેનો નંબર (વાદળી)</div>
    <div class="formula">ગુપ્ત અક્ષર = (મૂળ નંબર <b>+ Key</b>) ÷ 26 નો <b>શેષ</b></div>
    <p>ઉદાહરણ: <b>H</b> = 7, Key = 3 ⇒ 7 + 3 = 10 ⇒ <b>K</b></p>
    <div class="flow">
      <div class="node sm">H<small>7</small></div><div class="arrow"><small>+1</small>➜</div>
      <div class="node sm">I<small>8</small></div><div class="arrow"><small>+1</small>➜</div>
      <div class="node sm">J<small>9</small></div><div class="arrow"><small>+1</small>➜</div>
      <div class="node sm hl">K<small>10</small></div>
    </div>
    <p>ઉદાહરણ: <b>Y</b> = 24, Key = 3 ⇒ 24 + 3 = 27 ⇒ 27 ÷ 26 નો શેષ = 1 ⇒ <b>B</b> (Z પછી ફરી A થી શરૂ!)</p>
    <div id="clockWrap"><svg id="clock" viewBox="-150 -150 300 300"></svg></div>
    <div class="cap">26 અક્ષરો ઘડિયાળની જેમ ગોળ ફરે છે: Y ➜ Z ➜ A ➜ B</div>
    <p>ખોલવા (Decrypt) માટે ઊલટું: નંબરમાંથી Key <b>બાદ</b> કરો.</p>
  </section>

  <section class="card reveal">
    <h2>🕹️ ડેમો કેવી રીતે કરવો?</h2>
    <div class="flow">
      <div class="node sm">🎚️<b>Key 3</b><small>૧. ચાવી</small></div><div class="arrow">➜</div>
      <div class="node sm">✍️<b>HELLO</b><small>૨. લખો</small></div><div class="arrow">➜</div>
      <div class="node sm sec">🔒<b>KHOOR</b><small>૩. ગુપ્ત</small></div><div class="arrow">➜</div>
      <div class="node sm hl">🔓<b>HELLO</b><small>૪. ખોલો</small></div>
    </div>
    <ol class="steps">
      <li>ચાવી (Key) <b>3</b> સેટ કરો.</li>
      <li>તમારો સંદેશ લખો, જેમ કે <b>HELLO</b>.</li>
      <li><b>🔒 ગુપ્ત બનાવો</b> દબાવો અને વ્હીલ પર અક્ષરો ઝળકતા જુઓ, પરિણામ <b>KHOOR</b>!</li>
      <li>મિત્રને ફક્ત KHOOR બતાવો અને Key કહો. તે <b>🔓 ખોલો</b> દબાવીને HELLO મેળવશે.</li>
      <li>Key બદલીને ફરી પ્રયત્ન કરો અને જુઓ ગુપ્ત સંદેશ કેવો બદલાય છે.</li>
    </ol>
    <div class="tip">🎯 <b>પડકાર:</b> મિત્ર <b>ZHOFRPH</b> લખે અને Key 3 હોય તો તેનો અર્થ શું? (જવાબ: WELCOME)</div>
  </section>

  <section class="card reveal">
    <h2>⚠️ મર્યાદા (કેમ સુરક્ષિત નથી?)</h2>
    <div class="cap">ચોર બધી 25 ચાવી એક પછી એક અજમાવે છે 👇 (સાચી ચાવી મળે ત્યાં સુધી)</div>
    <div class="grid25" id="crack"></div>
    <div class="formula" id="crackTxt">…</div>
    <div class="bar"><span>🔓 સીઝર સાયફર: ફક્ત 25 ચાવી</span><i style="width:6%"></i></div>
    <div class="bar"><span>🔐 આધુનિક Encryption: અબજો-અબજો-અબજો ચાવી</span><i class="long"></i></div>
    <p>આ કોડમાં ફક્ત 25 જ ચાવી શક્ય છે, એટલે કોઈ બધી ચાવી અજમાવીને સહેલાઈથી તોડી શકે.
       આજના ઇન્ટરનેટમાં બેંક અને વોટ્સએપ ઘણી મજબૂત <b>Encryption</b> વાપરે છે, પણ તેનો પાયો આવા જ વિચારો પર છે.</p>
  </section>

  <footer>🔬 વિજ્ઞાન મેળો &nbsp;•&nbsp; બનાવનાર: તમે! 🌟</footer>
</main>

<script>
const L = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const S = 360 / 26;
const NS = "http://www.w3.org/2000/svg";
const svg = document.getElementById("wheel");
const keyEl = document.getElementById("key");
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const sleep = ms => new Promise(r => setTimeout(r, reduce ? 0 : ms));
let key = 3, rot = 0, token = 0;

/* ---------- SVG helpers ---------- */
function el(name, attrs, parent) {
  const e = document.createElementNS(NS, name);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  (parent || svg).appendChild(e);
  return e;
}
function ring(group, rOut, rIn, letterR, fill, lineCol, txtCol, clickable) {
  el("circle", {r:rOut, fill:fill, stroke:"#0b1026", "stroke-width":3}, group);
  el("circle", {r:rIn, fill:"#ffffff", "fill-opacity":0.6, stroke:"#0b1026", "stroke-width":2}, group);
  for (let i = 0; i < 26; i++) {
    const a = (i * S - 90) * Math.PI / 180;
    el("line", {x1:rIn*Math.cos(a), y1:rIn*Math.sin(a), x2:rOut*Math.cos(a), y2:rOut*Math.sin(a),
                stroke:lineCol, "stroke-width":1}, group);
    const m = (i + 0.5) * S - 90, mr = m * Math.PI / 180;
    const x = letterR * Math.cos(mr), y = letterR * Math.sin(mr);
    const t = el("text", {x:x, y:y, "text-anchor":"middle", "dominant-baseline":"central",
      "font-size":18, "font-weight":800, fill:txtCol, transform:"rotate(" + (m + 90) + " " + x + " " + y + ")"}, group);
    t.textContent = L[i];
    if (clickable) {
      t.classList.add("olet");
      t.addEventListener("click", () => tapLetter(i));
    }
  }
}
ring(svg, 200, 150, 175, "#f8fafc", "#94a3b8", "#0b1026", true);       // બહાર: મૂળ
const inner = el("g", {id:"inner"});
ring(inner, 148, 95, 122, "#ffd84a", "#a16207", "#7c2d12", false);      // અંદર: ગુપ્ત
el("circle", {r:12, fill:"#0b1026", stroke:"#ffd84a", "stroke-width":3});
el("circle", {r:4, fill:"#ffd84a"});
el("polygon", {id:"pointer", points:"-10,-216 10,-216 0,-198", fill:"#ff4d6d"});
const wedge = el("path", {id:"wedge", d:""});

function wedgePath(j) {
  const a0 = (j * S - 90) * Math.PI / 180, a1 = ((j + 1) * S - 90) * Math.PI / 180;
  const r1 = 95, r2 = 200, P = (r, a) => (r * Math.cos(a)).toFixed(2) + " " + (r * Math.sin(a)).toFixed(2);
  return "M " + P(r1, a0) + " L " + P(r2, a0) + " A " + r2 + " " + r2 + " 0 0 1 " + P(r2, a1) +
         " L " + P(r1, a1) + " A " + r1 + " " + r1 + " 0 0 0 " + P(r1, a0) + " Z";
}
function showWedge(j) { wedge.setAttribute("d", wedgePath(j)); wedge.classList.add("on"); }
function hideWedge() { wedge.classList.remove("on"); }

/* ---------- Key / rotation ---------- */
function applyRot() { inner.style.transform = "rotate(" + rot + "deg)"; }
function setKey(k, instantSpin) {
  const nk = ((k % 26) + 26) % 26;
  const target = -nk * S;                                  // અંદરનો A, બહારના (A+key) સામે આવે
  let delta = (((target - rot) % 360) + 540) % 360 - 180;  // સૌથી ટૂંકો રસ્તો
  if (instantSpin) delta += 720;
  rot += delta;
  applyRot();
  const changed = nk !== key;
  key = nk;
  keyEl.value = key;
  const big = document.getElementById("keyBig");
  big.textContent = key;
  if (changed) { big.classList.remove("pop"); void big.offsetWidth; big.classList.add("pop"); }
  let m = "";
  for (let i = 0; i < 26; i++) m += "<span style='animation-delay:" + (i * 15) + "ms'>" + L[i] + "→<b>" + L[(i + key) % 26] + "</b></span> ";
  document.getElementById("map").innerHTML = m;
}
keyEl.addEventListener("input", () => setKey(+keyEl.value));
document.getElementById("plus").onclick = () => setKey(key + 1);
document.getElementById("minus").onclick = () => setKey(key - 1);

/* ---------- Tap on a letter ---------- */
function tapLetter(j) {
  token++;
  showWedge(j);
  document.getElementById("pair").innerHTML =
    "બહાર <b>" + L[j] + "</b> &nbsp;➜&nbsp; અંદર <b style='color:#ff6bd6'>" + L[(j + key) % 26] + "</b>";
  setTimeout(() => { if (!sweeping) hideWedge(); }, 2200);
}

/* ---------- Drag to rotate ---------- */
let dragging = false;
function pt(ev) { return ev.touches && ev.touches.length ? ev.touches[0] : ev; }
function geom(ev) {
  const r = svg.getBoundingClientRect(), p = pt(ev), sc = r.width / 420;
  const dx = p.clientX - (r.left + r.width / 2), dy = p.clientY - (r.top + r.height / 2);
  return { dist: Math.hypot(dx, dy) / sc, ang: Math.atan2(dy, dx) * 180 / Math.PI + 90 };
}
function dragMove(ev) {
  if (!dragging) return;
  ev.preventDefault();
  const g = geom(ev);
  setKey(Math.round(-(((g.ang % 360) + 360) % 360) / S));
}
function dragStart(ev) {
  const g = geom(ev);
  if (g.dist < 150) { dragging = true; inner.classList.add("drag"); dragMove(ev); }
}
function dragEnd() { dragging = false; inner.classList.remove("drag"); }
svg.addEventListener("mousedown", dragStart);
svg.addEventListener("touchstart", dragStart, {passive:false});
window.addEventListener("mousemove", dragMove);
window.addEventListener("touchmove", dragMove, {passive:false});
window.addEventListener("mouseup", dragEnd);
window.addEventListener("touchend", dragEnd);

/* ---------- Encrypt / Decrypt with animation ---------- */
let sweeping = false;
async function run(mode) {
  const text = document.getElementById("inp").value;
  const out = document.getElementById("out"), chips = document.getElementById("chips");
  if (!text.trim()) { out.innerHTML = '<span class="ph">પહેલાં સંદેશ લખો 🙂</span>'; return; }
  const res = await fetch("/api/cipher", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({text, key, mode})
  });
  const data = await res.json();
  const result = data.result || "";
  const my = ++token;
  sweeping = true;
  out.innerHTML = ""; chips.innerHTML = "";
  let shown = 0;
  for (let i = 0; i < result.length; i++) {
    if (my !== token) return;                      // નવું ક્લિક થાય તો જૂનું બંધ
    const a = text[i], b = result[i];
    const isL = /[A-Za-z]/.test(a);
    if (isL && i < 30) {
      const plain = mode === "encrypt" ? a : b;    // બહારના વ્હીલ પરનો અક્ષર
      showWedge(L.indexOf(plain.toUpperCase()));
      document.getElementById("pair").innerHTML =
        "બહાર <b>" + plain.toUpperCase() + "</b> &nbsp;➜&nbsp; અંદર <b style='color:#ff6bd6'>" +
        (mode === "encrypt" ? b : a).toUpperCase() + "</b>";
    }
    const s = document.createElement("span");
    s.className = "ch";
    s.textContent = b === " " ? "\u00A0" : b;
    out.appendChild(s);
    if (isL && shown < 24) {
      shown++;
      const A = a.toUpperCase(), B = b.toUpperCase(), d = document.createElement("div");
      d.className = "chip";
      d.innerHTML = A + " → <b>" + B + "</b><small>" + L.indexOf(A) + (mode === "encrypt" ? " + " : " − ") + key + " = " + L.indexOf(B) + "</small>";
      chips.appendChild(d);
    }
    if (i < 30) await sleep(isL ? 230 : 60);
  }
  if (my === token) {
    sweeping = false;
    setTimeout(hideWedge, 600);
    confetti();
  }
}
document.getElementById("enc").onclick = () => run("encrypt");
document.getElementById("dec").onclick = () => run("decrypt");
document.getElementById("ex").onclick = () => {
  document.getElementById("inp").value = "HELLO";
  setKey(3);
  run("encrypt");
};
document.getElementById("cp").onclick = () => {
  const t = document.getElementById("out").textContent;
  if (navigator.clipboard) navigator.clipboard.writeText(t);
  const b = document.getElementById("cp"), old = b.textContent;
  b.textContent = "✅ કૉપી થયું"; setTimeout(() => b.textContent = old, 1400);
};

/* ---------- Button ripple ---------- */
document.querySelectorAll("button").forEach(b => {
  b.addEventListener("click", e => {
    const r = b.getBoundingClientRect(), d = Math.max(r.width, r.height);
    const s = document.createElement("span");
    s.className = "ripple";
    s.style.cssText = "width:" + d + "px;height:" + d + "px;left:" + (e.clientX - r.left - d / 2) + "px;top:" + (e.clientY - r.top - d / 2) + "px";
    b.appendChild(s); setTimeout(() => s.remove(), 600);
  });
});

/* ---------- Scroll reveal ---------- */
const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }),
                                    {threshold:.12});
document.querySelectorAll(".reveal").forEach((n, i) => { n.style.transitionDelay = (i % 3) * 80 + "ms"; io.observe(n); });

/* ---------- Typing subtitle ---------- */
(function () {
  const msg = "ગુપ્ત સંદેશ બનાવવાની અને ખોલવાની મજેદાર રીત!", t = document.getElementById("typer");
  let i = 0;
  (function tick() { t.textContent = msg.slice(0, i++); if (i <= msg.length) setTimeout(tick, reduce ? 0 : 55); })();
})();

/* ---------- Falling letters background ---------- */
(function () {
  if (reduce) return;
  const c = document.getElementById("bg"), x = c.getContext("2d");
  let w, h, drops = [];
  function size() {
    w = c.width = innerWidth; h = c.height = innerHeight;
    drops = Array.from({length: Math.floor(w / 38)}, () => ({x: Math.random() * w, y: Math.random() * h, v: .4 + Math.random() * 1.2,
            ch: L[Math.floor(Math.random() * 26)], s: 14 + Math.random() * 14}));
  }
  size(); addEventListener("resize", size);
  (function frame() {
    x.clearRect(0, 0, w, h);
    for (const d of drops) {
      x.font = "700 " + d.s + "px monospace";
      x.fillStyle = "rgba(160,200,255," + (0.12 + d.s / 90) + ")";
      x.fillText(d.ch, d.x, d.y);
      d.y -= d.v;
      if (d.y < -20) { d.y = h + 20; d.x = Math.random() * w; d.ch = L[Math.floor(Math.random() * 26)]; }
      if (Math.random() < .004) d.ch = L[Math.floor(Math.random() * 26)];
    }
    requestAnimationFrame(frame);
  })();
})();

/* ---------- Confetti ---------- */
const fx = document.getElementById("fx"), fxc = fx.getContext("2d");
function confetti() {
  if (reduce) return;
  fx.width = innerWidth; fx.height = innerHeight;
  const cols = ["#ffd84a", "#ff6bd6", "#52e5ff", "#6dffb0", "#ffffff"];
  const ps = Array.from({length: 110}, () => ({
    x: innerWidth / 2, y: innerHeight * 0.6, vx: (Math.random() - .5) * 16, vy: -8 - Math.random() * 11,
    r: 3 + Math.random() * 5, c: cols[Math.floor(Math.random() * cols.length)], rot: Math.random() * 6, vr: (Math.random() - .5) * .4, life: 0}));
  (function frame() {
    fxc.clearRect(0, 0, fx.width, fx.height);
    let alive = false;
    for (const p of ps) {
      p.life++; p.vy += .35; p.x += p.vx; p.y += p.vy; p.rot += p.vr;
      if (p.y < fx.height + 20 && p.life < 110) {
        alive = true;
        fxc.save(); fxc.translate(p.x, p.y); fxc.rotate(p.rot);
        fxc.globalAlpha = Math.max(0, 1 - p.life / 110);
        fxc.fillStyle = p.c; fxc.fillRect(-p.r, -p.r / 2, p.r * 2, p.r);
        fxc.restore();
      }
    }
    if (alive) requestAnimationFrame(frame); else fxc.clearRect(0, 0, fx.width, fx.height);
  })();
}

/* ---------- Pictures ---------- */
function col(p, c, i, cls) {
  return "<div class='col' style='animation-delay:" + (i * 60) + "ms'><div class='p'>" + p +
         "</div><div class='ar'>▼</div><div class='c " + (cls || "") + "'>" + c + "</div></div>";
}
(function () {
  let h = "", n = "";
  for (let i = 0; i < 12; i++) h += col(L[i], L[(i + 3) % 26], i, "");
  document.getElementById("shiftStrip").innerHTML = h;
  for (let i = 0; i < 26; i++) n += col(L[i], i, i, "num");
  document.getElementById("numStrip").innerHTML = n;
})();

(function () {                                   // ઘડિયાળ: Y → Z → A → B
  const s = document.getElementById("clock");
  function e(n, a, p) { const x = document.createElementNS(NS, n); for (const k in a) x.setAttribute(k, a[k]); (p || s).appendChild(x); return x; }
  const defs = e("defs", {});
  const mk = e("marker", {id:"ah", markerWidth:8, markerHeight:8, refX:5, refY:4, orient:"auto"}, defs);
  e("path", {d:"M0,0 L8,4 L0,8 z", fill:"#ffd84a"}, mk);
  const P = (r, a) => [r * Math.cos(a), r * Math.sin(a)];
  const ang = i => (i * S - 90) * Math.PI / 180;
  for (let i = 0; i < 26; i++) {
    const [x, y] = P(112, ang(i));
    let f = "rgba(255,255,255,.16)", tc = "#fff";
    if (i === 24) { f = "#ff6bd6"; }
    if (i === 25 || i === 0) { f = "#ffd84a"; tc = "#0b1026"; }
    if (i === 1) { f = "#6dffb0"; tc = "#0b1026"; }
    e("circle", {cx:x, cy:y, r:13, fill:f, stroke:"rgba(255,255,255,.4)"});
    const t = e("text", {x:x, y:y, "text-anchor":"middle", "dominant-baseline":"central", "font-size":12, "font-weight":800, fill:tc});
    t.textContent = L[i];
    const [nx, ny] = P(137, ang(i));
    const n = e("text", {x:nx, y:ny, "text-anchor":"middle", "dominant-baseline":"central", "font-size":8, fill:"#a9b8d6"});
    n.textContent = i;
  }
  const [x0, y0] = P(86, ang(24)), [x1, y1] = P(86, ang(27));
  e("path", {class:"dash", d:"M " + x0 + " " + y0 + " A 86 86 0 0 1 " + x1 + " " + y1, "marker-end":"url(#ah)"});
  const c1 = e("text", {x:0, y:-8, "text-anchor":"middle", "font-size":15, "font-weight":800, fill:"#ffd84a"}); c1.textContent = "Z પછી";
  const c2 = e("text", {x:0, y:14, "text-anchor":"middle", "font-size":15, "font-weight":800, fill:"#ffd84a"}); c2.textContent = "ફરી A! 🔄";
})();

(async function () {                             // ચોર બધી ચાવી અજમાવે છે
  const g = document.getElementById("crack"), t = document.getElementById("crackTxt"), TRUE = 19, C = "AXEEH";
  const dec = (s, k) => s.split("").map(ch => L[(L.indexOf(ch) - k + 26) % 26]).join("");
  const cells = [];
  for (let k = 1; k <= 25; k++) { const d = document.createElement("div"); d.className = "cell"; d.textContent = k; g.appendChild(d); cells.push(d); }
  if (reduce) { cells[TRUE - 1].classList.add("ok"); t.innerHTML = "✅ ચાવી <b>19</b> મળી ગઈ! સંદેશ: <b>HELLO</b>"; return; }
  const wait = ms => new Promise(r => setTimeout(r, ms));
  while (true) {
    cells.forEach(c => c.className = "cell");
    for (let k = 1; k <= 25; k++) {
      cells[k - 1].classList.add("try");
      t.innerHTML = "ચાવી <b>" + k + "</b> અજમાવી: AXEEH ➜ <b>" + dec(C, k) + "</b>";
      await wait(280);
      cells[k - 1].classList.remove("try");
      if (k === TRUE) {
        cells[k - 1].classList.add("ok");
        t.innerHTML = "✅ ચાવી <b>19</b> મળી ગઈ! સંદેશ: <b>HELLO</b>";
        await wait(2800);
        break;
      }
      cells[k - 1].classList.add("bad");
    }
  }
})();

/* ---------- Start: intro spin ---------- */
setKey(3, true);
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return Response(PAGE, mimetype="text/html")


def local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


if __name__ == "__main__":
    port = 5000
    print(f"\n  Laptop : http://localhost:{port}")
    print(f"  Mobile : http://{local_ip()}:{port}   (same Wi-Fi)\n")
    app.run(host="0.0.0.0", port=port, debug=False)
