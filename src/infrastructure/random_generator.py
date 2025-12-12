from random import randint, seed


class SeedGenerator:
    def __init__(self):
        self.seed_value = None

    def generate_random_seed(self, prepared_seed: int | None) -> int:
        if prepared_seed is not None:
            self.seed_value = prepared_seed
        else:
            self.seed_value = randint(1, 1000000)

        seed(self.seed_value)
        return self.seed_value
