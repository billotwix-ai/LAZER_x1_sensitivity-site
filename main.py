# ======================== IMPORTS =======================
import requests, os, jwt, json, binascii, time, urllib3, base64, re
import socket, threading, ssl, pytz, aiohttp, traceback, asyncio, subprocess
import datetime
from MG24GAMER import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2, sQ_pb2, Team_msg_pb2, RemoveFriend_Req_pb2, GetFriend_Res_pb2, spam_request_pb2, devxt_count_pb2, dev_generator_pb2, kyro_title_pb2, room_join_pb2
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import *; from xHeaders import *
from datetime import datetime
import urllib.parse
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import google.protobuf.json_format as json_format
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# ── auto-install phonenumbers if missing ──
try:
    import phonenumbers
except ImportError:
    subprocess.run(["pip", "install", "phonenumbers", "-q"], check=False)
    import phonenumbers

# =================== CONFIGURATION ======================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========= DNS FIX FOR FREEFIRE SERVERS =========
try:
    import dns.resolver as _dns_resolver
    _dns_res = _dns_resolver.Resolver()
    _dns_res.nameservers = ['8.8.8.8', '1.1.1.1']
    _orig_getaddrinfo = socket.getaddrinfo

    def _patched_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
        if isinstance(host, str) and 'freefiremobile.com' in host:
            try:
                answers = _dns_res.resolve(host, 'A')
                host = str(answers[0])
            except Exception:
                pass
        return _orig_getaddrinfo(host, port, family, type, proto, flags)

    socket.getaddrinfo = _patched_getaddrinfo
except ImportError:
    pass
# ================================================  

# =================== GLOBAL VARIABLES ===================
BOT_START_TIME = time.time()  # Tracks bot start time for /uptime command
online_writer = None
whisper_writer = None
spammer_uid = None
msg_spam_running = False
msg_spam_task = None
mg_spam_task = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
fast_spam_running = False
fast_spam_task = None
custom_spam_running = False
custom_spam_task = None
spam_request_running = False
spam_request_task = None
evo_fast_spam_running = False
evo_fast_spam_task = None
evo_custom_spam_running = False
evo_custom_spam_task = None
reject_spam_running = False
reject_spam_task = None
emote_hijack = False 
lag_running = False
lag_task = None
reject_spam_running = False
reject_spam_task = None
evo_cycle_running = False
_stdin_q = None
_stdin_thread_started = False
evo_cycle_task = None
status_response_cache = {} 
pending_status_requests = {}
room_info_cache = {}
last_status_packet = None
insquad = None 
joining_team = False 
online_writer = None 
whisper_writer = None 
last_bot_status_check = 0
senthi = False
squad_chat_authed = False        # True after bot has authenticated group chat once per join
squad_group_owner_uid = None     # UID of squad owner (for sending group messages)
squad_group_chat_code = None     # Chat code for the current group/squad
bot_status_cache_time = 30
cached_bot_status = None
last_status_packet = None
START_SPAM_DURATION = 18     
WAIT_AFTER_MATCH_SECONDS = 20 
START_SPAM_DELAY = 0.2       
region = 'PK'
WHITELISTED_UIDS = {
    "MĢ24_GÀMER", # don't change this text
    "415136165"
}
# ADMIN INFO FUNCTION FOR ADMIN COMMAND 
ADMIN_UID = "1901614992"
ADMIN_UIDS = {"1901614992" , ""}
BLOCKED_UIDS = set()  # UIDs blocked from using the bot
news_pending = {}  # Tracks which chat/uid is waiting for news country selection
_console_guild_chat_id = None   # Clan chat ID used for console → guild sending
_console_guild_bot_uid = None   # Bot's own UID for sending
_console_guild_chat_type = 1    # 1 = CLan chat type
_console_squad_chat_id = None   # Squad/group chat ID
_console_chat_target = "guild"  # "guild" or "group" — which chat console sends to
server2 = "BD"
key2 = "mg24"
BYPASS_TOKEN = "your_bypass_token_here"
YOUTUBE_API_KEY = "AIzaSyBVP3NiKKJvb-0ar2J3y9IFVVHHWRng4nA"
GEMINI_AI_API_KEY = "AIzaSyADPE-gPODMslNB6AElglDtBRv6PQDVChY"
GROQ_AI_API_KEY = None
OPENROUTER_AI_API_KEY = "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"
IG_SESSION_ID = ""  # Paste your Instagram sessionid cookie here to unlock private account stats
WHITELIST_ONLY = False
bot_enabled = True
_bot_jwt = None          # Holds the main bot JWT — reused for bio updates
BOT_OWNER_UID = 415136165  
BOT_SERVER_URL = None  # Set from login response — used for friend add/remove/list
PLAYER_NAME_CACHE = {}   # bounded below — evicts oldest when full
_PLAYER_NAME_CACHE_MAX = 500
freeze_running = False
freeze_task = None
FREEZE_EMOTES = [909052010, 909052010, 909052010]
FREEZE_DURATION = 10  # seconds
evo_emotes = {
    "1": "909000063",   # AK
    "2": "909000068",   # SCAR
    "3": "909000075",   # 1st MP40
    "4": "909040010",   # 2nd MP40
    "5": "909000081",   # 1st M1014
    "6": "909039011",   # 2nd M1014
    "7": "909000085",   # XM8
    "8": "909000090",   # Famas
    "9": "909000098",   # UMP
    "10": "909035007",  # M1887
    "11": "909042008",  # Woodpecker
    "12": "909041005",  # Groza
    "13": "909033001",  # M4A1
    "14": "909038010",  # Thompson
    "15": "909038012",  # G18
    "16": "909045001",  # Parafal
    "17": "909049010",  # P90
    "18": "909051003"   # m60
}
#------------------------------------------#

