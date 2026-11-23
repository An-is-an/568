# ---------- lane C: first order, location off ----------
FONT = "font-family: 'Noto Sans TC', system-ui, sans-serif"
ROOT = f'<div style="width: 390px; height: 844px; box-sizing: border-box; background: #F4F4F5; {FONT}; color: #1F2328; display: flex; flex-direction: column">'
BACK = '<svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"></path></svg>'
PIN = '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#5B6470" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0"><path d="M12 21s-7-6.2-7-11a7 7 0 0114 0c0 4.8-7 11-7 11z"></path><circle cx="12" cy="10" r="2.5"></circle></svg>'
LOC = '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0"><path d="M21 3L3 10.5l7.5 2.5 2.5 7.5z"></path></svg>'
MAPBTN = ('<button type="button" style="height: 48px; border: 1px solid #D5D8DD; border-radius: 8px; background: #FFFFFF; font: inherit; font-size: 15px; color: #1F2328; display: flex; align-items: center; gap: 10px; padding: 0 14px">'
          + PIN.replace('stroke="#5B6470"', 'stroke="currentColor"') + '<span style="flex: 1; text-align: left">在地圖上選點</span><span style="font-size: 12px; color: #5B6470">選用</span></button>')
def hdr(title):
    return (f'<div style="height: 56px; flex-shrink: 0; background: #FFFFFF; display: flex; align-items: center; padding: 0 8px; gap: 4px">'
            f'<a href="#" aria-label="返回" style="width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; color: #1F2328">{BACK}</a>'
            f'<div style="font-size: 17px; font-weight: 700">{title}</div></div>')
def field(kind, label, value=None, placeholder="", focus=False):
    mark = ('<div style="width: 10px; height: 10px; border-radius: 5px; background: #1F2328; flex-shrink: 0"></div>' if kind == "pick"
            else '<div style="width: 10px; height: 10px; box-sizing: border-box; border: 2px solid #1F2328; flex-shrink: 0"></div>')
    box = ("background: #FFFFFF; border: 2px solid #1F2328" if focus else "background: #F4F4F5; border: 1px solid #D5D8DD")
    val = f' value="{value}"' if value else f' placeholder="{placeholder}"'
    return (f'<div style="display: flex; align-items: center; gap: 10px; height: 48px; box-sizing: border-box; padding: 0 12px; {box}; border-radius: 8px">{mark}'
            f'<label for="f{kind}" style="font-size: 13px; color: #5B6470; flex-shrink: 0">{label}</label>'
            f'<input id="f{kind}" type="text"{val} style="flex: 1; min-width: 0; border: 0; background: none; font: inherit; font-size: 15px; color: #1F2328; padding: 0"></div>')
SWAP = ''
def inputs(pick, drop):
    return (f'<div style="flex-shrink: 0; background: #FFFFFF; border-bottom: 1px solid #D5D8DD; padding: 4px 16px 16px; display: flex; align-items: center; gap: 12px">'
            f'<div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 8px">{pick}{drop}</div>{SWAP}</div>')
def results(n=3):
    rows = []
    for i in range(1, n + 1):
        b = "border-bottom: 1px solid #E6E8EB; " if i < n else ""
        rows.append(f'<a href="#" style="display: flex; align-items: center; gap: 12px; padding: 12px 16px; min-height: 44px; {b}text-decoration: none; color: #1F2328">{PIN}'
                    f'<div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px"><div style="font-size: 15px; font-weight: 500">[搜尋結果 {i} 的名稱]</div>'
                    f'<div style="font-size: 13px; color: #5B6470">[縣市・行政區]・[完整地址]</div></div></a>')
    return ('<div style="font-size: 13px; font-weight: 500; color: #5B6470; margin-top: 4px">搜尋結果</div>'
            '<div style="background: #FFFFFF; border: 1px solid #D5D8DD; border-radius: 12px; display: flex; flex-direction: column">' + "".join(rows) + '</div>')

