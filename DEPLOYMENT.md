# 🚀 Deployment Qo'llanmasi

Bot ishga tushunga tayyor! Quyidagi yo'llardan birini tanlang:

---

## 1️⃣ **Local Development** (Offline test)

```bash
# Virtual environment yarating
python3.11 -m venv venv
source venv/bin/activate

# Dependencies o'rnating
pip install -r requirements.txt

# Bot ishga tushiring
python bot.py
```

**Log output:**
```
✅ Bot ishga tushdi!
```

Bot polling mode'da ishlaydi va `zapchast.db`'ga o'zgarishlarni saqlaydi.

---

## 2️⃣ **Production Deployment** (Server)

### Option A: Systemd Service (Recommended)

1. **Service fayl yarating** (`/etc/systemd/system/isuzu-bot.service`):
```ini
[Unit]
Description=Isuzu Zapchast Bot
After=network.target

[Service]
Type=simple
User=bot_user
WorkingDirectory=/opt/isuzu_zapchast_bot
Environment="PATH=/opt/isuzu_zapchast_bot/venv/bin"
ExecStart=/opt/isuzu_zapchast_bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. **Enable va start qiling:**
```bash
sudo systemctl enable isuzu-bot
sudo systemctl start isuzu-bot
sudo systemctl status isuzu-bot
```

3. **Logs ko'ring:**
```bash
sudo journalctl -u isuzu-bot -f
```

---

### Option B: Docker (Advanced)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

**Build va run:**
```bash
docker build -t isuzu-bot .
docker run -d --name isuzu-bot --restart always isuzu-bot
```

---

### Option C: Screen/Tmux (Simple)

```bash
screen -S isuzu-bot
cd /path/to/project
source venv/bin/activate
python bot.py

# Ctrl+A, then D to detach
```

Check status:
```bash
screen -ls
screen -r isuzu-bot
```

---

## 🔒 Security Notes

- ⚠️ `.env` faylni **gitga commit qilmang** (`.gitignore`'da mavjud)
- ⚠️ BOT_TOKEN'ni server'da environment variable sifatida saqlang
- ⚠️ Database faylini (`zapchast.db`) backup qiling

---

## 📊 Database Backup

```bash
# SQLite backup qiling
cp zapchast.db zapchast.db.backup

# Cron job orqali avtomatik backup (har soat):
0 * * * * cp /path/to/zapchast.db /path/to/backups/zapchast_$(date +\%Y\%m\%d_\%H\%M\%S).db
```

---

## 📝 Log Management

Loglarni fayl sifatida saqlash uchun `bot.py`'ni o'zgartiring:

```python
import logging

logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

---

## ✅ Production Checklist

- [ ] `.env` faylida to'g'ri BOT_TOKEN mavjudmi?
- [ ] Virtual environment o'rnatilganmi?
- [ ] requirements.txt o'rnatilganmi?
- [ ] Database (`zapchast.db`) mavjudmi?
- [ ] Bot local'da ishlab ko'ringanmi?
- [ ] Server'ga SSH access mavjudmi?
- [ ] Systemd/Docker/Screen setup tayyor?
- [ ] Backup system ko'rmaylanganmi?

---

## 🆘 Troubleshooting

**Bot ishlamay qoldi:**
```bash
# Logs ko'ring
journalctl -u isuzu-bot -n 50

# Bot process restart qiling
systemctl restart isuzu-bot
```

**Database xatosi:**
```bash
# Database'ni reset qiling (eski qismlar yo'q bo'lib ketadi!)
rm zapchast.db
python bot.py  # Yangi database yaratadi
```

**Memory leak:**
```bash
# Bot process memory'sini monitor qiling
watch -n 1 'ps aux | grep python'
```

---

## 📞 Support

Agar muammo bo'lsa, quyidagi loglarni tekshiring:
- `systemd`: `journalctl -u isuzu-bot`
- `docker`: `docker logs isuzu-bot`
- `screen`: Screen ichida `/log` yoki STDOUT'ni ko'ring

---

**Happy deploying! 🎉**