# Emote mapping for evo commands
EMOTE_MAP = {
    1: 909000063,
    2: 909000081,
    3: 909000075,
    4: 909000085,
    5: 909000134,
    6: 909000098,
    7: 909035007,
    8: 909051012,
    9: 909000141,
    10: 909034008,
    11: 909051015,
    12: 909041002,
    13: 909039004,
    14: 909042008,
    15: 909051014,
    16: 909039012,
    17: 909040010,
    18: 909035010,
    19: 909041005,
    20: 909051003,
    21: 909034001
}

# Animation map for /animation command
ANIMATION_MAP = {
    "arrival":    912038002,
    "parachute":  912039001,
    "backflip":   912040001,
    "roll":       912041001,
    "spin":       912042001,
    "slide":      912043001,
    "dash":       912044001,
    "jump":       912045001,
    "cartwheel":  912046001,
    "flip":       912047001,
    "dance1":     912048001,
    "dance2":     912049001,
    "dance3":     912050001,
    "salute":     912051001,
    "bow":        912052001,
    "wave":       912053001,
    "taunt":      912054001,
    "celebrate":  912055001,
    "fall":       912056001,
    "roll2":      912057001,
}

# Badge values for s1 to s8 commands - using your exact values
BADGE_VALUES = {
    "s1": 1048576,    # Your first badge
    "s2": 32768,      # Your second badge  
    "s3": 2048,       # Your third badge
    "s4": 64,         # Your fourth badge
    "s5": 262144     # Your seventh badge
}

# Admin Functions
def is_admin(uid):
    return str(uid) in ADMIN_UIDS

# Mute Functions 
def is_off():
    return not bot_enabled

def ff_num(val):
    return xMsGFixinG(str(val)) if val not in (None, "") else "N/A"

from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

def human_time(ts):
    try:
        ts = int(ts)
        if ts <= 0:
            return "N/A"
        bd_time = datetime.fromtimestamp(ts, ZoneInfo("Asia/Karachi"))
        return bd_time.strftime("%d %b %Y, %I:%M %p")
    except:
        return "N/A"

def titles():
    """Return all titles instead of just one random"""
    titles_list = [
        905090075, 904990072, 904990069, 905190079
    ]
    return titles_list  # Return the full list instead of random.choice            
    
def create_credentials_template():
    """Create a template credentials file"""
    template = """# Rijexx Free Fire Bot Credentials
# Fill in your Free Fire account credentials below

# Format 1: Comma-separated (RECOMMENDED)
uid=4263143059,password=2336099414_W0363_BY_SPIDEERIO_GAMING_WBYMF

# OR Format 2: Line-separated
# uid: 4263143059
# password: 2336099414_W0363_BY_SPIDEERIO_GAMING_WBYMF

# Save this file and restart the bot
"""
    
    filename = "MG24GAMER.txt"
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"📝 Created {filename} template file")
        print("✏️ Please edit it with your actual credentials")
        return False
    return True

async def fetch_news_rss(country_code):
    """Use Groq AI to generate a news summary for the given country (always in English)."""
    country_names = {
        "PK": "Pakistan",
        "UK": "United Kingdom",
        "US": "America",
    }
    country_name = country_names[country_code]
    today = datetime.now().strftime("%B %d, %Y")
    prompt = (
        f"Today is {today}. Give a brief news summary for {country_name}. "
        "Include 4-5 important topics or recent events happening in that country. "
        "Write in natural, conversational sentences. No bullet points. Keep it short. Write in English."
    )
    try:
        ai_summary = await asyncio.wait_for(
            talk_with_ai(prompt),
            timeout=60,
        )
        if not ai_summary:
            return "[B][C][FF0000]❌ Could not generate news. Try again later.", country_name
        return ai_summary, country_name
    except asyncio.TimeoutError:
        return "[B][C][FF0000]❌ News request timed out. Please try again.", country_name
    except Exception as e:
        return f"[B][C][FF0000]❌ Error fetching news: {str(e)}", country_name

