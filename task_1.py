import json
import argparse
import dicttoxml
from xml.dom import minidom


def arrange_data(rooms, students):
    for room in rooms:
        room['students'] = []
        for student in students:
            if room['id'] == student['room']:
                room['students'].append({'name': student['name'], 'id': student['id']})
    return  rooms


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-rp', '--rooms_path', type=str, required=True)
    parser.add_argument('-sp', '--students_path', type=str, required=True)
    parser.add_argument('-f', '--format', type=str, required=True)
    return parser


def main(rooms_path, students_path, format):
    with open(rooms_path) as room_json, open(students_path) as students_json:
        rooms = json.load(room_json)
        students = json.load(students_json)

    result = arrange_data(rooms, students)
    if format == 'json':
        with open('result.json', 'w') as f:
            json.dump(result, f, indent=2)
    else:
        xml = dicttoxml.dicttoxml(result, custom_root='rooms')
        new_xml = minidom.parseString(xml).toprettyxml()
        with open('result.xml', 'w') as f:
            f.write(new_xml)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    main(args.rooms_path, args.students_path, args.format)
