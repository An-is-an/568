# ---------- clickable prototype of the designer's version ----------
# Usage: python3 -I proto.py <project dir>  (same downloaded artboards as wireflow.py)
# Builds every screen exactly as wireflow.py does (it also rewrites Wireflow.dc.html, unchanged),
# then writes one artboard per screen (Pr*.dc.html, next to the others) with links between them,
# and prints the canvas.json entries for the "Prototype" page as JSON.
import re, sys, io, json, contextlib
P = sys.argv[1]
with contextlib.redirect_stdout(io.StringIO()):
    exec(open("wireflow.py", encoding="utf-8").read())

def _close(body, start, tag):
    """index just past the element that opens at `start`, honouring nesting of the same tag"""
    depth, i = 0, start
    pat = re.compile(rf'<{tag}\b|</{tag}>')
    for m in pat.finditer(body, start):
        depth += 1 if m.group(0) != f'</{tag}>' else -1
        if depth == 0:
            return m.end()
    raise AssertionError(f"unclosed <{tag}> at {start}")

def link(body, needle, target, tag=None, hint=None, nth=0):
    """make the element that contains `needle` go to `target`.
    tag=None: nearest enclosing <a> or <button>; tag='div' with a style `hint`: that row."""
    idx = -1
    for _ in range(nth + 1):
        idx = body.index(needle, idx + 1)
    tags = [tag] if tag else ["a", "button"]
    best = None
    for t in tags:
        for m in re.finditer(rf'<{t}\b[^>]*>', body):
            if m.start() > idx:
                break
            if hint and hint not in m.group(0):
                continue
            if m.start() <= idx < _close(body, m.start(), t) and (best is None or m.start() > best[1]):
                best = (t, m.start(), m.end())
    assert best, (needle, target)
    t, s, e = best
    end = _close(body, s, t)
    open_tag = body[s:e]
    if t == "a":
        new_open = re.sub(r'href="[^"]*"', f'href="{target}"', open_tag, count=1)
        close_len = len("</a>")
        new_close = "</a>"
    else:
        new_open = re.sub(r'^<' + t, f'<a href="{target}"', open_tag)
        new_open = re.sub(r'\s(type="button"|disabled|aria-pressed="[^"]*"|aria-expanded="[^"]*")', '', new_open)
        new_open = new_open.replace('style="', 'style="text-decoration: none; color: inherit; cursor: pointer; ', 1)
        close_len = len(f"</{t}>")
        new_close = "</a>"
    return body[:s] + new_open + body[e:end - close_len] + new_close + body[end:]

ROW = "padding: 12px 16px; display: flex; flex-direction: column; gap: 6px"   # hub() payment / invoice rows
RES = ["[搜尋結果 1 的名稱]", "[搜尋結果 2 的名稱]", "[搜尋結果 3 的名稱]"]

def prep(b):
    b = hscroll(home_header(b))
    return re.sub(r'href="(?!Pr)[^"#]*\.dc\.html"', 'href="#"', b)   # never jump into the older discussion boards

A, D, B, C = laneA, laneD, laneB, laneC
# the single entry point: pick a scenario; flows end back here
def _scenario(target, title, desc):
    return (f'<a href="{target}" style="display: flex; align-items: center; gap: 12px; min-height: 76px; box-sizing: border-box; background: #FFFFFF; border: 1px solid #D5D8DD; border-radius: 12px; padding: 14px 16px; text-decoration: none; color: #1F2328">'
            f'<span style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 4px"><span style="font-size: 17px; font-weight: 700">{title}</span>'
            f'<span style="font-size: 13px; line-height: 19px; color: #5B6470">{desc}</span></span>' + CHEV + '</a>')
MENU = ("<div style=\"width: 390px; height: 844px; box-sizing: border-box; background: #F4F4F5; font-family: 'Noto Sans TC', system-ui, sans-serif; color: #1F2328; "
        "padding: 72px 16px 24px; display: flex; flex-direction: column; gap: 12px\">"
        '<h1 style="margin: 0; font-size: 24px; font-weight: 700">即時快遞 Prototype</h1>'
        '<p style="margin: 0 0 12px; font-size: 15px; color: #3D444D">請選擇要體驗的情境</p>'
        + _scenario("PrA1.dc.html", "老用戶下單", "有最愛與歷程，已綁卡；可試對調鈕")
        + _scenario("PrB1.dc.html", "第一次下單", "沒有歷程、沒綁卡、沒發票設定")
        + _scenario("PrC1.dc.html", "第一次下單、沒開定位", "取件要自己填，會詢問定位權限")
        + '<p style="margin: auto 0 0; font-size: 13px; line-height: 19px; color: #5B6470">送出成功後按關閉，或在快遞首頁按返回，都會回到這一頁。</p></div>')
