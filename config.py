import os, time, re

id_pattern = re.compile(r'^.\d+$') 


class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "27394279")  # ⚠️ Required
    API_HASH  = os.environ.get("API_HASH", "90a9aa4c31afa3750da5fd686c410851") # ⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7492763086:AAGKmIggAREQZHGlVAc37SR1egEw-AH6Rys") # ⚠️ Required
    FORCE_SUB = os.environ.get('FORCE_SUB', 'The_TGguy') # ⚠️ Required
    AUTH_CHANNEL = int(FORCE_SUB) if FORCE_SUB and id_pattern.search(
    FORCE_SUB) else None
   
    # database config
    DB_URL  = os.environ.get("DB_URL", "mongodb+srv://python21java:8ZFGYMKJCqAPwsiO@filestore.f876hjv.mongodb.net/?retryWrites=true&w=majority&appName=Filestore")  # ⚠️ Required
    DB_NAME  = os.environ.get("DB_NAME","Bankao")  

    # Other Configs 
    ADMIN = int(os.environ.get("ADMIN", "1705634892")) # ⚠️ Required
    LOG_CHANNEL = int(os.environ.get('LOG_CHANNEL', '-1002953042083')) # ⚠️ Required
    DUMP_CHANNEL = int(os.environ.get('DUMP_CHANNEL', '-1002953042083'))
    
    BOT_UPTIME = BOT_UPTIME  = time.time()
    START_PIC = os.environ.get("START_PIC", "https://graph.org/file/15e82d7e665eccc8bd9c5.jpg")

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))


    caption = """
__**🎬 {0}**__
──────────────
**💾 Original:** __{1}__
**📦 Encoded:** __{2}__
**📉 Compression:** __{3}__
──────────────
*,⏱️ Downloaded:** __{4}__
**⏱️ Encoded:** __{5}__
**⏱️ Uploaded:** __{6}__
──────────────
"""

    dump = """
__**🎬 {0}**__
──────────────
**💾 Original:** __{1}__
**📦 Encoded:** __{2}__
**📉 Compression:** __{3}__
──────────────
*,👤 Mention:** {4}
**👤 ID:** `{5}`
──────────────
"""
