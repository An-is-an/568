import re, math, sys
P = sys.argv[1]  # project dir

def root(name):
    s = open(f"{P}/{name}", encoding="utf-8").read()
    a = s.index("</helmet>") + len("</helmet>")
    b = s.index("</x-dc>")
    return s[a:b].strip()

def rep(s, old, new, count=1):
    assert s.count(old) == count, (old[:80], s.count(old))
    return s.replace(old, new)

CH_NEXT = '<div style="font-size: 11px; font-weight: 700; background: #1F2328; color: #FFFFFF; border-radius: 4px; padding: 1px 6px">{}</div>'
CH_OUT = '<div style="font-size: 11px; font-weight: 700; border: 1px solid #1F2328; border-radius: 4px; padding: 0 5px; background: #FFFFFF">{}</div>'
QTAG = '<div style="display: inline-flex; align-items: center; height: 20px; padding: 0 7px; border-radius: 10px; background: #B45309; color: #FFFFFF; font-size: 11px; font-weight: 700">{}</div>'
CTA = '<a href="#" style="height: 52px; border-radius: 10px; background: #1F2328; color: #FFFFFF; font-size: 16px; font-weight: 700; display: flex; align-items: center; justify-content: center; text-decoration: none">{}</a>'
def hint(nxt, n):
    return ('<div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; font-size: 13px">'
            f'<div style="font-weight: 700">下一步：{nxt}</div><div style="color: #5B6470">還缺 {n} 項</div></div>\n    ')

# ---------- screens ----------
SWAP_SVG = '<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 4v16"></path><path d="M4 8l4-4 4 4"></path><path d="M16 20V4"></path><path d="M12 16l4 4 4-4"></path></svg>'
SWAP_BTN = ('<div style="position: relative; height: 0; z-index: 1">'
            '<button type="button" aria-label="取件與送件地址對調" style="position: absolute; right: 34px; top: -22px; width: 44px; height: 44px; border: 1px solid #D5D8DD; border-radius: 22px; background: #FFFFFF; padding: 0; display: flex; align-items: center; justify-content: center; color: #1F2328">'
            + SWAP_SVG.replace('width="22" height="22"', 'width="20" height="20"') + '</button></div>')
CARD_OPEN = '<div style="background: #FFFFFF; border: 1px solid #D5D8DD; border-radius: 12px; display: flex; flex-direction: column">'
def swapify(h):
    i = h.index(CARD_OPEN)
    m = re.compile(r'(</a>|</button>)(\s*)(<a |<button )').search(h, i)
    return h[:m.end(1)] + SWAP_BTN + h[m.end(1):]
INPUT_SWAP_RE = r'\s*<div style="flex-shrink: 0; display: flex; flex-direction: column; align-items: center; gap: 6px">.*?Q4</div>\s*</div>'
def noswap(h):
    h, k = re.subn(INPUT_SWAP_RE, '', h, count=1, flags=re.S); assert k == 1
    return h
LIMIT_BOX = ('<div style="background: #FFFFFF; border: 1px solid #D5D8DD; border-radius: 12px; padding: 12px 16px; display: flex; align-items: center; gap: 12px">'
             '<svg aria-hidden="true" width="30" height="30" viewBox="0 0 32 32" fill="none" stroke="#1F2328" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0">'
             '<circle cx="8" cy="23" r="3.5"></circle><circle cx="25" cy="23" r="3.5"></circle><path d="M3 18h11v-6H3z"></path><path d="M11.5 23h10l-2-11h-3"></path><path d="M20 12h4"></path></svg>'
             '<div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px">'
             '<div style="font-size: 15px; font-weight: 700">本服務由機車配送</div>'
             '<div style="font-size: 13px; color: #3D444D">包裹總重量 &lt; 15kg，長寬高皆 ≤ 40cm。</div></div></div>')
