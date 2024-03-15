import os
import sys
import subprocess
import logging


def main():
    command = sys.argv
    is_please = command[0].endswith("please")

    del command[0]

    if not command:
        logging.error("Not enough arguments.")
        return 1

    if command[0] == "will":
        if is_please:
            logging.error("`will` is not allowed in `please`.")
            return 1
        del command[0]

    if not command:
        logging.error("Not enough arguments.")
        return 1

    if len(command) >= 2 and not command[1].startswith("-"):
        command[0], command[1] = command[1], command[0]

    return subprocess.call(command)


if __name__ == "__main__":
    sys.exit(main())
