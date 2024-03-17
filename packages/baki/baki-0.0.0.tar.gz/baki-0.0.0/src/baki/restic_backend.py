"""
Backup / Restore backend for restic.
"""

import os
import re
import subprocess

from baki.cli import CliError, Colors, run_shell_cmd
from baki.interfaces import BackupBackendInterface


class ResticBackupBackend(BackupBackendInterface):
    # pylint: disable=R0902
    """
    Backend for restic
    url: https://restic.net/
    """

    def __init__(self, password_file_path, verbose=False):
        """
        Initializes restic as the backend.
        """
        self.verbose = verbose

        self.keep_within_days = int(10)
        self.hourly = int(24)
        self.daily = int(1)
        self.weekly = int(4)
        self.monthly = int(12)
        self.yearly = int(1)

        self.password_file_path = password_file_path
        try:
            os.path.isfile(self.password_file_path)
        except TypeError as exc:
            raise CliError(
                "Password file is required for restic backend") from exc
        except FileNotFoundError as exc:
            raise CliError("File not found.") from exc
        except PermissionError as exc:
            raise CliError("Permission denied.") from exc

    def _verify_source(self, dir_path):
        """Check if source exists."""
        if not os.path.isdir(dir_path):
            raise CliError(f"{dir_path} is not a valid directory")

    def _restic_check_repository_exists(self, repo_dir_path):
        """Restic operation to check if repository already exists."""
        cmd = (f'restic --repo "{repo_dir_path}" '
               f'--password-file="{self.password_file_path}" cat config')
        return_code, _ = run_shell_cmd(cmd=cmd, verbose=self.verbose)
        is_repo_exist = bool(return_code == 0)
        return is_repo_exist

    def _restic_init_repository(self, repo_dir_path):
        """Restic operation to initialize repository."""

        cmd = (f'restic init --repo="{repo_dir_path}" '
               f'--password-file="{self.password_file_path}"')
        return_code, _ = run_shell_cmd(cmd=cmd, verbose=self.verbose)
        if return_code != 0:
            raise CliError(
                f"Failed to initialise repository with {return_code}")

    def _restic_create_backup(self, source, target):
        """Restic operation to take backup."""
        cmd = (f'restic backup --repo "{target}" '
               f'--password-file="{self.password_file_path}" "{source}"')
        return_code, _ = run_shell_cmd(cmd=cmd, verbose=self.verbose)
        if return_code != 0:
            raise CliError(f"Failed to create a backup with {return_code}")

    def _restic_tag_expired_backups(
        # pylint: disable=R0913
        self,
        target,
        keep_within_days,
        hourly,
        daily,
        weekly,
        monthly,
        yearly,
    ):
        """Restic operation to tag the expired backups."""
        cmd = (f'restic forget --repo "{target}" '
               f'--password-file="{self.password_file_path}" '
               f"--keep-within={keep_within_days}d "
               f"--keep-hourly={hourly} "
               f"--keep-daily={daily} "
               f"--keep-weekly={weekly} "
               f"--keep-monthly={monthly} "
               f"--keep-yearly={yearly}")
        return_code, _ = run_shell_cmd(cmd=cmd, verbose=self.verbose)
        if return_code != 0:
            raise CliError("Failed to tag older backups "
                           f"from remote for deletion with {return_code}")

    def _restic_prune_expired_backups(self, target):
        """Restic operation to prune the expired backups."""
        cmd = (f'restic prune --repo "{target}" '
               f'--password-file="{self.password_file_path}"')
        return_code, _ = run_shell_cmd(cmd=cmd, verbose=self.verbose)
        if return_code != 0:
            raise CliError(f"Failed to prune backup with {return_code}")

    def _restic_integrity_check(self, target):
        """Restic operation to run an integrity check on the repository."""
        cmd = (f'restic check --repo "{target}" '
               f'--password-file="{self.password_file_path}"')
        return_code, _ = run_shell_cmd(cmd=cmd, verbose=self.verbose)
        if return_code != 0:
            raise CliError(f"Integrity check failed with {return_code}")

    def _restic_list_restore_snapshots(self, repo_dir_path):
        """Restic operation to list restorable snapshots."""

        def remove_footer_and_header(snapshot_data):
            """
            Removed the header and footer from restic's output
            for list of snapshots.
            """
            # Define a regular expression pattern
            # to capture the data between dashed lines
            pattern = re.compile(r"-" * 15 + r"\n(.+?)\n" + "-" * 15,
                                 re.DOTALL)
            # Use the pattern to search for the data between dashed lines
            match = pattern.search(snapshot_data)
            # Extract the data if a match is found
            if match:
                data_between_dashes = match.group(1).strip()
                return data_between_dashes

            return None

        cmd = (f'restic --repo="{repo_dir_path}" '
               f'--password-file="{self.password_file_path}" snapshots')
        return_code, stdout = run_shell_cmd(cmd=cmd, verbose=self.verbose)
        if return_code != 0:
            raise CliError(f"Failed to list snapshots with {return_code}")

        cleaned_snapshot_list = remove_footer_and_header(stdout)
        if cleaned_snapshot_list is None:
            raise CliError("Failed to match regexp with snapshot list")

        # Add latest snapshot
        cleaned_snapshot_list_with_extra = "latest\n"
        cleaned_snapshot_list_with_extra += cleaned_snapshot_list

        return cleaned_snapshot_list_with_extra

    def _restic_restore_from_snapshot(self, snapshot_id, source, target):
        """Restic operation to restore from a snapshot."""
        cmd = (f'restic --repo "{source}" '
               f'--password-file="{self.password_file_path}" '
               f'restore {snapshot_id} --target="{target}"')
        return_code, _ = run_shell_cmd(cmd=cmd, verbose=self.verbose)
        if return_code != 0:
            raise CliError(
                f"Failed to restore from a snapshot with {return_code}")

    def _fzf_select_snapshot(self, restic_snapshot_cleaned_output):
        """fzf operation to a restic snaphotselect from list."""
        snapshot_id = None
        try:
            # Pipe the list of snapshots to fzf.
            result = subprocess.run(
                ["echo", restic_snapshot_cleaned_output],
                text=True,
                check=True,
                stdout=subprocess.PIPE,
            )
            # Pass the list in fzf for selecting only one
            selected_snapshot = subprocess.run(
                ["fzf"],
                input=result.stdout,
                stdout=subprocess.PIPE,
                text=True,
                check=True,
                shell=True,
            )
            # Extract the snapshot ID from the selected input
            if selected_snapshot.stdout:
                snapshot_id = selected_snapshot.stdout.split()[0]
        except subprocess.CalledProcessError:
            snapshot_id = None

        return snapshot_id

    def backup(self, source, target):
        """
        Make a full or an incremental backup.
        """
        print(f"{Colors.BLUE}Taking a backup from "
              f"'{source}' to '{target}'{Colors.RESET}")
        self._verify_source(source)

        # -------------------------------------------------
        # Check if repository exists
        print(f"{Colors.BLUE}Checking repository{Colors.RESET}")
        is_repo_exist = self._restic_check_repository_exists(target)

        # -------------------------------------------------
        # Initialize repository
        if not is_repo_exist:
            print(f"{Colors.BLUE}Initializing repository{Colors.RESET}")
            self._restic_init_repository(target)

        # ---------------------------------------------------------------------------
        # Take backup
        print(f"{Colors.BLUE}Creating backup{Colors.RESET}")
        self._restic_create_backup(source, target)

        # ---------------------------------------------------------------------------
        # Tag and prune expired backups
        print(f"{Colors.BLUE}Tagging expired backups{Colors.RESET}")
        self._restic_tag_expired_backups(
            target=target,
            keep_within_days=self.keep_within_days,
            hourly=self.hourly,
            daily=self.daily,
            weekly=self.weekly,
            monthly=self.monthly,
            yearly=self.yearly,
        )

        # ---------------------------------------------------------------------------
        # Delete expired backups
        print(f"{Colors.BLUE}Prune expired backups{Colors.RESET}")
        self._restic_prune_expired_backups(target)

        # ---------------------------------------------------------------------------
        # Run integrity checks
        print(f"{Colors.BLUE}Running integrity check{Colors.RESET}")
        self._restic_integrity_check(target)

    def restore(self, source, target):
        """
        Restore to a previous checkpoint.
        """
        print(f"{Colors.BLUE}Restoring from "
              f"'{source}' to '{target}'{Colors.RESET}")
        self._verify_source(target)

        # -------------------------------------------------
        # Check if repository exists
        print(f"{Colors.BLUE}Checking repository{Colors.RESET}")
        is_repo_exist = self._restic_check_repository_exists(source)
        if not is_repo_exist:
            raise CliError(f"Repository {source} does not exist.")

        # ---------------------------------------------------------------------------
        # Run integrity checks
        print(f"{Colors.BLUE}Running integrity check{Colors.RESET}")
        self._restic_integrity_check(source)

        # ---------------------------------------------------------------------------
        # List all restorable snapshots
        restic_snapshot_cleaned_output = self._restic_list_restore_snapshots(
            source)

        # ---------------------------------------------------------------------------
        # Select snapshot with help from fzf
        snapshot_id = self._fzf_select_snapshot(restic_snapshot_cleaned_output)
        if snapshot_id is None:
            raise CliError("User skipped snapshot selection.")

        # ---------------------------------------------------------------------------
        # Do the restore
        print(f"{Colors.BLUE}Restoring{Colors.RESET}")
        self._restic_restore_from_snapshot(snapshot_id, source, target)
        print(f"{Colors.GREEN}Restored snapshot: '{snapshot_id}' "
              f"successfully{Colors.RESET}")

    def info(self):
        """
        Show information about the remote.
        """
        print("Mock info")
