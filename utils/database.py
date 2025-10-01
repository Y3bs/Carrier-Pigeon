from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import date, datetime,timedelta

load_dotenv()
DB_TOKEN = os.getenv('DB_TOKEN')
db = MongoClient(DB_TOKEN)

def find_player(id):
    try:
        return db.carrier.players.find_one({"id":id})
    except Exception as e:
        print(f"Error Fetching player's data\nError: {e}")
        

def save_player(id):
    try:
        doc = {
            "id": id,
            "sold": 0,
            "banned": 0,
            "earnings": 0,
            "wallets": {
                "vodafone":[],
                "instapay":[],
                "visa": []
            },
            "history": []
        }
        db.carrier.players.insert_one(doc)
    except Exception as e:
        print(f"Error Saving Data\nError: {e}")

def delete_player(id):
    try:
        db.carrier.players.delete_one({"id": id})
    except Exception as e:
        print(f"Error Deleting Player from database\nError: {e}")

def save_wallet(user_id: int,type:str,wallet: str):
    user = find_player(user_id)
    try:
        if type in ['vodafone','instapay']:
            if wallet not in user['wallets'][type]:
                db.carrier.players.update_one({"id":user_id},{"$push": {f"wallets.{type}": wallet}})

        if type == 'visa':
            exist = any(w['number'] == wallet[0] for w in user["wallets"][type])
            if not exist:
                card = {
                    "holder name": wallet[1],
                    "number": wallet[0]
                }
                db.carrier.players.update_one({"id":user_id},{"$push":{f"wallets.{type}":card}})

    except Exception as e:
        print(f"Error Saving wallet\nError: {e}")

def wallet_exist(user_id:int,type:str,wallet):
    try:
        user = db.carrier.players.find_one({"id":user_id})
        if type in ['vodafone','instapay']:
            return wallet in user['wallets'][type]
        elif type == 'visa':
            return any(w['number'] == wallet[0] for w in user["wallets"][type])
    except Exception as e:
        print(f"Error finding user's wallet\nError: {e}")

def log_account(user_id:int,op:str = None,price:int = None):
    now = datetime.now().isoformat()
    
    try:
        if op == "banned":
            db.carrier.players.update_one({"id":user_id},{"$inc":{"banned": 1}})
            action_doc ={
                "action": "banned",
                "time": now
            }
            db.carrier.players.update_one({"id":user_id},{"$push":{"history":action_doc}})
        
        elif op == 'sold':
            db.carrier.players.update_one({"id":user_id},{"$inc":{"sold":1}})

            if price is not None:
                db.carrier.players.update_one({"id":user_id},{"$inc":{"earnings": price}})
            
            action_doc = {
                "action": "sold",
                "time": now,
                "price": price if price is not None else 0
            }
            db.carrier.players.update_one({"id":user_id},{"$push":{"history":action_doc}})
    except Exception as e:
        print(f"Error logging account\nError: {e}")

def avg_sale(user_id:int):
    try:
        user = db.carrier.players.find_one({"id":user_id})
        total_earn = user['earnings']
        sold_actions = [h for h in user["history"] if h["action"] == "sold"]

        if not sold_actions:
            return 0.0
        return round(total_earn / len(sold_actions),2)
    except Exception as e:
        print(f"Error calculating the average sale\nError: {e}")

def success_rate(user_id:int):
    try:
        user = db.carrier.players.find_one({"id":user_id})
        return round(user['sold'] / (user['sold'] + user['banned']) * 100,2)
    except Exception as e:
        print(f"Error calculating the success rate\nError: {e}")

def increment_field(user_id: int, field: str, value: int):
    """
    Increment a numeric field by a fixed value
    
    Args:
        user_id: The user's ID
        field: The field name to increment (e.g., 'earnings', 'sold', 'banned')
        value: The amount to add (can be negative to subtract)
    """
    try:
        db.carrier.players.update_one({"id": user_id}, {"$inc": {field: value}})
    except Exception as e:
        print(f"Error incrementing field {field}\nError: {e}")