# C1 hub, nothing known
c1 = (ROOT + '''
  <div style="height: 56px; flex-shrink: 0; background: #FFFFFF; border-bottom: 1px solid #D5D8DD; display: flex; align-items: center; padding: 0 8px; gap: 4px">
    <button type="button" aria-label="返回" style="width: 44px; height: 44px; border: 0; background: none; padding: 0; display: flex; align-items: center; justify-content: center; color: #1F2328">''' + BACK + '''</button>
    <div style="font-size: 17px; font-weight: 700">即時快遞</div>
  </div>
  <div style="flex: 1; min-height: 0; padding: 16px; display: flex; flex-direction: column; gap: 12px">
    <div style="font-size: 13px; font-weight: 500; color: #5B6470">配送地址</div>
    <div style="background: #FFFFFF; border: 1px solid #D5D8DD; border-radius: 12px; display: flex; flex-direction: column">
      <a href="#" style="display: flex; gap: 12px; padding: 14px 16px; text-decoration: none; color: #1F2328; border: 2px dashed #1F2328; border-radius: 12px 12px 0 0; margin: -1px">
        <div style="width: 10px; height: 10px; border-radius: 5px; background: #1F2328; margin-top: 7px; flex-shrink: 0"></div>
        <div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 4px">
          <div style="display: flex; align-items: center; gap: 8px"><div style="font-size: 13px; color: #5B6470">取件</div>''' + CH_NEXT.format("尚未填寫") + '''</div>
          <div style="font-size: 16px; color: #5B6470">要從哪裡寄？</div>
          <div style="font-size: 13px; color: #5B6470">寄件人 [會員姓名]・[會員電話]</div>
        </div>''' + CHEV + '''
      </a>
      <a href="#" style="display: flex; gap: 12px; padding: 14px 16px; text-decoration: none; color: #1F2328">
        <div style="width: 10px; height: 10px; box-sizing: border-box; border: 2px solid #1F2328; margin-top: 7px; flex-shrink: 0"></div>
        <div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 4px">
          <div style="display: flex; align-items: center; gap: 8px"><div style="font-size: 13px; color: #5B6470">送件</div>''' + CH_OUT.format("尚未填寫") + '''</div>
          <div style="font-size: 16px; color: #5B6470">要送到哪裡？</div>
        </div>''' + CHEV + '''
      </a>
    </div>
    ''' + LIMIT_BOX + '''
    <a href="#info" style="font-size: 13px; font-weight: 500; min-height: 44px; display: flex; align-items: center">計費方式與服務說明</a>
  </div>
  <div style="flex-shrink: 0; background: #FFFFFF; border-top: 1px solid #D5D8DD; padding: 12px 16px 24px; display: flex; flex-direction: column; gap: 12px">
    <div style="display: flex; align-items: center; justify-content: space-between"><div style="font-size: 15px">運費</div><div style="font-size: 14px; color: #5B6470">填完配送地址後顯示</div></div>
    ''' + CTA.format("填寫配送地址") + '''
  </div>
</div>''')
c1 = swapify(c1)

USE_LOC = ('<button type="button" style="min-height: 56px; border: 1px solid #D5D8DD; border-radius: 8px; background: #FFFFFF; font: inherit; color: #1F2328; display: flex; align-items: center; gap: 10px; padding: 8px 14px; text-align: left">'
           + LOC + '<span style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px"><span style="font-size: 15px; font-weight: 500">使用目前位置</span>'
           '<span style="font-size: 12px; color: #5B6470">需要開啟定位權限</span></span></button>')
c2 = (ROOT + hdr("設定地址") + inputs(field("pick", "取件", placeholder="輸入取件地址或地標", focus=True), field("drop", "送件", placeholder="輸入送件地址"))
      + '<div style="flex: 1; min-height: 0; padding: 16px; display: flex; flex-direction: column; gap: 12px">' + USE_LOC + MAPBTN
      + '<div style="font-size: 13px; color: #5B6470">輸入地址或地標後，從搜尋結果選擇。</div></div></div>')

