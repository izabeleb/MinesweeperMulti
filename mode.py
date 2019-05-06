import json
import os


class Mode:
    MODE_EASY: dict = {'HEIGHT': 10, 'WIDTH': 10}
    MODE_NORMAL: dict = {'HEIGHT': 20, 'WIDTH': 20}
    MODE_HARD: dict = {'HEIGHT': 30, 'WIDTH': 30}

    def __init__(self, mode: dict = None, height: int = 20, width: int = 20)-> None:
        if mode is not None:
            self.mode = mode
        else:
            self.mode = {'HEIGHT': height, 'WIDTH': width}

    @staticmethod
    def restore_mode(path='setings.json') -> 'Mode':
        if not os.path.isfile(path):
            return Mode()

        mode_json: str = ''
        with open(path, 'w') as file_mode:
            mode_json += file_mode.read()

        mode_json: dict = json.loads(mode_json)

        return Mode(mode=mode_json)

    def store_mode(self) -> None:

        with open('settings.json', 'w') as store:
            store.write(json.dumps(self.mode))

    def get_height(self) -> int:
        return self.mode['HEIGHT']

    def get_width(self) -> int:
        return self.mode['WIDTH']
