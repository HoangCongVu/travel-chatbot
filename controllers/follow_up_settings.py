"""
Controller cho Follow-up Management
API để quản lý và giám sát follow-up messages
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Optional
import uuid

from services.follow_up_settings import FollowUpService
from models.follow_up_settings import UpdateFollowUpSettingsRequest
from utils.follow_up_scheduler import get_scheduler
from middleware.auth import get_current_admin

router = APIRouter(tags=["Follow-up"])

follow_up_settings = FollowUpService()


class ManualFollowUpRequest(BaseModel):
    """Request để gửi follow-up thủ công"""
    chat_id: uuid.UUID


class FollowUpToggleRequest(BaseModel):
    """Request để bật/tắt follow-up"""
    action: str  # "enable" hoặc "disable"


@router.get("/follow-up/status")
def get_follow_up_status() -> Dict:
    """
    Lấy trạng thái và cấu hình follow-up
    
    Returns:
        Dict chứa status + settings
    """
    settings = FollowUpService.get_settings()
    
    if not settings:
        raise HTTPException(
            status_code=404,
            detail="Settings not found. Please initialize the system first."
        )
    
    return {
        "status": "success",
        "data": {
            "is_enabled": settings.is_enabled,
            "delay_minutes": settings.delay_minutes,
            "max_count": settings.max_count,
            "active_hours": f"{settings.active_hours_start}h - {settings.active_hours_end}h",
            "scan_interval_minutes": settings.scan_interval_minutes
        }
    }


@router.post("/follow-up/toggle")
def toggle_follow_up(
    request: FollowUpToggleRequest,
    current_admin: str = Depends(get_current_admin)
) -> Dict:
    """
    Bật/tắt follow-up feature - Chỉ admin được phép
    
    Actions:
    - "enable": Bật follow-up + start scheduler
    - "disable": Tắt follow-up + stop scheduler
    
    Args:
        request: action (enable/disable)
        current_admin: Admin ID từ JWT token
        
    Returns:
        Dict chứa kết quả
    """
    try:
        scheduler = get_scheduler()
        admin_uuid = uuid.UUID(current_admin)
        
        if request.action == "enable":
            # Cập nhật DB
            settings = FollowUpService.update_settings(
                UpdateFollowUpSettingsRequest(is_enabled=True),
                admin_id=admin_uuid
            )
            
            # Start scheduler
            if not scheduler.is_running:
                scheduler.start()
            message = "Follow-up enabled and scheduler started"
            
        elif request.action == "disable":
            # Cập nhật DB
            settings = FollowUpService.update_settings(
                UpdateFollowUpSettingsRequest(is_enabled=False),
                admin_id=admin_uuid
            )
            
            # Stop scheduler
            if scheduler.is_running:
                scheduler.stop()
            message = "Follow-up disabled and scheduler stopped"
            
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid action: {request.action}. Use: enable or disable"
            )
        
        return {
            "status": "success",
            "message": message,
            "data": {
                "is_enabled": settings.is_enabled
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error toggling follow-up: {str(e)}"
        )


@router.post("/follow-up/config")
def configure_follow_up(
    request: UpdateFollowUpSettingsRequest,
    current_admin: str = Depends(get_current_admin)
) -> Dict:
    """
    Cấu hình follow-up settings - Chỉ admin được phép
    
    Args:
        request: Các tham số cần update
        current_admin: Admin ID từ JWT token
        
    Returns:
        Dict chứa settings mới
    """
    try:
        admin_uuid = uuid.UUID(current_admin)
        # Validate
        if request.delay_minutes is not None and request.delay_minutes < 1:
            raise HTTPException(
                status_code=400,
                detail="delay_minutes must be >= 1"
            )
        
        if request.max_count is not None and request.max_count < 1:
            raise HTTPException(
                status_code=400,
                detail="max_count must be >= 1"
            )
        
        if request.active_hours_start is not None and not (0 <= request.active_hours_start <= 23):
            raise HTTPException(
                status_code=400,
                detail="active_hours_start must be between 0-23"
            )
        
        if request.active_hours_end is not None and not (0 <= request.active_hours_end <= 23):
            raise HTTPException(
                status_code=400,
                detail="active_hours_end must be between 0-23"
            )
        
        if request.scan_interval_minutes is not None and request.scan_interval_minutes < 1:
            raise HTTPException(
                status_code=400,
                detail="scan_interval_minutes must be >= 1"
            )
        
        # Cập nhật vào DB
        settings = FollowUpService.update_settings(request, admin_id=admin_uuid)
        
        return {
            "status": "success",
            "message": "Configuration updated",
            "data": {
                "delay_minutes": settings.delay_minutes,
                "max_count": settings.max_count,
                "active_hours": f"{settings.active_hours_start}h - {settings.active_hours_end}h",
                "scan_interval_minutes": settings.scan_interval_minutes
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error configuring follow-up: {str(e)}"
        )


@router.post("/follow-up/trigger")
def trigger_follow_up_scan() -> Dict:
    """
    Trigger scan follow-up ngay lập tức (testing)
    
    Returns:
        Dict chứa kết quả scan
    """
    scheduler = get_scheduler()
    scheduler.run_now()
    
    return {
        "status": "success",
        "message": "Follow-up scan triggered successfully"
    }


@router.post("/follow-up/manual")
def send_manual_follow_up(request: ManualFollowUpRequest) -> Dict:
    """
    Gửi follow-up thủ công cho 1 chat cụ thể
    
    Args:
        request: Chứa chat_id cần gửi follow-up
        
    Returns:
        Dict chứa kết quả
    """
    try:
        message_id = follow_up_settings.send_follow_up_message(request.chat_id)
        
        if message_id:
            return {
                "status": "success",
                "message": "Follow-up sent successfully",
                "data": {
                    "message_id": str(message_id),
                    "chat_id": str(request.chat_id)
                }
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to send follow-up message"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error sending follow-up: {str(e)}"
        )