da = 'f2212101'
dec = ['80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', '8e', '8f', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff']
x_list = ['01','01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2a', '2b', '2c', '2d', '2e', '2f', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e', '3f', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f']

def Decrypt_ID(da):
    """EXACT SAME as your code"""
    if da != None and len(da) == 10:
        w = 128
        xxx = len(da)/2 - 1
        xxx = str(xxx)[:1]
        for i in range(int(xxx)-1):
            w = w * 128
        x1 = da[:2]
        x2 = da[2:4]
        x3 = da[4:6]
        x4 = da[6:8]
        x5 = da[8:10]
        return str(w * x_list.index(x5) + (dec.index(x2) * 128) + dec.index(x1) + (dec.index(x3) * 128 * 128) + (dec.index(x4) * 128 * 128 * 128))

    if da != None and len(da) == 8:
        w = 128
        xxx = len(da)/2 - 1
        xxx = str(xxx)[:1]
        for i in range(int(xxx)-1):
            w = w * 128
        x1 = da[:2]
        x2 = da[2:4]
        x3 = da[4:6]
        x4 = da[6:8]
        return str(w * x_list.index(x4) + (dec.index(x2) * 128) + dec.index(x1) + (dec.index(x3) * 128 * 128))
    
    return None

def Encrypt_ID(x):
    """EXACT SAME as your code"""
    x = int(x)
    x = x / 128 
    if x > 128:
        x = x / 128
        if x > 128:
            x = x / 128
            if x > 128:
                x = x / 128
                strx = int(x)
                y = (x - int(strx)) * 128
                stry = str(int(y))
                z = (y - int(stry)) * 128
                strz = str(int(z))
                n = (z - int(strz)) * 128
                strn = str(int(n))
                m = (n - int(strn)) * 128
                return dec[int(m)] + dec[int(n)] + dec[int(z)] + dec[int(y)] + x_list[int(x)]
            else:
                strx = int(x)
                y = (x - int(strx)) * 128
                stry = str(int(y))
                z = (y - int(stry)) * 128
                strz = str(int(z))
                n = (z - int(strz)) * 128
                strn = str(int(n))
                return dec[int(n)] + dec[int(z)] + dec[int(y)] + x_list[int(x)]

def decrypt_api(cipher_text):
    """EXACT SAME as your code"""
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain_text = unpad(cipher.decrypt(bytes.fromhex(cipher_text)), AES.block_size)
    return plain_text.hex()

def encrypt_api(plain_text):
    """EXACT SAME as your code"""
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

def encrypt_message(plaintext_bytes):
    """EXACT SAME as your Flask API"""
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(plaintext_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded)
    return binascii.hexlify(encrypted).decode('utf-8')    

def create_uid_protobuf(uid):
    """EXACT SAME as your Flask API"""
    msg = dev_generator_pb2.dev_generator()
    msg.saturn_ = int(uid)
    msg.garena = 1
    return msg.SerializeToString()

def enc(uid):
    """EXACT SAME as your Flask API"""
    pb = create_uid_protobuf(uid)
    return encrypt_message(pb)

def decode_player_info(binary):
    """EXACT SAME as your Flask API"""
    info = devxt_count_pb2.xt()
    info.ParseFromString(binary)
    return info    
    
def load_jwt_token():
    """Load token from token.json"""
    try:
        with open("token.json", "r") as f:
            data = json.load(f)
        token = data.get("token")
        if token:
            print(f"✅ Loaded token: {token[:20]}...")
            return token
        else:
            print("❌ No token found in token.json")
            return None
    except Exception as e:
        print(f"❌ Error loading token: {e}")
        return None

def load_tokens_ind():
    """Load bulk tokens from token_ind.json"""
    try:
        with open("token_ind.json", "r") as f:
            tokens = json.load(f)
        print(f"📦 Loaded {len(tokens)} tokens from token_ind.json")
        return tokens
    except:
        print("❌ No tokens found in token_ind.json")
        return None



def normalize_player_data(data):
    """Normalize API response fields to the expected key format regardless of case/naming"""
    # Normalize top-level keys
    # Support both the FF API format (basicInfo/clanBasicInfo) and wrapped formats
    acc_raw = (data.get("AccountInfo") or data.get("accountInfo") or
               data.get("basicInfo") or data.get("BasicInfo") or {})
    guild_raw = (data.get("GuildInfo") or data.get("guildInfo") or
                 data.get("clanBasicInfo") or data.get("ClanBasicInfo") or
                 data.get("clanInfo") or {})
    social_raw = (data.get("socialinfo") or data.get("SocialInfo") or
                  data.get("socialInfo") or data.get("social") or {})
    captain_raw = data.get("captainBasicInfo") or data.get("CaptainBasicInfo") or {}

    def pick(*keys, src, default="N/A"):
        for k in keys:
            v = src.get(k)
            if v not in (None, "", 0):
                return v
        return default

    acc = {
        # name: nickname (FF API), accountName, name
        "AccountName":       pick("nickname", "AccountName", "accountName", "name", src=acc_raw),
        # id: accountId (FF API), AccountId, uid
        "AccountId":         pick("accountId", "AccountId", "uid", "id", src=acc_raw),
        # level
        "AccountLevel":      pick("level", "AccountLevel", "accountLevel", src=acc_raw),
        # exp
        "AccountEXP":        pick("exp", "AccountEXP", "AccountExp", "accountExp", src=acc_raw),
        # likes: liked (FF API), AccountLikes
        "AccountLikes":      pick("liked", "AccountLikes", "accountLikes", "likes", src=acc_raw, default="0"),
        # region
        "AccountRegion":     pick("region", "AccountRegion", "accountRegion", src=acc_raw),
        # badge: badgeId (FF API), AccountBPID
        "AccountBPID":       pick("badgeId", "AccountBPID", "accountBpId", "bpBadgeId", src=acc_raw),
        # version: releaseVersion (FF API)
        "ReleaseVersion":    pick("releaseVersion", "ReleaseVersion", "version", src=acc_raw),
        # create time: createAt (FF API), AccountCreateTime (Unix timestamp)
        "AccountCreateTime": pick("createAt", "AccountCreateTime", "accountCreateTime", "createTime", src=acc_raw, default="0"),
        # last login: lastLoginAt (FF API), AccountLastLogin (Unix timestamp)
        "AccountLastLogin":  pick("lastLoginAt", "AccountLastLogin", "accountLastLogin", "lastLogin", src=acc_raw, default="0"),
        # pre-formatted last login string from API (e.g. "28 August 2025, 05:17 PM PKT")
        "AccountLastLoginFormatted": pick("lastLoginFormatted", src=acc_raw, default=""),
        # BR max rank: maxRank (FF API), maxRankingPoints, brMaxRank
        "BrMaxRank":         pick("maxRank", "maxRankingPoints", "BrMaxRank", "brMaxRank", src=acc_raw),
        # BR rank points: rankingPoints (FF API), rank, brRankPoint
        "BrRankPoint":       pick("rankingPoints", "rank", "BrRankPoint", "brRankPoint", src=acc_raw),
        # CS max rank: csMaxRank (FF API), csMaxRankingPoints
        "CsMaxRank":         pick("csMaxRank", "csMaxRankingPoints", "CsMaxRank", "csMaxRank", src=acc_raw),
        # CS rank points: csRank (FF API), csRankingPoints
        "CsRankPoint":       pick("csRank", "csRankingPoints", "CsRankPoint", "csRankPoint", src=acc_raw),
    }

    guild = {
        # name: clanName (FF API), GuildName
        "GuildName":     pick("clanName", "GuildName", "guildName", "name", src=guild_raw, default="No Guild"),
        # id: clanId (FF API), GuildID
        "GuildID":       pick("clanId", "GuildID", "GuildId", "guildId", "id", src=guild_raw),
        # owner: captainId (FF API), GuildOwner
        "GuildOwner":    pick("captainId", "GuildOwner", "guildOwner", "ownerId", src=guild_raw),
        # level: clanLevel (FF API), GuildLevel
        "GuildLevel":    pick("clanLevel", "GuildLevel", "guildLevel", "level", src=guild_raw),
        # members: memberNum (FF API), GuildMember
        "GuildMember":   pick("memberNum", "GuildMember", "guildMember", "memberCount", "members", src=guild_raw, default="0"),
        # capacity
        "GuildCapacity": pick("capacity", "GuildCapacity", "guildCapacity", src=guild_raw, default="0"),
    }

    social = {
        "language": pick("language", "Language", src=social_raw),
    }

    captain = {
        "accountId": pick("accountId", "AccountId", src=captain_raw, default=acc.get("AccountId", "N/A")),
    }

    data["AccountInfo"] = acc
    data["GuildInfo"] = guild
    data["socialinfo"] = social
    data["captainBasicInfo"] = captain
    return data


async def get_player_info(uid):
    """Fetch full player info from external API."""
    import aiohttp, asyncio
    try:
        url = f"https://wotaxxdev-api.vercel.app/info?uid={uid}"
        print(f"📊 /info → {url}")

        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as res:
                if res.status != 200:
                    return None, f"API error: HTTP {res.status}"
                raw_json = await res.json(content_type=None)

        print(f"📊 /info raw response: {str(raw_json)[:400]}")

        # API returns data under 'playerData' key (confirmed from logs)
        # Fallback chain: playerData → data → AccountInfo → raw root
        d = (
            raw_json.get("playerData") or
            raw_json.get("data") or
            raw_json.get("AccountInfo") or
            raw_json
        )
        if not isinstance(d, dict):
            d = raw_json

        # Guild may be nested separately
        guild_nested = (
            raw_json.get("guildInfo") or raw_json.get("GuildInfo") or
            d.get("guildInfo") or d.get("GuildInfo") or
            d.get("clanInfo") or d.get("clan") or {}
        )
        if not isinstance(guild_nested, dict):
            guild_nested = {}

        # Helper: search value across multiple dicts and key names, first non-empty wins
        def _mg(*dicts_then_keys, default="N/A"):
            srcs, keys = [], []
            for x in dicts_then_keys:
                if isinstance(x, dict):
                    srcs.append(x)
                else:
                    keys.append(x)
            for src in srcs:
                for k in keys:
                    v = src.get(k)
                    if v not in (None, "", 0, "N/A", "Unknown", "unknown"):
                        return str(v)
            return default

        # For timestamps — only accept positive integers
        def _ts(*dicts_then_keys):
            srcs, keys = [], []
            for x in dicts_then_keys:
                if isinstance(x, dict):
                    srcs.append(x)
                else:
                    keys.append(x)
            for src in srcs:
                for k in keys:
                    v = src.get(k)
                    try:
                        vi = int(v)
                        if vi > 0:
                            return str(vi)
                    except (TypeError, ValueError):
                        pass
            return "0"

        acc = {
            # Confirmed field names from API: nickname, accountId, level, exp, liked, region, lastLoginAt, rankingPoints, rank, csRank
            "AccountName":               _mg(d, "nickname", "AccountName", "name", "playerName", default="Unknown"),
            "AccountId":                 _mg(d, "accountId", "AccountId", "uid", "player_id", default=str(uid)),
            "AccountLevel":              _mg(d, "level", "AccountLevel", default="N/A"),
            "AccountEXP":                _mg(d, "exp", "AccountEXP", "experience", default="0"),
            "AccountLikes":              _mg(d, "liked", "likes", "AccountLikes", default="0"),
            "AccountRegion":             _mg(d, "region", "AccountRegion", default="N/A"),
            "AccountBPID":               _mg(d, "bannerId", "badgeId", "AccountBPID", "bpId", default="N/A"),
            "ReleaseVersion":            _mg(d, "version", "ReleaseVersion", "releaseVersion", default="OB53"),
            "AccountCreateTime":         _ts(d, "createdAt", "createTime", "AccountCreateTime", "create_time", "created_at"),
            "AccountLastLogin":          _ts(d, "lastLoginAt", "lastLogin", "AccountLastLogin", "last_login"),
            "AccountLastLoginFormatted": "",
            "BrRankPoint":               _mg(d, "rankingPoints", "BrRankPoint", "brRankPoints", "brRank", default="N/A"),
            "BrMaxRank":                 _mg(d, "rank", "BrMaxRank", "brMaxRank", default="N/A"),
            "CsRankPoint":               _mg(d, "csRankingPoints", "CsRankPoint", "csRankPoints", default="N/A"),
            "CsMaxRank":                 _mg(d, "csRank", "CsMaxRank", "csMaxRank", default="N/A"),
            "AccountPrimeLevel":         _mg(d, "primeLevel", "AccountPrimeLevel", "prime_level", "PrimeLevel", "seasonId", default="N/A"),
        }

        guild = {
            "GuildName":     _mg(guild_nested, d, "GuildName", "clanName", "guildName", default="No Guild"),
            "GuildID":       _mg(guild_nested, d, "GuildID", "clanId", "guildId", default="N/A"),
            "GuildOwner":    _mg(guild_nested, d, "GuildOwner", "captainId", "ownerId", default="N/A"),
            "GuildLevel":    _mg(guild_nested, d, "GuildLevel", "clanLevel", "guildLevel", default="N/A"),
            "GuildMember":   _mg(guild_nested, d, "GuildMember", "memberNum", "memberCount", default="0"),
            "GuildCapacity": _mg(guild_nested, d, "GuildCapacity", "capacity", "maxMember", default="0"),
        }

        data = {
            "AccountInfo": acc,
            "GuildInfo": guild,
            "socialinfo": {"language": _mg(d, "language", default="N/A")},
            "captainBasicInfo": {"accountId": acc.get("AccountId", str(uid))},
        }
        print(f"📊 info OK → name={acc['AccountName']} level={acc['AccountLevel']} region={acc['AccountRegion']} login={acc['AccountLastLogin']}")
        return data, None

    except asyncio.TimeoutError:
        return None, "Request timed out (15s)"
    except aiohttp.ClientConnectorError as e:
        return None, f"Connection error: {e}"
    except Exception as e:
        print(f"❌ get_player_info error: {e}")
        return None, str(e)


async def check_ban_status(uid):
    """Check ban status of a player using external API."""
    import aiohttp, asyncio
    try:
        url = f"https://wotaxxdev-api.vercel.app/check?uid={uid}"
        print(f"🔍 /check → {url}")

        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as res:
                if res.status != 200:
                    return None, f"API error: HTTP {res.status}"
                raw_json = await res.json(content_type=None)

        print(f"🔍 /check raw response: {raw_json}")
        return raw_json, None

    except asyncio.TimeoutError:
        return None, "Request timed out (15s)"
    except aiohttp.ClientConnectorError as e:
        return None, f"Connection error: {e}"
    except Exception as e:
        print(f"❌ check_ban_status error: {e}")
        return None, str(e)


async def get_player_likes_internal(uid, region="bd"):
    """Fetch player name and likes directly from the game server using internal protobuf — no external APIs."""
    import aiohttp, asyncio, ssl as ssl_mod
    try:
        token = load_jwt_token()
        if not token:
            return None, None, "No JWT token available"

        encrypted_payload = enc(uid)
        if region.lower() == "ind":
            url = "https://client.ind.freefiremobile.com/GetPlayerPersonalShow"
        elif region.lower() == "us":
            url = "https://client.us.freefiremobile.com/GetPlayerPersonalShow"
        elif region.lower() == "sg":
            url = "https://client.sg.freefiremobile.com/GetPlayerPersonalShow"
        else:
            url = "https://client.bd.freefiremobile.com/GetPlayerPersonalShow"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB53",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }

        ssl_context = ssl_mod.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl_mod.CERT_NONE

        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                url,
                data=bytes.fromhex(encrypted_payload),
                headers=headers,
                ssl=ssl_context,
            ) as res:
                if res.status != 200:
                    return None, None, f"Game server error: {res.status}"
                raw = await res.read()
                try:
                    decrypted = bytes.fromhex(decrypt_api(raw.hex()))
                except Exception:
                    decrypted = raw
                info = decode_player_info(decrypted)
                player_name = getattr(info, "AccountName", None) or getattr(info, "nickname", None) or "Unknown"
                likes = getattr(info, "Liked", None) or getattr(info, "liked", None) or getattr(info, "AccountLikes", None) or 0
                return str(player_name), int(likes), None
    except asyncio.TimeoutError:
        return None, None, "Request timed out"
    except Exception as e:
        return None, None, str(e)


