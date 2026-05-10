import os
import sqlite3

class DBActions:
    def __init__(self,data_base):
        self.data_base = data_base

    def close_db(self):
        self.data_base.close()

    def get_data(self)->dict:
        query = "SELECT username, password  FROM Users WHERE user_id='1' "
        my_cursor = self.data_base.cursor()
        my_cursor.execute(query)
        my_result = my_cursor.fetchall()
        admin_user = {"user_name":my_result[0][0],"password":my_result[0][1]}
        return admin_user
 
    def get_all_rooms_as_dicts(self):
        query = "SELECT * FROM rooms"
        cursor = self.data_base.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        all_rooms = []
        for row in rows:
            room_dict = {
                "room_number": str(row[1]),"room_price": str(row[2]),    
                "bed_type": str(row[3]), "accessible": "true" if row[4] == 1 else "false"}
            all_rooms.append(room_dict)
        return all_rooms