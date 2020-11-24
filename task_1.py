import argparse
from modules import JsonLoader, JsonSaver, XMLSaver


def arrange_data(rooms, students):
    for room in rooms:
        room['students'] = []
    for student in students:
        rooms[student['room']]['students'].append({'name': student['name'], 'id': student['id']})
    return rooms


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-rp', '--rooms_path', type=str, required=True)
    parser.add_argument('-sp', '--students_path', type=str, required=True)
    parser.add_argument('-f', '--format', type=str, required=True)
    return parser


def main(rooms_path, students_path, format):
    rooms = JsonLoader(rooms_path).load()
    students = JsonLoader(students_path).load()

    result = arrange_data(rooms, students)

    if format == 'json':
        JsonSaver(result).save()
    elif format == 'xml':
        XMLSaver(result).save()
    else:
        print('Choose xml or json as output format.')


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    main(args.rooms_path, args.students_path, args.format)
