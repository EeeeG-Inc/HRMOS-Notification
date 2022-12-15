from hrmos import Hrmos
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

class HrmosYesterdayNotification:
    def __init__(self):
        # 通知不要なユーザID
        self.user_black_list = [
            1,
            2,
            3,
            4,
            5,
            6,
        ]

    def run(self):
        hrmos = Hrmos()

        # API Token を取得する
        auth = hrmos.get_authentication_token()
        token = auth['token']

        # ユーザ全員を取得
        # users = {}
        # for user in hrmos.get_users(token):
        #     if user['id'] in self.user_black_list:
        #         continue
        #     users[user['id']] = user

        # 昨日の全ユーザ日次勤怠データを取得
        work_outputs = {}
        jst_yesterday = datetime.now(ZoneInfo("Asia/Tokyo")) - timedelta(1)
        str_jst_yesterday = jst_yesterday.strftime("%Y-%m-%d")
        for work_output in hrmos.get_work_outputs_daily(token, str_jst_yesterday):
            if work_output['user_id'] in self.user_black_list:
                continue
            work_outputs[work_output['user_id']] = work_output

        # Slack 通知
        text = f"{str_jst_yesterday} の勤怠情報\n\n"
        for user_id, work_output in work_outputs.items():
            text += hrmos.get_str_yesterday_work_output(work_output)

        hrmos.slack_post_via_webhook(text, 'HRMOS Yesterday', ':hourglass:', hrmos.config.webhook_urls['webhook_url_hrmos_yesterday_notification'])

        print('Slack Post About HRMOS Yesterday Done!')


hrmos_yesterday_notification = HrmosYesterdayNotification()
hrmos_yesterday_notification.run()
