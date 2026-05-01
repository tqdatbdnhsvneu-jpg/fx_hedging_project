import os
import pandas as pd
from datetime import datetime
import pytz

class StorageManager:
    """GitOps and local persistence tracking module."""

    def __init__(self):
        self.history_dir = "history"
        self.logs_dir = "logs"
        self.file_path = os.path.join(self.history_dir, "performance_log.csv")
        self.tz = pytz.timezone("Asia/Ho_Chi_Minh")
        
        os.makedirs(self.history_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)

    def save_daily_record(self, current_rate: float, forecast_signal: str, ai_suggestions: list):
        """Archives operational metrics natively tracking time aligned with GMT+7."""
        now = datetime.now(self.tz)
        today_date = now.strftime("%Y-%m-%d %H:%M:%S")
        
        data = {
            "timestamp": [today_date],
            "spot_rate": [current_rate],
            "prophet_signal": [forecast_signal],
            "ai_feature_suggestions": [str(ai_suggestions)]
        }
        
        df_new = pd.DataFrame(data)
        
        if not os.path.isfile(self.file_path):
            df_new.to_csv(self.file_path, index=False)
        else:
            df_new.to_csv(self.file_path, mode='a', header=False, index=False)
