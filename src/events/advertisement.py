from random import choice
from src.infrastructure.constants import ADVERTISEMENTS
from src.infrastructure.logger import logger


class AdvertisementEvent():
    '''Display advertisement to the console and ask to skip it'''

    def __init__(self, casino):
        self.casino = casino

    def _skip_advertisement(self):
        '''Ask player to continue by skipping advertisement'''
        input("Skip add?\n > ")

    def advertisement_event(self) -> bool:
        '''Print advertisement to the CLI'''
        # print("ADV")
        logger.info(
            "Displayed advertisement to the player.")
        print(f"[📺 Adv] {choice(ADVERTISEMENTS)}")
        # self._skip_advertisement()
        return True
