"""
Repository cho Follow-up Settings
"""
import uuid
from db import Session
from models.follow_up_settings import FollowUpSettings, FollowUpSettingsResponse, UpdateFollowUpSettingsRequest


class FollowUpSettingsRepository:
    
    @staticmethod
    def get_settings() -> FollowUpSettingsResponse | None:
        """
        Lấy cấu hình follow-up (chỉ có 1 record duy nhất)
        """
        with Session() as session:
            settings = session.query(FollowUpSettings).first()
            if settings:
                return FollowUpSettingsResponse.model_validate(settings)
            return None
    
    @staticmethod
    def create_default_settings() -> FollowUpSettingsResponse:
        """
        Tạo settings mặc định (gọi 1 lần duy nhất khi khởi tạo hệ thống)
        """
        with Session() as session:
            settings = FollowUpSettings(
                is_enabled=False,
                delay_minutes=30,
                max_count=3,
                active_hours_start=8,
                active_hours_end=22,
                scan_interval_minutes=1
            )
            session.add(settings)
            session.commit()
            session.refresh(settings)
            return FollowUpSettingsResponse.model_validate(settings)
    
    @staticmethod
    def update_settings(payload: UpdateFollowUpSettingsRequest, admin_id: uuid.UUID | None = None) -> FollowUpSettingsResponse:
        """
        Cập nhật cấu hình follow-up
        Tự động tạo settings mặc định nếu chưa có
        """
        with Session() as session:
            settings = session.query(FollowUpSettings).first()
            
            # Nếu chưa có settings, tạo mặc định
            if not settings:
                settings = FollowUpSettings(
                    is_enabled=False,
                    delay_minutes=30,
                    max_count=3,
                    active_hours_start=8,
                    active_hours_end=22,
                    scan_interval_minutes=1
                )
                session.add(settings)
                session.flush()  # Để có ID
            
            # Update các field
            update_data = payload.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(settings, field, value)
            
            # Update admin_id nếu có
            if admin_id:
                settings.admin_id = admin_id
            
            session.commit()
            session.refresh(settings)
            return FollowUpSettingsResponse.model_validate(settings)