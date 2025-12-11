from src.infrastructure.logger import logger
import logging.config
from src.common.config import LOGGING_CONFIG
from src.facade.facade import Facade


def main() -> None:
    # define logger in accordance with config file
    logging.config.dictConfig(LOGGING_CONFIG)
    logger.info("Logging initialized.")
    print("Welcome to the turn-base Casino game!")

    try:
        while True:
            # read user command
            steps = input("Enter quantity of simulation steps: ")
            seed_input = input(
                "Enter seed or just press enter to have a random seed: ").strip()
            seed = int(seed_input) if seed_input else None
            logger.info(
                f"User entered simulation parameters: steps - {steps}, seed - {seed}")

            facade = Facade()
            facade.facade(steps, seed)

            # stop the program if stop word was given
            # if steps.lower() in ("exit", "quit"):
            #     print("Exiting the CLI.")
            #     logger.info("Logging stopped.")
            #     break

    except KeyboardInterrupt:
        print("Exiting the console.")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
