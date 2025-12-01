"""
Background Scheduler cho Follow-up Messages
Sử dụng APScheduler để định kỳ quét và gửi follow-up
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging
import threading

from services.follow_up_settings import FollowUpService
from agents.follow_up_agents import FollowUpConfig

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FollowUpScheduler:
    """Scheduler quản lý background jobs cho follow-up"""
    
    def __init__(self):
        """Khởi tạo scheduler"""
        self.scheduler = None
        self.follow_up_settings = FollowUpService()
        self.is_running = False
        self._lock = threading.Lock()
    
    def _ensure_scheduler(self):
        """Khởi tạo scheduler mới nếu chưa có hoặc đã shutdown"""
        if self.scheduler is None:
            self.scheduler = BackgroundScheduler()
    
    def _follow_up_job(self):
        """
        Job chính: Quét và gửi follow-up messages
        Được gọi định kỳ theo SCAN_INTERVAL_MINUTES
        """
        try:
            logger.info(f"🔄 [Follow-up Job] Starting at {datetime.now()}")
            
            # Xử lý tất cả follow-ups
            stats = self.follow_up_settings.process_all_followups()
            
            logger.info(
                f"✅ [Follow-up Job] Completed - "
                f"Success: {stats['success']}, "
                f"Failed: {stats['failed']}, "
                f"Total: {stats['total']}"
            )
            
        except Exception as e:
            logger.error(f"❌ [Follow-up Job] Error: {e}", exc_info=True)
    
    def start(self):
        """
        Khởi động scheduler
        
        Scheduler sẽ chạy job follow-up mỗi scan_interval_minutes phút (từ DB)
        """
        with self._lock:
            if self.is_running:
                logger.warning("⚠️ Scheduler is already running")
                return
            
            self._ensure_scheduler()
            
            # Lấy cấu hình từ DB
            settings = FollowUpConfig.get_settings()
            
            # Thêm job vào scheduler
            self.scheduler.add_job(
                func=self._follow_up_job,
                trigger=IntervalTrigger(minutes=settings.scan_interval_minutes),
                id='follow_up_job',
                name='Follow-up Message Scanner',
                replace_existing=True
            )
            
            # Khởi động scheduler
            self.scheduler.start()
            self.is_running = True
            
            logger.info(
                f"🚀 Follow-up Scheduler started! "
                f"Scanning every {settings.scan_interval_minutes} minutes. "
                f"Active hours: {settings.active_hours_start}h - {settings.active_hours_end}h"
            )
    
    def stop(self):
        """Dừng scheduler"""
        with self._lock:
            if not self.is_running:
                logger.warning("⚠️ Scheduler is not running")
                return
            
            if self.scheduler:
                self.scheduler.shutdown(wait=False)
                self.scheduler = None
            
            self.is_running = False
            logger.info("🛑 Follow-up Scheduler stopped")
    
    def run_now(self):
        """
        Chạy follow-up job ngay lập tức (không chờ schedule)
        Hữu ích cho testing hoặc trigger thủ công
        """
        logger.info("▶️ Running follow-up job manually...")
        self._follow_up_job()


# Global instance
_scheduler_instance = None


def get_scheduler() -> FollowUpScheduler:
    """
    Lấy singleton instance của scheduler
    
    Returns:
        FollowUpScheduler instance
    """
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = FollowUpScheduler()
    return _scheduler_instance
