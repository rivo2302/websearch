import datetime
from ampalibe import Model
from ampalibe import Logger


class CustomModel(Model):
    def __init__(self):
        super().__init__()

    @Model.verif_db
    def set_name(self, user_id, name):

        req = """
            UPDATE amp_user SET name = %s WHERE user_id = %s;
        """
        try:
            self.cursor.execute(req, (name, user_id))
            self.db.commit()
            return True
        except Exception as e:
            Logger.error(e)
            self.db.rollback()
            return False

    @Model.verif_db
    def get_name(self, user_id):
        req = """
            SELECT name FROM amp_user WHERE user_id = %s
        """
        res = self.cursor.execute(req, (user_id,))
        if res:
            return self.cursor.fetchone()[0]
        self.cursor.close()
        return None

    @Model.verif_db
    def add_query(self, user_id, query, type):
        # First I have to get the ID facebook of the user
        req = """
            SELECT id FROM amp_user WHERE user_id = %s
        """
        self.cursor.execute(req, (user_id,))
        id = self.cursor.fetchone()[0]
        self.db.commit()
        if not id:
            return False

        req = """
            INSERT INTO amp_report (amp_user_id, query,type,count,create_date) VALUES (%s, %s,%s,1,%s)
        """
        try:
            self.cursor.execute(
                req, (id, query, type, datetime.datetime.now())
            )
            self.db.commit()
            return True
        except Exception as e:
            Logger.error(e)
            self.db.rollback()
            return False
