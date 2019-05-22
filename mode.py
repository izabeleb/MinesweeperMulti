import os
import json

class Mode:
    MODE_EASY: dict = {'HEIGHT': 10, 'WIDTH': 10, "BOMBS": 25}
    MODE_NORMAL: dict = {'HEIGHT': 20, 'WIDTH': 20, "BOMBS" : 100}
    MODE_HARD: dict = {'HEIGHT': 30, 'WIDTH': 30, "BOMBS" : 225}

    def __init__(self, mode: dict = None, height: int = 20, width: int = 20, bombs: int = None)-> None:
        
        if bombs is None:
            
            bombs = height * width // 4
        
        if mode is not None:
            self.mode = mode
        else:
            self.mode = {'HEIGHT': height, 'WIDTH': width, 'BOMBS': bombs}

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
    
    def get_bomb_count(self) -> int:
        return self.mode['BOMBS']