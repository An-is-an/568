# ---------- address detail page, Lalamove style: map on top, fields in a sheet below ----------
# exec'd from wireflow.py; uses CH_OUT and CTA from there.
_F = "font-family: 'Noto Sans TC', system-ui, sans-serif"
_FIELD = "height: 48px; box-sizing: border-box; border: 1px solid #D5D8DD; border-radius: 8px; background: #FFFFFF; font: inherit; font-size: 15px; color: #1F2328; padding: 0 12px"
_BACK = '<svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"></path></svg>'
_MAP = ('<svg aria-hidden="true" width="390" height="290" viewBox="0 0 390 290" style="position: absolute; left: 0; top: 0">'
        '<rect width="390" height="290" fill="#E6E8EB"></rect>'
        '<g fill="none" stroke="#FFFFFF" stroke-linecap="round">'
        '<path d="M-10 230 L400 120" stroke-width="22"></path>'
        '<path d="M120 -10 L170 300" stroke-width="12"></path>'
        '<path d="M-10 90 L250 40 L400 60" stroke-width="8"></path>'
        '<path d="M250 40 L300 300" stroke-width="8"></path>'
        '<path d="M30 300 L60 150 L170 130" stroke-width="6"></path></g>'
        '<g fill="#D5D8DD"><rect x="190" y="160" width="46" height="34" rx="3"></rect><rect x="40" y="40" width="60" height="30" rx="3"></rect>'
        '<rect x="300" y="190" width="54" height="40" rx="3"></rect></g></svg>')
_PIN = ('<svg aria-hidden="true" width="34" height="44" viewBox="0 0 34 44" style="position: absolute; left: 178px; top: 132px">'
        '<path d="M17 42s14-13.5 14-24A14 14 0 003 18c0 10.5 14 24 14 24z" fill="#1F2328"></path>'
        '<circle cx="17" cy="18" r="5.5" fill="#FFFFFF"></circle></svg>')
_LOCATE = ('<button type="button" aria-label="回到目前位置" style="position: absolute; right: 12px; bottom: 28px; width: 44px; height: 44px; border: 1px solid #D5D8DD; border-radius: 8px; background: #FFFFFF; padding: 0; display: flex; align-items: center; justify-content: center; color: #1F2328">'
           '<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="1.5" fill="currentColor"></circle><path d="M12 2v4M12 18v4M2 12h4M18 12h4"></path></svg></button>')
_CONTACTS = ('<button type="button" aria-label="從通訊錄帶入姓名與電話" style="width: 44px; height: 44px; border: 0; background: none; padding: 0; display: flex; align-items: center; justify-content: center; color: #1F2328">'
             '<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="3.5" width="14" height="17" rx="2"></rect><circle cx="12" cy="10" r="2.5"></circle><path d="M8 17c.6-2 2.1-3 4-3s3.4 1 4 3"></path></svg></button>')
_STAR = ('<button type="button" aria-pressed="false" style="align-self: flex-start; min-height: 44px; border: 0; background: none; padding: 0 4px 0 0; font: inherit; font-size: 14px; font-weight: 500; color: #1F2328; display: flex; align-items: center; gap: 6px">'
         '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 3.5l2.6 5.3 5.9.9-4.2 4.1 1 5.8-5.3-2.8-5.3 2.8 1-5.8-4.2-4.1 5.9-.9z"></path></svg>'
         '加入最愛</button>')

