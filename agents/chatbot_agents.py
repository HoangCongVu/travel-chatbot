"""
Setup và định nghĩa các AI agents cho chatbot
"""
import os
from autogen import AssistantAgent, UserProxyAgent
from services.tour_search import TourSearchService
from services.web_search import WebSearchService
from utils.agent_prompts import (
    get_coordinator_system_message,
    get_recommendation_system_message,
    get_user_proxy_system_message
)


# Cấu hình LLM
CONFIG_LIST = [
    {
        "model": "gpt-4o-mini",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]

# Tool schemas cho các chức năng tìm kiếm
TOOLS_SCHEMA = [
    {
 "type": "function",
        "function": {
            "name": "search_tour_chat", 
            "description": "Sử dụng hàm này để tìm kiếm tour du lịch dựa trên MỘT HOẶC NHIỀU tiêu chí: địa điểm, khoảng giá, và/hoặc ngày khởi hành.",
            "parameters": { 
                "type": "object", 
                "properties": { 
                    "destination": { 
                        "type": "string", 
                        "description": "Tên địa điểm người dùng muốn tìm. Ví dụ: 'Đà Nẵng', 'Singapore'"
                    },
                    "min_price": {
                        "type": "number",
                        "description": "Giá tối thiểu (VNĐ). Suy luận từ 'giá rẻ', 'từ X triệu'. Mặc định là 0."
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Giá tối đa (VNĐ). Suy luận từ 'giá rẻ', 'dưới X triệu'. Ví dụ: 'dưới 5 triệu' -> 5000000"
                    },
                    "target_date": {
                        "type": "string",
                        "description": "Ngày khởi hành mong muốn (YYYY-MM-DD). Suy luận từ 'cuối tuần', 'tháng 12'."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Số lượng tour tối đa trả về (mặc định là 3)",
                        "default": 3
                    }
                },
                "required": [], # Không bắt buộc tham số nào, để agent linh hoạt
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_web_information",
            "description": "Tìm kiếm thông tin thời gian thực trên web (Google Search). Sử dụng khi người dùng hỏi về thông tin mới nhất, tin tức, thời tiết, sự kiện, hoặc thông tin không có trong cơ sở dữ liệu tour. Ví dụ: 'thời tiết Đà Nẵng hôm nay', 'lễ hội Singapore tháng 12', 'tin tức du lịch Việt Nam'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Câu hỏi hoặc từ khóa cần tìm kiếm trên web"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Số lượng kết quả tối đa (mặc định là 5)",
                        "default": 5
                    }
                },
                "required": ["query"],
            },
        },
    },
]


def create_user_proxy_agent():
    """
    Tạo UserProxy agent - Agent thực thi các function calls
    
    Returns:
        UserProxyAgent đã được config
    """
    user_proxy = UserProxyAgent(
        name="UserProxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,  # CHỈ reply 1 lần sau mỗi function call
        is_termination_msg=lambda x: x.get("content") is not None and "FINAL_ANSWER:" in x.get("content", ""),
        code_execution_config=False,
        system_message=get_user_proxy_system_message(),
        default_auto_reply=""  # Không reply mặc định
    )
    
    # Đăng ký các functions
    user_proxy.register_function(
        function_map={
            "search_tour_chat": TourSearchService.search_tour_chat,
            "search_web_information": WebSearchService.search_web_information
        }
    )
    
    return user_proxy


def create_coordinator_agent(context_message: str):
    """
    Tạo IntelligentCoordinator agent - Agent phân tích và điều phối
    
    Args:
        context_message: Context từ lịch sử chat
        
    Returns:
        AssistantAgent đã được config
    """
    return AssistantAgent(
        name="IntelligentCoordinator",
        system_message=get_coordinator_system_message(context_message),
        llm_config={"config_list": CONFIG_LIST, "tools": TOOLS_SCHEMA},
    )


def create_recommendation_agent():
    """
    Tạo RecommendationAgent - Agent chuyên gia tư vấn
    
    Returns:
        AssistantAgent đã được config
    """
    return AssistantAgent(
        name="RecommendationAgent", 
        system_message=get_recommendation_system_message(),
        llm_config={"config_list": CONFIG_LIST},
    )