F = lambda k: f"Pr{k}.dc.html"
# (key, title, body, [(needle, target_key, kwargs)])
screens = [
 ("Menu", "情境選單（從這裡開始播放）", MENU, []),
 ("A1", "A1 快遞首頁（剛進入）", A[0][1], [("[目前位置或上次地址]", "AP", {}), ("要送到哪裡？", "A2", {}), (">填寫地址<", "A2", {}),
     ("[最愛地址 1]", "A4", {}), ("[歷程地址 1]", "A4", {}), ("[歷程地址 2]", "A4", {}), ("[歷程地址 3]", "A3", {}),
     ('aria-label="取件與送件地址對調"', "D2", {}), ('aria-label="返回"', "Menu", {})]),
 ("A2", "A2 地址輸入頁", A[1][1], [(r, "A3", {}) for r in RES] + [('aria-label="返回快遞首頁"', "A1", {})]),
 ("A3", "A3 送件地址詳情", A[2][1], [(">確認<", "A4", {}), ('aria-label="返回地址輸入頁"', "A2", {})]),
 ("A4", "A4 快遞首頁（已填完）", A[3][1], [("[取件地址與樓層門牌]", "AP", {}), ("[送件地址與樓層門牌]", "A3", {}), ("送出訂單・[折後價]", "A5", {})]),
 ("A5", "A5 確認彈窗", A[4][1], [(">確認送出<", "A6", {}), ("返回修改", "A4", {})]),
 ("A6", "A6 送出成功", A[5][1], [('aria-label="關閉"', "Menu", {})]),
 ("AP", "A 取件地址詳情（從快遞首頁點取件）", pk, [(">確認<", "A4", {}), ('aria-label="返回地址輸入頁"', "A4", {})]),
 ("D2", "A2 對調後的快遞首頁", D[1][1], [("要從哪裡寄？", "D3", {}), (">填寫地址<", "D3", {}), ('aria-label="取件與送件地址對調"', "A1", {})]),
 ("D3", "A2 地址輸入頁（填取件）", D[2][1], [(r, "D4", {}) for r in RES] + [('aria-label="返回"', "D2", {})]),
 ("D4", "A2 取件地址詳情（寄件人空白）", D[3][1], [(">確認<", "D5", {}), ('aria-label="返回地址輸入頁"', "D3", {})]),
 ("D5", "A2 快遞首頁（填完地址）", D[4][1], [("送出訂單・[折後價]", "A5", {})]),
 ("B1", "B1 快遞首頁（第一次進入）", B[0][1], [("要送到哪裡？", "B2", {}), (">填寫地址<", "B2", {}), ('aria-label="返回"', "Menu", {})]),
 ("B2", "B2 地址輸入頁（沒有歷程）", B[1][1], [(r, "B3", {}) for r in RES] + [('aria-label="返回快遞首頁"', "B1", {})]),
 ("B3", "B3 送件地址詳情", B[2][1], [(">確認<", "B4", {}), ('aria-label="返回地址輸入頁"', "B2", {})]),
 ("B4", "B4 快遞首頁（還沒綁卡）", B[3][1], [("送出訂單・[折後價]", "B5", {}), (">付款方式<", "B6", {"tag": "div", "hint": ROW})]),
 ("B5", "B5 快遞首頁（按送出後提示）", B[4][1], [(">付款方式<", "B6", {"tag": "div", "hint": ROW})]),
 ("B6", "B6 付款與優惠（未綁定）", B[5][1], [("新增綁定支付", "B7", {}), ('aria-label="返回快遞首頁"', "B5", {})]),
 ("B7", "B7 付款與優惠（綁完卡）", B[6][1], [('aria-label="返回快遞首頁"', "B8", {})]),
 ("B8", "B8 快遞首頁（綁完卡）", B[7][1], [(">發票資訊<", "B9", {"tag": "div", "hint": ROW})]),
 ("B9", "B9 發票資訊", B[8][1], [("儲存變更", "B10", {}), ('aria-label="返回快遞首頁"', "B8", {})]),
 ("B10", "B10 快遞首頁（都設定好）", B[9][1], [("送出訂單・[折後價]", "B11", {})]),
 ("B11", "B11 運送須知（尚未讀完）", B[10][1], [("繼續往下閱讀", "B12", {}), ('aria-label="關閉，返回快遞首頁"', "B10", {})]),
 ("B12", "B12 運送須知（讀完）", B[11][1], [(">我已閱讀並同意<", "B13", {}), ('aria-label="關閉，返回快遞首頁"', "B10", {})]),
 ("B13", "B13 確認彈窗", B[12][1], [(">確認送出<", "B14", {}), ("返回修改", "B10", {})]),
 ("B14", "B14 送出成功", B[13][1], [('aria-label="關閉"', "Menu", {})]),
 ("C1", "C1 快遞首頁（沒開定位）", C[0][1], [("要從哪裡寄？", "C2", {}), (">填寫地址<", "C2", {}), ('aria-label="返回"', "Menu", {})]),
 ("C2", "C2 地址輸入頁（先填取件）", C[1][1], [("使用目前位置", "C3", {}), ('aria-label="返回"', "C1", {})]),
 ("C3", "C3 系統詢問定位權限", C[2][1], [("不允許", "C4", {}), ("使用 App 期間允許", "C6", {}), ("允許一次", "C6", {})]),
 ("C4", "C4 地址輸入頁（定位未開啟）", C[3][1], [(r, "C5", {}) for r in RES] + [('aria-label="返回"', "C1", {})]),
 ("C5", "C5 取件地址詳情", C[4][1], [(">確認<", "C6", {}), ('aria-label="返回地址輸入頁"', "C4", {})]),
 ("C6", "C6 地址輸入頁（選好取件）", C[5][1], [(r, "C7", {}) for r in RES] + [('aria-label="返回"', "C1", {})]),
 ("C7", "C7 送件地址詳情", C[6][1], [(">確認<", "C8", {}), ('aria-label="返回地址輸入頁"', "C6", {})]),
 ("C8", "C8 快遞首頁（填完地址）", C[7][1], [("送出訂單・[折後價]", "B5", {})]),
]