def detail(kind, addr, contact="empty"):
    """kind: 'drop' | 'pick'. contact: 'empty' (blank, required) | 'member' (prefilled with member data)."""
    pick = kind == "pick"
    title = "取件地址詳情" if pick else "送件地址詳情"
    who = "寄件人" if pick else "收件人"
    mark = ('<span aria-hidden="true" style="width: 10px; height: 10px; border-radius: 5px; background: #1F2328; flex-shrink: 0"></span>' if pick
            else '<span aria-hidden="true" style="width: 10px; height: 10px; box-sizing: border-box; border: 2px solid #1F2328; flex-shrink: 0"></span>')
    tag = '<span style="font-size: 12px; color: #5B6470">必填</span>'
    if contact == "member":
        phone = 'value="[會員電話]"'; name = 'value="[會員姓名]"'
    else:
        phone = f'placeholder="{who}手機號碼"'; name = f'placeholder="{who}姓名"'
    note = "給司機的取件說明" if pick else "給司機的說明"
    return f'''<div style="width: 390px; height: 844px; box-sizing: border-box; background: #FFFFFF; {_F}; color: #1F2328; display: flex; flex-direction: column; overflow: hidden">
  <div style="height: 290px; flex-shrink: 0; position: relative">
    {_MAP}
    <div style="position: absolute; left: 12px; right: 12px; top: 12px; min-height: 52px; box-sizing: border-box; background: #FFFFFF; border: 1px solid #D5D8DD; border-radius: 10px; display: flex; align-items: center; gap: 8px; padding: 0 4px 0 0">
      <a href="#" aria-label="返回地址輸入頁" style="width: 44px; height: 44px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; color: #1F2328">{_BACK}</a>
      {mark}
      <div style="flex: 1; min-width: 0; font-size: 15px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">{addr}</div>
      <a href="#" style="font-size: 14px; font-weight: 500; min-height: 44px; display: flex; align-items: center; padding: 0 8px">修改</a>
    </div>
    {_PIN}
    <div style="position: absolute; left: 0; right: 0; top: 182px; text-align: center; font-size: 12px; color: #3D444D">拖曳地圖微調位置</div>
    {_LOCATE}
  </div>
  <div style="flex: 1; min-height: 0; margin-top: -16px; position: relative; background: #FFFFFF; border-radius: 16px 16px 0 0; padding: 16px 16px 8px; display: flex; flex-direction: column; gap: 10px">
    <h1 style="margin: 0; font-size: 18px; font-weight: 700">{title}</h1>
    <input type="text" aria-label="樓層或門牌號碼，選填" placeholder="樓層或門牌號碼（選填）" style="{_FIELD}">
    <div style="display: flex; align-items: center; gap: 8px"><span style="font-size: 14px; font-weight: 700">{who}</span>{tag}<button type="button" style="margin-left: auto; min-height: 44px; border: 0; background: none; padding: 0 0 0 12px; font: inherit; font-size: 14px; font-weight: 500; color: #1F2328; text-decoration: underline; text-underline-offset: 3px">填入我的資料</button></div>
    <div style="display: flex; align-items: center; height: 48px; box-sizing: border-box; border: 1px solid #D5D8DD; border-radius: 8px; background: #FFFFFF; padding: 0 2px 0 12px">
      <input type="text" aria-label="{who}姓名" {name} style="flex: 1; min-width: 0; border: 0; background: none; font: inherit; font-size: 15px; color: #1F2328; padding: 0">
      {_CONTACTS}
    </div>
    <div style="display: flex; align-items: center; height: 48px; box-sizing: border-box; border: 1px solid #D5D8DD; border-radius: 8px; background: #FFFFFF; padding: 0 12px">
      <span style="font-size: 15px; color: #5B6470; padding-right: 8px">+886</span>
      <input type="tel" aria-label="{who}手機號碼" {phone} style="flex: 1; min-width: 0; border: 0; background: none; font: inherit; font-size: 15px; color: #1F2328; padding: 0">
    </div>
    <textarea aria-label="備註，選填" placeholder="{note}（選填）" style="height: 64px; box-sizing: border-box; border: 1px solid #D5D8DD; border-radius: 8px; background: #FFFFFF; font: inherit; font-size: 15px; color: #1F2328; padding: 10px 12px; resize: none"></textarea>
    <div style="font-size: 12px; color: #5B6470; margin-top: -4px">目前未開放代收代墊</div>
    {_STAR}
  </div>
  <div style="flex-shrink: 0; background: #FFFFFF; border-top: 1px solid #E6E8EB; padding: 12px 16px 24px">
    {CTA.format("確認")}
  </div>
</div>'''