# Lane A (returning user)
s1 = root("Main.dc.html")
PAYSEC_A = r'\s*<div style="font-size: 13px; font-weight: 500; color: #5B6470; margin-top: 8px">付款與發票</div>.*?</svg>\s*</div>\s*</div>'
s1, k = re.subn(PAYSEC_A, '', s1, count=1, flags=re.S); assert k == 1 and "付款方式" not in s1
s1, k = re.subn(r'(\s*</div>\s*<div style="flex-shrink: 0; background: #FFFFFF; border-top: 1px solid #D5D8DD; padding: 12px 16px 24px; display: flex; flex-direction: column; gap: 12px">)',
                lambda m: "\n    " + LIMIT_BOX + m.group(1), s1); assert k == 1
s1_base = s1
s1 = swapify(s1)
s2 = noswap(root("AddressInput.dc.html"))
SAVE_BTN = ('<button type="button" aria-pressed="false" style="align-self: flex-start; margin-top: -8px; min-height: 44px; border: 0; background: none; padding: 0 4px; font: inherit; font-size: 14px; font-weight: 500; color: #1F2328; display: flex; align-items: center; gap: 6px">'
            '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 3.5l2.6 5.3 5.9.9-4.2 4.1 1 5.8-5.3-2.8-5.3 2.8 1-5.8-4.2-4.1 5.9-.9z"></path></svg>'
            '加入最愛</button>\n\n    ')
def add_save(body):
    old = '修改</a>\n    </div>\n\n    '
    assert body.count(old) == 1
    return body.replace(old, old + SAVE_BTN)
Q1_RE = r'<div style="display: inline-flex[^"]*">Q1</div>\s*<div style="font-size: 12px; color: #5B6470">必填或選填，待確認</div>'
def required(h):
    h, k = re.subn(Q1_RE, '<div style="font-size: 12px; color: #5B6470">必填</div>', h); assert k == 1
    return h
s3 = rep(required(add_save(root("AddressDetail.dc.html"))), ">完成</a>", ">確認</a>")
V2R = root("V2HomeReady.dc.html")
V2R, k = re.subn(r'<a href="#limits"[^>]*>物品的材積與重量限制</a>', lambda m: LIMIT_BOX, V2R); assert k == 1
V2R, k = re.subn(r'\s*<div style="display: inline-flex[^"]*">Q5</div>', '', V2R); assert k == 1
V2R = swapify(V2R)
s4 = V2R
s5 = root("V2ConfirmSheet.dc.html")
s5, k = re.subn(r'\s*<div style="display: flex; align-items: center; gap: 8px">\s*<div style="flex: 1; min-width: 0; font-size: 13px; color: #5B6470">送出訂單即表示同意.*?Q6</div>\s*</div>', '', s5, flags=re.S)
assert k == 1
s6 = root("V2Success.dc.html")

# hub variants from V2HomeReady
P_OPEN = '<div style="display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-bottom: 1px solid #E6E8EB">\n        <div style="font-size: 15px; width: 72px; flex-shrink: 0">付款方式</div>'
P_OPEN_D = '<div style="display: flex; align-items: center; gap: 12px; padding: 12px 16px; border: 2px dashed #1F2328; margin: 0 -1px">\n        <div style="font-size: 15px; width: 72px; flex-shrink: 0">付款方式</div>'
I_OPEN = '<div style="display: flex; align-items: center; gap: 12px; padding: 12px 16px">\n        <div style="font-size: 15px; width: 72px; flex-shrink: 0">發票資訊</div>'
I_OPEN_D = '<div style="display: flex; align-items: center; gap: 12px; padding: 12px 16px; border: 2px dashed #1F2328; border-radius: 0 0 12px 12px; margin: -1px">\n        <div style="font-size: 15px; width: 72px; flex-shrink: 0">發票資訊</div>'
VAL = '<div style="flex: 1; min-width: 0; font-size: 15px; color: #5B6470; text-align: right">{}</div>'
def chipval(*parts):
    return '<div style="flex: 1; min-width: 0; display: flex; justify-content: flex-end; align-items: center; gap: 8px">' + "".join(parts) + '</div>'
SET = '<div style="flex: 1; min-width: 0; font-size: 15px; color: #1F2328; text-align: right">{}</div>'
SEND_RE = r'<a href="V2ConfirmSheet\.dc\.html" style="height: 52px;[^"]*">送出訂單・\[折後價\]</a>'

