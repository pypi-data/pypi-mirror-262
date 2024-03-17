"""
Abstart data types / Interfaces.
"""

from abc import ABC, abstractmethod


class BackupBackendInterface(ABC):
    """
    Interface for the backup / restore backend.
    """

    @abstractmethod
    def backup(self, source, target):
        """
        Make a full or an incremental backup.
        """
        raise NotImplementedError

    @abstractmethod
    def restore(self, source, target):
        """
        Restore to a previous checkpoint.
        """
        raise NotImplementedError

    @abstractmethod
    def info(self):
        """
        Show information about the remote.
        """
        raise NotImplementedError