def get_ff_server_url(region, endpoint):
    """Return the correct Free Fire server URL for the given region and endpoint."""
    if BOT_SERVER_URL:
        return f"{BOT_SERVER_URL}/{endpoint}"
    region = region.upper()
    base = {
        "IND": "https://client.ind.freefiremobile.com",
        "BD":  "https://client.bd.freefiremobile.com",
        "US":  "https://client.us.freefiremobile.com",
        "SG":  "https://client.sg.freefiremobile.com",
        "ME":  "https://client.me.freefiremobile.com",
        "PK":  "https://client.me.freefiremobile.com",
        "SAC": "https://client.sac.freefiremobile.com",
    }.get(region, "https://client.me.freefiremobile.com")
    return f"{base}/{endpoint}"


def get_friend_server_url(region, endpoint):
    """Return URL for friend endpoints.
    Uses BOT_SERVER_URL when set (same as get_ff_server_url) so the bot
    always routes through the server that was assigned at login (e.g. polarbear).
    Falls back to regional freefiremobile.com only when BOT_SERVER_URL is not set.
    """
    if BOT_SERVER_URL:
        return f"{BOT_SERVER_URL}/{endpoint}"
    region = region.upper()
    base = {
        "IND": "https://client.ind.freefiremobile.com",
        "BD":  "https://client.bd.freefiremobile.com",
        "US":  "https://client.us.freefiremobile.com",
        "SG":  "https://client.sg.freefiremobile.com",
        "ME":  "https://client.me.freefiremobile.com",
        "PK":  "https://client.me.freefiremobile.com",
        "SAC": "https://client.sac.freefiremobile.com",
    }.get(region, "https://client.me.freefiremobile.com")
    return f"{base}/{endpoint}"


