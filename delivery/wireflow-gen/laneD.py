# ---------- lane A2: returning user taps swap ----------
YD = 1824
d1 = s1
PICK_MISS = ('<a href="#" style="display: flex; gap: 12px; padding: 14px 16px; text-decoration: none; color: #1F2328; border: 2px dashed #1F2328; border-radius: 12px 0 0 0; margin: -1px">'
             '<div style="width: 10px; height: 10px; border-radius: 5px; background: #1F2328; margin-top: 7px; flex-shrink: 0"></div>'
             '<div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 4px">'
             '<div style="display: flex; align-items: center; gap: 8px"><div style="font-size: 13px; color: #5B6470">取件</div>' + CH_NEXT.format("尚未填寫") + '</div>'
             '<div style="font-size: 16px; color: #5B6470">要從哪裡寄？</div>'
             '<div style="font-size: 13px; color: #5B6470">寄件人：選好取件地址後填寫</div></div>' + CHEV + '</a>')
DROP_ME = ('<a href="#" style="display: flex; gap: 12px; padding: 14px 16px; text-decoration: none; color: #1F2328">'
           '<div style="width: 10px; height: 10px; box-sizing: border-box; border: 2px solid #1F2328; margin-top: 7px; flex-shrink: 0"></div>'
           '<div style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 4px">'
           '<div style="font-size: 13px; color: #5B6470">送件</div>'
           '<div style="font-size: 16px; font-weight: 500">[目前位置或上次地址]</div>'
           '<div style="font-size: 13px; color: #5B6470">收件人 [會員姓名]・[會員電話]</div></div>' + CHEV + '</a>')
d2, k = re.subn(r'<a href="AddressInput\.dc\.html" style="display: flex; gap: 12px; padding: 14px 16px;[^"]*">.*?</a>\s*<a href="AddressInput\.dc\.html"[^>]*>.*?</a>',
                lambda m: PICK_MISS.replace('border-radius: 12px 0 0 0', 'border-radius: 12px 12px 0 0') + DROP_ME, s1_base, count=1, flags=re.S); assert k == 1
d2 = swapify(d2)
d2 = rep(d2, "最愛與歷程，點一下帶入送件地址", "最愛與歷程，點一下帶入取件地址")
d2 = rep(d2, ">填寫送件地址</a>", ">填寫取件地址</a>")
d3 = (ROOT + hdr("設定地址") + inputs(field("pick", "取件", value="[輸入中的取件地址]", focus=True), field("drop", "送件", value="[目前位置或上次地址]"))
      + '<div style="flex: 1; min-height: 0; padding: 16px; display: flex; flex-direction: column; gap: 12px">' + MAPBTN + results()
      + '<div style="font-size: 13px; color: #5B6470">選好取件地址後，進入取件地址詳情。</div></div></div>')
d4 = detail("pick", "[選好的取件地址]")
d5 = V2R
for a_, b_ in [("寄件人 [會員姓名]・[會員電話]", "寄件人 [姓名]・[電話]"), ("收件人 [姓名]・[電話]", "收件人 [會員姓名]・[會員電話]"),
               ("[取件地址與樓層門牌]", "[選好的取件地址]"), ("[送件地址與樓層門牌]", "[目前位置或上次地址]")]:
    d5 = rep(d5, a_, b_)
laneD = [("1 快遞首頁（剛進入）", d1, "與 A 列第 1 頁相同。地址卡片右側是對調鈕。"),
         ("2 快遞首頁（對調後）", d2, "聯絡人跟著地址走：會員資料移到收件人，寄件人變空白。主按鈕依第一個缺的地址改成「填寫取件地址」，最愛與歷程改為帶入取件。地址卡片的變化已經夠明顯，不另外提示。"),
         ("3 地址輸入頁（填取件）", d3, "游標停在取件欄位，送件已是原本的地址。地址輸入頁不放對調鈕。"),
         ("4 取件地址詳情", d4, "使用者自己選的取件地址，經過取件地址詳情。寄件人不是會員本人，欄位空白，姓名與電話必填。"),
         ("5 快遞首頁（填完地址）", d5, "兩個地址都有，主按鈕變成「送出訂單・金額」，運費依對調後的地址重新計算。")]
edgesD = ["按對調", "點取件列或主按鈕", "選好取件地址", "確認", "送出訂單"]
for i, t in enumerate(edgesD):
    x1 = L(i) + SW; x2 = L(i + 1) - 1
    y = YD + 422
    arrows.append(H_(x1, x2, y, True, aria=f"按對調：從{laneD[i][0]}到" + (laneD[i+1][0] if i + 1 < len(laneD) else "A 列第 5 頁") + f"，{t}"))
    lab(x1 + 8, y - 8 - 20 * math.ceil(len(t) / 8), 134, t)
cyd = YD + 422
labels.append(f'<div style="position: absolute; left: {L(5)}px; top: {cyd - 72}px; width: 390px; height: 144px; box-sizing: border-box; padding: 16px 20px; display: flex; align-items: center; background: #FFFFFF; border: 2px solid #1F2328; border-radius: 12px; font-size: 16px; line-height: 24px"><span><b>接 A 列第 5 頁起</b><br>確認彈窗、送出成功與老用戶相同</span></div>')
arrows.append(H_(X0, W - X0, 1540, False))
place(laneD, YD, "d")
lab(X0, 1576, 4000, "A2｜老用戶按對調：請別人把東西寄給自己", size=36, lh=48, color="#1F2328", weight=700, align="left")
lab(X0, 1628, 4000, "聯絡人跟著地址走；主按鈕寫第一個缺的地址（填寫送件地址／填寫取件地址），兩個都有才是「送出訂單・金額」", size=18, lh=26, color="#5B6470", align="left")