CHEV = '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#5B6470" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0"><path d="M9 5l7 7-7 7"></path></svg>'
ERR_ICON = '<svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0"><circle cx="12" cy="12" r="9"></circle><path d="M12 7.5v5.5"></path><path d="M12 16.5h.01"></path></svg>'
def row(label, value_html, err=None, last=False):
    border = "" if last else "border-bottom: 1px solid #E6E8EB; "
    top = (f'<div style="display: flex; align-items: center; gap: 12px"><div style="font-size: 15px; width: 72px; flex-shrink: 0">{label}</div>'
           f'{value_html}{CHEV}</div>')
    e = (f'<div style="display: flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 500; color: #C62828">{ERR_ICON}{err}</div>' if err else "")
    return f'<div style="{border}padding: 12px 16px; display: flex; flex-direction: column; gap: 6px">{top}{e}</div>'
PAY_ROW_RE = re.escape(P_OPEN) + r'.*?</svg>\s*</div>'
INV_ROW_RE = re.escape(I_OPEN) + r'.*?</svg>\s*</div>'
def hub(pay, inv):
    s = rep(V2R, "[取件地址與樓層門牌]", "[目前位置]")
    pay_v = {"missing": chipval(CH_OUT.format("尚未綁定")),
             "error": chipval(CH_OUT.format("尚未綁定")),
             "card": SET.format("[卡別] •••• [末四碼]")}[pay]
    inv_v = {"missing": chipval(CH_OUT.format("尚未設定")),
             "error": chipval(CH_OUT.format("尚未設定")),
             "set": SET.format("手機條碼 [/ABC1234]")}[inv]
    pr = row("付款方式", pay_v, "請先綁定信用卡" if pay == "error" else None)
    ir = row("發票資訊", inv_v, "請先設定發票資訊" if inv == "error" else None, last=True)
    s, k = re.subn(PAY_ROW_RE, lambda m: pr, s, flags=re.S); assert k == 1
    s, k = re.subn(INV_ROW_RE, lambda m: ir, s, flags=re.S); assert k == 1
    return s