def encode_varint(value):
    """Encode an integer as a protobuf varint and return hex string."""
    buf = []
    value = int(value)
    while True:
        towrite = value & 0x7f
        value >>= 7
        if value:
            buf.append(towrite | 0x80)
        else:
            buf.append(towrite)
            break
    return ''.join(f'{b:02x}' for b in buf)


def send_friend_request_single(uid, token, region="PK"):
    """Send friend request directly to Free Fire server.
    Returns (True, None) on success or (False, error_str) on failure."""
    try:
        # Load bot UID from token.json so it matches the JWT token
        try:
            with open("token.json", "r") as f:
                token_data = json.load(f)
            bot_uid = int(token_data.get("bot_uid", 0))
        except Exception:
            bot_uid = 0

        if bot_uid == 0:
            msg = "bot_uid missing in token.json — restart bot"
            print(f"❌ {msg}")
            return False, msg

        bot_uid_varint = encode_varint(bot_uid)
        target_uid_varint = encode_varint(uid)
        payload = f"08{bot_uid_varint}10{target_uid_varint}"
        encrypted_payload = encrypt_api(payload)

        url = get_ff_server_url(region, "RequestAddingFriend")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB53",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }

        print(f"📤 ADD payload hex (pre-encrypt): {payload}")
        print(f"📤 Sending friend request to {uid} (bot_uid={bot_uid}) → {url}")
        response = requests.post(url, data=bytes.fromhex(encrypted_payload), headers=headers, timeout=10, verify=False)
        print(f"📤 RequestAddingFriend → HTTP {response.status_code} | body: {response.content[:300]}")

        # Check for duplicate / already friends in the response body
        body_text = response.content.decode("utf-8", errors="ignore").lower()
        if "duplicate" in body_text or "already" in body_text or "exist" in body_text:
            print(f"⚠️ Friend {uid} already added or request already pending")
            return False, "ALREADY_ADDED"

        if response.status_code == 200:
            print(f"✅ Friend request sent to {uid}")
            return True, None
        else:
            return False, f"HTTP {response.status_code}"

    except Exception as e:
        print(f"❌ send_friend_request_single error: {e}")
        return False, str(e)    
    
