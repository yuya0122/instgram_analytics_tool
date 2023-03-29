import configparser
import json
from pprint import pprint
import requests
from time import sleep

from core.base import Base

class InstagramGraphClient(Base):
    def __init__(self, base_url, business_account_id, access_token, username):
        self.base_url = base_url
        self.business_account_id = business_account_id
        self.access_token = access_token
        self.username = username

    # ユーザーを取得
    def fetch_user(self, data_fields):
        url = f"{self.base_url}/{self.business_account_id}"
        fields = f"business_discovery.username({self.username}){{{data_fields}}}"
        params = { "fields": fields, "access_token": self.access_token}

        return requests.get(url, params = params).json()["business_discovery"]

    # メディアを取得
    def fetch_medias(self, data_fields):
        url = f"{self.base_url}/{self.business_account_id}"
        fields = f"business_discovery.username({self.username}){{media{{{data_fields}}}}}"
        params = { "fields": fields, "access_token": self.access_token}

        res = requests.get(url, params = params).json()["business_discovery"]
        media = []

        for i in range(len(res["media"]["data"])):
            media.append(res["media"]["data"][i])

        if "paging" not in res["media"].keys():
            return media

        if "after" not in res["media"]["paging"]["cursors"].keys():
            return media
        
        # Instagram Graph APIの仕様上、一度のリクエストで取得できるのは25件までなので、それ以上取得したい場合は複数回リクエストを送る                
        after = res["media"]["paging"]["cursors"]["after"]
        while after is not None:
            url = f"{self.base_url}/{self.business_account_id}"
            fields = f"business_discovery.username({self.username}){{media.after({after}){{{data_fields}}}}}"
            params = { "fields": fields, "access_token": self.access_token}

            res = requests.get(url, params = params).json()["business_discovery"]

            for i in range(len(res["media"]["data"])):
                media.append(res["media"]["data"][i])

            if "after" in res["media"]["paging"]["cursors"].keys():
                after = res["media"]["paging"]["cursors"]["after"]
            else:
                after = None

            sleep(1) # API制限にかからないよう適度に時間を空ける

        return media

    # インサイト（ユーザー）を取得
    def fetch_user_insight(self, metric, period):
        url = f"{self.base_url}/{self.business_account_id}/insights"
        params = { "metric": metric, "period": period, "access_token": self.access_token}

        return requests.get(url, params = params).json()["data"]

    # インサイト（メディア）を取得
    def fetch_media_insight(self, media_id, metric):
        url = f"{self.base_url}/{media_id}/insights"
        params = {"metric": metric, "access_token": self.access_token}
        return requests.get(url, params = params).json()["data"]

        


    
    