f1 = root("Bp1Home.dc.html")
PAYSEC_B = r'\s*<div style="font-size: 13px; font-weight: 500; color: #5B6470; margin-top: 8px">付款與發票</div>.*?</svg>\s*</a>\s*</div>'
f1, k = re.subn(PAYSEC_B, '', f1, count=1, flags=re.S); assert k == 1 and "付款方式" not in f1
f1, k = re.subn(r'<div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; font-size: 13px">\s*<div style="font-weight: 700">下一步：填寫送件地址</div>\s*<div style="color: #5B6470">還缺 3 項</div>\s*</div>\s*', '', f1); assert k == 1
f1 = rep(f1, ">繼續</a>", ">填寫送件地址</a>")
f1 = rep(f1, '<a href="#info"', LIMIT_BOX + '\n\n    <a href="#info"')
f1 = swapify(f1)
f2 = noswap(root("FtAddressInput.dc.html"))
f3 = rep(required(add_save(root("FtAddressDetail.dc.html"))), ">完成</a>", ">確認</a>")
f4 = hub("missing", "missing")
f4e = hub("error", "error")
f5 = '''<div style="width: 390px; height: 844px; box-sizing: border-box; background: #FFFFFF; font-family: 'Noto Sans TC', system-ui, sans-serif; color: #1F2328; display: flex; flex-direction: column">
  <div style="height: 56px; flex-shrink: 0; display: flex; align-items: center; padding: 0 8px; position: relative">
    <a href="#" aria-label="返回快遞首頁" style="width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; color: #1F2328">
      <svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"></path></svg>
    </a>
    <h1 style="position: absolute; left: 60px; right: 60px; margin: 0; text-align: center; font-size: 18px; font-weight: 700">付款與優惠</h1>
  </div>
  <section style="padding: 12px 16px 20px; display: flex; flex-direction: column; gap: 10px">
    <h2 style="margin: 0 0 0 -16px; padding-left: 12px; border-left: 4px solid #1F2328; font-size: 19px; font-weight: 700; line-height: 28px">付款方式</h2>
    <div style="font-size: 14px; color: #3D444D">綁定支付</div>
    <button type="button" style="height: 52px; border: 1px solid #D5D8DD; border-radius: 10px; background: #FFFFFF; font: inherit; font-size: 16px; font-weight: 500; color: #1F2328; display: flex; align-items: center; justify-content: center; gap: 8px">新增綁定支付
      <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"></path></svg>
    </button>
  </section>
  <div aria-hidden="true" style="height: 8px; flex-shrink: 0; background: #F4F4F5"></div>
  <section style="padding: 20px 16px; display: flex; flex-direction: column; gap: 10px">
    <h2 style="margin: 0 0 0 -16px; padding-left: 12px; border-left: 4px solid #1F2328; font-size: 19px; font-weight: 700; line-height: 28px">優惠折抵</h2>
    <div style="font-size: 14px; color: #3D444D">優惠券</div>
    <button type="button" style="min-height: 48px; border: 0; background: none; padding: 0; font: inherit; color: #1F2328; display: flex; align-items: center; gap: 12px; text-align: left">
      <svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" style="flex-shrink: 0"><path d="M3 6h18v4a2 2 0 000 4v4H3v-4a2 2 0 000-4z"></path><path d="M14 7v10" stroke-dasharray="2 2"></path></svg>
      <span style="flex: 1; min-width: 0; font-size: 16px; font-weight: 500">未選擇優惠券</span>
      <span style="font-size: 14px">變更</span>
      <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0"><path d="M9 5l7 7-7 7"></path></svg>
    </button>
  </section>
</div>'''
CARD_ROW = ('<label style="min-height: 56px; box-sizing: border-box; border: 2px solid #1F2328; border-radius: 10px; background: #FFFFFF; padding: 0 14px; display: flex; align-items: center; gap: 12px">'
            '<input type="radio" name="paycard" checked="checked" style="width: 22px; height: 22px; margin: 0; accent-color: #1F2328">'
            '<span style="flex: 1; min-width: 0; font-size: 16px; font-weight: 500">[卡別] •••• [末四碼]</span>'
            + QTAG.format("Q8") + '</label>\n    ')
