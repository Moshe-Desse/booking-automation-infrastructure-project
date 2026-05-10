BOOKING_BASE_URL = "https://automationintesting.online/api/" 
USER_NAME = "admin"
PASSWORD = "password"
LOGIN_RESOURCE = "auth/login"
EXPECTED_LATENCY_MS = 1500
EXPECTED_STATUS_SUCCESS_CODE = 200
EXPECTED_CREATED_SUCCESS_CODE = 201
EXPECTED_UNAUTHORIZED_CODE = 401 
EXPECTED_DELETE_CODE = 405
EXPECTED_FAILED_CODE = 409
CHECK_IN_DATE = "2026-05-29"
CHECK_OUT_DATE = "2026-05-30"
INVALID_ID = 9999
NEW_ROOM_DATA_01 = {
        "roomName": "101",
        "type": "Suite",
        "accessible": True,
        "image": "https://link-to-image.com/room.png",
        "description": "Nice suite with freshing Mini Bar and WiFi",
        "roomPrice": 300,
        "features": ["WiFi", "Mini Bar"]
                }
NEW_ROOM_DATA_02 = {
    "roomName": "999",
    "type": "Double",
    "accessible": True,
    "image": "/images/room999.jpg",
    "description": "This is a test room created by automation",
    "features": ["WiFi", "TV"],
    "roomPrice": 250
}