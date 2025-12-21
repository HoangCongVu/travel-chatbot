"""
Utility functions for time-related operations
"""

from datetime import datetime


def get_time_context() -> dict:
    """
    Lấy thông tin thời gian hiện tại để sử dụng trong các system messages
    
    Returns:
        Dict chứa thông tin thời gian
    """
    now = datetime.now()
    
    # Thứ trong tuần
    weekday_map = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
    current_weekday = weekday_map[now.weekday()]
    
    # Định dạng ngày tháng
    current_date = now.strftime("%d/%m/%Y")
    current_day = now.day
    current_month = now.month
    current_year = now.year
    
    # Tính tháng tới
    next_month = current_month + 1 if current_month < 12 else 1
    next_year = current_year if current_month < 12 else current_year + 1
    
    # Tên tháng
    month_names = ["", "Tháng Một", "Tháng Hai", "Tháng Ba", "Tháng Tư", "Tháng Năm", "Tháng Sáu",
                   "Tháng Bảy", "Tháng Tám", "Tháng Chín", "Tháng Mười", "Tháng Mười Một", "Tháng Mười Hai"]
    current_month_name = month_names[current_month]
    next_month_name = month_names[next_month]
    
    # Mùa du lịch
    if 5 <= current_month <= 8:
        season = "Hè/Cao điểm (du lịch biển)"
    elif 9 <= current_month <= 11:
        season = "Thu (miền Bắc, Tây Nguyên)"
    elif current_month == 12 or current_month <= 2:
        season = "Đông (Sapa, miền Nam)"
    else:
        season = "Xuân (ngắm hoa, lễ hội)"
    
    # Cuối tuần
    days_until_weekend = (5 - now.weekday()) % 7
    if days_until_weekend == 0:
        weekend_info = "hôm nay là cuối tuần"
    elif days_until_weekend == 1:
        weekend_info = "cuối tuần là ngày mai"
    else:
        weekend_info = f"cuối tuần còn {days_until_weekend} ngày"
    
    return {
        "weekday": current_weekday,
        "date": current_date,
        "day": current_day,
        "month": current_month,
        "year": current_year,
        "month_name": current_month_name,
        "next_month": next_month,
        "next_month_name": next_month_name,
        "season": season,
        "weekend_info": weekend_info
    }