def start_autooo(self):    
    try:
        fields = {
            1: 9,
            2: {
                1: 12480598706,
            },
        }
        packet = create_protobuf_packet(fields).hex()
        header_length = len(encrypt_packet(packet, self.key, self.iv)) // 2
        header_length_final = dec_to_hex(header_length)
        if len(header_length_final) == 2:
            final_packet = "0515000000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 3:
            final_packet = "051500000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 4:
            final_packet = "05150000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 5:
            final_packet = "0515000" + header_length_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)
    except Exception as e:
        print(e)

def load_credentials_from_file(filename="MG24GAMER.txt"):
    """
    Load UID and password from MG24GAMER.txt file
    """
    try:
        if not os.path.exists(filename):
            print(f"❌ {filename} not found!")
            create_credentials_template()
            return None, None
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        uid = None
        password = None
        
        # Try to find uid and password using regex
        import re
        
        # Look for uid=value or uid: value
        uid_match = re.search(r'(?:uid\s*[=:]\s*)(\d+)', content, re.IGNORECASE)
        if uid_match:
            uid = uid_match.group(1)
        
        # Look for password=value or password: value
        pass_match = re.search(r'(?:password\s*[=:]\s*)([^\s\n\r]+)', content, re.IGNORECASE)
        if pass_match:
            password = pass_match.group(1)
        
        if not uid or not password:
            print(f"❌ Could not find UID/password in {filename}")
            print("📝 Please make sure the file contains:")
            print("   uid=YOUR_UID,password=YOUR_PASSWORD")
            print("   OR")
            print("   uid: YOUR_UID")
            print("   password: YOUR_PASSWORD")
            return None, None
        
        print(f"✅ Loaded credentials from {filename}")
        print(f"👤 UID: {uid}")
        print(f"🔑 Password: {password}")
        
        return uid, password
        
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return None, None

# Load emotes from JSON file (your format)
def load_emotes_from_json():
    """Load emote IDs from emotes.json (or any matching file in current directory)."""
    import glob as _glob

    # Try these filenames in order
    candidates = (
        ["emotes.json"]
        + _glob.glob("emotes*.json")
        + _glob.glob("attached_assets/emotes*.json")
    )
    # Deduplicate while preserving order
    seen = set()
    candidates = [c for c in candidates if not (c in seen or seen.add(c))]

    for emotes_file in candidates:
        try:
            with open(emotes_file, 'r') as f:
                emotes_data = json.load(f)
            number_emotes = emotes_data.get("EMOTES", {}).get("numbers", {})
            name_emotes   = emotes_data.get("EMOTES", {}).get("names", {})
            if name_emotes:
                print(f"✅ Loaded {len(number_emotes)} number emotes and {len(name_emotes)} named emotes from {emotes_file}")
                return {"numbers": number_emotes, "names": name_emotes}
        except Exception:
            continue

    print("⚠️ emotes.json not found — /e list will show 0 names. Place emotes.json next to main.py")
    return {"numbers": {}, "names": {}}

