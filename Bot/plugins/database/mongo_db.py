from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import Message

from Bot import MONGO_DB as DB_URL, BOT_NAME, OWNER_ID

cluster = MongoClient(DB_URL)
db = cluster['Encoding']
users = db[BOT_NAME]

def ensure_user_exists(user_id):
    """
    Auto-create user settings if they don't exist.
    This replaces the approval system - users get default settings immediately.
    """
    user_id = int(user_id)
    existing_user = users.find_one({'user_id': user_id})
    if existing_user is None:
        # Create default settings for new user
        users.insert_one({
            'user_id': user_id,
            'resolution': '480p',
            'preset': 'fast',
            'audio_type': 'aac',
            'vcodec': 'x264', 
            'crf': 26
        })
        return True
    return False

def check_user_mdb(id):
    ensure_user_exists(id)  # Auto-create if doesn't exist
    got = users.find_one({'user_id': int(id)})
    if got is not None:
        return int(got['user_id'])
    return int(id)  # Return user ID as confirmation

def check_crf_mdb(id):
    ensure_user_exists(id)  # Auto-create if doesn't exist
    got = users.find_one({'user_id': int(id)})
    if got is not None:
        return int(got['crf'])
    return 26  # Default fallback

def check_resolution_settings(id):
    ensure_user_exists(id)  # Auto-create if doesn't exist
    got = users.find_one({'user_id': int(id)})
    if got is not None:
        return got['resolution']
    return '480p'  # Default fallback
    
def check_preset_settings(id):
    ensure_user_exists(id)  # Auto-create if doesn't exist
    got = users.find_one({'user_id': int(id)})
    if got is not None:
        return got['preset']
    return 'fast'  # Default fallback
    
def check_vcodec_settings(id):
    ensure_user_exists(id)  # Auto-create if doesn't exist
    got = users.find_one({'user_id': int(id)})
    if got is not None:
        return got['vcodec']
    return 'x264'  # Default fallback
    
def check_audio_type_mdb(id):
    ensure_user_exists(id)  # Auto-create if doesn't exist
    got = users.find_one({'user_id': int(id)})
    if got is not None:
        return str(got['audio_type'])
    return 'aac'  # Default fallback
    
def update_resolution_settings(id, new):
    ensure_user_exists(id)  # Auto-create if doesn't exist
    got = users.update_one({'user_id': int(id)}, {'$set': {'resolution': new}}) 
    if got is not None:
        return 'Success' 

def update_preset_settings(id, new):
    ensure_user_exists(id)  # Auto-create if doesn't exist
    got = users.update_one({'user_id': int(id)}, {'$set': {'preset': new}}) 
    if got is not None:
        return 'Success' 

def update_vcodec_settings(id, new):
    ensure_user_exists(id)  # Auto-create if doesn't exist
    got = users.update_one({'user_id': int(id)}, {'$set': {'vcodec': new}}) 
    if got is not None:
        return 'Success'

def update_audio_type_mdb(id, new):
    ensure_user_exists(id)  # Auto-create if doesn't exist
    got = users.update_one({'user_id': int(id)}, {'$set': {'audio_type': new}}) 
    if got is not None:
        return 'Success'        
    
def update_crf(id, new):
    ensure_user_exists(id)  # Auto-create if doesn't exist
    got = users.update_one({'user_id': int(id)}, {'$set': {'crf': new}}) 
    if got is not None:
        return 'Success' 

def owner_check():
    """Ensure owner and dev have access"""
    ensure_user_exists(OWNER_ID)
    ensure_user_exists(953362604)  # DEV ID

owner_check()
