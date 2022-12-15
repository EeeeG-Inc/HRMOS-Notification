from modules.hrmos import Hrmos
from datetime import datetime
from zoneinfo import ZoneInfo

class HrmosWeeklyWorkloadNotificationForNotion:
    def __init__(self, user_black_list: list):
        self.hrmos = Hrmos()
        self.user_black_list = user_black_list
        self.jst_today = datetime.now(ZoneInfo("Asia/Tokyo"))
        self.str_this_month = self.jst_today.strftime('%Y-%m')

    def run(self) -> None:
        token = self.__get_authentication_token()
        self.__slack_post_via_webhook(
            self.__get_work_output_months_monthly(token, self.str_this_month),
            self.__get_users(token),
            self.str_this_month,
            self.jst_today.strftime("%Y-%m-%d")
        )

    """
    API Token を取得する
    """
    def __get_authentication_token(self) -> str:
        auth = self.hrmos.get_authentication_token()
        return auth['token']

    """
    ユーザ全員を取得
    """
    def __get_users(self, token: str) -> dict:
        users = {}
        for user in self.hrmos.get_users(token):
            if user['id'] in self.user_black_list:
                continue
            users[user['id']] = user
        return users

    """
    今月の全ユーザ月次レポートを取得
    """
    def __get_work_output_months_monthly(self, token: str, str_this_month: str) -> dict:
        work_output_months = {}
        for work_output_month in self.hrmos.get_work_output_months_monthly(token, str_this_month):
            if work_output_month['user_id'] in self.user_black_list:
                continue
            work_output_months[work_output_month['user_id']] = work_output_month
        return work_output_months

    """
    Slack 通知 (人数分)
    """
    def __slack_post_via_webhook(self, work_output_months: dict, users: dict, str_this_month: str, str_jst_today: str) -> None:
        text = f"{str_this_month} の勤怠情報\n\n"
        for user_id, work_output in work_output_months.items():
            text += self.hrmos.get_str_this_month_work_output(work_output, users[user_id], str_jst_today)
            self.hrmos.slack_post_via_webhook(
                text,
                'HRMOS This Month',
                ':hourglass_flowing_sand:',
                self.hrmos.config.webhook_urls['webhook_url_hrmos_weekly_workload_notification_for_notion']
            )
            text = ''

        print('Slack Post About HRMOS This Month Done!')
