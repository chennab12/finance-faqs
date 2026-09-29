"""Animated financial decision cues with reduced-motion support."""
from html import escape
from streamlit.components.v1 import html

def show(title,stages):
    safe=[escape(x) for x in stages]
    blocks=[]
    for i,label in enumerate(safe):
        x=24+190*i
        blocks.append(f'<g class="card c{i}"><rect x="{x}" y="66" width="166" height="83" rx="15" fill="#fff" stroke="#b9cdbd"/><text x="{x+12}" y="98" class="num">{i+1:02}</text><text x="{x+12}" y="128" class="label">{label}</text></g>')
    arrows=''.join(f'<path d="M{190+190*i} 108 h22" stroke="#27785c" stroke-width="3" marker-end="url(#arrow)"/>' for i in range(3))
    page=f'''<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0;font-family:system-ui,Arial,sans-serif}}.wrap{{overflow-x:auto;border:1px solid #c8dacb;border-radius:16px;background:linear-gradient(110deg,#ecf8ed,#fff8e6)}}svg{{width:100%;min-width:760px;height:auto;display:block}}.title{{font-size:21px;font-weight:750;fill:#215240}}.label{{font-size:14px;font-weight:650;fill:#215240}}.num{{font-size:17px;font-weight:800;fill:#27785c}}.small{{font-size:14px;fill:#446e59}}.card{{animation:glow 4.8s infinite}}.c1{{animation-delay:1.2s}}.c2{{animation-delay:2.4s}}.c3{{animation-delay:3.6s}}.coin{{animation:bob 2s ease-in-out infinite}}@keyframes glow{{20%{{filter:drop-shadow(0 4px 6px #9acba6)}}}}@keyframes bob{{50%{{transform:translateY(-8px)}}}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style></head><body><div class="wrap"><svg viewBox="0 0 930 265" role="img" aria-label="{escape(title)}: {escape(' to '.join(stages))}"><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7" fill="#27785c"/></marker></defs><text x="24" y="38" class="title">{escape(title)} · visual memory cue</text>{arrows}{''.join(blocks)}<rect x="24" y="176" width="662" height="66" rx="13" fill="white" stroke="#c8dacb"/><text x="40" y="201" class="small">A useful choice begins with a goal, tradeoffs and current source.</text><text x="40" y="225" class="small">Numbers are estimates; protect cash needs and check risks.</text><g class="coin"><circle cx="822" cy="203" r="40" fill="#e6b85c" stroke="#a8752c" stroke-width="4"/><text x="822" y="220" text-anchor="middle" font-size="50" fill="#6b501b">$</text></g></svg></div></body></html>'''
    html(page,height=280,scrolling=False)
