"""
The main application.
"""

import logging
import sys

from baki.cli import CliError, CliParser
# TODO: Enable config
# from baki.config import Config
from baki.logger import Logger
from baki.restic_backend import ResticBackupBackend


def app():
    """
    Main application logic.

    Raises:
        KeyboardInterrupt: User tried to kill the process.
    """

    usage = "baki <command> [<args>]\n"
    usage += "\n"
    usage += "The most commonly used baki commands are:\n"
    usage += "   backup     Make a backup.\n"
    usage += "   restore    Restore from a checkpoint.\n"

    try:
        # TODO: Enable config
        # config = Config()
        cli = CliParser(usage=usage)
        verbose = cli.global_args.verbose
        password_file_path = cli.global_args.password_file_path

        # Configure logger
        logger = Logger()
        if verbose:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.ERROR)

        # logger.info("This is an info log")
        # logger.debug("This is a debug log")
        # logger.warning("This is a warning log")
        # logger.error("This is an error log")
        # logger.critical("This is a critial log")

        # print(f"We called {cli.command} with {cli.args}")
        backup_backend = ResticBackupBackend(
            password_file_path=password_file_path, verbose=verbose)
        if cli.command == "info":
            backup_backend.info()
        elif cli.command == "backup":
            backup_backend.backup(source=cli.args.source,
                                  target=cli.args.target)
        elif cli.command == "restore":
            backup_backend.restore(source=cli.args.source,
                                   target=cli.args.target)
        else:
            raise CliError("Invalid command")

    except CliError as e:
        print(e)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation interrupted by user.")
        sys.exit(1)


if __name__ == "__main__":
    app()
