import pymongo
from datetime import datetime
import requests
import os

db_client = pymongo.MongoClient(os.environ.get("MONGO_URL"))
db = db_client["ottawa"]
col_users = db["user"]
col_codes = db["codes"]




class Users:
    def __init__(self, _id: int):
        self.id = _id

    def insert(self, username):
        json = {
            "_id": self.id,
            "name": username,
            "thanks": 0,
            "xp": 0,
            "voice_xp": 0,
            "description": None,
            "coins": 0
        }
        try:
            x = col_users.insert_one(json)
            return x
        except Exception as error:
            return error

    @property
    def info(self):
        x = col_users.find_one({"_id": self.id})
        print(x)
        return x

    def _all(self, module: str):
        return [i for i in col_users.find().sort(module, -1)]

    @property
    def all(self):
        return col_users.find()

    def top_xp(self, count: int = 10):
        top = []
        for n, i in enumerate(col_users.find().sort("xp", -1)):
            if n == count:
                _ids = [i.get("_id") for i in top]
                if self.id not in _ids:
                    index = self._all("xp").index(self.info)
                    x = self.info
                    x["num"] = index
                    top.append(x)
                break
            if len(top) >= count:
                break
            i["num"] = n + 1
            top.append(i)
        return top

    def top_thanks(self, count: int = 10):
        top = []
        for n, i in enumerate(col_users.find().sort("thanks", -1)):
            if n == count:
                _ids = [i.get("_id") for i in top]
                if self.id not in _ids:
                    index = self._all("thanks").index(self.info)
                    x = self.info
                    x["num"] = index
                    top.append(x)
                break
            if len(top) >= count:
                break
            i["num"] = n + 1
            top.append(i)
        return top

    def top_voice(self, count: int = 10):
        top = []
        for n, i in enumerate(col_users.find().sort("voice_xp", -1)):
            if n == count:
                _ids = [i.get("_id") for i in top]
                if self.id not in _ids:
                    index = self._all("voice_xp").index(self.info)
                    x = self.info
                    x["num"] = index
                    top.append(x)
                break
            if len(top) >= count:
                break
            i["num"] = n + 1
            top.append(i)
        return top

    def update_xp(self, count: int = 1):
        old_xp = self.info.get("xp")
        col_users.update_one({"_id": self.id}, {"$set": {"xp": old_xp+count}})

    def update_where(self, module: str, new_value):
        col_users.update_one({"_id": self.id}, {"$set": {module: new_value}})

    def get_from_page_id(self, module: str, page_id: int):
        l = round(len([i for i in self.all]) / 10)
        z = []
        if page_id > l or page_id <= 0:
            return
        main_list = []
        bad_num = []
        for i in range(len(self._all(module=module))):
            if i % 10:
                bad_num.append(i)
        for n, i in enumerate(self._all(module=module)):
            if n not in bad_num:
                z.append(main_list)
                main_list = []
            i["num"] = n + 1
            main_list.append(i)
        return z[page_id]

    @staticmethod
    def delete_one(_id):
        col_users.delete_one({"_id": _id})


class Codes:
    def __init__(self, code_id: str):
        self.code_id = code_id

    @property
    def info(self):
        x = col_codes.find_one({"_id": self.code_id})
        return x

    def insert(self, title, description, type, author_id, copyrights, code):
        json = {
            "_id": self.code_id,
            "title": title,
            "description": description,
            "type": type,
            "author_id": author_id,
            "copyrights": copyrights,
            "code": code,
            "data": datetime.now().timestamp(),
            "link": self._create_link(title, type, code)
        }
        try:
            x = col_codes.insert_one(json)
            return x
        except Exception as error:
            return error

    @staticmethod
    def _create_link(title, type, code):
        json = {
            "api_dev_key": os.environ.get("KEY_PASTBIN"),
            "api_paste_code": "%s\n# Copyright (c) 2021 OTTAWA server\n# Discord: https://discord.gg/ottawa\n# Note: this auto paste," % code,
            "api_paste_private": "0",
            "api_paste_name": title,
            "api_paste_format": type,
            "api_user_key": "",
            "api_option": "paste"
        }
        x = requests.post("https://pastebin.com/api/api_post.php", data=json)
        return x.content.decode("utf-8")

    @staticmethod
    def get_all_code():
        json = col_codes.find()
        return json

