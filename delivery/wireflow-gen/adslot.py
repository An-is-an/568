# ---------- ad slot comparison: the delivery home page banner ----------
# Usage: python3 -I adslot.py <project dir>  (same downloaded artboards as wireflow.py)
# Reuses the screen-building part of wireflow.py (everything before its layout section).
import re, sys
P = sys.argv[1]
_src = open("wireflow.py", encoding="utf-8").read()
exec(_src[:_src.index("# ---------- layout ----------")])

CONTENT = 'flex: 1; min-height: 0; padding: 16px; display: flex; flex-direction: column; gap: 12px'
def clip(h):
    return rep(h, CONTENT, CONTENT + '; overflow: hidden')

# 1 the current page, from the requester's screenshot, in wireframe gray
_IMG = ('<div role="img" aria-label="現行插圖：機車與包裹" style="position: absolute; right: 12px; top: 64px; width: 170px; height: 150px; box-sizing: border-box; '
        'border: 1px dashed #A3A9B1; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 13px; color: #5B6470">[現行插圖]</div>')
def _addr(tag, ph):
    return ('<div style="height: 56px; box-sizing: border-box; border: 1px solid #D5D8DD; border-radius: 10px; padding: 0 14px; display: flex; align-items: center; gap: 12px">'
            f'<div style="width: 24px; height: 24px; border-radius: 12px; background: #1F2328; color: #FFFFFF; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center">{tag}</div>'
            f'<div style="font-size: 16px; color: #5B6470">{ph}</div></div>')
def _half(icon, t, sub):
    return ('<div style="flex: 1; min-width: 0; display: flex; align-items: center; gap: 8px">' + icon +
            f'<div style="flex: 1; min-width: 0"><div style="font-size: 16px; font-weight: 700">{t}</div><div style="font-size: 12px; color: #3D444D">{sub}</div></div>' + CHEV + '</div>')
_DOLLAR = '<div aria-hidden="true" style="width: 24px; height: 24px; flex-shrink: 0; border-radius: 12px; background: #1F2328; color: #FFFFFF; font-size: 14px; font-weight: 700; display: flex; align-items: center; justify-content: center">$</div>'
_RECEIPT = '<svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1F2328" stroke-width="2" stroke-linejoin="round" style="flex-shrink: 0"><path d="M5 3h14v18l-3-2-2 2-2-2-2 2-2-2-3 2z"></path><path d="M9 8h6M9 12h6"></path></svg>'
_CLOCK = '<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"></circle><path d="M12 7v5l3 2"></path></svg>'
CURRENT = f'''<div style="width: 390px; height: 844px; box-sizing: border-box; position: relative; background: #F4F4F5; font-family: 'Noto Sans TC', system-ui, sans-serif; color: #1F2328; display: flex; flex-direction: column">
  <div style="position: absolute; left: 0; top: 0; width: 390px; height: 280px; background: #E6E8EB"></div>
  {_IMG}
  <div style="position: relative; flex: 1; min-height: 0; display: flex; flex-direction: column">
    <div style="height: 64px; flex-shrink: 0; display: flex; align-items: center; justify-content: space-between; padding: 0 12px">
      <button type="button" aria-label="返回" style="width: 44px; height: 44px; border: 0; border-radius: 10px; background: #FFFFFF; padding: 0; display: flex; align-items: center; justify-content: center; color: #1F2328">
        <svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"></path></svg>
      </button>
      <button type="button" aria-label="訂單紀錄" style="width: 44px; height: 44px; border: 0; border-radius: 10px; background: #FFFFFF; padding: 0; display: flex; align-items: center; justify-content: center; color: #1F2328">{_RECEIPT}</button>
    </div>
    <div style="padding: 16px 16px 0; display: flex; flex-direction: column; gap: 4px">
      <h1 style="margin: 0; font-size: 24px; font-weight: 700">即時快遞</h1>
      <div style="font-size: 15px; font-weight: 500">機車快捷投遞，準時抵達！</div>
    </div>
    <div style="margin: 24px 12px 0; background: #FFFFFF; border-radius: 16px; padding: 16px 12px; display: flex; flex-direction: column; gap: 12px">
      {_addr("寄", "請輸入取件地址")}
      {_addr("收", "請輸入送件地址")}
      <div style="display: flex; align-items: center; gap: 12px; padding: 4px 0">{_half(_DOLLAR, "付款方式", "請新增付款方式")}<div style="width: 1px; height: 36px; background: #D5D8DD"></div>{_half(_RECEIPT, "發票資訊", "請選擇發票方式")}</div>
      <div style="background: #F4F4F5; border-radius: 10px; padding: 10px 12px; display: flex; flex-direction: column; gap: 2px">
        <div style="font-size: 14px; font-weight: 700">本服務由機車配送</div>
        <div style="font-size: 12px; color: #3D444D">包裹總重量 &lt; 15kg，長寬高皆 ≤ 40cm。</div>
      </div>
    </div>
    <div style="margin: 20px 22px 0; display: flex; flex-direction: column; gap: 8px">
      <div role="img" aria-label="現行的輪播廣告" style="height: 87px; box-sizing: border-box; background: #E6E8EB; border: 1px solid #A3A9B1; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 15px; font-weight: 500">[輪播廣告 1:4]</div>
      <div aria-hidden="true" style="display: flex; justify-content: center; gap: 4px"><span style="width: 12px; height: 4px; border-radius: 2px; background: #3D444D"></span><span style="width: 4px; height: 4px; border-radius: 2px; background: #A3A9B1"></span><span style="width: 4px; height: 4px; border-radius: 2px; background: #A3A9B1"></span></div>
    </div>
  </div>
  <div style="position: relative; flex-shrink: 0; background: #FFFFFF; border-top: 1px solid #D5D8DD; padding: 12px 16px 24px; display: flex; flex-direction: column; gap: 12px">
    <div style="display: flex; align-items: center; justify-content: space-between">
      <div><div style="font-size: 15px; font-weight: 700">運費</div><div style="font-size: 13px; color: #3D444D">ⓘ 服務詳細說明</div></div>
      <div style="font-size: 14px">依實際配送里程計費</div>
    </div>
    <div style="display: flex; gap: 8px">
      <button type="button" aria-label="預約時間" style="width: 52px; height: 52px; border: 1px solid #D5D8DD; border-radius: 10px; background: #FFFFFF; padding: 0; display: flex; align-items: center; justify-content: center; color: #1F2328">{_CLOCK}</button>
      <a href="#" style="flex: 1; height: 52px; border-radius: 10px; background: #1F2328; color: #FFFFFF; font-size: 16px; font-weight: 700; display: flex; align-items: center; justify-content: center; text-decoration: none">開始預訂</a>
    </div>
  </div>
</div>'''

