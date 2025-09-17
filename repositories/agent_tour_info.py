import json
from agents.agent_tour_info import agent_tour, agent_tour_type
from services.tour import TourService
from services.tour_type import TourTypeService
from models.tour import TourCreateModel
from models.tour_type import CreateTourType, UpdateTourType


class AgentTourInfoRepository: 
    @staticmethod
    def extract_info_from_text(payload: str):
        try:
            # -------------------------------
            # B1: Trích xuất tour_type từ agent
            # -------------------------------
            tour_type_response = agent_tour_type.generate_reply(
                messages=[{"role": "user", "content": payload}],
            )
            tour_type_data = json.loads(tour_type_response)

            tour_type_id = tour_type_data.get("tour_type_id")
            tour_type_name = tour_type_data.get("tour_type_name")
            if not tour_type_id or not tour_type_name:
                raise ValueError("Agent không trả về đầy đủ tour_type_id và tour_type_name")

            # -------------------------------
            # B2: Kiểm tra tour_type trong DB
            # -------------------------------
            tour_type = TourTypeService.get(tour_type_id)
            if tour_type:
                # Nếu tên khác agent trả về, update lại
                if tour_type.type_name != tour_type_name:
                    update_data = UpdateTourType(type_name=tour_type_name)
                    tour_type = TourTypeService.update(tour_type_id, update_data)
            else:
                # Nếu chưa có, tạo mới với id + name từ agent
                new_type = CreateTourType(id=tour_type_id, type_name=tour_type_name)
                tour_type = TourTypeService.create(new_type)

            # -------------------------------
            # B3: Trích xuất thông tin tour từ agent
            # -------------------------------
            main_response = agent_tour.generate_reply(
                messages=[{"role": "user", "content": payload}],
            )
            main_data = json.loads(main_response)

            # -------------------------------
            # B4: Gộp dữ liệu tour
            # -------------------------------
            combined_data = {
                **main_data,
                # "price_type": tour_type_data.get("price_type", "Một giá"),
                "tour_type_id": tour_type.id,
            }

            # -------------------------------
            # B5: Tạo tour
            # -------------------------------
            new_tour = TourCreateModel(**combined_data)
            new_tour = TourService.create(new_tour)

            print("✅ Đã tạo tour:", new_tour.id)
            return new_tour.id

        except Exception as e:
            print("❌ Lỗi khi trích xuất tour:", str(e))
            return {
                "error": "Không thể xử lý dữ liệu đầu vào",
                "message": str(e),
            }