c3 = ('<div style="width: 390px; height: 844px; position: relative; overflow: hidden">' + c2
      + '<div aria-hidden="true" style="position: absolute; top: 0; right: 0; bottom: 0; left: 0; background: rgba(31, 35, 40, 0.45)"></div>'
      + f'<section aria-label="系統詢問定位權限" style="position: absolute; left: 50px; top: 250px; width: 290px; box-sizing: border-box; background: #FFFFFF; border-radius: 14px; overflow: hidden; {FONT}; color: #1F2328; text-align: center">'
      + '<div style="padding: 20px 16px 16px; display: flex; flex-direction: column; gap: 8px">'
      + '<div style="font-size: 16px; font-weight: 700; line-height: 22px">允許「[App 名稱]」使用你的位置？</div>'
      + '<div style="font-size: 13px; line-height: 18px; color: #3D444D">[用途說明，例如：用來帶入取件地址]</div></div>'
      + "".join(f'<button type="button" style="display: block; width: 100%; min-height: 48px; border: 0; border-top: 1px solid #D5D8DD; background: #FFFFFF; font: inherit; font-size: 16px; font-weight: {w}; color: #1F2328">{t}</button>'
                for t, w in [("使用 App 期間允許", 700), ("允許一次", 500), ("不允許", 500)])
      + '</section></div>')

NOTICE = ('<div style="background: #FFFFFF; border: 1px solid #D5D8DD; border-radius: 12px; padding: 12px 14px; display: flex; gap: 10px">'
          + LOC + '<div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 4px">'
          '<div style="font-size: 14px; font-weight: 700">定位未開啟，無法帶入目前位置</div>'
          '<div style="font-size: 13px; color: #3D444D">可以直接搜尋地址，或到設定開啟定位。</div>'
          '<a href="#settings" style="font-size: 14px; font-weight: 500; min-height: 32px; display: flex; align-items: center">前往設定</a></div></div>')
c4 = (ROOT + hdr("設定地址") + inputs(field("pick", "取件", value="[輸入中的取件地址]", focus=True), field("drop", "送件", placeholder="輸入送件地址"))
      + '<div style="flex: 1; min-height: 0; padding: 16px; display: flex; flex-direction: column; gap: 12px">' + NOTICE + MAPBTN + results() + '</div></div>')
c5 = (ROOT + hdr("設定地址") + inputs(field("pick", "取件", value="[選好的取件地址]"), field("drop", "送件", value="[輸入中的送件地址]", focus=True))
      + '<div style="flex: 1; min-height: 0; padding: 16px; display: flex; flex-direction: column; gap: 12px">' + MAPBTN + results()
      + '<div style="font-size: 13px; color: #5B6470">選好送件地址後，進入地址詳情頁。</div></div></div>')
# ---------- lane A side page: pickup detail with editable sender ----------
pk = detail("pick", "[取件地址]", "member")
pkC = rep(pk, "[取件地址]", "[選好的取件地址]")
c6 = f3
c7 = rep(f4, "[目前位置]", "[選好的取件地址]")

laneC = [("1 快遞首頁（第一次進入、沒開定位）", c1, "沒有目前位置也沒有上次地址，取件和送件都標「尚未填寫」。主按鈕寫「填寫配送地址」，點了進地址輸入頁，游標停在第一個缺的欄位（取件）。一進來不要求定位權限。"),
         ("2 地址輸入頁（先填取件）", c2, "游標先停在取件欄位。點「使用目前位置」才要求定位權限；之前拒絕過的人點了不會再跳系統詢問，直接出現第 4 頁的提示。"),
         ("3 系統詢問定位權限", c3, "系統對話框，用途說明由 App 提供。只給大概位置時不自動帶入，只用來排序搜尋結果和當地圖起點。"),
         ("4 地址輸入頁（定位未開啟）", c4, "不擋路：說明定位未開啟並給前往設定的入口，同時可以直接搜尋。搜尋結果一定顯示縣市和行政區。"),
         ("5 取件地址詳情", pkC, "取件地址是使用者自己選的，一定經過這一頁：補樓層門牌，寄件人預設帶入會員資料、可以修改，要改回本人按「填入我的資料」。欄位最後有「加入最愛」，按確認時地址、樓層與寄件人一起存入最愛。按確認回到地址輸入頁。Q2"),
         ("6 地址輸入頁（選好取件）", c5, "取件已填好，游標自動跳到送件欄位。允許定位的人帶入目前位置後也到這一頁，不經過取件地址詳情。"),
         ("7 地址詳情頁（送件）", c6, "與 B 列第 3 頁相同。"),
         ("8 快遞首頁（填完地址）", c7, "取件的樓層門牌與寄件人已在第 5 頁確認過。其餘與 B 列第 4 頁相同。")]
