import os
import shutil

from nextcord import file
from utils.config_loader import CONFIG

class FreshManager:
    def __init__(self):
        self.fresh_path = CONFIG["fresh"]
        self.taken_path = CONFIG["taken"]

        # Ensure folders exist
        os.makedirs(self.fresh_path, exist_ok=True)
        os.makedirs(self.taken_path, exist_ok=True)

    # 📂 List files in fresh
    def list_fresh(self, game_type: str = None):
        files = os.listdir(self.fresh_path)
        if game_type:
            return [f for f in files]
        return files

    # 📂 List files in taken
    def list_taken(self,game_type:str = None):
        files = os.listdir(self.taken_path)
        if game_type:
            return [f for f in files]
        return files

    # 🎫 Get the first available file
    def get_first_fresh(self, game_type: str = None):
        fresh_path = os.path.join('accs','fresh',game_type)
        files = os.listdir(fresh_path)
        return os.path.join(fresh_path,files[0]) if files else None

    # 📦 Move a file to taken
    def move_to_taken(self,username:str,game_type:str):
        taken_path = os.path.join('accs','taken',game_type)
        file_path = self.get_first_fresh(game_type)
        file_name = os.path.basename(file_path)
        new_name = f'{username}_{file_name}'
        new_path = os.path.join(taken_path,new_name)
        shutil.move(file_path,new_path)
        

    # 📤 Upload a new account file
    def upload_file(self, file_content: str, game_type: str):
        try:
            # always save into the correct fresh folder
            fresh = self.list_fresh(game_type)
            path = os.path.join(self.fresh_path)

            # make sure the folder exists
            os.makedirs(path, exist_ok=True)

            # create a unique name based on current timestamp
            file_name = f"{game_type}_{len(fresh)}.txt"
            full_path = os.path.join(path, file_name)

        # write the file
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(file_content)

            return file_name
        except Exception as e:
            print(f"Error saving file: {e}")
            return False


    # ℹ️ Get folder stats
    def get_info(self):
        fresh = len(os.listdir(self.fresh_path))
        taken = len(os.listdir(self.taken_path))
        return {"fresh": fresh, "taken": taken}

fresh_manager = FreshManager()