import json
import dicttoxml
from xml.dom import minidom


class Loader():
    def __init__(self, path):
        self.path = path

    def load(self):
        raise NotImplementedError


class JsonLoader(Loader):
    def __init__(self, path):
        super().__init__(path)

    def load(self):
        try:
            with open(self.path) as loadfile:
                return json.load(loadfile)

        except FileNotFoundError:
            return 'File not found.'


class Saver():
    def __init__(self, result):
        self.result = result

    def save(self):
        raise NotImplementedError


class JsonSaver(Saver):
    def __init__(self, result):
        super().__init__(result)

    def save(self):
        with open('result.json', 'w') as f:
            json.dump(self.result, f, indent=2)


class XMLSaver(Saver):
    def __init__(self, result):
        super().__init__(result)

    def save(self):
        xml = dicttoxml.dicttoxml(self.result, custom_root='rooms')
        new_xml = minidom.parseString(xml).toprettyxml()
        with open('result.xml', 'w') as f:
            f.write(new_xml)