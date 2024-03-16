from __future__ import annotations

import logging
from abc import abstractmethod
from numbers import Number
from typing import Any

from ruamel.yaml import YAML, CommentedMap, CommentedSeq, round_trip_dump
from ruamel.yaml.error import MarkedYAMLError


class Yaml:
    ruamel_yaml: YAML = YAML()
    ruamel_yaml.preserve_quotes = True

    @classmethod
    def parse_yaml_str(cls, yaml_str: str) -> YamlValue:
        try:
            ruamel_value = cls.ruamel_yaml.load(yaml_str)
            return cls._to_yaml_value(ruamel_value)
        except MarkedYAMLError as e:
            location = cls.__get_location_from_yaml_error(e)
            logging.error(f"YAML syntax error at {location}: \n{e}")

    @classmethod
    def write_yaml_str(cls, ruamel_commented_map: CommentedMap) -> str:
        return round_trip_dump(ruamel_commented_map)

    @classmethod
    def __get_location_from_yaml_error(cls, e):
        mark = e.context_mark if e.context_mark else e.problem_mark
        return YamlLocation(
            line=mark.line + 1,
            column=mark.column + 1,
        )

    @classmethod
    def _to_yaml_value(cls, ruamel_value: object) -> YamlValue:
        if isinstance(ruamel_value, str):
            return YamlString(ruamel_value=ruamel_value)
        if isinstance(ruamel_value, bool):
            return YamlBoolean(ruamel_value=ruamel_value)
        if isinstance(ruamel_value, Number):
            return YamlNumber(ruamel_value=ruamel_value)
        if ruamel_value is None:
            return YamlNull()
        if isinstance(ruamel_value, CommentedMap):
            return YamlObject(ruamel_value=ruamel_value)
        if isinstance(ruamel_value, CommentedSeq):
            return YamlList(ruamel_value=ruamel_value)
        logging.error(f"Unsupported Ruamel YAML object type: {type(ruamel_value).__name__}\n{str(ruamel_value)}")


class YamlLocation:
    def __init__(self, line: int, column: int):
        self.line: int = line
        self.column: int = column

    def __str__(self):
        return f"(line {self.line},col {self.column})"


# class YamlErrorLevel(Enum):
#     WARNING = "warning"
#     ERROR = "error"
#
#
# @dataclass
# class YamlError:
#     level: YamlErrorLevel
#     location: YamlLocation
#     message: str
#
#     def __str__(self) -> str:
#         level_str = "WARNING | " if self.level == YamlErrorLevel.WARNING else "ERROR   | "
#         location_str = "" if self.location is None else f" {self.location}"
#         return f"{level_str}{self.message}{location_str}"
#
#
# class YamlErrors:
#     def __init__(self):
#         self.errors: List[YamlError] = []
#
#     def error(self, message: str, location: YamlLocation | None = None) -> None:
#         self.errors.append(YamlError(level=YamlErrorLevel.ERROR, message=message, location=location))
#
#     def warning(self, message: str, location: YamlLocation | None = None) -> None:
#         self.errors.append(YamlError(level=YamlErrorLevel.WARNING, message=message, location=location))
#
#     def __str__(self) -> str:
#         error_lines = [str(error) for error in self.errors]
#         return "\n".join(error_lines)


class YamlValue:
    """
    Base class for yaml data structure objects
    """

    def __init__(self, ruamel_value: object, location: YamlLocation | None = None):
        self.location: YamlLocation | None = None

    def set_location(self, location: YamlLocation | None) -> None:
        self.location = location

    @abstractmethod
    def unpacked(self) -> Any:
        pass


class YamlString(YamlValue):
    def __init__(self, ruamel_value: str):
        super().__init__(ruamel_value)
        self.value: str = ruamel_value

    def unpacked(self) -> str:
        return self.value


class YamlNumber(YamlValue):
    def __init__(self, ruamel_value: Number):
        super().__init__(ruamel_value)
        self.value: Number = ruamel_value

    def unpacked(self) -> Number:
        return self.value


class YamlBoolean(YamlValue):
    def __init__(self, ruamel_value: bool):
        super().__init__(ruamel_value)
        self.value: bool = ruamel_value

    def unpacked(self) -> bool:
        return self.value


class YamlNull(YamlValue):
    def __init__(self):
        super().__init__(None)
        self.value: None = None

    def unpacked(self) -> None:
        return None


