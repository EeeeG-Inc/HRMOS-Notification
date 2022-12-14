from dotenv import load_dotenv
import os

load_dotenv()


class Config():
    def __init__(self):
        is_debug = os.getenv('IS_DEBUG')

        if is_debug is None:
            self.is_debug = False
        else:
            self.is_debug = bool(int(is_debug))

        self.END_POINT = 'https://ieyasu.co/api/' + os.getenv('COMPANY_NAME')
        self.HRMOS_SECRET_KEY = os.getenv('HRMOS_SECRET_KEY')
        self.webhook_urls = {
            'default': os.getenv('WEBHOOK_URL_DEFAULT'),
            'webhook_url_hrmos_weekly_workload_notification_for_notion': os.getenv('WEBHOOK_URL_HRMOS_WEEKLY_WORKLOAD_NOTIFICATION_FOR_NOTION'),
            'webhook_url_hrmos_yesterday_notification': os.getenv('WEBHOOK_URL_HRMOS_YESTERDAY_NOTIFICATION'),
        }
