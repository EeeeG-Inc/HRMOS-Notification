from modules.hrmos import Hrmos
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

class HrmosYesterdayNotification:
    def __init__(self):
        self.hrmos = Hrmos()

        # 通知不要なユーザID
        self.user_black_list = [
            1,
            2,
            3,
            4,
            5,
            6,
        ]

    def run(self) -> None:
        # API Token を取得する
        token = self.__get_authentication_token()

        # 昨日の全ユーザ日次勤怠データを取得
        jst_yesterday = datetime.now(ZoneInfo("Asia/Tokyo")) - timedelta(1)
        str_jst_yesterday = jst_yesterday.strftime("%Y-%m-%d")
        work_outputs = self.__get_work_outputs_daily(token, str_jst_yesterday)

        # Slack 通知
        self.__slack_post_via_webhook(work_outputs, str_jst_yesterday)

    def __get_authentication_token(self) -> str:
        auth = self.hrmos.get_authentication_token()
        return auth['token']

    def __get_work_outputs_daily(self, token: str, str_jst_yesterday: str) -> dict:
        work_outputs = {}
        for work_output in self.hrmos.get_work_outputs_daily(token, str_jst_yesterday):
            if work_output['user_id'] in self.user_black_list:
                continue
            work_outputs[work_output['user_id']] = work_output
        return work_outputs

    def __slack_post_via_webhook(self, work_outputs: dict, str_jst_yesterday: str) -> None:
        text = f"{str_jst_yesterday} の勤怠情報\n\n"
        for user_id, work_output in work_outputs.items():
            text += self.hrmos.get_str_yesterday_work_output(work_output)
        self.hrmos.slack_post_via_webhook(text, 'HRMOS Yesterday', ':hourglass:', self.hrmos.config.webhook_urls['webhook_url_hrmos_yesterday_notification'])
        print('Slack Post About HRMOS Yesterday Done!')
