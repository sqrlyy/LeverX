import json
from xml.dom.minidom import parseString
import dicttoxml


class Loader:
    def __init__(self, result_list):
        self.result_list = result_list

    def upload(self):
        raise NotImplementedError


class XmlLoader(Loader):
    def upload(self):
        xml = dicttoxml.dicttoxml(self.result_list, custom_root='result', attr_type=False)
        dom = parseString(xml).toprettyxml()
        with open('result.xml', 'w') as test:
            test.writelines(dom)


class JsonLoader(Loader):
    def upload(self):
        with open('result.json', 'w') as result:
            json.dump(self.result_list, result, ensure_ascii=False, indent=4)


class LoaderFactory:
    def get_serializer(self, _format, data):
        if _format == 'json':
            return JsonLoader(data)
        elif _format == 'xml':
            return XmlLoader(data)
        else:
            raise ValueError(_format)