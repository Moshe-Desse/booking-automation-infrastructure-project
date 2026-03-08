BOOKING_BASE_URL = "https://automationintesting.online/api/" 
USERNAME = "admin"
PASSWORD = "password"
LOGIN_RESOURCE = "auth/login"
EXPECTED_STATUS_SUCCESS_CODE = 200
NEW_ROOM_DATA = {
        "roomName": "101",
        "type": "Suite",
        "accessible": True,
        "image": "https://link-to-image.com/room.png",
        "description": "Nice suite with freshing Mini Bar and WiFi",
        "roomPrice": 300,
        "features": ["WiFi", "Mini Bar"]
                }