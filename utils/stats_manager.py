import json
import os
from datetime import datetime, timedelta
import shutil
import asyncio

from aiohttp._websocket.models import WS_DEFLATE_TRAILING

class StatsManager:
    def __init__(self, filename: str = "data/stats.json"):
        self.filename = filename
        self.data = {}
        self.load()

    async def auto_save(self,interval=300):
        while True:
            stats_manager.save()
            await asyncio.sleep(interval)

    # ----------------- File Handling -----------------
    def load(self):
        """Load stats from file into memory"""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def save(self):
        """Save current stats to file"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        shutil.copy(self.filename, self.filename + '.bak')

    # ----------------- User Handling -----------------
    def get_user(self, user_id: int) -> dict:
        """Return a user's stats, creating them if they don't exist"""
        uid = str(user_id)
        if uid not in self.data:
            self.data[uid] = {
                "sold": 0,
                "banned": 0,
                "earnings": 0,
                "wallets": {},
                "history": []
            }
            self.save()
        return self.data[uid]

    # ----------------- Logging -----------------
    def log(self, user_id: int, op: str = None, price: int = None):
        """Log a user's action and update stats accordingly"""
        user = self.get_user(user_id)
        now = datetime.now().isoformat()

        if op == "banned":
            user["banned"] += 1
            user["history"].append({"action": "banned", "time": now})

        elif op == "sold":
            user["sold"] += 1
            user["earnings"] += price or 0
            user["history"].append({"action": "sold", "price": price, "time": now})

        self.save()
    
    def log_wallet(self,user_id:int,type:str,wallet:str):
        user = self.get_user(user_id)

        if type in ['vodafone','instapay']:
            if type not in user["wallets"]:
                user["wallets"][type] = []
            if wallet not in user["wallets"][type]:
                user["wallets"][type].append(wallet)
        
        if type == 'visa':
            if type not in user["wallets"]:
                user["wallets"][type] = []
            exist = any(w['number'] == wallet[0] for w in user["wallets"][type])
            if not exist:
                user["wallets"][type].append({
                    'holder name': wallet[1],
                    'number': wallet[0]
                })
        
        self.save()
    
    def wallet_exist(self,user_id:int,type:str,wallet) -> bool:
        user = self.get_user(user_id)

        if type not in user["wallets"]:
            return False

        if type in ['vodafone','instapay']:
            return wallet in user['wallets'][type]
        elif type == 'visa':
            return any(w['number'] == wallet[0] for w in user["wallets"][type])

        return False

    # ----------------- Stats Helpers -----------------
    def avg_sale(self, user_id: int) -> float:
        """Return average sale price for a user"""
        user = self.get_user(user_id)
        total_earn = user["earnings"]
        sold_actions = [h for h in user["history"] if h["action"] == "sold"]

        if not sold_actions:
            return 0.0
        return round(total_earn / len(sold_actions),2)

    def weekly_sum(self, user_id: int):
        """Return actions and counts for the last 7 days"""
        user = self.get_user(user_id)
        now = datetime.now()
        week_ago = now - timedelta(days=7)

        actions = [
            a for a in user["history"]
            if datetime.fromisoformat(a["time"]) >= week_ago
        ]
        sold = sum(1 for a in actions if a["action"] == "sold")
        banned = sum(1 for a in actions if a["action"] == "banned")

        return actions, sold, banned

    def success_rate(self,user_id:int):
        user = self.get_user(user_id)
        return round(user['sold'] / (user['sold'] + user['banned']) * 100,2)

stats_manager = StatsManager('data/stats.json')
