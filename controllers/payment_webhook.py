from fastapi import APIRouter, Request, HTTPException, Depends
from services.payment_webhook_service import PaymentWebhookService
import os

router = APIRouter()

SEPAY_WEBHOOK_KEY = os.getenv("SEPAY_WEBHOOK_KEY")

@router.post("/webhook/sepay")
async def sepay_webhook(request: Request):
    """
    Webhook endpoint để nhận thông báo từ SePay
    
    **Security:** Kiểm tra API key trong Authorization header
    
    **SePay webhook format:**
    ```json
    {
        "id": 123456,
        "transferId": "SEPAY_ABC123",
        "transferType": "in",
        "accountNumber": "0123456789",
        "amount": 17600000,
        "content": "Thanh toan booking ABC",
        "when": "2025-12-04 10:00:00"
    }
    ```
    
    **Luồng xử lý:**
    1. Verify API key
    2. Tìm payment theo transferId (transaction_id)
    3. Cập nhật payment_status = "success"
    4. Set paid_at = current time
    5. Cập nhật booking status = "confirmed"
    """
    # Debug: Log biến môi trường và header
    print(f"🔑 SEPAY_WEBHOOK_KEY from env: {SEPAY_WEBHOOK_KEY}")
    
    # 1. Kiểm tra Authorization
    auth = request.headers.get("authorization")
    print(f"📨 Authorization header received: {auth}")
    
    if not auth:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    expected_auth = f"apikey {SEPAY_WEBHOOK_KEY}"
    print(f"🔐 Expected authorization: {expected_auth}")
    
    if auth.lower() != expected_auth.lower():
        raise HTTPException(
            status_code=403, 
            detail=f"Invalid API Key. Expected: {expected_auth}, Got: {auth}"
        )

    # 2. Nhận dữ liệu
    body = await request.json()
    print(f"📦 Webhook body: {body}")

    # 3. Xử lý webhook
    service = PaymentWebhookService()
    result = await service.handle_webhook(body)
    
    if not result:
        # Nếu không tìm thấy payment, trả về success để SePay không gọi lại
        print("⚠️ Payment not found, but returning success to avoid retry")
        txn_id = body.get("code") or body.get("referenceCode") or body.get("transferId")
        return {
            "message": "Webhook received but payment not found",
            "transaction_id": txn_id,
            "status": "not_found"
        }

    return {
        "message": "Webhook processed successfully",
        "payment_id": str(result.id),
        "status": result.payment_status
    }
