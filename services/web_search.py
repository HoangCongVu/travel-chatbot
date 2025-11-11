from utils.web_search import general_web_search
import json

class WebSearchService:
    """Service để tìm kiếm thông tin thời gian thực trên web"""
    
    @staticmethod
    def search_web_information(query: str, num_results: int = 5) -> str:
        """
        Tìm kiếm thông tin thời gian thực trên web
        
        Args:
            query: Câu hỏi/từ khóa tìm kiếm
            num_results: Số kết quả tối đa (mặc định 5)
            
        Returns:
            JSON string chứa kết quả tìm kiếm
        """
        try:
            result = general_web_search(query, num_results)
            
            if "error" in result:
                return json.dumps({
                    "success": False,
                    "error": result["error"],
                    "message": "Không thể tìm kiếm thông tin lúc này"
                }, ensure_ascii=False)
            
            return json.dumps({
                "success": True,
                "query": result["query"],
                "summary": result["summary"],
                "sources": result["sources"],
                "total_results": len(result["sources"])
            }, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": str(e),
                "message": "Đã xảy ra lỗi khi tìm kiếm thông tin"
            }, ensure_ascii=False)