PAY_LBL = '<div style="font-size: 14px; color: #3D444D">綁定支付</div>\n    '
f5b = rep(f5, PAY_LBL, PAY_LBL + CARD_ROW)
f5b = rep(f5b, '</section>\n</div>', '</section>\n  <div role="status" style="margin: auto 16px 24px; background: #1F2328; color: #FFFFFF; border-radius: 10px; padding: 0 16px; min-height: 48px; display: flex; align-items: center; font-size: 14px">已綁定，並選用這張卡</div>\n</div>')
f6 = hub("card", "error")
f7 = '''<div style="width: 390px; height: 844px; box-sizing: border-box; background: #FFFFFF; font-family: 'Noto Sans TC', system-ui, sans-serif; color: #1F2328; display: flex; flex-direction: column">
  <div style="height: 56px; flex-shrink: 0; display: flex; align-items: center; padding: 0 8px; position: relative">
    <a href="#" aria-label="返回快遞首頁" style="width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; color: #1F2328">
      <svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"></path></svg>
    </a>
    <h1 style="position: absolute; left: 60px; right: 60px; margin: 0; text-align: center; font-size: 18px; font-weight: 700">發票資訊</h1>
  </div>
  <div style="flex: 1; min-height: 0; padding: 12px 16px 16px; display: flex; flex-direction: column; gap: 14px">
    <fieldset style="margin: 0; padding: 0; border: 0; min-width: 0; display: flex; flex-direction: column; gap: 8px">
      <legend style="padding: 0 0 0 12px; margin: 0 0 8px -16px; border-left: 4px solid #1F2328; font-size: 19px; font-weight: 700; line-height: 28px">發票類型</legend>
      <div style="display: flex; flex-wrap: wrap; column-gap: 24px"><label style="display: flex; align-items: center; gap: 8px; min-height: 44px; font-size: 16px"><input type="radio" name="invtype" value="personal" checked="checked" style="width: 22px; height: 22px; margin: 0; accent-color: #1F2328">個人</label><label style="display: flex; align-items: center; gap: 8px; min-height: 44px; font-size: 16px"><input type="radio" name="invtype" value="company" style="width: 22px; height: 22px; margin: 0; accent-color: #1F2328">企業</label><label style="display: flex; align-items: center; gap: 8px; min-height: 44px; font-size: 16px"><input type="radio" name="invtype" value="carrier" style="width: 22px; height: 22px; margin: 0; accent-color: #1F2328">載具</label><label style="display: flex; align-items: center; gap: 8px; min-height: 44px; font-size: 16px"><input type="radio" name="invtype" value="donate" style="width: 22px; height: 22px; margin: 0; accent-color: #1F2328">捐贈</label></div>
    </fieldset>
    <ul style="margin: 0; padding: 0 0 0 20px; display: flex; flex-direction: column; gap: 4px; font-size: 13px; line-height: 20px; color: #3D444D">
      <li>發票開立後不主動提供紙本發票，將E-mail至您的電子信箱，敬請確認電子信箱是否填寫正確。</li>
      <li>系統會於開獎日翌日起後10日內自動幫您對獎，中獎後將E-mail通知您，並以郵局掛號寄出紙本發票作為兌獎憑證。</li>
      <li>提醒您，發票經開立後，不得任意改開企業發票。</li>
    </ul>
    <input type="email" aria-label="電子信箱" placeholder="請輸入電子信箱" style="height: 52px; box-sizing: border-box; border: 1px solid #D5D8DD; border-radius: 10px; background: #FFFFFF; font: inherit; font-size: 16px; color: #1F2328; padding: 0 16px">
  </div>
  <div style="flex-shrink: 0; border-top: 1px solid #E6E8EB; padding: 12px 16px 24px">
    <button type="button" disabled style="width: 100%; height: 52px; border: 0; border-radius: 10px; background: #E6E8EB; color: #5B6470; font: inherit; font-size: 16px; font-weight: 700">儲存變更</button>
  </div>
</div>'''
f8 = hub("card", "set")
f9 = root("FtNotice.dc.html")
f9 = rep(f9, "讀到最底部後才能送出訂單", "讀到最底部後才能按同意")
f9 = rep(f9, ">送出訂單・[折後價]</button>", ">我已閱讀並同意</button>")
f10 = root("FtNoticeDone.dc.html")
f10, k = re.subn(r'\s*<div style="display: flex; flex-direction: column; gap: 8px">\s*<div style="font-size: 13px; font-weight: 500; color: #5B6470">送出前確認</div>.*?\[折後價\]</div>\s*</div>\s*</div>', '', f10, flags=re.S); assert k == 1
f10, k = re.subn(r'<a href="FtSuccess\.dc\.html"[^>]*>我已閱讀，送出訂單・\[折後價\]</a>\s*<a href="FtHomeReady\.dc\.html"[^>]*>返回修改</a>', lambda m: CTA.format("我已閱讀並同意"), f10); assert k == 1
f10c = s5
f11 = root("FtSuccess.dc.html")

# ---------- layout ----------
W, H = 7612, 5724
SW, SH, PITCH, X0 = 390, 844, 540, 96
Y1, Y2 = 400, 3248
def L(i): return X0 + i * PITCH

