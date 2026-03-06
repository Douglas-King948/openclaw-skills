"""Daily Report Sender - 飞书日报发送器"""

from .sender import send_daily_report, send_work_report, send_summary

__version__ = "1.0.0"
__all__ = ["send_daily_report", "send_work_report", "send_summary"]
