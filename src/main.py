from src.infrastructure.logger import logger
import logging.config
from src.common.config import LOGGING_CONFIG
from src.facade.facade import Facade
import time


def main() -> None:
    # define logger in accordance with config file
    logging.config.dictConfig(LOGGING_CONFIG)
    logger.info("Logging initialized.")
    print("Welcome to the turn-base Casino game!")
    print("Before starting, please, fill out and sign this little document:\n")
    print("You will be unable to stop the simulation from within until it won't reach it's last step.")
    try:
        while True:
            # read user command
            steps = input("Enter quantity of simulation steps: ")
            seed_input = input(
                "Enter seed or just press enter to have a random seed: ").strip()
            seed = int(seed_input) if seed_input else None
            user_name = input("Enter your name: ")
            time.sleep(1)
            print("Executor signature: The Devil")
            time.sleep(2)
            print("Customer signature: The Fool")
            time.sleep(2)
            logger.info(
                f"User entered simulation parameters: steps - {steps}, seed - {seed}, user name - {user_name}")

            facade = Facade()
            facade.run_simulation(user_name, int(steps), seed)

            # stop the program if stop word was given
            # if steps.lower() in ("exit", "quit"):
            #     print("Exiting the CLI.")
            #     logger.info("Logging stopped.")
            #     break

    except KeyboardInterrupt:
        print("Exiting the console.")
    # except Exception as e:
    #     logger.error(e)
    #     print(e)


if __name__ == "__main__":
    main()