# 2-6 the designer's home page with the banner block
_TAG = '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" style="flex-shrink: 0"><path d="M3 12V4h8l10 10-8 8z"></path><circle cx="7.5" cy="8.5" r="1.5"></circle></svg>'
def promo_row(expanded):
    # gray bar; the page ground is #F4F4F5, so the bar uses the next gray step to stay visible
    d = "M6 15l6-6 6 6" if expanded else "M6 9l6 6 6-6"
    return (f'<button type="button" aria-expanded="{"true" if expanded else "false"}" aria-label="快遞專屬優惠，{"收起" if expanded else "展開"}" style="flex-shrink: 0; min-height: 48px; border: 0; border-radius: 10px; background: #E6E8EB; padding: 0 12px 0 14px; font: inherit; font-size: 14px; font-weight: 500; color: #1F2328; display: flex; align-items: center; gap: 8px">'
            + _TAG + '<span style="flex: 1; text-align: left">快遞專屬優惠</span>'
            f'<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0"><path d="{d}"></path></svg></button>')
CODE_BAR = ('<div style="height: 48px; box-sizing: border-box; background: #FFFFFF; border: 1px solid #C9CDD3; border-top: 0; border-radius: 0 0 10px 10px; '
            'padding: 0 6px 0 12px; display: flex; align-items: center; gap: 8px">'
            '<div style="font-size: 13px; color: #5B6470; flex-shrink: 0">序號</div>'
            '<div style="flex: 1; min-width: 0; font-size: 15px; font-weight: 700; letter-spacing: 1px">[ABCD1234]</div>'
            '<button type="button" style="height: 36px; border: 1px solid #1F2328; border-radius: 18px; background: #FFFFFF; font: inherit; font-size: 13px; font-weight: 700; color: #1F2328; padding: 0 12px">複製序號</button></div>')