class YamlObject(YamlValue):
    def __init__(self, ruamel_value: CommentedMap):
        super().__init__(ruamel_value)
        self.yaml_dict: dict[str, YamlValue] = {
            key: self.__convert_map_value(ruamel_object=ruamel_value, key=key, value=value)
            for key, value in ruamel_value.items()
        }

    def __convert_map_value(self, ruamel_object: CommentedMap, key, value) -> YamlValue:
        ruamel_location = ruamel_object.lc.value(key)
        line: int = ruamel_location[0]
        column: int = ruamel_location[1]
        yaml_value = Yaml._to_yaml_value(ruamel_value=value)
        yaml_value.set_location(YamlLocation(line=line, column=column))
        return yaml_value

    def __iter__(self):
        return iter(self.yaml_dict)

    def keys(self):
        return self.yaml_dict.keys()

    def items(self):
        return self.yaml_dict.items()

    def get(self, index) -> YamlValue | None:
        return self.yaml_dict.get(index)

    def read_yaml_object(self, key: str) -> YamlObject | None:
        """
        An appropriate error log is generated if the value is not a YamlObject or if the key is missing
        :return: a YamlObject if the value for the key is a YamlObject, otherwise None.
        """
        return self.read_value(key=key, expected_type=YamlObject, required=True, default_value=None)

    def read_yaml_object_opt(self, key: str) -> YamlObject | None:
        """
        An appropriate error log is generated if the value is not a YamlObject
        :return: a YamlObject if the value for the key is a YamlObject, otherwise None.
        """
        return self.read_value(key=key, expected_type=YamlObject, required=False, default_value=None)

    def read_yaml_list(self, key: str) -> YamlList | None:
        """
        An appropriate error log is generated if the value is not a YamlList or if the key is missing
        :return: a YamlList if the value for the key is a YamlList, otherwise None.
        """
        return self.read_value(key=key, expected_type=YamlList, required=True, default_value=None)

    def read_yaml_list_opt(self, key: str) -> YamlList | None:
        """
        An appropriate error log is generated if the value is not a YamlObject
        :return: a YamlObject if the value for the key is a YamlObject, otherwise None.
        """
        return self.read_value(key=key, expected_type=YamlList, required=False, default_value=None)

    def read_yaml_string_opt(self, key: str, default_value: str | None = None) -> YamlString | None:
        """
        An appropriate error log is generated if the value is not a string
        :return: a YamlString if the value for the key is a YAML string, otherwise None.
        """
        return self.read_value(key=key, expected_type=YamlString, required=False, default_value=default_value)

    def read_yaml_string(self, key: str) -> YamlString | None:
        """
        An appropriate error log is generated if the value is not a string or if the key is missing.
        :return: a YamlString if the value for the key is a YAML string, otherwise None.
        """
        return self.read_value(key=key, expected_type=YamlString, required=True)

    def read_string_opt(self, key: str, default_value: str | None = None) -> str | None:
        """
        An appropriate error log is generated if the value is not a string
        :return: a str if the value for the key is a YAML string, otherwise None.
        """
        yaml_string_value = self.read_value(
            key=key, expected_type=YamlString, required=False, default_value=default_value
        )
        return yaml_string_value.value if isinstance(yaml_string_value, YamlString) else None

    def read_string(self, key: str) -> str | None:
        """
        An appropriate error log is generated if the value is not a string or if the key is missing.
        :return: a YamlString if the value for the key is a YAML string, otherwise None.
        """
        yaml_string_value = self.read_value(key=key, expected_type=YamlString, required=True, default_value=None)
        return yaml_string_value.value if isinstance(yaml_string_value, YamlString) else None

    def read_bool(self, key: str) -> bool | None:
        """
        An appropriate error log is generated if the value is not a bool or if the key is missing
        :return: a bool if the value for the key is a YAML boolean, otherwise None.
        """
        yaml_boolean_value = self.read_value(key=key, expected_type=YamlBoolean, required=True, default_value=None)
        return yaml_boolean_value.value if isinstance(yaml_boolean_value, YamlString) else None

    def read_bool_opt(self, key: str, default_value: bool | None = None) -> bool | None:
        """
        An appropriate error log is generated if the value is not a bool.
        :return: a bool if the value for the key is a YAML boolean, otherwise None.
        """
        yaml_boolean_value = self.read_value(
            key=key, expected_type=YamlBoolean, required=False, default_value=default_value
        )
        return yaml_boolean_value.value if isinstance(yaml_boolean_value, YamlBoolean) else None

    def read_number(self, key: str) -> Number | None:
        """
        An appropriate error log is generated if the value is not a number or if the key is missing
        :return: a bool if the value for the key is a YAML number, otherwise None.
        """
        yaml_number_value = self.read_value(key=key, expected_type=YamlNumber, required=True, default_value=None)
        return yaml_number_value.value if isinstance(yaml_number_value, YamlNumber) else None

    def read_number_opt(self, key: str, default_value: Number | None = None) -> Number | None:
        """
        An appropriate error log is generated if the value is not a number.
        :return: a Number if the value for the key is a YAML number, otherwise None.
        """
        yaml_number_value = self.read_value(
            key=key, expected_type=YamlNumber, required=False, default_value=default_value
        )
        return yaml_number_value.value if isinstance(yaml_number_value, YamlNumber) else None

    def read_value(
        self,
        key: str,
        expected_type: type = None,
        required: bool = False,
        default_value=None,
    ) -> YamlValue:
        if key not in self.yaml_dict:
            if required:
                logging.error(f"'{key}' is required")
            return default_value
        yaml_value: YamlValue = self.yaml_dict.get(key)
        if expected_type is not None and not isinstance(yaml_value, expected_type):
            logging.error(
                f"'{key}' expected a {expected_type.__name__}, but was {type(yaml_value).__name__} {yaml_value.location}",
            )
        return yaml_value

    def unpacked(self):
        return {key: yaml_value.unpacked() for key, yaml_value in self.yaml_dict.items()}


class YamlList(YamlValue):
    def __init__(self, ruamel_value: CommentedSeq):
        super().__init__(ruamel_value)
        self.value: list[YamlValue] = [
            self.__convert_array_value(ruamel_value=ruamel_list_value, commented_seq=ruamel_value, index=index)
            for index, ruamel_list_value in enumerate(ruamel_value)
        ]

    def __convert_array_value(self, ruamel_value, commented_seq: CommentedSeq, index: int) -> YamlValue:
        ruamel_location = commented_seq.lc.key(index)
        line: int = ruamel_location[0]
        column: int = ruamel_location[1]
        yaml_value = Yaml._to_yaml_value(ruamel_value=ruamel_value)
        yaml_value.set_location(YamlLocation(line=line, column=column))
        return yaml_value

    def __iter__(self):
        return iter(self.value)

    def unpacked(self):
        return [yaml_value.unpacked() for yaml_value in self.value]
