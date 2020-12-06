import os
import argparse
import json
from mysql.connector.errors import DatabaseError, IntegrityError
from loader import LoaderFactory
from dbhandler import DBCreator, Writer, Query


class JsonHandler(object):
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path) as load_file:
            return json.load(load_file)


class Parser(object):
    @staticmethod
    def create_arg_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('-rp', '--rooms_path', type=str, required=True)
        parser.add_argument('-sp', '--students_path', type=str, required=True)
        parser.add_argument('-f', '--format', type=str, required=True)
        return parser

    @staticmethod
    def parse_rooms(rooms_list):
        units = []
        for room in rooms_list:
            print(room)
            unit = (room['id'], room['name'])
            units.append(unit)
        return units

    @staticmethod
    def parse_students(students_list):
        units = []
        for student in students_list:
            unit = (student['id'], student['name'], student['birthday'], student['room'], student['sex'])
            units.append(unit)
        return units


def main(rooms_path, students_path, format):
    if os.path.exists(rooms_path) and os.path.exists(students_path):

        students_dir = rooms_path
        rooms_dir = students_path
        _format = format

        students = JsonHandler(students_dir).load()
        rooms = JsonHandler(rooms_dir).load()
        rooms_vals = Parser.parse_rooms(rooms)
        student_vals = Parser.parse_students(students)

        room_fields = "id INTEGER NOT NULL, name VARCHAR(10), PRIMARY KEY(id)"
        student_fields = ("""id INTEGER NOT NULL,
                          name VARCHAR(100) NOT NULL,
                          birthday DATETIME,
                          room INTEGER NOT NULL,
                          sex VARCHAR(1) NOT NULL,
                          PRIMARY KEY(id),
                          FOREIGN KEY(room) REFERENCES rooms(id) ON DELETE CASCADE """)
        try:
            db = DBCreator()
            db.create_db()
            db.create_table(name='rooms', fields=room_fields)
            db.create_table(name='students', fields=student_fields)
            db.disconnect()
        except DatabaseError as e:
            db.disconnect()
            pass

        try:
            writer = Writer()
            writer.write('rooms', rooms_vals, 'id, name')
            writer.write('students', student_vals, 'id, name, birthday, room, sex')
            writer.disconnect()
        except IntegrityError as e:
            writer.disconnect()
            pass

        result_dict = {}

        query = Query()
        try:
            query.create_index('students_room', 'students', 'room')
            query.create_index('rooms_id', 'rooms', 'id')
        except DatabaseError as e:
            pass

        result_dict['minimum avg age'] = query.find_rooms_with_min_avg_age()
        result_dict['amount students in room'] = query.count_students_in_rooms()
        result_dict['male/female rooms'] = query.find_rooms_male_female()
        result_dict['maximum age difference'] = query.find_rooms_with_max_diff_age()
        query.disconnect()
        loader = LoaderFactory()
        loader.get_serializer(_format, result_dict).upload()
    else:
        raise OSError('file does not exists')


if __name__ == "__main__":
    arg_parser = Parser.create_arg_parser()
    parsed_args = arg_parser.parse_args()
    main(parsed_args.rooms_path, parsed_args.students_path, parsed_args.format)
