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
 