# Load emotes globally
EMOTES_DATA = load_emotes_from_json()
NUMBER_EMOTES = EMOTES_DATA["numbers"]
NAME_EMOTES = EMOTES_DATA["names"]

# Helper functions for ghost join
def dec_to_hex(decimal):
    """Convert decimal to hex string"""
    hex_str = hex(decimal)[2:]
    return hex_str.upper() if len(hex_str) % 2 == 0 else '0' + hex_str.upper()



async def encrypt_packet(packet_hex, key, iv):
    """Encrypt packet using AES CBC"""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    packet_bytes = bytes.fromhex(packet_hex)
    padded_packet = pad(packet_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded_packet)
    return encrypted.hex()

async def nmnmmmmn(packet_hex, key, iv):
    """Wrapper for encrypt_packet"""
    return await encrypt_packet(packet_hex, key, iv)
    

def generate_random_hex_color():
    """Generate random hex color for messages"""
    return ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

def bunner_():
    """Generate random avatar ID"""
    return random.randint(100000000, 999999999)

# Add this function to your code
def Encrypt(number):
    """Encrypt function from your first TCP bot"""
    number = int(number)
    encoded_bytes = []
    
    while True:
        byte = number & 0x7F
        number >>= 7
        if number:
            byte |= 0x80
        encoded_bytes.append(byte)
        if not number:
            break
    
    return bytes(encoded_bytes).hex()


async def send_working_join_request(target_uid, key, iv, region, LoGinDaTaUncRypTinG):
    """Send join request that actually works"""
    
    try:
        # Step 1: Reset bot to solo mode
        print("🔄 Resetting bot to solo mode...")
        await reset_bot_state(key, iv, region)
        await asyncio.sleep(1)
        
        # Step 2: Create bot's own squad (so it has context)
        print("🏠 Creating bot squad...")
        squad_packet = await OpEnSq(key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', squad_packet)
        await asyncio.sleep(1)
        
        # Step 3: Send join request
        print(f"📨 Sending join request to {xMsGFixinG(target_uid)}...")
        join_packet = await create_working_join_request(target_uid, key, iv, region, LoGinDaTaUncRypTinG)
        
        if join_packet:
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            print(f"✅ Bot join request sent! Player can now accept.")
            return True
        else:
            print(f"❌ Failed to create join packet")
            return False
            
    except Exception as e:
        print(f"❌ Error in working join request: {e}")
        return False
        
async def handle_join_req_command(inPuTMsG, uid, chat_id, key, iv, region, chat_type, LoGinDaTaUncRypTinG):
    """Handle /join_req command - bot sends join request to player"""
    
    parts = inPuTMsG.strip().split()
    
    if len(parts) < 2:
        error_msg = f"""[B][C][FF0000]❌ Usage: /join_req (player_uid)
Example: /join_req 123456789

What happens:
1. Bot goes solo mode
2. Bot creates its own squad  
3. Bot sends join request to player
4. Player sees: "BotName wants to join your team"
5. Player clicks Accept → Bot joins player's team
"""
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    target_uid = parts[1]
    
    if not target_uid.isdigit():
        error_msg = f"[B][C][FF0000]❌ Invalid UID! Must be numbers only.\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    
    # Send initial message
    initial_msg = f"""[B][C][00FF00]🤖 BOT JOIN REQUEST INITIATED

👤 Target Player: {xMsGFixinG(target_uid)}
⚙️ Steps:
1. Bot resetting to solo mode...
2. Bot creating squad...
3. Sending join request...

⏳ Please wait...
"""
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    
    try:
        success = await send_working_join_request(target_uid, key, iv, region, LoGinDaTaUncRypTinG)
        
        if success:
            success_msg = f"""[B][C][00FF00]✅ BOT JOIN REQUEST SENT!

🎯 Target: {xMsGFixinG(target_uid)}
🤖 Bot Name: MG24 GAMER
✅ Status: Ready to join

📱 Player will see:
"MG24 GAMER wants to join your team"

✅ When player clicks ACCEPT:
Bot will automatically join player's team!
"""
        else:
            success_msg = f"""[B][C][FF0000]❌ FAILED!

Possible reasons:
1. Bot not connected properly
2. Bot already in a squad
3. Server issue

Try again in 10 seconds.
"""
        
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        
        # Cleanup: Leave squad after sending request
        await asyncio.sleep(3)
        leave_packet = await ExiT(0, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        print("🧹 Bot cleaned up (left squad)")
        
    except Exception as e:
        error_msg = f"[B][C][FF0000]❌ Error: {str(e)[:50]}\n"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)        
        
async def create_simple_start_packet(key, iv):
    """Create simple start match packet (00 00 00 d6)"""
    
    # This appears to be a minimal start packet
    # 00 00 00 d6 in hex = 214 in decimal (packet type?)
    
    fields = {
        1: 214,  # Packet type for start match (d6 hex = 214 decimal)
        2: {
            1: 1,  # Start match command
        }
    }
    
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Generate final packet
    final_packet = await GeneRaTePk(packet_hex, '0514', key, iv)  # Use appropriate packet type
    
    print(f"✅ Simple start match packet created")
    return final_packet
    
async def create_detailed_start_packet(key, iv, region="IND"):
    """Create detailed start match packet with device info"""
    
    # Decoded from your hex: contains device info (vivo, arm64, etc.)
    
    fields = {
        1: 269,  # 0x10D = 269 decimal (detailed start packet)
        2: {
            1: 8,           # Unknown
            2: 8,           # Unknown
            3: 11,          # Unknown
            4: 1,           # Unknown
            5: "vivo",      # Device brand
            6: "130",       # Device model
            7: "arm64-v8a", # CPU architecture
            8: "f538dc9b-cec9-43cd-8125-95f7f4f1f7e3",  # Device ID
            9: "FFD58FB4F76F648C2A5E21EBCFA3AAE81B4C9B7D97",  # Unknown
            10: "voice",    # Audio type
            11: "V2059",    # Version
            12: "mt6785",   # Processor
            13: "AFFD58FB4F76F648C2A5E21EBCFA3AAE81B4C9B7D97",  # Unknown
            14: "IND_1999120752610979840",  # Region + timestamp
            15: 269         # Packet length?
        }
    }
    
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    
    # Determine packet type based on region
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
        
    final_packet = await GeneRaTePk(packet_hex, packet_type, key, iv)
    
    print(f"✅ Detailed start match packet created")
    return final_packet
        
async def generate_guest_accounts(count=1, name="BlackApis", password_prefix="FF"):
    """Generate guest accounts using the API"""
    api_url = f"https://gen-by-black-api.vercel.app/generate?name={name}&password_prefix={password_prefix}"
    
    accounts = []
    failed_attempts = 0
    max_retries = 10
    
    print(f"📡 Generating {count} guest accounts...")
    
    for i in range(count):
        retry_count = 0
        success = False
        
        while retry_count < max_retries and not success:
            try:
                print(f"🔄 Attempt {retry_count + 1}/{max_retries} for account {i + 1}/{count}...")
                
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                    async with session.get(api_url) as response:
                        
                        if response.status == 200:
                            data = await response.json()
                            
                            if data.get("success"):
                                account = {
                                    'uid': data.get('uid'),
                                    'password': data.get('password'),
                                    'name': data.get('name'),
                                    'timestamp': time.time()
                                }
                                accounts.append(account)
                                print(f"✅ Account {i + 1}: {account['uid']}")
                                success = True
                                failed_attempts = 0  # Reset failed attempts counter
                                
                            else:
                                print(f"❌ API error: {data.get('message', 'Unknown error')}")
                                retry_count += 1
                                await asyncio.sleep(2)
                                
                        elif response.status == 503:
                            print(f"⚠️ Server busy (503), retrying in 3 seconds...")
                            retry_count += 1
                            await asyncio.sleep(3)
                            
                        else:
                            print(f"❌ HTTP {response.status}, retrying...")
                            retry_count += 1
                            await asyncio.sleep(2)
                            
            except asyncio.TimeoutError:
                print(f"⏰ Timeout, retrying...")
                retry_count += 1
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"❌ Error: {str(e)[:50]}...")
                retry_count += 1
                await asyncio.sleep(2)
        
        if not success:
            print(f"❌ Failed to generate account {i + 1} after {max_retries} attempts")
            failed_attempts += 1
            
            # If too many failures in a row, stop
            if failed_attempts >= 3:
                print("🛑 Too many failures, stopping...")
                break
        
        # Small delay between accounts to avoid rate limiting
        if i < count - 1:
            await asyncio.sleep(1)
    
    return accounts

