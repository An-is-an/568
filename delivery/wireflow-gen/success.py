# ---------- order sent: the current app's page, redrawn in wireframe gray (out of scope, not redesigned) ----------
_X = '<svg aria-hidden="true" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 5l14 14M19 5L5 19"></path></svg>'
_WARN = '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0"><path d="M12 3.5L2.5 20h19z"></path><path d="M12 10v4.5"></path><path d="M12 17.5h.01"></path></svg>'
SUCCESS = f'''<div style="width: 390px; height: 844px; box-sizing: border-box; background: #FFFFFF; font-family: 'Noto Sans TC', system-ui, sans-serif; color: #1F2328; display: flex; flex-direction: column">
  <div style="height: 56px; flex-shrink: 0; display: flex; align-items: center; justify-content: flex-end; padding: 0 8px">
    <button type="button" aria-label="關閉" style="width: 44px; height: 44px; border: 0; background: none; padding: 0; display: flex; align-items: center; justify-content: center; color: #1F2328">{_X}</button>
  </div>
  <div style="flex: 1; min-height: 0; padding: 40px 20px 0; display: flex; flex-direction: column; align-items: center; gap: 12px; text-align: center">
    <div role="img" aria-label="現行插圖：手機地圖與機車騎士" style="width: 310px; height: 190px; box-sizing: border-box; border: 1px dashed #A3A9B1; border-radius: 8px; background: #F4F4F5; display: flex; align-items: center; justify-content: center; font-size: 14px; color: #5B6470">[現行插圖]</div>
    <h1 style="margin: 36px 0 0; font-size: 20px; font-weight: 700">您的訂單已送出</h1>
    <p style="margin: 0; font-size: 15px; line-height: 22px; color: #3D444D">您的訂單正在尋找騎士中，<br>最晚將於 <b style="color: #1F2328">30 分鐘</b> 後通知您結果。</p>
    <div style="align-self: stretch; margin-top: 20px; background: #F4F4F5; border-radius: 10px; padding: 14px 14px; display: flex; align-items: center; gap: 8px; text-align: left; font-size: 14px">{_WARN}<span>溫馨提醒，開啟推播可即時接收訂單狀態通知。</span></div>
  </div>
  <div style="flex-shrink: 0; border-top: 1px solid #E6E8EB; padding: 16px 16px 24px">
    {CTA.format("查看訂單")}
  </div>
</div>'''
