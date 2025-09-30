import json
import os

def load_config():
    with open('data/config.json','r') as f:
        return json.load(f)

CONFIG = load_config()