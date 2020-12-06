import mysql


class Connection(object):
    def __init__(self):
        self.db = self.connect()
        self.cursor = self.db.cursor()

    def connect(self):
        db = mysql.connector.connect(host='localhost',
                                     user='root',
                                     passwd='root',
                                     auth_plugin='mysql_native_password')
        return db

    def disconnect(self):
        self.cursor.close()
        self.db.close()


class DBCreator(Connection):
    def create_db(self):
        self.cursor.execute("CREATE DATABASE result")

    def create_table(self, name, fields):
        self.cursor.execute("USE result")
        self.cursor.execute("CREATE TABLE {} ({})".format(name, fields))


class Writer(Connection):
    def write(self, table_name, value, fields):
        self.cursor.execute("USE result")
        s_amount = "%s," * len(fields.split(','))
        s_amount = s_amount[:-1]
        query = "INSERT INTO {}({}) VALUES ({})".format(table_name, fields, s_amount)
        self.cursor.executemany(query, value)
        self.db.commit()


class Query(Connection):
    def create_index(self, index_name, table_name, column_name):
        self.cursor.execute("USE result")
        self.cursor.execute("CREATE INDEX {} ON {} ({})".format(index_name,
                                                                table_name,
                                                                column_name))
        self.db.commit()

    def count_students_in_rooms(self):
        self.cursor.execute("USE result")
        self.cursor.execute(
            """SELECT rooms.name, COUNT(students.id)
            FROM students
            LEFT JOIN rooms
            ON students.room = rooms.id
            GROUP BY rooms.id"""
        )
        result = self.cursor.fetchall()
        return result

    def find_rooms_with_max_diff_age(self):
        self.cursor.execute("USE result")
        self.cursor.execute(
            """SELECT rooms.name
            FROM rooms JOIN students
            ON rooms.id = students.room
            GROUP BY rooms.id
            ORDER BY DATEDIFF(MAX(students.birthday), MIN(students.birthday)) DESC
            LIMIT 5"""
        )
        result = self.cursor.fetchall()
        return result

    def find_rooms_with_min_avg_age(self):
        self.cursor.execute("USE result")
        self.cursor.execute(
            """SELECT rooms.name
            FROM rooms JOIN students
            ON rooms.id = students.room
            GROUP BY rooms.id
            ORDER BY AVG(students.birthday) ASC
            LIMIT 5"""
        )
        result = self.cursor.fetchall()
        return result

    def find_rooms_male_female(self):
        self.cursor.execute("USE result")
        self.cursor.execute(
            """SELECT rooms.name FROM rooms
            LEFT JOIN students  ON rooms.id = students.room
            WHERE students.sex IN ('F','M')
            GROUP BY students.room
            HAVING COUNT(DISTINCT students.sex) = 2
            ORDER BY students.room"""
        )
        result = self.cursor.fetchall()
        return result
