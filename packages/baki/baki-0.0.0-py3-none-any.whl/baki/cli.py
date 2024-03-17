"""
Module for command line argument operations.
"""

import argparse
import os
import shlex
import subprocess
import sys

from baki import __version__


class Colors:
    # pylint: disable=R0903
    """ANSI color codes."""

    CYAN = "\033[96m"
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


class CliError(Exception):
    """Exception for reporting an error for the command line"""

    def __init__(self, message):
        super().__init__(f"{Colors.RED}ERROR: {message}{Colors.RESET}")


def run_shell_cmd(cmd, verbose):
    """Runs a shell command."""

    command_list = shlex.split(cmd)
    return_code = None
    stdout = None
    try:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            check=True,
            shell=False,
        )
        return_code = result.returncode
        stdout = result.stdout
        stderr = None
    except subprocess.CalledProcessError as e:
        return_code = e.returncode
        stdout = None
        stderr = e.stderr

    if verbose:
        print(f"{Colors.YELLOW}{cmd}{Colors.RESET}")
        if stdout is not None:
            print(f"{Colors.CYAN}{stdout}{Colors.RESET}")
        if stderr is not None:
            print(f"{Colors.RED}{stderr}{Colors.RESET}")

    return int(return_code), stdout


def valid_file_type(filepath):
    """
    Custom argparse type for a path to an existing file
    given from the command line.
    """
    try:
        absolute_filepath = os.path.abspath(os.path.expanduser(filepath))
        if not os.path.isfile(absolute_filepath):
            raise argparse.ArgumentTypeError(
                f"{absolute_filepath} is not a valid file")
        return absolute_filepath
    except Exception as exc:
        raise argparse.ArgumentTypeError(
            f"{filepath} is not a valid file") from exc


class CliParser:
    """
    Parses the command-line arguments.
    """

    def __init__(self, usage=""):
        parser = argparse.ArgumentParser(usage=usage)
        parser.add_argument("command",
                            nargs="?",
                            default=None,
                            help="Subcommand to run")
        parser.add_argument("--version",
                            action="store_true",
                            help="Get version.")
        parser.add_argument("-v",
                            "--verbose",
                            action="store_true",
                            help="Enable verbose mode.")
        parser.add_argument(
            "-p",
            "--password_file_path",
            type=valid_file_type,
            help=("File that contains the password for "
                  "backup/restore operations."),
        )

        # Finds how many arguments until command is found
        known_args, _ = parser.parse_known_args()
        self.cmd_offset = 0
        for i, arg in enumerate(sys.argv):
            self.cmd_offset = i
            if arg == known_args.command:
                break
        self.cmd_offset += 1

        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        raw_global_arguments = sys.argv[1:self.cmd_offset]
        args = parser.parse_args(raw_global_arguments)

        if args.command is not None and not hasattr(self, args.command):
            print("Unrecognized command")
            parser.print_help()
            sys.exit(1)

        # Display help message if no command is selected.
        if args.command is None and (len(sys.argv) < 2):
            parser.print_help()
            sys.exit(1)

        # Check version
        if args.version:
            print(__version__)
            sys.exit(0)

        # use dispatch pattern to invoke method with same name
        if args.command is not None:
            self.args = getattr(self, args.command)()
        else:
            self.args = None
        self.global_args = args
        self.command = args.command

    def backup(self):
        """
        Taking a backup from source to the target.
        """
        parser = argparse.ArgumentParser(
            description="Taking a backup from source to the target")
        parser.add_argument("source", help="Backup source directory path")
        parser.add_argument("target", help="Backup target directory path")
        args = parser.parse_args(sys.argv[self.cmd_offset:])
        return args

    def restore(self):
        """
        Restore from a checkpoint.
        """
        parser = argparse.ArgumentParser(
            description="Restore from a checkpoint")
        parser.add_argument("source", help="Restore source directory path")
        parser.add_argument("target", help="Restore target directory path")
        args = parser.parse_args(sys.argv[self.cmd_offset:])
        return args
