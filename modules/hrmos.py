from modules.config import Config
import json
from pprint import pprint
import requests
from zoneinfo import ZoneInfo

class Hrmos():
    def __init__(self):
        self.config = Config()

    """
    HRMOS の API Secret Key を利用して Basic 認証を行い、有効期限が 1 日に限定された API Token を取得する
    """
    def get_authentication_token(self) -> dict:
        return requests.get(
            self.config.END_POINT + '/v1/authentication/token',
            headers={
                'Authorization': 'Basic ' + self.config.HRMOS_SECRET_KEY,
                'Content-Type': 'application/json',
            }
        ).json()

    """
    会社に所属する全ユーザを取得
    """
    def get_users(self, token: str) -> dict:
        return requests.get(
            self.config.END_POINT + '/v1/users',
            headers={
                'Authorization': 'Token ' + token,
                'Content-Type': 'application/json',
            }
        ).json()

    """
    指定日による、全ユーザ日次勤怠データ (1日分) を取得
    """
    def get_work_outputs_daily(self, token: str, day: str) -> dict:
        return requests.get(
            self.config.END_POINT + '/v1/work_outputs/daily/' + day,
            headers={
                'Authorization': 'Token ' + token,
                'Content-Type': 'application/json',
            }
        ).json()

    """
    指定月による、全ユーザ日次勤怠データ (存在する全ての日付) を取得
    """
    def get_work_outputs_monthly(self, token: str, month: str) -> dict:
        return requests.get(
            self.config.END_POINT + '/v1/work_outputs/monthly/' + month,
            headers={
                'Authorization': 'Token ' + token,
                'Content-Type': 'application/json',
            }
        ).json()

    """
    指定月による、全ユーザ月次レポートを取得
    """
    def get_work_output_months_monthly(self, token: str, month: str) -> dict:
        return requests.get(
            self.config.END_POINT + '/v1/work_output_months/monthly/' + month,
            headers={
                'Authorization': 'Token ' + token,
                'Content-Type': 'application/json',
            }
        ).json()

    """
    Slack 投稿用のテキストを作成 (yesterday)
    """
    def get_str_yesterday_work_output(self, work_output: dict) -> str:
        start_at = work_output["start_at"] if work_output["start_at"] else '[No Data]'
        end_at = work_output["end_at"] if work_output["end_at"] else '[No Data]'
        total_working_hours = work_output["total_working_hours"] if work_output["total_working_hours"] else '[No Data]'

        text = f'■ {work_output["full_name"]}\n' + \
            f'勤務時間: {start_at} - {end_at}\n' + \
            f'稼働時間: {total_working_hours}\n\n'
        return text

    """
    Slack 投稿用のテキストを作成 (month)
    """
    def get_str_this_month_work_output(self, work_output: dict, user: dict, today: str) -> str:
        full_name = user["last_name"] + user["first_name"]
        total_working_hours = work_output["total_working_hours"] if work_output["total_working_hours"] else '[No Data]'
        over_work_time = work_output["over_work_time"] if work_output["over_work_time"] else '[No Data]'

        text = f'■ {full_name}\n' + \
            f'```\n' + \
            f'|Name|Date|稼働時間|残業時間|残業理由|\n' + \
            f'|:-|:-|:-|:-|:-|\n' + \
            f'|{full_name}|{today}|{total_working_hours}|{over_work_time}||\n' + \
            f'```\n'
        return text

    """
    Slack チャンネルに Webhook で Post する
    """
    def slack_post_via_webhook(self, text: str, bot_name: str, bot_emoji: str, webhook_url: str) -> None:
        if self.config.is_debug:
            webhook_url = self.config.webhook_urls['default']

        requests.post(webhook_url, json.dumps({
            'text': text,
            'username': bot_name,
            'icon_emoji': bot_emoji,
            'link_names': 1,
        }))
