from functools import total_ordering
import re


@total_ordering
class Version:

    component_re = re.compile(r'(\d+ | [a-z]+  | \.)', re.VERBOSE)

    def __init__(self, version=None):
        self.version = self.parse(version)

    def __eq__(self, other):
        c = self._cmp(other)
        return c == 0

    def __gt__(self, other):
        c = self._cmp(other)
        return c > 0

    def parse(self, version):
        value = version
        components = [x for x in self.component_re.split(value) if x and x != '.']
        for i, obj in enumerate(components):
            try:
                components[i] = int(obj)
            except ValueError:
                if components[i] == '-':
                    components.remove('-')
                if components[i] == 'alpha' or components[i] == 'a':
                    components[i] = 1
                if components[i] == 'beta' or components[i] == 'b':
                    components[i] = 2
                if components[i] == 'rc':
                    components[i] = 3
        return components

    def _cmp(self, other):
        if self.version == other.version:
            return 0
        if self.version < other.version:
            return -1
        if self.version > other.version:
            return 1


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), 'le failed'
        assert Version(version_2) > Version(version_1), 'ge failed'
        assert Version(version_2) != Version(version_1), 'neq failed'


if __name__ == "__main__":
    main()