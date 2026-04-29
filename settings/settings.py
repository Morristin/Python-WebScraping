import json
import logging
from functools import wraps
from pathlib import Path
from typing import Sequence, MutableMapping

external_setting = {}


class Settings:
    """ A class for modules to quick access setting file and easily edit setting. """

    setting_file_path = Path(__file__).parent / Path('settings.json')

    def __init__(self, setting: Sequence = None):
        if setting is not None:
            self._settings = setting
        else:
            with open(self.setting_file_path, 'r') as setting_file:
                self._settings = json.loads(setting_file.read())

    def __repr__(self):
        return f'<Settings object contains item: {', '.join(i for i in self._settings)}>'

    def __eq__(self, other):
        return self._settings == other

    def __getitem__(self, item):
        if item in external_setting:
            return external_setting[item]()

        if isinstance(self._settings[item], MutableMapping):
            return Settings(self._settings[item])
        else:  # The item is already the atom of setting.
            return self._settings[item]

    def __getattribute__(self, item):
        if item in external_setting:
            return external_setting[item]()

        try:
            return super().__getattribute__(item)
        except AttributeError:
            return self[item]  # Reuse the implement of `__getitem__`.

    @staticmethod
    def get_from_external_file(filename: str = None):
        def decorator(func):
            nonlocal filename
            filename = func.__name__ + '.txt' if filename is None else filename

            @wraps(func)
            def _():
                return (Path(__file__).parent / Path(filename)).read_text()

            external_setting[func.__name__] = _
            return _

        return decorator

    @get_from_external_file('get_text_prompt.txt')
    def get_text_prompt(self) -> str:
        pass

    @staticmethod
    def _set_deep_level_item(content, key, value) -> bool:
        """
        Use recursive method to find the key and modify its value.

        :param content: The content need to be modified. Best if it's modifiable.
        :return: Whether the set succeeds. This used as a flag while recursing.

        Because the `_settings.json` is a mutable mapping,
        modify do not need `return` statement to take effect.
        """
        if not isinstance(content, MutableMapping):
            return False
        if key in content:
            content[key] = value
            return True

        for item in content.values():
            if Settings._set_deep_level_item(item, key, value):
                return True
        else:
            return False

    def set(self, key, value):
        with open(self.setting_file_path, 'r') as setting_file:
            setting_dic = json.loads(setting_file.read())
        if not self._set_deep_level_item(setting_dic, key, value):
            logging.warning(f'Can not modify settings: {key} not found.')
            raise KeyError(f'Can not find key: {key}')
        with open(self.setting_file_path, 'w') as setting_file:
            json.dump(setting_dic, setting_file, indent=2)

        # Refresh current settings.
        with open(self.setting_file_path, 'r') as setting_file:
            self._settings = json.loads(setting_file.read())


# Create instance for modules to quick access settings.
settings = Settings()