def save_guest_accounts(accounts, filename="guest_accounts.json"):
    """Save guest accounts to JSON file"""
    try:
        # Load existing accounts if file exists
        existing = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                existing = json.load(f)
        
        # Combine with new accounts
        all_accounts = existing + accounts
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(all_accounts, f, indent=2)
        
        print(f"💾 Saved {len(accounts)} accounts to {filename}")
        print(f"📊 Total accounts: {len(all_accounts)}")
        
        return True
    except Exception as e:
        print(f"❌ Error saving accounts: {e}")
        return False

async def generate_and_save_accounts(count, name="BlackApis", password_prefix="FF"):
    """Generate and save accounts with progress updates"""
    start_time = time.time()
    
    print(f"\n🎯 GENERATING {count} GUEST ACCOUNTS")
    print("="*50)
    
    accounts = await generate_guest_accounts(count, name, password_prefix)
    
    if accounts:
        # Save to file
        save_guest_accounts(accounts)
        
        # Display results
        elapsed = time.time() - start_time
        print("\n" + "="*50)
        print("📊 GENERATION COMPLETE")
        print("="*50)
        print(f"✅ Success: {len(accounts)}/{count} accounts")
        print(f"⏱️ Time: {elapsed:.1f} seconds")
        print(f"📁 Saved to: guest_accounts.json")
        
        # Show first 3 accounts as preview
        print("\n📋 FIRST 3 ACCOUNTS:")
        for i, acc in enumerate(accounts[:3]):
            print(f"  {i+1}. UID: {acc['uid']} | Pass: {acc['password']}")
        
        if len(accounts) > 3:
            print(f"  ... and {len(accounts) - 3} more")
    
    return accounts        
        
async def start_match(key, iv, region, detailed=False):
    """Start Free Fire match - bot must be in a squad/team"""
    
    try:
        if detailed:
            start_packet = await create_detailed_start_packet(key, iv, region)
        else:
            start_packet = await create_simple_start_packet(key, iv)
        
        if start_packet:
       