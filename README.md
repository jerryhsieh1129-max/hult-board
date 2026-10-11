# hult-board

中山大學 Hult Prize 幹部看板（需要密碼）。網頁會自動更新，資料在上傳前已用密碼加密（PBKDF2-SHA256 + AES-256-GCM），repo 裡只有加密後的內容。

Password-protected officer board for Hult Prize at NSYSU. The data is encrypted before upload; this repository only holds ciphertext.

- `index.html`：看板頁面（在瀏覽器裡用密碼解密）
- `data.enc.json`：加密後的資料，由排程定期更新
- `tools/`：產生與加密資料的腳本（不含密碼）
