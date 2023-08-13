import os
import time

import dotenv

from Harmonie import Harmonie


def main():
    harmonie = Harmonie()

    if os.getenv('PYTHON_ENV') != 'dev':
        while True:
            harmonie.run()
            time.sleep(300)
    else:
        harmonie.run()

if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
