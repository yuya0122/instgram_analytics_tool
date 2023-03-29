import configparser
import datetime
import os
import time
import logging

from client.spread_sheet_client import SpreadSheetClient
from client.instagram_graph_client import InstagramGraphClient
from core.base import Base

class Task(Base):
    
    def __init__(self):
        self.ssc = SpreadSheetClient(
            key_file_path=os.path.join(self._PROJECT_ROOT, self.config["dirs"]["secret_dir"], self.config["spread_sheet"]["key_file_name"])
        )
        self.igc = InstagramGraphClient(
            base_url=self.config["instagram_api"]["base_url"], 
            business_account_id=self.config["instagram_api"]["business_account_id"],
            access_token=self.config["instagram_api"]["access_token"], 
            username=self.config["instagram_api"]["username"]
        )

    def write_user_insight(self):
        self.logger.info("start: write_user_insight")  
        # ユーザーインサイトの取得
        res = self.igc.fetch_user_insight(
            metric="impressions,reach,profile_views",
            period="day"
            )
        self.logger.info(res)
        wb = self.ssc.open_workbook_by_name(name=self.config["spread_sheet"]["book_name"])
        ws = wb.worksheet("result_user_insight")
        # 前日
        end_time = res[0]["values"][0]["end_time"]
        impressions = res[0]["values"][0]["value"]
        reach = res[1]["values"][0]["value"]
        profile_views = res[2]["values"][0]["value"]
        ws.append_row(values=[end_time, impressions, reach, profile_views])
        # 当日
        end_time = res[0]["values"][1]["end_time"]
        impressions = res[0]["values"][1]["value"]
        reach = res[1]["values"][1]["value"]
        profile_views = res[2]["values"][1]["value"]
        # result_sheetへ結果書き込み
        ws.append_row(values=[end_time, impressions, reach, profile_views])
        self.logger.info("finish: write_user_insight")  
            
    def write_media_insight(self):
        self.logger.info("start: write_media_insight")  
        # メディア一覧の取得
        list_media = self.igc.fetch_medias(
            data_fields="timestamp,caption,like_count,comments_count,mediaproducttype,media_type"
        )
        # メディアごとのインサイトを取得
        list_media_info = []
        for media in list_media:
            # engagement: いいね数・コメント数・保存数の合計、reach: メディアを閲覧したユニークユーザーの合計数、impressions: メディアが閲覧された合計回数、saved: 保存数
            try:
                media_insight = self.igc.fetch_media_insight(media["id"],metric="reach,impressions,saved")
            except Exception as e:
                continue
            list_media_info.append({
                "media": media,
                "insight": media_insight
            })
        # result_sheetへ結果書き込み
        wb = self.ssc.open_workbook_by_name(name=self.config["spread_sheet"]["book_name"])
        ws = wb.worksheet("result_media_insight")
        dt = datetime.datetime.now()
        dt = dt.strftime("%Y-%m-%d %H:%M:%S")
        for media_info in list_media_info:
            media = media_info["media"]
            insight = media_info["insight"]
            # media
            id = media["id"]
            media_type = media["media_type"]
            timestamp = media["timestamp"]
            caption = media["caption"]
            like_count = media["like_count"]
            comments_count = media["comments_count"]
            # insight
            reach = insight[0]["values"][0]["value"]
            impressions = insight[1]["values"][0]["value"]
            saved = insight[2]["values"][0]["value"]
            # result_sheetへ結果書き込み
            self.logger.info(media_info)
            ws.append_row(values=[dt, id, media_type, timestamp, caption, like_count, comments_count, reach, impressions, saved])
        self.logger.info("finish: write_media_insight")  


    def execute(self):
        self.logger.info("start execute task")
        self.write_user_insight()
        self.write_media_insight()
        self.logger.info("finish execute task")


