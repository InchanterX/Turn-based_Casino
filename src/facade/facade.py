from src.infrastructure.random_generator import SeedGenerator
from src.infrastructure.casino import Casino
# from src.infrastructure.player import Player


class Facade:
    def __init__(self):
        pass

    def run_simulation(self, default_name: str, steps: int = 10, input_seed: int | None = None) -> None:
        seed_generator = SeedGenerator()
        seed = seed_generator.generate_random_seed(input_seed)

        casino = Casino()
        # player = Player()
        casino.register_default(default_name)

        for _ in range(steps):
            casino.random_event()