edgesC = ["點取件列或主按鈕", "點使用目前位置", "不允許", "選好取件地址", "確認", "選好送件地址", "確認", "送出訂單"]
Y3 = 4624
for i, t in enumerate(edgesC):
    x1 = L(i) + SW; x2 = L(i + 1) - 1
    y = Y3 + 422
    arrows.append(H_(x1, x2, y, True, aria=f"沒開定位：從{laneC[i][0]}到" + (laneC[i+1][0] if i + 1 < len(laneC) else "B 列第 5 頁") + f"，{t}"))
    lab(x1 + 8, y - 8 - 20 * math.ceil(len(t) / 8), 134, t)
# branch: allow (3 -> 5)
BYC = 4544
arrows.append(V_(L(2) + 340, BYC, Y3, False))
arrows.append(H_(L(2) + 340, L(5) + 340, BYC, False))
arrows.append(V_(L(5) + 340, BYC, Y3 - 1, True, aria="沒開定位：在系統詢問按允許，帶入目前位置，到地址輸入頁（選好取件）"))
lab(L(2) + 400, BYC - 28, 900, "允許：帶入目前位置當取件地址，跳到第 6 頁（自動帶入的取件不經過取件地址詳情）", align="left")
# connector card to lane B page 5
cy = Y3 + 422
labels.append(f'<div style="position: absolute; left: {L(8)}px; top: {cy - 84}px; width: 390px; height: 168px; box-sizing: border-box; padding: 16px 20px; display: flex; align-items: center; background: #FFFFFF; border: 2px solid #1F2328; border-radius: 12px; font-size: 16px; line-height: 24px"><span><b>接 B 列第 5 頁起</b><br>送出訂單後的欄位提示、付款與優惠、發票資訊、運送須知、確認彈窗、送出成功，都與第一次下單相同</span></div>')
arrows.append(H_(X0, W - X0, 4264, False))
place(laneC, Y3, "c")
lab(X0, 4320, 4000, "C｜第一次下單、沒開定位：沒有目前位置，也沒有上次地址", size=36, lh=48, color="#1F2328", weight=700, align="left")
lab(X0, 4372, 4000, "一進來不要求定位；點「使用目前位置」時才問。不開定位也能用搜尋或地圖填完", size=18, lh=26, color="#5B6470", align="left")

xP = L(7)
body = re.sub(r'href="[^"#]*\.dc\.html"', 'href="#"', pk)
body = re.sub(r'\bid="([\w-]+)"', lambda m: f'id="{m.group(1)}-ap"', body)
body = re.sub(r'\bfor="([\w-]+)"', lambda m: f'for="{m.group(1)}-ap"', body)
screens.append(f'<div style="position: absolute; left: {xP}px; top: {Y1}px; width: {SW}px; height: {SH}px; outline: 1px solid #C9CDD3">\n{body}\n</div>')
lab(xP, Y1 - 40, SW + 100, "取件地址詳情（從第 4 頁點取件）", size=20, lh=28, color="#1F2328", weight=700, align="left")
lab(xP, Y1 + SH + 24, SW, "非必經，從快遞首頁點取件那一列進入。寄件人預設帶入會員資料，不另加標籤；可直接改成其他人或從通訊錄覆蓋，要改回本人按「填入我的資料」。欄位最後有「加入最愛」，按確認時地址、樓層與寄件人一起存入最愛。按確認回到第 4 頁。Q2", size=15, lh=22, align="left")
arrows.append(V_(L(3) + 360, 300, Y1, False))
arrows.append(H_(L(3) + 360, xP + 340, 300, False))
arrows.append(V_(xP + 340, 300, Y1 - 1, True, aria="老用戶：從快遞首頁（已填完）點取件那一列，到取件地址詳情"))
lab(L(3) + 420, 272, 360, "點取件列：修改樓層或寄件人", align="left")