def promo_open(ratio="5:2", code=False):
    # the banner block, open: header on top, banners inside the same gray block, no page dots
    w = 280; h = {"5:2": 112, "2:1": 140}[ratio]
    def card(label):
        img = (f'<div style="position: relative; height: {h}px; box-sizing: border-box; background: #F4F4F5; border: 1px solid #C9CDD3; border-radius: {"10px 10px 0 0" if code else "10px"}; '
               f'display: flex; align-items: center; justify-content: center; font-size: 14px; color: #5B6470">{label}'
               '<div style="position: absolute; left: 8px; top: 8px; font-size: 11px; font-weight: 700; background: #FFFFFF; color: #1F2328; border-radius: 4px; padding: 1px 6px">優惠</div></div>')
        return f'<div style="flex-shrink: 0; width: {w}px; display: flex; flex-direction: column">{img}{CODE_BAR if code else ""}</div>'
    head = promo_row(True).replace("border-radius: 10px; background: #E6E8EB;", "background: none;")
    return ('<section aria-label="快遞專屬優惠，第 1 張，共 3 張" style="flex-shrink: 0; background: #E6E8EB; border-radius: 10px; overflow: hidden; display: flex; flex-direction: column">'
            + head + '<div style="padding: 0 0 12px 12px"><div style="display: flex; gap: 8px">'
            + card(f"[車隊上傳的優惠圖 {ratio}]") + card("[第 2 張]") + '</div></div></section>')
def entry(ratio="5:2", code=False):
    return clip(rep(s1, LIMIT_BOX, LIMIT_BOX + "\n    " + promo_open(ratio, code)))
e52 = entry()
e21 = entry("2:1")
ec = entry(code=True)
filled = clip(rep(s4, LIMIT_BOX, LIMIT_BOX + "\n    " + promo_row(False)))
opened = rep(clip(rep(s4, LIMIT_BOX, LIMIT_BOX + "\n    " + promo_open())), CONTENT + '; overflow: hidden', CONTENT + '; overflow: hidden; justify-content: flex-end')

items = [
    ("1 現行做法", CURRENT,
     "照現行畫面畫成灰階。1:4 的輪播 banner 在卡片下方，有頁數點點；高度不到 90，圖上的字很小。看起來像能點，實際點了沒有反應。"),
    ("2 入口：展開的優惠區塊（建議）", e52,
     "兩個地址還沒填完，是吸引下單的時刻：優惠區塊預設展開，放在物品限制下方（物品限制規則不放在廣告下方），與第 4 頁同一個灰底區塊。banner 5:2，約 280 × 112。一次一張、可手動滑，右側露出下一張；不放頁數點點、不自動播放，每次進入輪流換第一張，讓各車隊公平曝光。「優惠」標籤由 App 疊上。在 iPhone SE 這類小螢幕，區塊會被裁到畫面下緣，要往下滑才看得完整。"),
    ("3 地址填完：收成一行", filled,
     "送件地址填完後，付款與發票出現，banner 收成物品限制下方的一條灰底「快遞專屬優惠」，不顯示圖片、不寫張數，右側只有展開圖示，送出前不搶注意力。不完全藏起來：內容是序號時，使用者還找得到。運費與主按鈕的折後價是計價規則，與 banner 無關。"),
    ("4 點開「快遞專屬優惠」", opened,
     "在原地展開同一組 banner，banner 放在同一個灰底區塊裡，不跳頁、不是連結；頁面捲到 banner 的位置（畫面上方被捲出）。廣告改為 5:2（約 280 × 112），比 3:1 窄一點、高一點；不放頁數點點，靠右側露出的下一張暗示可滑。與入口同一個區塊、同一個比例，車隊只做一份素材。再點一次（收起圖示）回到第 3 頁。"),
    ("5 比較：banner 改 2:1", e21,
     "同第 2 頁，banner 改 2:1，約 280 × 140，比 5:2 高約 30；區塊更搶眼，小螢幕上大半會在畫面外。給需求方看「更大」的樣子。"),
    ("6 內容是序號優惠時", ec,
     "車隊上架時有選填序號文字，banner 下方才多一列序號與「複製序號」；沒填就只顯示圖片。圖片本身仍不能點，與第 2 頁同一個區塊。複製後到「付款與優惠」兌換（兌換畫面待補）。"),
]

SW, SH, PITCH, X0, Y = 390, 844, 540, 96, 340
W = X0 * 2 + PITCH * (len(items) - 1) + SW
H = Y + SH + 260
labels, extra = [], []
def lab(left, top, width, text, size=15, lh=20, color="#3D444D", weight=400):
    labels.append(f'<div style="position: absolute; left: {left}px; top: {top}px; width: {width}px; font-size: {size}px; line-height: {lh}px; font-weight: {weight}; color: {color}">{text}</div>')
