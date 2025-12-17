from random import choice


class EventsInstruments:
    def __init__(self, casino):
        self.casino = casino

    def random_player(self):
        '''
        Select random player from the list.
        In default implementation there is only one player, so it will always chose it.
        '''
        if len(self.casino.players) == 0:
            return None
        return choice(self.casino.players)

    def random_goose(self):
        '''
        Select random goose from the list.
        '''
        if len(self.casino.geese) == 0:
            return None
        return choice(self.casino.geese)