laneA = [("1 快遞首頁（剛進入）", s1, "取件與寄件人已帶入，地址卡片右側有對調鈕。主按鈕直接寫「填寫送件地址」，不寫還缺幾項；付款與發票在送件地址設定完整前隱藏。物品限制從這一頁就顯示，沿用現行文字。Q2"),
         ("2 地址輸入頁", s2, "兩個地址同頁，這一頁只選地址，不放對調鈕。"),
         ("3 地址詳情頁（送件）", s3, "收件人併進這一頁，取消配送資訊頁；姓名與電話必填。地址下方可「加入最愛」，按確認時地址、樓層與收件人一起存進最愛。"),
         ("4 快遞首頁（已填完）", s4, "送件地址設定完整後，付款與發票才出現，帶入上次的設定。主按鈕變成「送出訂單・金額」。"),
         ("5 確認彈窗", s5, "只放地址、收件人與金額。老用戶已讀過運送須知，這裡不再放同意文字。「返回修改」回到第 4 頁。"),
         ("6 送出成功", s6, "寫明免費取消的期限並給取消入口。")]
laneB = [("1 快遞首頁（第一次進入）", f1, "沒有最愛與歷程，取件只帶入目前位置。主按鈕直接寫「填寫送件地址」；付款與發票在送件地址設定完整前隱藏。物品限制從這一頁就顯示，沿用現行文字。"),
         ("2 地址輸入頁（沒有歷程）", f2, "沒有歷程與最愛，直接列出搜尋結果。"),
         ("3 地址詳情頁（送件）", f3, "收件人只能手動填或從通訊錄帶入，姓名與電話必填。地址下方可「加入最愛」，下次出現在快遞首頁的最愛與歷程。"),
         ("4 快遞首頁（還沒綁卡）", f4, "送件地址設定完整後，付款與發票才出現，標「尚未綁定」「尚未設定」。主按鈕是「送出訂單・金額」，不會帶去綁卡或發票。註冊時填過信箱的會員，發票會帶入「個人・會員信箱」，不會缺發票。"),
         ("5 快遞首頁（按送出後提示）", f4e, "資料不全時按送出訂單不換頁，在付款與發票欄位下方出現紅字；使用者自己點欄位去補。"),
         ("6 付款與優惠（未綁定）", f5, "沿用現行的付款與優惠頁，從付款欄位進入。按「新增綁定支付」走現行綁卡流程（畫面待補）；完成、放棄或失敗都回到這一頁。沒綁卡就返回，回到第 5 頁，紅字仍在。"),
         ("7 付款與優惠（綁完卡）", f5b, "綁卡完成後回到這一頁，新卡已選上。已綁定時的樣子沒有現行截圖，先示意。按返回回到快遞首頁，已填資料保留。Q8 是否自動選用新卡待確認。"),
         ("8 快遞首頁（綁完卡）", f6, "付款帶入新卡，紅字消失；發票的紅字留著，直到設定完成。"),
         ("9 發票資訊", f7, "沿用現行的整頁發票資訊頁，先不調整做法。從發票欄位進入，填好後按儲存變更回到快遞首頁。"),
         ("10 快遞首頁（都設定好）", f8, "紅字都消失。第一次下單按送出訂單後，先讀運送須知，讀完再到確認彈窗。"),
         ("11 運送須知（尚未讀完）", f9, "第一次下單先讀運送須知；沒讀到底不能按同意（維持滑到底）。Q6"),
         ("12 運送須知（讀完）", f10, "讀到底後才能按「我已閱讀並同意」。這一頁只處理條款，不放訂單明細。"),
         ("13 確認彈窗", f10c, "與老用戶相同的確認彈窗。送出前看到的最後一個畫面就是訂單明細。"),
         ("14 送出成功", f11, "與老用戶相同。")]
edgesA = ["點送件列或主按鈕", "選好送件地址", "確認", "送出訂單", "確認送出"]
edgesB = ["點送件列或主按鈕", "選好送件地址", "確認", "送出訂單", "點付款方式", "新增綁定支付並綁定成功", "返回", "點發票資訊", "儲存變更", "送出訂單", "讀到底", "我已閱讀並同意", "確認送出"]

