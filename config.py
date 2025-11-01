import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Render Environment Variable’dan oladi

# 👇 bu ID seni Telegram’dagi admin sifatida tanitadi
# Admin ID ni olish uchun: @userinfobot ga yoz — u senga ID beradi
ADMIN_ID = int(os.getenv("ADMIN_ID", "6313092609"))  # bu yerda o‘zingning ID’ingni qo‘y
