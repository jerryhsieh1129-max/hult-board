// usage: HP_PW='<password>' HP_SALT='<base64 salt>' node encrypt.js <public.json> <data.enc.json>
// PBKDF2-SHA256（600,000 次）＋ AES-256-GCM。鹽固定（換密碼才換），IV 每次隨機。
const fs = require('fs'), crypto = require('crypto');
const [inp, out] = process.argv.slice(2);
const pw = process.env.HP_PW, saltB64 = process.env.HP_SALT;
if (!pw || !saltB64 || !inp || !out) { console.error('missing HP_PW / HP_SALT / paths'); process.exit(1); }
const ITER = 600000, salt = Buffer.from(saltB64, 'base64');
const key = crypto.pbkdf2Sync(Buffer.from(pw, 'utf8'), salt, ITER, 32, 'sha256');
const iv = crypto.randomBytes(12);
const c = crypto.createCipheriv('aes-256-gcm', key, iv);
const ct = Buffer.concat([c.update(fs.readFileSync(inp)), c.final(), c.getAuthTag()]);
fs.writeFileSync(out, JSON.stringify({v: 1, kdf: 'PBKDF2-SHA256', iter: ITER, salt: saltB64, iv: iv.toString('base64'), ct: ct.toString('base64')}));
console.log(JSON.stringify({bytes: ct.length, iter: ITER}));