STROKE = "#5B6470"
mid = [0]
def svg_seg(left, top, w, h, d, head, aria, dashed=False):
    style = f"position: absolute; left: {left}px; top: {top}px; width: {w}px; height: {h}px; overflow: visible; fill: none; stroke: {STROKE}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round"
    if dashed: style += "; stroke-dasharray: 8 6"
    a11y = f'role="img" aria-label="{aria}"' if aria else 'aria-hidden="true"'
    defs = ""; me = ""
    if head:
        mid[0] += 1; mk = f"dc-arrow-head-filled-wf{mid[0]}"
        defs = f'<defs><marker id="{mk}" orient="auto" markerWidth="5" markerHeight="5" refX="2" refY="2" overflow="visible"><path d="M0 0 L4 2 L0 4 Z" fill="{STROKE}" stroke="none" style="stroke: none; fill: {STROKE}; fill: context-stroke; stroke-dasharray: none"/></marker></defs>'
        me = f' marker-end="url(#{mk})"'
    return f'<svg {a11y} width="{w}" height="{h}" viewBox="0 0 {w} {h}" preserveAspectRatio="none" style="{style}">{defs}<path d="{d}"{me}></path></svg>'
def H_(x1, x2, y, head, direction="right", aria=None, dashed=False):
    n = x2 - x1; hh = 4 if head else 0
    d = f"M 0 4 L {n-hh} 4" if direction == "right" else f"M {n} 4 L {hh} 4"
    return svg_seg(x1, y - 4, n, 8, d, head, aria, dashed)
def V_(x, y1, y2, head, direction="down", aria=None, dashed=False):
    n = y2 - y1; hh = 4 if head else 0
    d = f"M 4 0 L 4 {n-hh}" if direction == "down" else f"M 4 {n} L 4 {hh}"
    return svg_seg(x - 4, y1, 8, n, d, head, aria, dashed)

arrows, labels = [], []
def lab(left, top, width, text, size=15, lh=20, color="#3D444D", weight=400, align="center"):
    labels.append(f'<div style="position: absolute; left: {left}px; top: {top}px; width: {width}px; text-align: {align}; font-size: {size}px; line-height: {lh}px; font-weight: {weight}; color: {color}">{text}</div>')

def lane(items, edges, Y, prefix, back=None):
    for i, t in enumerate(edges):
        x1 = L(i) + SW; x2 = L(i + 1) - 1
        fwd_y = Y + 382 if back == i else Y + 422
        arrows.append(H_(x1, x2, fwd_y, True, aria=f"{prefix}從{items[i][0]}到{items[i+1][0]}：{t}"))
        lines = math.ceil(len(t) / 8)
        lab(x1 + 8, fwd_y - 8 - 20 * lines, 134, t)
    if back is not None:
        i, t = back
        y = Y + 462
        x1 = L(i) + SW + 1; x2 = L(i + 1)
        arrows.append(H_(x1, x2, y, True, "left", aria=f"{prefix}從{items[i+1][0]}回到{items[i][0]}：{t}"))
        lab(x1 + 7, y + 12, 134, t)

laneA_back = None
# lane A forward + back (5 -> 4)
for i, t in enumerate(edgesA):
    x1 = L(i) + SW; x2 = L(i + 1) - 1
    y = Y1 + (382 if i == 3 else 422)
    arrows.append(H_(x1, x2, y, True, aria=f"老用戶：從{laneA[i][0]}到{laneA[i+1][0]}，{t}"))
    lab(x1 + 8, y - 8 - 20 * math.ceil(len(t) / 8), 134, t)
yb = Y1 + 462; x1 = L(3) + SW + 1; x2 = L(4)
arrows.append(H_(x1, x2, yb, True, "left", aria="老用戶：從確認彈窗按返回修改，回到快遞首頁（已填完）"))
lab(x1 + 7, yb + 12, 134, "返回修改")
# lane A branches from screen 1 top
arrows.append(V_(360, 230, Y1, False, aria=None))
arrows.append(H_(360, L(3) + 300, 230, False, aria=None))
arrows.append(V_(L(3) + 300, 230, Y1 - 1, True, aria="老用戶：從快遞首頁點最愛或有聯絡人的歷程，直接到快遞首頁（已填完）"))
lab(500, 202, 560, "點最愛或有聯絡人的歷程：直接帶入地址與聯絡人，跳到第 4 頁", align="left")
arrows.append(V_(440, 300, Y1, False, aria=None))
arrows.append(H_(440, L(2) + 300, 300, False, aria=None))
arrows.append(V_(L(2) + 300, 300, Y1 - 1, True, aria="老用戶：從快遞首頁點尚無聯絡人的歷程，到地址詳情頁補聯絡人"))
lab(500, 272, 440, "點尚無聯絡人的歷程：帶入地址，到第 3 頁補聯絡人", align="left")

