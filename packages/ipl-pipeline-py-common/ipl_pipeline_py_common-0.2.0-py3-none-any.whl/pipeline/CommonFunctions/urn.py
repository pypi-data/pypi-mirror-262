"""
Handles parsing of IPL URNs

example:
    urn:iplsplatoon:production:commentators:id:{id}
"""
from typing import List


class URN:
    ns: str
    ns_specific: str
    sub_component: str
    id_provider: str
    id_type: str
    identifier: str

    @staticmethod
    def get_from_index(input_list: List[any], i: int, default=None):
        if len(input_list) < i:
            if default:
                return default
            raise IndexError
        return input_list[i]

    def __init__(self, urn: str):
        try:
            string_split = urn.split(':')
            if string_split[0] != "urn":
                raise ValueError('Invalid URN')
            self.ns = self.get_from_index(string_split, 1)
            self.ns_specific = self.get_from_index(string_split, 2)
            self.sub_component = self.get_from_index(string_split, 3)
            self.id_provider = self.get_from_index(string_split, 4)
            self.id_type = self.get_from_index(string_split, 5)
            self.identifier = self.get_from_index(string_split, 6)
        except IndexError:
            raise ValueError('Invalid URN')
