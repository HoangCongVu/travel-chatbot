class MessageRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_message_by_id(self, message_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM messages WHERE id = %s", (message_id,))
        return cursor.fetchone()

    def save_message(self, message_data):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "INSERT INTO messages (content, sender_id, receiver_id) VALUES (%s, %s, %s)",
            (message_data['content'], message_data['sender_id'], message_data['receiver_id'])
        )
        self.db_connection.commit()
        return cursor.lastrowid

    def delete_message(self, message_id):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM messages WHERE id = %s", (message_id,))
        self.db_connection.commit()
        return cursor.rowcount