from random import seed
from src.infrastructure.casino import Casino
# from src.infrastructure.player import Player


class Facade:
    '''Execute the simulation itself by calling appropriate function for asked amount of times'''

    def __init__(self):
        pass

    def run_simulation(self, default_name: str, steps: int = 10, input_seed: int | None = None) -> None:
        # seed_generator = SeedGenerator()
        # seed = seed_generator.generate_random_seed(input_seed)
        seed(input_seed)

        casino = Casino()
        # player = Player()
        casino.register_default(default_name)

        print("----------------------------------")
        for step in range(steps):
            casino.make_effects_step()
            if casino.players_status_check():
                break
            casino.random_event(step)
            print(f"[Step: {step}]")
            print("----------------------------------")