screens = []
for i, (title, body, cap) in enumerate(items):
    x = X0 + i * PITCH
    body = re.sub(r'href="[^"#]*\.dc\.html"', 'href="#"', body)
    body = re.sub(r'\bid="([\w-]+)"', lambda m: f'id="{m.group(1)}-ad{i+1}"', body)
    body = re.sub(r'\bfor="([\w-]+)"', lambda m: f'for="{m.group(1)}-ad{i+1}"', body)
    screens.append(f'<div style="position: absolute; left: {x}px; top: {Y}px; width: {SW}px; height: {SH}px; outline: 1px solid #C9CDD3">\n{body}\n</div>')
    lab(x, Y - 40, SW + 100, title, size=20, lh=28, color="#1F2328", weight=700)
    lab(x, Y + SH + 24, SW, cap, size=15, lh=22)
# arrow 2 -> 3
x1, x2, ay = X0 + PITCH + SW, X0 + 2 * PITCH - 1, Y + 422
extra.append(f'<svg role="img" aria-label="從入口到地址填完：填完送件地址" width="{x2-x1}" height="8" viewBox="0 0 {x2-x1} 8" style="position: absolute; left: {x1}px; top: {ay-4}px; overflow: visible; fill: none; stroke: #5B6470; stroke-width: 2; stroke-linecap: round">'
             f'<defs><marker id="dc-arrow-head-filled-ad1" orient="auto" markerWidth="5" markerHeight="5" refX="2" refY="2" overflow="visible"><path d="M0 0 L4 2 L0 4 Z" style="stroke: none; fill: #5B6470"></path></marker></defs>'
             f'<path d="M 0 4 L {x2-x1-4} 4" marker-end="url(#dc-arrow-head-filled-ad1)"></path></svg>')
lab(x1 + 8, ay - 48, 134, "填完送件地址", size=15, lh=20)
x1, x2 = X0 + 2 * PITCH + SW, X0 + 3 * PITCH - 1
extra.append(f'<svg role="img" aria-label="從地址填完到展開：點快遞專屬優惠" width="{x2-x1}" height="8" viewBox="0 0 {x2-x1} 8" style="position: absolute; left: {x1}px; top: {ay-4}px; overflow: visible; fill: none; stroke: #5B6470; stroke-width: 2; stroke-linecap: round">'
             f'<defs><marker id="dc-arrow-head-filled-ad2" orient="auto" markerWidth="5" markerHeight="5" refX="2" refY="2" overflow="visible"><path d="M0 0 L4 2 L0 4 Z" style="stroke: none; fill: #5B6470"></path></marker></defs>'
             f'<path d="M 0 4 L {x2-x1-4} 4" marker-end="url(#dc-arrow-head-filled-ad2)"></path></svg>')
lab(x1 + 8, ay - 48, 134, "點快遞專屬優惠", size=15, lh=20)
# separators: current | proposal | comparison
for k in (1, 4):
    sx = X0 + k * PITCH - (PITCH - SW) // 2
    extra.append(f'<div aria-hidden="true" style="position: absolute; left: {sx}px; top: {Y - 60}px; width: 0; height: {SH + 260}px; border-left: 2px dashed #D5D8DD"></div>')
lab(X0, 96, W - 2 * X0, "廣告版位｜快遞首頁的 banner：比例與位置的比較", size=36, lh=48, color="#1F2328", weight=700)
lab(X0, 148, W - 2 * X0, "banner 由合作車隊自行上架、不能點，內容不一定是序號優惠。版位規則不假設內容：入口放大、地址填完收成一行、不自動播放、只收靜態圖。以「我的版本」A 列第 1、4 頁為底。", size=18, lh=26, color="#5B6470")

html = f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<title>廣告版位比較</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
body{{margin:0}}
a{{color:#1F2328}}a:hover{{color:#000000}}
</style>
</helmet>
<div style="position: relative; width: {W}px; height: {H}px; background: #FFFFFF; font-family: 'Noto Sans TC', system-ui, sans-serif; color: #1F2328">
{chr(10).join(extra)}
{chr(10).join(screens)}
{chr(10).join(labels)}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{H}}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''
open(f"{P}/AdSlot.dc.html", "w", encoding="utf-8").write(html)
print(len(html), "bytes;", W, "x", H)