SKEL = '''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
body{{margin:0}}
a{{color:#1F2328}}a:hover{{color:#000000}}
[data-hscroll]::-webkit-scrollbar{{display:none}}
</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":390,"height":844}}}}'>
class Component extends DCLogic {{
renderVals() {{
{vals}
}}
}}
</script>
</body>
</html>
'''
import os
def swap_toggle(b):
    """homes with both addresses: the swap button exchanges the two addresses in place; contacts follow
    their address (member data moves to the recipient), and so does the note. Drawn as two copies of the address card."""
    i = b.find(CARD_OPEN)
    if i < 0 or '<button type="button" aria-label="取件與送件地址對調"' not in b:
        return b, None
    j = _close(b, i, "div")
    card = b[i:j]
    addr = re.findall(r'<div style="font-size: 16px; font-weight: 500">([^<]*)</div>', card)
    snd = re.search(r'寄件人 ([^<]*)<', card); rcv = re.search(r'收件人 ([^<]*)<', card)
    if len(addr) < 2 or not (snd and rcv):
        return b, None          # one address still missing: nothing to exchange here
    pa, da = addr[0], addr[1]
    alt = card
    for a_, b_ in ((pa, "\x00P"), (da, "\x00D"), ("寄件人 " + snd.group(1), "\x00S"), ("收件人 " + rcv.group(1), "\x00R")):
        alt = alt.replace(a_, b_, 1)
    alt = (alt.replace("\x00P", da).replace("\x00D", pa)
              .replace("\x00S", "寄件人 " + rcv.group(1)).replace("\x00R", "收件人 " + snd.group(1)))
    # a note belongs to its address too: the drop-off note moves up to the pickup row
    note = re.search(r'\s*<div style="font-size: 13px; color: #5B6470">備註 [^<]*</div>', alt)
    if note:
        nd = note.group(0)
        alt = alt[:note.start()] + alt[note.end():]
        sender = re.search(r'<div style="font-size: 13px; color: #5B6470">寄件人 [^<]*</div>', alt)
        assert sender
        alt = alt[:sender.end()] + nd + alt[sender.end():]
    on = '<button type="button" aria-label="取件與送件地址對調" onClick="{{toggleSwap}}"'
    card, alt = (c.replace('<button type="button" aria-label="取件與送件地址對調"', on, 1) for c in (card, alt))
    b = (b[:i] + '<sc-if value="{{plain}}" hint-placeholder-val="{{ true }}">' + card + '</sc-if>'
         '<sc-if value="{{swapped}}" hint-placeholder-val="{{ false }}">' + alt + '</sc-if>' + b[j:])
    js = ("const s = this.state || {};\n"
          "return { plain: !s.swapped, swapped: !!s.swapped, toggleSwap: () => this.setState({ swapped: !(this.state || {}).swapped }) };")
    return b, js

