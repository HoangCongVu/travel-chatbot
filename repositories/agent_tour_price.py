import json
import uuid
from agents.agent_tour_price import agent_tour_price
from services.visa_price import VisaPriceService
from services.price_by_package import PriceByPackageService
from services.price_by_date import PriceByDateService
from models.visa_price import CreateVisaPrice
from models.price_by_package import CreatePriceByPackage
from models.price_by_date import CreatePriceByDate

class AgentTourPriceRepository:
    
    @staticmethod
    def extract_prices_from_text(payload: str, tour_id: uuid.UUID) -> dict:
        try:
            reply = agent_tour_price.generate_reply(
                messages=[{"role": "user", "content": payload}]
            )
            
            try:
                data = json.loads(reply)
            except json.JSONDecodeError:
                print("❌ Lỗi JSON từ AI. Trả về mảng rỗng.")
                data = {
                    "visa_prices": [],
                    "price_by_packages": [],
                    "price_by_dates": []
                }

            # Lấy các mảng con, mặc định là [] nếu không tồn tại
            visa_prices = data.get("visa_prices", [])
            price_by_packages = data.get("price_by_packages", [])
            price_by_dates = data.get("price_by_dates", [])

            # Lưu vào bảng visa_prices
            for item in visa_prices:
                record = CreateVisaPrice(tour_id=tour_id, price=item.get("price"))
                VisaPriceService.create(record)

            # Lưu vào bảng price_by_packages
            for item in price_by_packages:
                record = CreatePriceByPackage(
                    tour_id=tour_id,
                    package_name=item.get("package_name"),
                    price=item.get("price")
                )
                PriceByPackageService.create(record)

            # Lưu vào bảng price_by_dates
            for item in price_by_dates:
                record = CreatePriceByDate(
                    tour_id=tour_id,
                    date=item.get("date"),
                    price=item.get("price")
                )
                PriceByDateService.create(record)

            return {
                "tour_id": tour_id,
                "prices": data
            }

        except Exception as e:
            print("❌ Lỗi khi trích xuất giá tour:", str(e))
            return {
                "error": "Không thể xử lý dữ liệu đầu vào",
                "message": str(e)
            }