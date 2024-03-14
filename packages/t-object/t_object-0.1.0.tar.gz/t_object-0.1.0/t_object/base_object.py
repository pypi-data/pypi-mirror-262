"""This module contains the Base Thoughtful Object."""

import json
import os
import pickle

from pydantic import BaseModel, ValidationError, TypeAdapter


class _BaseThoughtfulObject(BaseModel):
    """This class is the base class for all Thoughtful objects."""

    def convert_to_json_string(self) -> str:
        """Converts an episode to a json string."""
        return self.model_dump_json(indent=4)

    def save_to_json_file(self, file_path: str = "") -> str:
        """Saves an episode to a json file.

        Args:
            file_path (str): The path to the file.
        """
        folder_path = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(folder_path):
            folder_path = os.getcwd()
        self._custom_model_config['json_file_path'] = os.path.join(folder_path, f"{self.__class__.__name__}-%s.json")

        file_path = file_path or self._get_json_default_file_path()
        if not file_path:
            raise ValueError("File path must be provided or set in the model config.")
        _, extension = os.path.splitext(file_path)
        if extension != ".json":
            raise ValueError(f"File extension must be .json, not {extension}")

        with open(file_path, "w") as file:
            file.write(self.convert_to_json_string())
        return file_path

    def save_to_pickle_file(self, file_path: str) -> str:
        """Saves an object to a pickle file.

        Args:
            file_path (str): The path to the file.
        """
        file_path = file_path or self.model_config.get("pickle_file_name")
        if not file_path:
            raise ValueError("File path must be provided or set in the model config.")
        with open(file_path, "wb") as file:
            pickle.dump(self, file)
        return file_path

    def pretty_string(self) -> str:
        """Converts an object to a string."""
        try:
            text = f"\n==={self.__class__.__name__}===\n"
            for key, value in self.__dict__.items():
                value_type = f"<{value.__class__.__name__}>"
                if isinstance(value, list):
                    text += f"{key}: LIST[{len(value)}] \n"
                    for number, item in enumerate(value):
                        text += f" [{number}] <{item.__class__.__name__}> {self._add_space(item)} \n"
                elif isinstance(value, tuple):
                    text += f"{key}: TUPLE[{len(value)}] \n"
                    for number, item in enumerate(value):
                        text += f" [{number}] <{item.__class__.__name__}> {self._add_space(item)} \n"
                elif isinstance(value, dict):
                    text += f"{key}: DICT[{len(value.keys())}] \n"
                    for k, v in value.items():
                        text += f" [{k}] <{v.__class__.__name__}> {self._add_space(v)} \n"
                else:
                    text += f"{key}: {value_type} {self._add_space(value)} \n"
            return text[:-1]
        except Exception as e:
            raise ValueError(f"Unable to convert object to string. {e}")

    def _add_space(self, text: object):
        text = text.pretty_string() if isinstance(text, _BaseThoughtfulObject) else str(text)
        spaces = 4
        return text.replace("\n", "\n" + spaces * " ")

    @classmethod
    def load_from_pickle_file(cls, file_path: str):
        """Loads an object from a pickle file and returns the object.

        Args:
            file_path (str): The path to the file.

        Returns:
            object: The objects.
        """
        try:
            with open(file_path, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to load file {file_path}. File not Found.")
        except Exception as e:
            raise Exception(f"Unable to load file {file_path}. {e}")

    @classmethod
    def load_from_json_file(cls, file_path: str) -> "_BaseThoughtfulObject":
        """Loads an object from a json file and returns the object.

        Args:
            file_path (str): The path to the file.

        Returns:
            object: The objects.
        """
        try:
            with open(file_path, "r") as file:
                return cls.model_validate_json(file.read())
        except ValidationError as e:
            raise ValidationError(f"Unable to load file {file_path}. Some fields are missing . \n {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to load file {file_path}. File not Found.")
        except Exception as e:
            raise Exception(f"Unable to load file {file_path}. {e}")

    def get_json_schema(self, file_path):
        """Returns the json schema for the object."""
        _, extension = os.path.splitext(file_path)
        if extension != ".json":
            raise ValueError(f"File extension must be .json, not {extension}")

        with open(file_path, "w") as file:
            file.write(json.dumps(self.model_json_schema(), indent=4))

    def _get_json_default_file_path(self):
        """Get default json file path"""
        try:
            self._custom_model_config['json_file_counter'] += 1
            return self._custom_model_config['json_file_path'] % (self._custom_model_config['json_file_counter'])
        except KeyError:
            return None