def contact_fill(b):
    """favorites toggle and contact fields on address detail: '填入我的資料' fills the member, the contacts icon fills a contact,
    both overwrite name and phone together; typing still works (controlled inputs)."""
    if ">填入我的資料<" not in b:
        return b, "return {};"
    init = {}
    for kind, suffix, hole, handler in (("text", "姓名", "cname", "onName"), ("tel", "手機號碼", "cphone", "onPhone")):
        m = re.search(rf'<input type="{kind}" aria-label="([^"]*{suffix})" (value|placeholder)="([^"]*)"', b)
        assert m, kind
        label, attr, val = m.groups()
        init[hole] = val if attr == "value" else ""
        b = b[:m.start()] + f'<input type="{kind}" aria-label="{label}" placeholder="{label}" value="{{{{{hole}}}}}" onChange="{{{{{handler}}}}}"' + b[m.end():]
    b = re.sub(r'<button type="button"( style="[^"]*")>填入我的資料</button>', r'<button type="button" onClick="{{fillMe}}"\1>填入我的資料</button>', b, count=1)
    b = b.replace('<button type="button" aria-label="從通訊錄帶入姓名與電話"', '<button type="button" aria-label="從通訊錄帶入姓名與電話" onClick="{{fillContact}}"', 1)
    assert "{{fillMe}}" in b and "{{fillContact}}" in b
    # 加入最愛 toggles: heart fills, label becomes 已加入最愛
    m = re.search(r'<button type="button" aria-pressed="false"( style="[^"]*">)(<svg [^>]*?)fill="none"([^>]*>.*?</svg>)加入最愛</button>', b, re.S)
    assert m, "favorites button"
    b = b[:m.start()] + ('<button type="button" aria-pressed="{{favPressed}}" onClick="{{toggleFav}}"' + m.group(1)
                         + m.group(2) + 'fill="{{favFill}}"' + m.group(3) + '{{favLabel}}</button>') + b[m.end():]
    js = ("const s = this.state || {};\n"
          f"return {{ cname: s.cname ?? {json.dumps(init['cname'], ensure_ascii=False)}, cphone: s.cphone ?? {json.dumps(init['cphone'], ensure_ascii=False)},\n"
          "  onName: (e) => this.setState({ cname: e.target.value }), onPhone: (e) => this.setState({ cphone: e.target.value }),\n"
          "  fillMe: () => this.setState({ cname: '[會員姓名]', cphone: '[會員電話]' }),\n"
          "  fillContact: () => this.setState({ cname: '[通訊錄的姓名]', cphone: '[通訊錄的電話]' }),\n"
          "  favPressed: s.fav ? 'true' : 'false', favFill: s.fav ? 'currentColor' : 'none', favLabel: s.fav ? '已加入最愛' : '加入最愛',\n"
          "  toggleFav: () => this.setState({ fav: !(this.state || {}).fav }) };")
    return b, js
keys = {k for k, *_ in screens}
rows = {"A": 0, "D": 1, "B": 2, "C": 3}
order_in_row = {}
boards = {}
for key, title, body, links in screens:
    b = prep(body)
    for needle, tgt, kw in links:
        assert tgt in keys, tgt
        b = link(b, needle, F(tgt), **kw)
    b, vals = contact_fill(b)
    b, sv = swap_toggle(b)
    if sv:
        assert vals == "return {};", key
        vals = sv
    open(f"{P}/{F(key)}", "w", encoding="utf-8").write(SKEL.format(title=title, body=b, vals=vals))
    if key == "Menu":   # left of the rows, beside row A
        boards[F(key)] = {"h": 844, "w": 390, "x": -560, "y": 0, "is_interactive": True, "page": "proto", "title": title}
        continue
    r = "A" if key == "AP" else key[0]
    n = order_in_row.get(r, 0); order_in_row[r] = n + 1
    boards[F(key)] = {"h": 844, "w": 390, "x": n * 470, "y": rows[r] * 1300, "is_interactive": True, "page": "proto", "title": title}
print(json.dumps(boards, ensure_ascii=False))