# lane B forward + back (5 -> 4)
for i, t in enumerate(edgesB):
    x1 = L(i) + SW; x2 = L(i + 1) - 1
    y = Y2 + (382 if i == 4 else 422)
    arrows.append(H_(x1, x2, y, True, aria=f"第一次下單：從{laneB[i][0]}到{laneB[i+1][0]}，{t}"))
    lab(x1 + 8, y - 8 - 20 * math.ceil(len(t) / 8), 134, t)
yb = Y2 + 462; x1 = L(4) + SW + 1; x2 = L(5)
arrows.append(H_(x1, x2, yb, True, "left", aria="第一次下單：沒綁卡就從付款與優惠返回，回到快遞首頁（按送出後提示）"))
lab(x1 + 7, yb + 12, 134, "沒綁卡就返回")
# bypass 3 -> 8
BY = 3144
arrows.append(V_(L(2) + 300, BY, Y2, False, dashed=True))
arrows.append(H_(L(2) + 300, L(9) + 300, BY, False, dashed=True))
arrows.append(V_(L(9) + 300, BY, Y2 - 1, True, aria="第一次下單：已綁過卡且有發票設定時，從地址詳情頁直接到快遞首頁（都設定好）", dashed=True))
lab(L(2) + 360, BY - 28, 700, "已綁過卡且有發票設定（例如叫車時設定過）：略過第 4～9 頁", align="left")

# divider
arrows.append(H_(X0, W - X0, 2964, False))

# ---------- screens ----------
screens = []
def place(items, Y, tag):
    for i, (title, body, cap) in enumerate(items):
        x = L(i)
        body = re.sub(r'href="[^"#]*\.dc\.html"', 'href="#"', body)
        body = re.sub(r'\bid="([\w-]+)"', lambda m: f'id="{m.group(1)}-{tag}{i+1}"', body)
        body = re.sub(r'\bfor="([\w-]+)"', lambda m: f'for="{m.group(1)}-{tag}{i+1}"', body)
        screens.append(f'<div style="position: absolute; left: {x}px; top: {Y}px; width: {SW}px; height: {SH}px; outline: 1px solid #C9CDD3">\n{body}\n</div>')
        lab(x, Y - 40, SW + 100, title, size=20, lh=28, color="#1F2328", weight=700, align="left")
        lab(x, Y + SH + 24, SW, cap, size=15, lh=22, align="left")
place(laneA, Y1, "a")
place(laneB, Y2, "b")

lab(X0, 96, 3000, "A｜老用戶：已綁卡、有上次的發票設定", size=36, lh=48, color="#1F2328", weight=700, align="left")
lab(X0, 148, 3000, "主路徑 6 頁；從最愛或歷程帶入時可略過地址頁", size=18, lh=26, color="#5B6470", align="left")
lab(X0, 3000, 3000, "B｜第一次下單：沒有歷程、沒綁過卡、沒有發票設定（最差情況）", size=36, lh=48, color="#1F2328", weight=700, align="left")
lab(X0, 3052, 3000, "主按鈕：第一步寫「填寫送件地址」，之後都是「送出訂單・金額」；資料不全時按下不換頁，在缺的欄位出現紅字", size=18, lh=26, color="#5B6470", align="left")

exec(open('laneC.py', encoding='utf-8').read())
exec(open('laneD.py', encoding='utf-8').read())
html = f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<title>我的版本完整 wireflow</title>
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
{chr(10).join(arrows)}
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
open(f"{P}/Wireflow.dc.html", "w", encoding="utf-8").write(html)
print(len(html), "bytes;", len(arrows), "arrow svgs;", mid[0], "heads")
