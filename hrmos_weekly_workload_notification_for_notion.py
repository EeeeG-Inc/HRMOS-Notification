from hrmos import Hrmos
from datetime import datetime, timedelta

class HrmosWeeklyWorkloadNotificationForNotion:
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
        users = {}
        for user in hrmos.get_users(token):
            if user['id'] in self.user_black_list:
                continue
            users[user['id']] = user

        # 今月の全ユーザ日次勤怠データを取得
        work_output_months = {}
        today = datetime.now()
        str_today = today.strftime('%Y-%m-%d')
        str_this_month = today.strftime('%Y-%m')
        for work_output_month in hrmos.get_work_output_months_monthly(token, str_this_month):
            if work_output_month['user_id'] in self.user_black_list:
                continue
            work_output_months[work_output_month['user_id']] = work_output_month

        # Slack 通知
        text = f"{str_this_month} の勤怠情報\n\n"
        for user_id, work_output in work_output_months.items():
            text += hrmos.get_str_this_month_work_output(work_output, users[user_id], str_today)
            hrmos.slack_post_via_webhook(text, 'HRMOS This Month', ':hourglass_flowing_sand:', hrmos.config.webhook_urls['webhook_url_hrmos_yesterday_notification'])
            text = ''

        print('Slack Post About HRMOS This Month Done!')


hrmos_weekly_workload_notification_for_notion = HrmosWeeklyWorkloadNotificationForNotion()
hrmos_weekly_workload_notification_for_notion.run()
